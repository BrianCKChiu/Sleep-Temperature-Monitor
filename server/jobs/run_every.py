import asyncio


async def run_every(__seconds: int, func, *args, **kwargs):
    while True:
        func(*args, **kwargs)
        await asyncio.sleep(300)
