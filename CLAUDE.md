# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repo

https://github.com/dev123in432/nexus-security-agent-game

## Setup (Windows)

**Prerequisites:** Python 3.10+ — get it from https://www.python.org/downloads/ and tick "Add Python to PATH" during install. Windows 11 users can skip this; the setup script will install it via `winget` automatically.

**First-time setup** — run once in PowerShell from the project folder:
```powershell
.\setup.ps1
```
This checks/installs Python, sets execution policy, creates `.venv`, and installs all dependencies.

**Run the game:**
```powershell
.venv\Scripts\Activate.ps1
python main.py
```
Or without activating: `.venv\Scripts\python.exe main.py`

Always use `.venv\Scripts\python` rather than the system Python.

## Architecture

The game is a terminal REPL built around a central `GameEngine` in `game/engine.py`. The engine holds all state: the current `Player`, the active mission, and the mission registry. On each loop iteration it prints a prompt, reads input, and dispatches to either global commands or the active mission.

**Command routing:** `engine.py` calls `handle_global_command()` from `commands.py` first. If that returns `False` (unhandled), the input is forwarded to `active_mission.handle_command()`. Global commands include `help`, `whoami`, `missions`, `start`, `status`, `clear`, `exit`, and the hidden easter egg (`birthday` / `dad`).

**Missions:** Each mission lives in `game/missions/` and extends `BaseMission`. The `handle_command()` method returns `True` when the mission is complete, which signals the engine to award XP, check for rank-up, auto-unlock the next mission, and save. Missions are stateful instances (tracking progress flags like `_scanned`, `_traced`) — they are instantiated once at engine startup and reused.

**UI:** All terminal output goes through `game/ui.py`, which wraps `rich`. The module is imported as a namespace (`import game.ui as ui`) and passed into missions and commands — there is no UI class instance. Key functions: `typewrite()` for dramatic character-by-character output, `fake_scan()` and `fake_trace()` for animated progress, `glitch()` for flickering text effects.

**Save system:** `save.json` is written to the project root on mission complete and on exit. It stores `handle`, `xp`, and `completed_missions`. Loaded automatically at startup by `engine.load_save()`.

**Color palette:** Matrix green `#00FF41` is the primary color throughout. Use `DIM_GREEN = "#007A20"` for secondary text, `cyan` for info/highlights, `red` for warnings/errors. All constants are defined at the top of `ui.py` and duplicated locally in `commands.py`.

## Shell Commands

Never prefix bash commands with `cd <project-dir> &&`. The working directory is already set to the project root. Run `git`, `python`, and other commands directly — e.g. `git status`, not `cd C:/... && git status`. Compound commands with `cd` trigger unnecessary approval prompts.

## Adding a new mission

1. Create `game/missions/m0N_name.py` extending `BaseMission`
2. Set `id`, `title`, `briefing`, `objectives`, `xp_reward`
3. Implement `handle_command()` returning `True` on completion
4. Register it in `GameEngine.__init__()` in `engine.py`
