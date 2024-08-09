import aiohttp
import asyncio

url = "http://127.0.0.1:8001/sync"

async def make_request(session):
    try:
        async with session.get(url) as response:
            return await response.json()
    except aiohttp.ClientError as e:
        return {"error": str(e)}

async def make_601_requests():
    num_requests = 601
    results = []

    async with aiohttp.ClientSession() as session:
        tasks = [make_request(session) for _ in range(num_requests)]
        results = await asyncio.gather(*tasks)
    return results

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    results = loop.run_until_complete(make_601_requests())
    for result in results:
        print(result)
