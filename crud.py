from typing import List, Optional, Union

from httpx import get
from lnbits.helpers import urlsafe_short_hash

from . import db
from .models import CreateLeague, League, CreateDivision, Division, Team
from .player_models import Player, PlayerTeam
import json
from loguru import logger


async def get_league() -> Optional[League]:
    row = await db.fetchone("SELECT * FROM sattrick.league")
    return League(**row) if row else None


async def create_league(data: CreateLeague) -> League:
    league_id = urlsafe_short_hash()
    await db.execute(
        """
        INSERT INTO sattrick.league (id, name, description, country, wallet)
        VALUES (?, ?, ?, ?, ?)
        """,
        (league_id, data.name, data.description, data.country, data.wallet),
    )
    league = await get_league()
    assert league, "Newly created league couldn't be retrieved"
    return league

async def update_league(data: CreateLeague, league_id: str) -> League:
    await db.execute(
        """
        UPDATE sattrick.league SET name = ?, description = ?, wallet = ?
        WHERE id = ?
        """,
        (data.name, data.description, data.wallet, league_id),
    )
    league = await get_league()
    assert league, "Updated league couldn't be retrieved"
    return league

# async def get_leagues(wallet_ids: Union[str, List[str]]) -> League:
#     if isinstance(wallet_ids, str):
#         wallet_ids = [wallet_ids]

#     q = ",".join(["?"] * len(wallet_ids))
#     rows = await db.fetchall(
#         f"SELECT * FROM sattrick.league WHERE wallet IN ({q})", (wallet_ids,)
#     )

#     return League(**rows[0]) if rows else None


async def get_division(division_id: str) -> Optional[Division]:
    row = await db.fetchone(
        "SELECT * FROM sattrick.division WHERE id = ?", (division_id,)
    )
    return Division(**row) if row else None


async def get_divisions() -> List[Division]:
    rows = await db.fetchall("SELECT * FROM sattrick.division")
    return [Division(**row) for row in rows]


async def create_division(data: CreateDivision, league_id: str) -> Division:
    division_id = urlsafe_short_hash()
    await db.execute(
        """
        INSERT INTO sattrick.division (id, league, name, description, rank)
        VALUES (?, ?, ?, ?, ?)
        """,
        (division_id, league_id, data.name, data.description, data.rank),
    )
    division = await get_division(division_id)
    assert division, "Newly created division couldn't be retrieved"
    return division

async def get_team(team_id: str) -> Optional[Team]:
    row = await db.fetchone(
        "SELECT * FROM sattrick.team WHERE id = ?", (team_id,)
    )
    return Team(**row) if row else None

async def create_team(data: Team) -> Team:
    await db.execute(
        """
        INSERT INTO sattrick.team (id, name, default_formation, division)
        VALUES (?, ?, ?, ?)
        """,
        (data.id, data.name, data.default_formation, data.division),
    )
    team = await get_team(data.id)
    assert team, "Newly created team couldn't be retrieved"
    return team

async def get_player(player_id: str) -> Optional[Player]:
    row = await db.fetchone(
        "SELECT * FROM sattrick.player WHERE player_id = ?", (player_id,)
    )
    if row is None:
        return None
    
    player_data = dict(row)
    player_data['positions'] = json.loads(player_data['positions'])
    player_data['attributes'] = json.loads(player_data['attributes'])
    return Player(**player_data) if row else None

async def create_player(data: Player):
    positions = json.dumps([position.value for position in data.positions])
    attributes = json.dumps(data.attributes.dict())
    preferred_foot = data.preferred_foot.value
    
    await db.execute(
        """
        INSERT INTO sattrick.player (player_id, nationality, dob, first_name, last_name, short_name, positions, fitness, stamina, form, attributes, potential_skill, preferred_foot, value)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (data.player_id, data.nationality, data.dob, data.first_name, data.last_name, data.short_name, positions, data.fitness, data.stamina, data.form, attributes, data.potential_skill, preferred_foot, data.value),
    )
    player = await get_player(data.player_id)
    assert player, "Newly created player couldn't be retrieved"
    return player
