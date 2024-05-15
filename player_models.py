from pydantic import BaseModel
from .player_attributes import PlayerAttributes, Positions, PreferredFoot
from typing import Optional


class Player(BaseModel):
    """
    Parameters
    ----------
    player_id: UUID
        Player's unique ID in the database.
    nationality: str
        Player's nationality.
    first_name: str
    last_name: str
    short_name: str
        How the player is called commonly. Some players have nicknames that have nothing to do with their real names,
        such as Pelé, Kaká, Ronaldinho, Pepe, etc.
    positions: list[Positions]
        The positions that the player can play. Currently, we are only implementing the FW, MF, DF and GK. Players can
        only play as such.
    fitness: float
        Indicates how much the player is ready for a game. This also relates to how likely the player can get injured,
        and how fast his stamina drops. Values go from 0.0 to 100.0, with higher values meaning that the player
        is less likely to get injured, has less stamina issues and can recover quickly between games. This value can be
        improved with training.
    stamina: float
        Indicates the current stamina of the player in the game session. Values go from 0.0 to 100.0, with higher
        values meaning that the player can still perform well in a game. The longer the player stays in a game,
        the more the stamina drops. Lower stamina values in a game can lead to injuries and can lower player's fitness,
        and the player takes longer to recover after a game.
    form: float
        Indicates how confident the player is for a game. Values range from 0.0 to 1.0. Higher values indicate that
        the player is more confident, and can perform better in a game. It can be improved after winning important
        games, scoring streaks, getting a good performance/rating in a game or winning a title.
    attributes: PlayerAttributes
        Set of skills that a player possesses, such as attacking, defending, midfield and goalkeeper skills. The higher
        the values, the better the player performs in such areas. Skill values range from 0 to 99.
    potential_skill: int
        Indicates potential overall that a player can reach. These are only metrics that are used
        to calculate player's prospects. The values have the same range as the skill values.
    preferred_foot: PreferredFoot
        The player's preferred foot for shooting. Can have an impact in goal scoring.
    value: float
        How much the player is currently valued on the market. Takes into account the player's age, performance,
        form, skill, potential skill and international reputation.
    """

    player_id: str
    nationality: str
    dob: str
    first_name: str
    last_name: str
    short_name: str
    positions: list[Positions]
    fitness: float
    stamina: float
    form: float
    attributes: PlayerAttributes
    potential_skill: int
    preferred_foot: PreferredFoot
    value: float


class PlayerTeam(BaseModel):
    player: Player
    team: str
    number: int
