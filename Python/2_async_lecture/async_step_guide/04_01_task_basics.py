import asyncio

from utils import async_measure_time

async def tick():
    print("Tick")
    await asyncio.sleep(1)
    print("Tock")
    return 'Tick-Tock'

@async_measure_time
async def main():
    t1 = asyncio.create_task(tick(), name='tick1')
    t2 = asyncio.ensure_future(tick())
    # t1 = tick()
    # t2 = tick()

    # print("1")
    # await t1
    # print("2")
    # await t2
    # print("3")

    results = await asyncio.gather(t1, t2)
    print("4")
    
    print(f'{t1.get_name()}. Done = {t1.done()}')
    print(f'{t2.get_name()}. Done = {t2.done()}')

    for x in results:
        print(x)


if __name__ == '__main__':
    asyncio.run(main())
