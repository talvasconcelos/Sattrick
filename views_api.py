from http import HTTPStatus

from fastapi import Depends, Query
from fastapi.exceptions import HTTPException
from loguru import logger

from lnbits.core.crud import get_user
from lnbits.decorators import (
    WalletTypeInfo,
    require_admin_key,
    require_invoice_key,
)

from . import sattrick_ext
from .crud import (
    create_division,
    create_league,
    get_division,
    get_divisions,
    get_league,
    update_league,
    create_team,
    create_player,
)
from .models import CreateDivision, CreateLeague, Division, League
from .helpers import TeamGenerator
# @sattrick_ext.get("/api/v1/league")
# async def api_get_leagues(
#     wallet: WalletTypeInfo = Depends(require_invoice_key),
#     all_wallets: bool = Query(False),
# ):
#     wallet_ids = [wallet.wallet.id]

#     if all_wallets:
#         user = await get_user(wallet.wallet.user)
#         wallet_ids = user.wallet_ids if user else []

#     league = await get_leagues(wallet_ids)

#     return league.dict() if league else None

# LEAGUE

@sattrick_ext.post("/api/v1/league")
async def api_create_league(
    data: CreateLeague, wallet: WalletTypeInfo = Depends(require_admin_key)
):
    league = await create_league(data=data)
    return league.dict()

@sattrick_ext.patch("/api/v1/{league_id}")
async def api_update_league(
    data: CreateLeague, league_id: str, wallet: WalletTypeInfo = Depends(require_admin_key)
):
    league = await update_league(data=data, league_id=league_id)
    return league.dict()

# DIVISIONS

@sattrick_ext.get("/api/v1/divisions")
async def api_get_league_divisions(
    wallet: WalletTypeInfo = Depends(require_invoice_key)
):
    league = await get_league()
    if not league:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="League not found")

    if league.wallet != wallet.wallet.id:
        raise HTTPException(status_code=HTTPStatus.FORBIDDEN, detail="League not found")

    divisions = await get_divisions()
    return [division.dict() for division in divisions]

@sattrick_ext.post("/api/v1/{league_id}/division")
async def api_create_division(
    data: CreateDivision,
    league_id: str,
    wallet: WalletTypeInfo = Depends(require_admin_key),
):
    league = await get_league()
    assert league, "League not found"
    division = await create_division(data=data, league_id=league_id)
    if division:
        # create teams
        teams, players = TeamGenerator(league.country, division.id).generate()
        for team in teams:
            await create_team(team)
        for player in players:
            await create_player(player.player)
    return division.dict()
