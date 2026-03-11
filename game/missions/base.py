from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from game.player import Player
    import game.ui as ui_module


class BaseMission(ABC):
    id: str = ""
    title: str = ""
    briefing: str = ""
    objectives: list[str] = []
    xp_reward: int = 100

    def start(self, player: "Player", ui: "ui_module") -> None:
        ui.mission_briefing(self.title, self.briefing, self.objectives)

    @abstractmethod
    def handle_command(self, cmd: str, args: list[str], player: "Player", ui: "ui_module") -> bool:
        """Process a command. Returns True if mission is now complete."""
        ...

    def hint(self) -> str:
        return "No hint available."

    def available_commands(self) -> list[tuple[str, str]]:
        """Return list of (command, description) for this mission."""
        return []
