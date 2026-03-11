from dataclasses import dataclass, field
from typing import List


RANKS = [
    (0,    "Cadet"),
    (100,  "Analyst"),
    (300,  "Agent"),
    (600,  "Elite Hacker"),
]


def rank_for_xp(xp: int) -> str:
    rank = RANKS[0][1]
    for threshold, name in RANKS:
        if xp >= threshold:
            rank = name
    return rank


@dataclass
class Player:
    handle: str = "AGENT"
    xp: int = 0
    completed_missions: List[str] = field(default_factory=list)

    @property
    def rank(self) -> str:
        return rank_for_xp(self.xp)

    def add_xp(self, amount: int) -> bool:
        """Add XP and return True if rank changed."""
        old_rank = self.rank
        self.xp += amount
        new_rank = self.rank
        return new_rank != old_rank

    def to_dict(self) -> dict:
        return {
            "handle": self.handle,
            "xp": self.xp,
            "completed_missions": self.completed_missions,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Player":
        return cls(
            handle=data.get("handle", "AGENT"),
            xp=data.get("xp", 0),
            completed_missions=data.get("completed_missions", []),
        )

    def next_rank_info(self) -> tuple[str, int] | None:
        """Return (next_rank_name, xp_needed) or None if maxed."""
        for threshold, name in RANKS:
            if self.xp < threshold:
                return (name, threshold - self.xp)
        return None
