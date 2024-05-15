import asyncio

from fastapi import APIRouter

from lnbits.db import Database
from lnbits.helpers import template_renderer
from lnbits.tasks import create_permanent_unique_task

db = Database("ext_sattrick")


sattrick_ext: APIRouter = APIRouter(
    prefix="/sattrick", tags=["sattrick"]
)

sattrick_static_files = [
    {
        "path": "/sattrick/static",
        "name": "sattrick_static",
    }
]


def sattrick_renderer():
    return template_renderer(["sattrick/templates"])


from .tasks import wait_for_paid_invoices
from .views import *  # noqa
from .views_api import *  # noqa


scheduled_tasks: list[asyncio.Task] = []


def sattrick_stop():
    for task in scheduled_tasks:
        try:
            task.cancel()
        except Exception as ex:
            logger.warning(ex)


def sattrick_start():
    task = create_permanent_unique_task("ext_sattrick", wait_for_paid_invoices)
    scheduled_tasks.append(task)
