import asyncio
import aiohttp

import time
from utils import async_measure_time

async def download_site(url, session):
    async with session.get(url) as response:
        # time.sleep(1)
        print(f"Read {response.content.total_bytes} from {url}")


@async_measure_time
async def download_all_sites(sites):
    async with aiohttp.ClientSession() as session:
        tasks = []
        for url in sites:
            task = asyncio.create_task(download_site(url, session))
            # await task
            tasks.append(task)

        try:
            print('before await')
            await asyncio.gather(*tasks, return_exceptions=True)
            # for task in tasks:
            #     await task
        except Exception as ex:
            print(repr(ex))


if __name__ == "__main__":
    sites = [
                "https://www.engineerspock.com",
                "https://enterprisecraftsmanship.com/",
            ] * 80
    loop = asyncio.get_event_loop()
    loop.run_until_complete(download_all_sites(sites))

