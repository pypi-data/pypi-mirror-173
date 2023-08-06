"""
Program Init.

Romeo Program.
"""
from typing import List
from resources.program import ProgramConfig
from navigator.conf import asyncpg_url
from aiohttp.web_urldispatcher import SystemRoute
from aiohttp.web import middleware
from aiohttp import web, hdrs


@middleware
async def app_session(request, handler):
    user_id = None
    if isinstance(request.match_info.route, SystemRoute):  # eg. 404
        return await handler(request)
    # avoid authorization backend on excluded methods:
    if request.method == hdrs.METH_OPTIONS:
        return await handler(request)
    return await handler(request)


class romeo(ProgramConfig):
    __version__ = '0.0.1'
    app_description = """
    API for ROMEO
    """
    _middleware: List = [app_session]
