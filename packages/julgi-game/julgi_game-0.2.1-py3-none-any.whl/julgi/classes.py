from __future__ import annotations

from dataclasses import dataclass, field
from hashlib import blake2s

from .util import stat


@dataclass
class User:
    name: str
    blake: str = field(init=False)

    max_hp: int = field(init=False)
    hp: int = field(init=False)

    attack: int = field(init=False)
    magic: int = field(init=False)
    speed: int = field(init=False)
    ability: int = field(init=False)
    hit: int = field(init=False)
    critical: int = field(init=False)

    skills: list[Skill] = field(default_factory=list, init=False)

    def __post_init__(self):
        self.blake = blake2s(self.name.encode("utf-8")).hexdigest()

        self.max_hp = stat(
            int(self.blake[0:6], 16), value_max=0xFFFFFF, low=8000, high=15000
        )
        self.hp = self.max_hp

        self.attack = stat(
            int(self.blake[4:8], 16), value_max=0xFFFF, low=1500, high=3000
        )
        self.magic = stat(
            int(self.blake[8:12], 16), value_max=0xFFFF, low=1000, high=3000
        )
        self.speed = stat(
            int(self.blake[12:16], 16), value_max=0xFFFF, low=1000, high=3000
        )
        self.ability = stat(
            int(self.blake[16:20], 16), value_max=0xFFFF, low=1000, high=3000
        )
        self.hit = stat(int(self.blake[20:22], 16), value_max=0xFF, low=70, high=100)
        self.critical = stat(
            int(self.blake[22:24], 16), value_max=0xFF, low=10, high=30
        )

    @property
    def live(self) -> bool:
        return self.hp > 0

    def reset_hp(self):
        self.hp = self.max_hp


@dataclass
class Skill:
    name: str
    stat: str
    multiplier: float
    heal: bool = False


@dataclass
class BattleMetaData:
    user1: User
    user2: User
    seed: str


@dataclass
class BattleData:
    user: str
    user_hp: int
    user_max_hp: int
    other: str
    other_hp: int
    other_max_hp: int
    use_skill: bool = False
    skill: Skill | None = None
    use_heal: bool = False
    heal_amount: int | None = None
    is_hit: bool = True
    is_critical: bool = False
    damage: int | None = None


@dataclass
class PostBattleData:
    winner: str
    turns: int
