from fastapi import Depends, Request
from fastapi.templating import Jinja2Templates
from starlette.responses import HTMLResponse

from lnbits.core.models import User
from lnbits.decorators import check_user_exists

from . import sattrick_ext, sattrick_renderer

from .resources.names import NAMES
from .crud import get_league

# from .helpers import TeamGenerator

templates = Jinja2Templates(directory="templates")


@sattrick_ext.get("/", response_class=HTMLResponse)
async def index(
    request: Request,
    user: User = Depends(check_user_exists),
):
    countries = [country["region"] for country in NAMES]
    league = await get_league()
    # create 10 teams with 10 players each

    # teams = TeamGenerator("PRT", num_teams=2).generate()

    # for team in teams:
    #     # print(team)
    #     for player in team.squad:
    #         print(player)

    return sattrick_renderer().TemplateResponse(
        "sattrick/index.html",
        {
            "request": request,
            "user": user.dict(),
            "countries": countries,
            "league": league.dict(),
        },
    )
