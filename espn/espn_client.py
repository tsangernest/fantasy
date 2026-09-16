import asyncio
import httpx
from pprint import PrettyPrinter
from starlette.status import HTTP_200_OK, HTTP_404_NOT_FOUND

pp = PrettyPrinter(indent=2, width=1)


NFL = "https://sports.core.api.espn.com/v2/sports/football/leagues/nfl/athletes"


async def get_info():
    async with httpx.AsyncClient() as aclient:
        response = await aclient.get(
            url=f"{NFL}/3139477",
            params={"lang": "en", "region": "us"},
        )
        if HTTP_200_OK == response.status_code:
            pp.pprint(response.json())
            pp.pprint(response.json().keys())
        return HTTP_404_NOT_FOUND

asyncio.run(get_info())

