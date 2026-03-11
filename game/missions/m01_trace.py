import time
from game.missions.base import BaseMission

SUSPICIOUS_IP = "185.220.101.47"


class M01Trace(BaseMission):
    id = "01"
    title = "Trace the Intruder"
    briefing = (
        "ALERT: An unknown IP is hammering the school network with thousands of "
        "connection attempts per minute. We need you to scan the network, trace "
        "the attacker's origin, analyze their methods, and BLOCK them."
    )
    objectives = [
        "Scan the network to find the suspicious IP",
        "Trace the IP to its origin",
        "Analyze the attack pattern",
        "Block the attacker with the firewall",
    ]
    xp_reward = 100

    def __init__(self):
        self._scanned = False
        self._traced = False
        self._analyzed = False

    def available_commands(self) -> list[tuple[str, str]]:
        return [
            ("scan network", "Scan the network for anomalies"),
            ("trace <ip>", "Trace an IP address hop-by-hop"),
            ("analyze <ip>", "Analyze traffic from an IP"),
            ("firewall block <ip>", "Block an IP with the firewall"),
        ]

    def hint(self) -> str:
        if not self._scanned:
            return "Try 'scan network' to find who is attacking us."
        if not self._traced:
            return f"Try 'trace {SUSPICIOUS_IP}' to find where the attacker is located."
        if not self._analyzed:
            return f"Try 'analyze {SUSPICIOUS_IP}' to see what they're doing."
        return f"Try 'firewall block {SUSPICIOUS_IP}' to shut them out."

    def handle_command(self, cmd: str, args: list[str], player, ui) -> bool:
        if cmd == "scan":
            return self._cmd_scan(args, ui)
        elif cmd == "trace":
            return self._cmd_trace(args, ui)
        elif cmd == "analyze":
            return self._cmd_analyze(args, ui)
        elif cmd == "firewall":
            return self._cmd_firewall(args, ui)
        else:
            ui.failure(f"Unknown command: {cmd}. Type 'help' for available commands.")
            return False

    def _cmd_scan(self, args: list[str], ui) -> bool:
        if not args or args[0] != "network":
            ui.failure("Usage: scan network")
            return False
        ui.fake_scan("SCHOOL NETWORK", duration=3.0)
        time.sleep(0.4)
        ui.warn("ANOMALY DETECTED")
        ui.warn(f"{SUSPICIOUS_IP} — 4,200 connection attempts in 60 seconds")
        ui.info("This IP is NOT on our network. It is external.")
        self._scanned = True
        return False

    def _cmd_trace(self, args: list[str], ui) -> bool:
        if not args:
            ui.failure("Usage: trace <ip>")
            return False
        ip = args[0]
        if ip != SUSPICIOUS_IP:
            ui.info(f"Tracing {ip}... nothing suspicious found.")
            return False
        if not self._scanned:
            ui.warn("You need to scan the network first.")
            return False
        ui.fake_trace(SUSPICIOUS_IP)
        self._traced = True
        return False

    def _cmd_analyze(self, args: list[str], ui) -> bool:
        if not args:
            ui.failure("Usage: analyze <ip>")
            return False
        ip = args[0]
        if ip != SUSPICIOUS_IP:
            ui.info(f"No suspicious activity from {ip}.")
            return False
        if not self._scanned:
            ui.warn("Scan the network first.")
            return False

        from rich.table import Table
        from rich import box

        ui.console.print(f"\n  [bold #00FF41]TRAFFIC ANALYSIS: {ip}[/]\n")
        table = Table(box=box.SIMPLE, show_header=True, header_style="dim #00FF41")
        table.add_column("TIMESTAMP", style="dim #00FF41")
        table.add_column("TYPE", style="bold #00FF41")
        table.add_column("TARGET PORT", style="cyan")
        table.add_column("COUNT", style="bold white")

        rows = [
            ("03:41:02", "PORT SCAN", "22 (SSH)", "841"),
            ("03:41:18", "PORT SCAN", "80 (HTTP)", "1,204"),
            ("03:41:35", "PORT SCAN", "443 (HTTPS)", "944"),
            ("03:41:52", "BRUTE FORCE", "22 (SSH)", "1,211"),
        ]
        for r in rows:
            table.add_row(*r)
            time.sleep(0.2)
            ui.console.print(table)

        ui.console.print()
        ui.warn("Attack type: PORT SCAN + SSH BRUTE FORCE")
        ui.info("Attacker is trying to find open ports and guess passwords.")
        self._analyzed = True
        return False

    def _cmd_firewall(self, args: list[str], ui) -> bool:
        if len(args) < 2 or args[0] != "block":
            ui.failure("Usage: firewall block <ip>")
            return False
        ip = args[1]
        if ip != SUSPICIOUS_IP:
            ui.failure(f"{ip} is not a known threat.")
            return False
        if not self._scanned:
            ui.warn("You should scan and trace the IP first.")
            return False

        ui.console.print(f"\n  [#00FF41]>>> APPLYING FIREWALL RULE...[/]")
        time.sleep(0.3)
        for rule in [
            f"iptables -A INPUT -s {ip} -j DROP",
            f"iptables -A OUTPUT -d {ip} -j DROP",
            "RULE SAVED TO /etc/firewall/rules.d/blocked.conf",
        ]:
            time.sleep(0.4)
            ui.console.print(f"  [dim #00FF41]  {rule}[/]")

        time.sleep(0.5)
        ui.success(f"{ip} has been BLOCKED. No further connections possible.")
        return True
