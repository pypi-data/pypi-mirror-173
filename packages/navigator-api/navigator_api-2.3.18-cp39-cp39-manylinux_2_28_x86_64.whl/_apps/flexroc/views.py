import time
from aiohttp import web

async def handler(request):
    session = await get_session(request)
    print('Handler Session: ', session)
    session['last_visit'] = time.time()
    return web.Response(text='OK')

async def other(request):
    session = await get_session(request)
    print('Other Session', session)
    print(session['last_visit'])
    return web.Response(text='Other')
