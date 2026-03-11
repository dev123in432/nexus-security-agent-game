from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from game.engine import GameEngine

GREEN = "#00FF41"
CYAN = "cyan"


def handle_global_command(cmd: str, args: list[str], engine: "GameEngine") -> bool:
    """Handle global commands. Returns True if handled."""
    ui = engine.ui
    player = engine.player

    if cmd == "help":
        _cmd_help(engine)
        return True
    elif cmd == "whoami":
        _cmd_whoami(engine)
        return True
    elif cmd == "missions":
        _cmd_missions(engine)
        return True
    elif cmd == "start":
        _cmd_start(args, engine)
        return True
    elif cmd == "status":
        _cmd_status(engine)
        return True
    elif cmd == "clear":
        ui.console.clear()
        return True
    elif cmd == "exit" or cmd == "quit":
        engine.running = False
        return True
    elif cmd in ("birthday", "dad"):
        ui.birthday_easter_egg()
        return True

    return False


def _cmd_help(engine: "GameEngine"):
    ui = engine.ui
    from rich.table import Table
    from rich import box

    ui.console.print(f"\n  [bold {GREEN}]AVAILABLE COMMANDS[/]\n")
    table = Table(box=box.SIMPLE, show_header=False)
    table.add_column("CMD", style=f"bold {GREEN}", width=22)
    table.add_column("DESC", style=f"dim {GREEN}")

    global_cmds = [
        ("help", "Show this help screen"),
        ("whoami", "Display your agent profile"),
        ("missions", "List all missions and their status"),
        ("start <id>", "Begin a mission (e.g. start 01)"),
        ("status", "Current system status overview"),
        ("clear", "Clear the terminal"),
        ("exit", "Save and exit"),
    ]
    for cmd, desc in global_cmds:
        table.add_row(cmd, desc)

    ui.console.print(table)

    if engine.active_mission:
        mission_cmds = engine.active_mission.available_commands()
        if mission_cmds:
            ui.console.print(f"\n  [bold {GREEN}]MISSION COMMANDS — {engine.active_mission.title}[/]\n")
            mt = Table(box=box.SIMPLE, show_header=False)
            mt.add_column("CMD", style=f"bold {GREEN}", width=22)
            mt.add_column("DESC", style=f"dim {GREEN}")
            for cmd, desc in mission_cmds:
                mt.add_row(cmd, desc)
            ui.console.print(mt)
            ui.console.print(f"  [dim {GREEN}]Tip: type 'hint' for a nudge in the right direction[/]")

    ui.console.print()


def _cmd_whoami(engine: "GameEngine"):
    ui = engine.ui
    player = engine.player
    from rich.panel import Panel

    next_rank = player.next_rank_info()
    next_str = f"[dim {GREEN}]{next_rank[1]} XP to {next_rank[0]}[/]" if next_rank else f"[bold {GREEN}]MAX RANK[/]"

    content = (
        f"[bold {GREEN}]HANDLE:[/]  [{GREEN}]{player.handle}[/]\n"
        f"[bold {GREEN}]RANK:  [/]  [{GREEN}]{player.rank}[/]\n"
        f"[bold {GREEN}]XP:    [/]  [{GREEN}]{player.xp}[/]  {next_str}\n"
        f"[bold {GREEN}]MISSIONS COMPLETE:[/]  [{GREEN}]{len(player.completed_missions)}[/]"
    )
    panel = Panel(content, title=f"[bold {GREEN}]AGENT PROFILE[/]", border_style=GREEN, padding=(0, 2))
    ui.console.print()
    ui.console.print(panel)
    ui.console.print()
    ui.xp_bar(player.xp)
    ui.console.print()


def _cmd_missions(engine: "GameEngine"):
    ui = engine.ui
    player = engine.player
    from rich.table import Table
    from rich import box

    ui.console.print(f"\n  [bold {GREEN}]MISSION ROSTER[/]\n")
    table = Table(box=box.ROUNDED, show_header=True, header_style=f"bold {GREEN}", border_style=GREEN)
    table.add_column("ID", style=f"bold {GREEN}", width=4)
    table.add_column("MISSION", style=f"{GREEN}", width=26)
    table.add_column("XP", style=CYAN, width=6)
    table.add_column("STATUS", width=16)

    for mission in engine.missions.values():
        mid = mission.id
        is_complete = mid in player.completed_missions
        is_active = engine.active_mission and engine.active_mission.id == mid

        if is_complete:
            status = f"[bold {GREEN}][✓ COMPLETE][/]"
        elif is_active:
            status = f"[bold {CYAN}][► ACTIVE  ][/]"
        else:
            status = f"[dim {GREEN}][  LOCKED  ][/]"

        table.add_row(mid, mission.title, str(mission.xp_reward), status)

    ui.console.print(table)
    ui.console.print()


def _cmd_start(args: list[str], engine: "GameEngine"):
    ui = engine.ui
    if not args:
        ui.failure("Usage: start <mission_id> (e.g. start 01)")
        return

    mid = args[0].zfill(2)
    if mid not in engine.missions:
        ui.failure(f"Mission '{mid}' not found. Type 'missions' to see available missions.")
        return

    if mid in engine.player.completed_missions:
        ui.info(f"Mission {mid} already completed. Type 'missions' to see what's next.")
        return

    mission = engine.missions[mid]
    engine.active_mission = mission
    mission.start(engine.player, ui)


def _cmd_status(engine: "GameEngine"):
    ui = engine.ui
    player = engine.player
    from rich.panel import Panel
    from rich.table import Table
    from rich import box

    completed = len(player.completed_missions)
    total = len(engine.missions)
    threat_level = "CRITICAL" if completed == 0 else ("ELEVATED" if completed < total else "SECURE")
    threat_color = "bold red" if completed == 0 else ("bold yellow" if completed < total else f"bold {GREEN}")

    content = (
        f"[bold {GREEN}]SYSTEM:[/]       [{GREEN}]NEXUS SECURITY NETWORK v4.2[/]\n"
        f"[bold {GREEN}]AGENT:[/]        [{GREEN}]{player.handle} ({player.rank})[/]\n"
        f"[bold {GREEN}]THREAT LEVEL:[/] [{threat_color}]{threat_level}[/]\n"
        f"[bold {GREEN}]MISSIONS:[/]     [{GREEN}]{completed}/{total} complete[/]\n"
        f"[bold {GREEN}]XP:[/]           [{GREEN}]{player.xp}[/]"
    )
    panel = Panel(content, title=f"[bold {GREEN}]SYSTEM STATUS[/]", border_style=GREEN, padding=(0, 2))
    ui.console.print()
    ui.console.print(panel)
    ui.console.print()
