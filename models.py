from typing import List, Optional

from pydantic import BaseModel, Field

# from .player_models import PlayerTeam


class Manager(BaseModel):
    id: str
    name: str
    team: str
    wallet: str
    

class Team(BaseModel):
    id: str
    name: str
    default_formation: str
    division: str


class CreateLeague(BaseModel):
    name: str = Field(...)
    description: str = Field(None, max_length=255)
    country: str = Field(...)
    wallet: str = Field(...)


class League(CreateLeague):
    id: str


class CreateDivision(BaseModel):
    name: str = Field(...)
    description: str = Field(None, max_length=255)
    rank: int = Field(..., ge=1)  # index of the division in the league


class Division(CreateDivision):
    id: str
    league: str
