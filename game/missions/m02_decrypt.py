import time
from game.missions.base import BaseMission

CORRECT_SHIFT = 5
PLAINTEXT = "OPERATION NIGHTFALL: DEPLOY SECURITY PATCH AT MIDNIGHT. ACCESS CODE: ALPHA-7-TANGO"


def caesar_encrypt(text: str, shift: int) -> str:
    result = []
    for ch in text:
        if ch.isalpha():
            base = ord('A') if ch.isupper() else ord('a')
            result.append(chr((ord(ch) - base + shift) % 26 + base))
        else:
            result.append(ch)
    return "".join(result)


def caesar_decrypt(text: str, shift: int) -> str:
    return caesar_encrypt(text, 26 - shift)


CIPHERTEXT = caesar_encrypt(PLAINTEXT, CORRECT_SHIFT)


class M02Decrypt(BaseMission):
    id = "02"
    title = "The Encrypted Files"
    briefing = (
        "EMERGENCY: The headmaster's critical files have been encrypted by an "
        "unknown party using a Caesar cipher. The key to decrypting them is hidden "
        "in a riddle. Find the shift key and decrypt the files to reveal their contents."
    )
    objectives = [
        "List files in the secure vault (/vault)",
        "Read the encrypted file",
        "Figure out the cipher shift key",
        "Decrypt the file with the correct key",
    ]
    xp_reward = 150

    def __init__(self):
        self._listed = False
        self._read = False
        self._hint_used = False

    def available_commands(self) -> list[tuple[str, str]]:
        return [
            ("ls /vault", "List files in the secure vault"),
            ("cat /vault/<filename>", "Read a file"),
            ("decrypt /vault/<filename>", "Decrypt a file"),
            ("hint", "Get a hint about the cipher key"),
        ]

    def hint(self) -> str:
        self._hint_used = True
        return (
            'CIPHER HINT: "The key is the number of letters in the word CYBER."\n'
            '  Count carefully: C-Y-B-E-R = ? letters'
        )

    def handle_command(self, cmd: str, args: list[str], player, ui) -> bool:
        if cmd == "ls":
            return self._cmd_ls(args, ui)
        elif cmd == "cat":
            return self._cmd_cat(args, ui)
        elif cmd == "decrypt":
            return self._cmd_decrypt(args, player, ui)
        elif cmd == "hint":
            ui.info(self.hint())
            return False
        else:
            ui.failure(f"Unknown command: {cmd}. Type 'help' for available commands.")
            return False

    def _cmd_ls(self, args: list[str], ui) -> bool:
        path = args[0] if args else ""
        if path not in ("/vault", "vault", "/vault/"):
            ui.failure(f"ls: cannot access '{path}': No such file or directory")
            return False

        from rich.table import Table
        from rich import box

        ui.console.print(f"\n  [bold #00FF41]Directory listing: /vault[/]\n")
        table = Table(box=box.SIMPLE, show_header=True, header_style="dim #00FF41")
        table.add_column("PERMISSIONS", style="dim #00FF41")
        table.add_column("OWNER", style="dim #00FF41")
        table.add_column("SIZE", style="cyan")
        table.add_column("DATE", style="dim #00FF41")
        table.add_column("NAME", style="bold #00FF41")

        table.add_row("-rw-r--r--", "headmaster", "1.2K", "Mar 12 03:47", "MISSION_BRIEF.enc")
        table.add_row("-rw-r--r--", "headmaster", "0.4K", "Mar 12 03:47", "README.txt")
        ui.console.print(table)
        ui.console.print()
        ui.warn(".enc files have been ENCRYPTED — contents are scrambled")
        self._listed = True
        return False

    def _cmd_cat(self, args: list[str], ui) -> bool:
        if not args:
            ui.failure("Usage: cat /vault/<filename>")
            return False
        fname = args[0].replace("/vault/", "").replace("/vault", "").strip("/")
        if fname == "README.txt":
            ui.console.print()
            ui.console.print("  [#00FF41]These files have been encrypted. Find the key.[/]")
            ui.console.print("  [#00FF41]HINT: Read the classics.[/]")
            return False
        elif fname == "MISSION_BRIEF.enc":
            ui.console.print()
            ui.console.print(f"  [dim #00FF41]--- MISSION_BRIEF.enc ---[/]")
            ui.console.print(f"  [bold #00FF41]{CIPHERTEXT}[/]")
            ui.console.print(f"  [dim #00FF41]--- END OF FILE ---[/]")
            ui.console.print()
            ui.info("This text is encrypted with a Caesar cipher. Use 'decrypt' to decode it.")
            self._read = True
            return False
        else:
            ui.failure(f"cat: {fname}: No such file or directory")
            return False

    def _cmd_decrypt(self, args: list[str], player, ui) -> bool:
        if not args:
            ui.failure("Usage: decrypt /vault/<filename>")
            return False
        fname = args[0].replace("/vault/", "").replace("/vault", "").strip("/")
        if fname != "MISSION_BRIEF.enc":
            ui.failure(f"decrypt: {fname}: No such file or directory")
            return False
        if not self._read:
            ui.warn("You should read the file first with: cat /vault/MISSION_BRIEF.enc")

        ui.console.print()
        ui.info("Caesar cipher detected. Enter shift key (1-25):")
        ui.console.print(f"  [dim #00FF41]Tip: type 'hint' if you're stuck[/]")
        ui.console.print()

        while True:
            try:
                raw = ui.console.input(f"  [bold #00FF41]shift key > [/]").strip()
            except (EOFError, KeyboardInterrupt):
                ui.info("Decryption cancelled.")
                return False

            if raw.lower() == "hint":
                ui.info(self.hint())
                continue

            if not raw.isdigit():
                ui.failure("Please enter a number between 1 and 25.")
                continue

            shift = int(raw)
            if not 1 <= shift <= 25:
                ui.failure("Shift must be between 1 and 25.")
                continue

            attempt = caesar_decrypt(CIPHERTEXT, shift)
            ui.console.print()
            ui.console.print(f"  [dim #00FF41]Decrypting with shift {shift}...[/]")
            time.sleep(0.8)

            if shift == CORRECT_SHIFT:
                ui.console.print(f"  [bold #00FF41]--- DECRYPTED OUTPUT ---[/]")
                ui.typewrite(f"  {attempt}", "#00FF41", delay=0.02)
                ui.console.print(f"  [bold #00FF41]--- END ---[/]")
                ui.console.print()
                ui.success("CORRECT KEY! File successfully decrypted.")
                return True
            else:
                ui.console.print(f"  [dim #00FF41]Result: {attempt[:60]}...[/]")
                ui.failure("That doesn't look right. Try another key.")
                ui.console.print()
