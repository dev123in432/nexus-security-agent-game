# NEXUS Security Division

A terminal-based cybersecurity game for kids (ages 10–13). Play as a white-hat admin protecting a school network from real threats — written in Python with a Matrix-style green terminal aesthetic.

![Python](https://img.shields.io/badge/Python-3.10+-green) ![Platform](https://img.shields.io/badge/Platform-Windows-blue)

---

## The Mission

You are an agent of the NEXUS Security Division. Three missions stand between the school network and total compromise:

| # | Mission | Objective |
|---|---------|-----------|
| 01 | **Trace the Intruder** | Scan the network, trace a suspicious IP, and block the attacker |
| 02 | **The Encrypted Files** | Crack a Caesar cipher to decrypt the headmaster's stolen files |
| 03 | **The Rogue Admin** | Find and delete a backdoor account before it causes damage |

Complete missions to earn XP and rise through the ranks: **Cadet → Analyst → Agent → Elite Hacker**

---

## Installation

### Quick Start (Windows)

1. Download `nexus-security-game-v1.0.0.zip` from [Releases](../../releases)
2. Unzip to a folder
3. Open PowerShell in that folder and run:

```powershell
.\setup.ps1
```

The setup script will install Python automatically (via winget on Windows 11) if it isn't already installed.

### Manual Setup

Requires Python 3.10+.

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python main.py
```

---

## Playing the Game

```
[VIPER@NEXUS ~]$ missions       — see all missions
[VIPER@NEXUS ~]$ start 01       — begin a mission
[VIPER@NEXUS ~]$ help           — show available commands
[VIPER@NEXUS ~]$ whoami         — view your rank and XP
```

Your progress is saved automatically between sessions.

---

## Built With

- [Rich](https://github.com/Textualize/rich) — terminal UI, panels, progress bars
- [pyfiglet](https://github.com/pwaller/pyfiglet) — ASCII art titles
