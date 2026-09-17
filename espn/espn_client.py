import asyncio
import httpx
from pprint import PrettyPrinter
from starlette.status import HTTP_200_OK, HTTP_404_NOT_FOUND

pp = PrettyPrinter(indent=2)


# NFL = "https://sports.core.api.espn.com/v2/sports/football/leagues/nfl/athletes"
NFL_INJURIES = "https://site.api.espn.com/apis/site/v2/sports/football/nfl"
PARAMS = {"lang": "en", "region": "us"}


async def get_info():
    async with httpx.AsyncClient(params=PARAMS) as aclient:
        response = await aclient.get(
            url=f"{NFL_INJURIES}/injuries",
            headers={"Accept": "application/json"},
        )
        if HTTP_200_OK == response.status_code:
            pp.pprint(response.json().keys())
            breakpoint()
        return HTTP_404_NOT_FOUND

asyncio.run(get_info())

