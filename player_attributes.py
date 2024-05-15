from pydantic import BaseModel
from enum import IntEnum, auto


class PreferredFoot(IntEnum):
    LEFT = auto()
    RIGHT = auto()
    BOTH = auto()


class Positions(IntEnum):
    GK = auto()
    DF = auto()
    MF = auto()
    FW = auto()


class Attributes(BaseModel):
    def get_overall(self) -> int:
        attrs = self.dict()
        return int(sum(attrs.values()) / len(attrs))


class OffensiveAttributes(Attributes):
    shot_power: int
    shot_accuracy: int
    free_kick: int
    penalty: int
    positioning: int


class PhysicalAttributes(Attributes):
    strength: int
    aggression: int
    endurance: int


class DefensiveAttributes(Attributes):
    tackling: int
    interception: int
    positioning: int


class IntelligenceAttributes(Attributes):
    vision: int
    passing: int
    crossing: int
    ball_control: int
    dribbling: int
    skills: int
    team_work: int


class GkAttributes(Attributes):
    reflexes: int
    jumping: int
    positioning: int
    penalty: int

    def get_general_overall(self) -> int:
        return int((self.reflexes + self.jumping + self.positioning) / 3)


class PlayerAttributes(BaseModel):
    offensive: OffensiveAttributes
    physical: PhysicalAttributes
    defensive: DefensiveAttributes
    intelligence: IntelligenceAttributes
    gk: GkAttributes

    def get_overall(self, position: Positions) -> int:
        if position == Positions.GK:
            return self.get_gk_overall()
        elif position == Positions.DF:
            return self.get_df_overall()
        elif position == Positions.MF:
            return self.get_mf_overall()
        elif position == Positions.FW:
            return self.get_fw_overall()
        return 0

    def get_gk_overall(self) -> int:
        return int(
            (
                self.gk.get_overall() * 3
                + self.defensive.get_overall() * 2
                + self.physical.get_overall()
                + self.intelligence.get_overall()
            )
            / 7
        )

    def get_df_overall(self) -> int:
        return int(
            (
                self.defensive.get_overall() * 3
                + self.physical.get_overall() * 2
                + self.intelligence.get_overall()
                + self.offensive.get_overall()
            )
            / 7
        )

    def get_mf_overall(self) -> int:
        return int(
            (
                self.defensive.get_overall()
                + self.physical.get_overall() * 2
                + self.intelligence.get_overall() * 3
                + self.offensive.get_overall()
            )
            / 7
        )

    def get_fw_overall(self) -> int:
        return int(
            (
                self.defensive.get_overall()
                + self.physical.get_overall()
                + self.intelligence.get_overall() * 2
                + self.offensive.get_overall() * 3
            )
            / 7
        )
