from __future__ import annotations
import json
import os
from pathlib import Path

import game.ui as ui
from game.player import Player
from game.missions.base import BaseMission
from game.missions.m01_trace import M01Trace
from game.missions.m02_decrypt import M02Decrypt
from game.missions.m03_rogue import M03Rogue
from game.commands import handle_global_command

SAVE_FILE = Path(__file__).parent.parent / "save.json"
GREEN = "#00FF41"


class GameEngine:
    def __init__(self):
        self.player: Player = Player()
        self.active_mission: BaseMission | None = None
        self.running: bool = True
        self.ui = ui

        self.missions: dict[str, BaseMission] = {
            "01": M01Trace(),
            "02": M02Decrypt(),
            "03": M03Rogue(),
        }

    def load_save(self) -> bool:
        if SAVE_FILE.exists():
            try:
                with open(SAVE_FILE) as f:
                    data = json.load(f)
                self.player = Player.from_dict(data)
                return True
            except Exception:
                pass
        return False

    def save_game(self):
        try:
            with open(SAVE_FILE, "w") as f:
                json.dump(self.player.to_dict(), f, indent=2)
        except Exception as e:
            ui.warn(f"Could not save game: {e}")

    def setup_new_player(self):
        ui.banner()
        ui.console.print(f"  [{GREEN}]Before we begin, agent — we need your codename.[/]")
        ui.console.print(f"  [dim {GREEN}](This is the name you'll be known by on the network.)[/]")
        ui.console.print()
        while True:
            try:
                handle = ui.console.input(f"  [bold {GREEN}]Enter your handle (e.g. VIPER, GHOST, CIPHER): [/]").strip()
            except (EOFError, KeyboardInterrupt):
                handle = "AGENT"
                break
            if handle:
                handle = handle.upper()
                break
            ui.failure("You need a codename to proceed.")

        self.player = Player(handle=handle)
        ui.console.print()
        ui.typewrite(f"  IDENTITY REGISTERED: {handle}", GREEN, delay=0.04)
        ui.typewrite("  ACCESS GRANTED. WELCOME TO NEXUS.", GREEN, delay=0.04)
        ui.console.print()

    def greet_returning_player(self):
        ui.banner()
        ui.console.print(f"  [{GREEN}]SAVE FILE DETECTED. Welcome back, [bold]{self.player.handle}[/].[/]")
        ui.console.print(f"  [dim {GREEN}]Rank: {self.player.rank} | XP: {self.player.xp} | Missions: {len(self.player.completed_missions)} complete[/]")
        ui.console.print()

    def _get_prompt(self) -> str:
        mission_tag = ""
        if self.active_mission:
            mission_tag = f"[dim {GREEN}][M{self.active_mission.id}][/] "
        return f"{mission_tag}[bold {GREEN}][{self.player.handle}@NEXUS ~]$[/] "

    def run(self):
        save_exists = self.load_save()

        if save_exists:
            self.greet_returning_player()
        else:
            self.setup_new_player()

        ui.info("Type 'help' for commands, or 'missions' to see your mission list.")
        ui.console.print()

        while self.running:
            try:
                raw = ui.console.input(self._get_prompt()).strip()
            except (EOFError, KeyboardInterrupt):
                ui.console.print()
                ui.info("Use 'exit' to quit.")
                continue

            if not raw:
                continue

            parts = raw.split()
            cmd = parts[0].lower()
            args = parts[1:]

            # Global commands take priority
            if handle_global_command(cmd, args, self):
                continue

            # Dispatch to active mission
            if self.active_mission:
                # hint is handled globally but route to mission
                if cmd == "hint":
                    ui.info(self.active_mission.hint())
                    continue

                complete = self.active_mission.handle_command(cmd, args, self.player, ui)
                if complete:
                    self._complete_mission(self.active_mission)
            else:
                ui.failure(f"Unknown command: '{cmd}'. Type 'help' for available commands.")
                ui.info("You don't have an active mission. Use 'missions' to see the list, then 'start <id>'.")

        # Exiting
        self.save_game()
        ui.console.print()
        ui.typewrite("  Saving progress...", GREEN, delay=0.03)
        ui.typewrite("  NEXUS connection closed. Stay sharp, agent.", GREEN, delay=0.03)
        ui.console.print()

    def _complete_mission(self, mission: BaseMission):
        ui.mission_complete_splash(mission.title, mission.xp_reward)
        old_rank = self.player.rank
        ranked_up = self.player.add_xp(mission.xp_reward)
        self.player.completed_missions.append(mission.id)
        self.active_mission = None

        if ranked_up:
            ui.rank_up_celebration(old_rank, self.player.rank)

        self.save_game()

        # Auto-unlock next mission message
        next_id = str(int(mission.id) + 1).zfill(2)
        if next_id in self.missions and next_id not in self.player.completed_missions:
            ui.console.print()
            ui.info(f"New mission unlocked: [{next_id}] {self.missions[next_id].title}")
            ui.info(f"Type 'start {next_id}' to begin.")
        elif not any(mid not in self.player.completed_missions for mid in self.missions):
            ui.console.print()
            ui.glitch("  ALL MISSIONS COMPLETE. YOU ARE A TRUE ELITE HACKER.", GREEN)
            ui.console.print()
