import time
from game.missions.base import BaseMission

ROGUE_USER = "sv_admin99"

USERS = [
    {"username": "jsmith",     "role": "Teacher",   "dept": "Mathematics", "created": "2024-09-01 08:30", "email": "j.smith@school.edu"},
    {"username": "mwilson",    "role": "Teacher",   "dept": "Science",     "created": "2024-09-01 08:45", "email": "m.wilson@school.edu"},
    {"username": "patel_k",    "role": "Teacher",   "dept": "English",     "created": "2024-09-01 09:00", "email": "k.patel@school.edu"},
    {"username": "admin1",     "role": "Admin",     "dept": "IT Support",  "created": "2024-08-15 10:00", "email": "admin@school.edu"},
    {"username": "headmaster", "role": "Principal", "dept": "Management",  "created": "2023-01-10 09:00", "email": "head@school.edu"},
    {"username": "lib_jones",  "role": "Staff",     "dept": "Library",     "created": "2024-09-01 08:15", "email": "b.jones@school.edu"},
    {"username": "r_chen",     "role": "Teacher",   "dept": "Art",         "created": "2024-09-03 11:00", "email": "r.chen@school.edu"},
    {"username": ROGUE_USER,   "role": "ADMIN",     "dept": "—",           "created": "2026-03-12 03:17", "email": "sv99@tempmail.xyz"},
]

ROGUE_HISTORY = [
    ("2026-03-12 03:17:04", "ACCOUNT CREATED",       "Unknown source",        "SUCCESS"),
    ("2026-03-12 03:18:11", "PRIVILEGE ESCALATION",  "127.0.0.1",             "SUCCESS"),
    ("2026-03-12 03:19:44", "FILE ACCESS /vault",     "185.220.101.47",        "SUCCESS"),
    ("2026-03-12 03:21:02", "MODIFIED user.conf",    "185.220.101.47",        "SUCCESS"),
    ("2026-03-12 03:22:18", "ATTEMPTED root access", "185.220.101.47",        "BLOCKED"),
]


class M03Rogue(BaseMission):
    id = "03"
    title = "The Rogue Admin"
    briefing = (
        "CRITICAL ALERT: Our monitoring system has detected an unauthorized admin account "
        "that appeared in the user database at 3am. It has already accessed restricted files. "
        "You must find the rogue account, investigate it, and DELETE it before it does "
        "more damage. Move fast — every minute counts."
    )
    objectives = [
        "List all users and find the suspicious one",
        "Inspect the suspicious account for evidence",
        "Delete the rogue account to secure the system",
    ]
    xp_reward = 200

    def __init__(self):
        self._listed = False
        self._inspected = False
        self._deleted = False

    def available_commands(self) -> list[tuple[str, str]]:
        return [
            ("users list", "Show all user accounts"),
            ("users inspect <username>", "Inspect a user account in detail"),
            ("users delete <username>", "Delete a user account"),
        ]

    def hint(self) -> str:
        if not self._listed:
            return "Run 'users list' to see all accounts on the system."
        if not self._inspected:
            return "Look for accounts created at unusual hours, with no department, or suspicious email domains."
        return f"Use 'users delete {ROGUE_USER}' to remove the rogue account."

    def handle_command(self, cmd: str, args: list[str], player, ui) -> bool:
        if cmd == "users":
            return self._cmd_users(args, player, ui)
        else:
            ui.failure(f"Unknown command: {cmd}. Type 'help' for available commands.")
            return False

    def _cmd_users(self, args: list[str], player, ui) -> bool:
        if not args:
            ui.failure("Usage: users [list|inspect|delete] ...")
            return False

        sub = args[0]
        if sub == "list":
            return self._users_list(ui)
        elif sub == "inspect":
            if len(args) < 2:
                ui.failure("Usage: users inspect <username>")
                return False
            return self._users_inspect(args[1], ui)
        elif sub == "delete":
            if len(args) < 2:
                ui.failure("Usage: users delete <username>")
                return False
            return self._users_delete(args[1], player, ui)
        else:
            ui.failure(f"Unknown users subcommand: {sub}")
            return False

    def _users_list(self, ui) -> bool:
        from rich.table import Table
        from rich import box

        ui.console.print(f"\n  [bold #00FF41]SYSTEM USER DATABASE — {len(USERS)} ACCOUNTS[/]\n")
        table = Table(box=box.SIMPLE, show_header=True, header_style="dim #00FF41")
        table.add_column("USERNAME", style="bold #00FF41", width=14)
        table.add_column("ROLE", style="#00FF41", width=10)
        table.add_column("DEPT", style="dim #00FF41", width=16)
        table.add_column("CREATED", style="dim #00FF41", width=18)
        table.add_column("EMAIL", style="cyan", width=24)

        for u in USERS:
            is_rogue = u["username"] == ROGUE_USER
            row_style = "bold red" if is_rogue else ""
            table.add_row(
                u["username"],
                u["role"],
                u["dept"],
                u["created"],
                u["email"],
                style=row_style,
            )
            time.sleep(0.05)

        ui.console.print(table)
        ui.console.print()
        ui.warn("One account looks suspicious. Use 'users inspect <username>' to investigate.")
        self._listed = True
        return False

    def _users_inspect(self, username: str, ui) -> bool:
        from rich.table import Table
        from rich import box

        user = next((u for u in USERS if u["username"] == username), None)
        if not user:
            ui.failure(f"User '{username}' not found.")
            return False

        is_rogue = username == ROGUE_USER
        ui.console.print(f"\n  [bold #00FF41]USER PROFILE: {username}[/]\n")

        for k, v in user.items():
            color = "bold red" if is_rogue else "#00FF41"
            ui.console.print(f"  [dim #00FF41]{k.upper():<16}[/] [{color}]{v}[/]")

        if is_rogue:
            ui.console.print()
            ui.warn("ACCOUNT CREATED AT 3AM — HIGHLY SUSPICIOUS")
            ui.warn("EMAIL DOMAIN: tempmail.xyz — DISPOSABLE ADDRESS")
            ui.warn("NO DEPARTMENT ASSIGNED — NOT A REAL STAFF MEMBER")
            ui.console.print()
            ui.console.print(f"  [bold #00FF41]LOGIN HISTORY:[/]\n")
            table = Table(box=box.SIMPLE, show_header=True, header_style="dim #00FF41")
            table.add_column("TIME", style="dim #00FF41", width=20)
            table.add_column("ACTION", style="bold red", width=24)
            table.add_column("SOURCE IP", style="cyan", width=18)
            table.add_column("RESULT", style="bold #00FF41", width=10)
            for row in ROGUE_HISTORY:
                time.sleep(0.1)
                result_color = "bold red" if row[3] == "SUCCESS" else "yellow"
                table.add_row(row[0], row[1], row[2], f"[{result_color}]{row[3]}[/]")
                ui.console.print(table)
            ui.console.print()
            ui.warn("This is the attacker's backdoor account!")
            self._inspected = True
        else:
            ui.info("This account appears to be legitimate.")

        return False

    def _users_delete(self, username: str, player, ui) -> bool:
        user = next((u for u in USERS if u["username"] == username), None)
        if not user:
            ui.failure(f"User '{username}' not found.")
            return False

        if username != ROGUE_USER:
            ui.failure(f"WARNING: '{username}' is a legitimate account. Do NOT delete real users!")
            return False

        ui.console.print()
        ui.warn(f"You are about to PERMANENTLY DELETE account: {username}")
        ui.warn("This cannot be undone. Are you sure?")
        ui.console.print()

        try:
            confirm = ui.console.input(f"  [bold red]Type 'CONFIRM' to proceed: [/]").strip()
        except (EOFError, KeyboardInterrupt):
            ui.info("Deletion cancelled.")
            return False

        if confirm != "CONFIRM":
            ui.info("Deletion cancelled.")
            return False

        ui.console.print()
        ui.console.print(f"  [#00FF41]>>> DELETING ACCOUNT: {username}...[/]")
        for step in [
            "Revoking session tokens...",
            "Removing from authentication database...",
            "Purging access logs (backdated entries)...",
            "Closing open connections from 185.220.101.47...",
            "Account deletion complete.",
        ]:
            time.sleep(0.4)
            ui.console.print(f"  [dim #00FF41]  {step}[/]")

        ui.console.print()
        ui.success(f"Rogue account '{username}' has been ELIMINATED.")
        ui.success("System is now secure.")
        self._deleted = True
        return True
