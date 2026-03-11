import time
import random
import sys

from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, BarColumn, TextColumn, TimeElapsedColumn
from rich.text import Text
from rich.table import Table
from rich import box
import pyfiglet

console = Console()

GREEN = "#00FF41"
DIM_GREEN = "#007A20"
CYAN = "cyan"
RED = "red"
WHITE = "white"
YELLOW = "yellow"


def _g(text: str, bold: bool = False) -> Text:
    t = Text(text, style=f"bold {GREEN}" if bold else GREEN)
    return t


def banner():
    console.clear()
    _matrix_burst(rows=8, duration=0.6)
    fig = pyfiglet.figlet_format("NEXUS", font="big")
    lines = fig.strip().split("\n")
    for line in lines:
        console.print(line, style=f"bold {GREEN}")
    console.print()
    console.print(f"  [bold {GREEN}]N E X U S   S E C U R I T Y   D I V I S I O N[/]")
    console.print(f"  [dim {GREEN}]{'═' * 52}[/]")
    time.sleep(0.3)
    typewrite("  CONNECTION ESTABLISHED... IDENTITY VERIFIED", GREEN, delay=0.03)
    typewrite("  WELCOME, AGENT.", GREEN, delay=0.05)
    console.print(f"  [dim {GREEN}]{'═' * 52}[/]")
    console.print()


def _matrix_burst(rows: int = 12, duration: float = 1.0):
    """Brief matrix rain animation."""
    chars = "01アイウエオカキクケコサシスセソタチツテトナニヌネノハヒフヘホ"
    width = 80
    end_time = time.time() + duration
    rendered = 0
    while time.time() < end_time and rendered < rows:
        line = ""
        for _ in range(width):
            if random.random() < 0.15:
                line += f"[bold {GREEN}]{random.choice(chars)}[/]"
            elif random.random() < 0.3:
                line += f"[dim {GREEN}]{random.choice(chars)}[/]"
            else:
                line += " "
        console.print(line)
        time.sleep(0.05)
        rendered += 1


def matrix_rain(duration: float = 2.0):
    """Full matrix rain animation."""
    console.clear()
    _matrix_burst(rows=24, duration=duration)
    console.clear()


def typewrite(text: str, color: str = GREEN, delay: float = 0.03):
    for ch in text:
        sys.stdout.write(f"\033[38;2;0;255;65m{ch}\033[0m")
        sys.stdout.flush()
        time.sleep(delay)
    sys.stdout.write("\n")
    sys.stdout.flush()


def glitch(text: str, color: str = GREEN):
    """Flash garbled text then resolve to real text."""
    chars = "!@#$%^&*<>?/\\|{}[]~`"
    for _ in range(4):
        garbled = "".join(random.choice(chars) if random.random() < 0.5 else c for c in text)
        console.print(f"[{color}]{garbled}[/]", end="\r")
        time.sleep(0.08)
    console.print(f"[bold {color}]{text}[/]")


def fake_scan(target: str = "NETWORK", duration: float = 3.0):
    """Animated scan with hex addresses and progress bar."""
    console.print(f"\n  [{GREEN}]>>> INITIATING DEEP SCAN on [{WHITE}]{target}[/]...[/]\n")
    time.sleep(0.3)
    ips = [
        "192.168.1.1", "192.168.1.24", "10.0.0.1", "10.0.0.24",
        "172.16.0.8", "172.16.0.15", "172.16.0.42", "185.220.101.47",
    ]
    total_steps = 40
    step_time = duration / total_steps

    with Progress(
        TextColumn(f"  [bold {GREEN}]{{task.fields[hex_addr]}}[/]"),
        BarColumn(bar_width=20, style=DIM_GREEN, complete_style=GREEN),
        TextColumn(f"[{GREEN}]{{task.percentage:>3.0f}}%[/]"),
        TextColumn(f"[dim {GREEN}]{{task.fields[ip]}}[/]"),
        console=console,
        transient=False,
    ) as progress:
        task = progress.add_task(
            "scan",
            total=total_steps,
            hex_addr="0x0000",
            ip="...",
        )
        for i in range(total_steps):
            hex_addr = f"0x{random.randint(0x1000, 0xFFFF):04X}"
            ip = ips[min(i * len(ips) // total_steps, len(ips) - 1)]
            progress.update(task, advance=1, hex_addr=hex_addr, ip=ip)
            time.sleep(step_time)

    console.print()
    console.print(f"  [bold {GREEN}]SCAN COMPLETE[/]")


def fake_trace(ip: str):
    """Hop-by-hop traceroute animation."""
    hops = [
        ("192.168.1.1",     "2ms",   "Local Gateway",           "N/A",        "Home ISP"),
        ("10.45.0.1",       "8ms",   "Regional Hub",            "N/A",        "BackboneNet"),
        ("84.17.40.1",      "22ms",  "Amsterdam, Netherlands",  "52.37°N",    "LEASEWEB"),
        ("62.115.43.254",   "35ms",  "Frankfurt, Germany",      "50.11°N",    "TELIA"),
        ("195.22.195.36",   "61ms",  "Moscow, Russia",          "55.75°N",    "ROSTELECOM"),
        (ip,                "88ms",  "*** ORIGIN LOCATED ***",  "55.75°N",    "TOR EXIT NODE"),
    ]
    console.print(f"\n  [{GREEN}]>>> TRACING ROUTE TO [{WHITE}]{ip}[/] ...[/]\n")
    time.sleep(0.5)

    table = Table(box=box.SIMPLE, show_header=True, header_style=f"dim {GREEN}")
    table.add_column("HOP", style=f"dim {GREEN}", width=4)
    table.add_column("IP ADDRESS", style=f"bold {GREEN}", width=18)
    table.add_column("LAT", style=CYAN, width=8)
    table.add_column("LOCATION", style=f"{GREEN}", width=24)
    table.add_column("ISP", style=f"dim {GREEN}", width=16)

    for i, (hop_ip, lat_val, location, lat, isp) in enumerate(hops, 1):
        time.sleep(0.5)
        table.add_row(str(i), hop_ip, lat_val, location, isp)
        console.print(table)
        if i < len(hops):
            # Reprint with growing table — clear last and reprint
            pass  # rich handles incremental display

    console.print()
    console.print(f"  [bold {RED}]⚠  ORIGIN CONFIRMED: TOR EXIT NODE — ANONYMOUS ATTACKER[/]")


def mission_briefing(title: str, desc: str, objectives: list[str]):
    glitch(f"  INCOMING TRANSMISSION: {title}", GREEN)
    time.sleep(0.4)
    obj_text = "\n".join(f"  [{GREEN}]▶[/] {o}" for o in objectives)
    content = f"[dim {GREEN}]{desc}[/]\n\n[bold {GREEN}]OBJECTIVES:[/]\n{obj_text}"
    panel = Panel(
        content,
        title=f"[bold {GREEN}]{title}[/]",
        border_style=GREEN,
        padding=(1, 2),
    )
    console.print(panel)
    console.print()


def success(msg: str):
    console.print(f"  [bold {GREEN}]✓  {msg}[/]")


def failure(msg: str):
    console.print(f"  [bold {RED}]✗  {msg}[/]")


def info(msg: str):
    console.print(f"  [{CYAN}]ℹ  {msg}[/]")


def warn(msg: str):
    console.print(f"  [bold {YELLOW}]⚠  {msg}[/]")


def rank_up_celebration(old_rank: str, new_rank: str):
    console.print()
    console.print(f"  [dim {GREEN}]{'═' * 52}[/]")
    glitch(f"  RANK UP!", GREEN)
    console.print(f"  [{GREEN}]{old_rank}[/] [dim {GREEN}]→[/] [bold {GREEN}]{new_rank}[/]")
    console.print(f"  [dim {GREEN}]{'═' * 52}[/]")
    console.print()


def mission_complete_splash(title: str, xp: int):
    console.print()
    console.print(f"  [dim {GREEN}]{'█' * 52}[/]")
    glitch(f"  MISSION COMPLETE: {title}", GREEN)
    console.print(f"  [bold {GREEN}]+{xp} XP AWARDED[/]")
    console.print(f"  [dim {GREEN}]{'█' * 52}[/]")
    time.sleep(0.5)


def xp_bar(xp: int, max_xp: int = 600):
    filled = int((xp / max_xp) * 30)
    bar = "█" * filled + "░" * (30 - filled)
    console.print(f"  [{GREEN}][{bar}] {xp}/{max_xp} XP[/]")


def birthday_easter_egg():
    console.clear()
    matrix_rain(1.5)
    console.clear()
    fig = pyfiglet.figlet_format("HAPPY\nBIRTHDAY", font="big")
    for line in fig.strip().split("\n"):
        time.sleep(0.05)
        # Alternate colors for celebration effect
        color = random.choice(["#00FF41", "cyan", "yellow", "#FF69B4", "white"])
        console.print(line, style=f"bold {color}")

    time.sleep(0.3)
    stars = " ".join(["★" if random.random() > 0.5 else "✦" for _ in range(20)])
    console.print()
    console.print(f"  [{YELLOW}]{stars}[/]")
    console.print()

    panel = Panel(
        f"[bold white]Happy Birthday — Love, Dad ❤️[/]\n\n"
        f"[{GREEN}]You are the best son in the world.\n"
        f"Keep hacking, keep learning, keep being awesome.[/]",
        border_style=YELLOW,
        padding=(1, 4),
    )
    console.print(panel)
    console.print()
    console.print(f"  [{YELLOW}]{stars}[/]")
    time.sleep(3)
    console.clear()
