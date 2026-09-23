import pytest
from pprint import pprint

from httpx import AsyncClient as httpxAsyncClient
from sqlalchemy import select
from starlette import status

from src.api.deps import SessionDep
from src.models import Team


@pytest.mark.anyio
async def test_retrieve_nfl_teams(aclient: httpxAsyncClient, session: SessionDep):
    r = await aclient.get(
        url="https://site.api.espn.com/apis/site/v2/sports/football/nfl/teams",
        params={"lang": "en", "region": "us"},
        headers={
            "Accept": "application/json",
            "Accept-Language": "en-US,en;q=0.8",
            "Referrer": "https://www.google.com",
            # "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        },
    )
    assert status.HTTP_200_OK == r.status_code
    json_r = r.json()
    teams = json_r["sports"][0]["leagues"][0]["teams"]

    data = []
    for _ in teams:
        if "Arizona Cardinals" == _['team']["displayName"]:
            data.append({
                "espn_id": _['team']['id'],
                "display_name": _['team']['displayName'],
                "abbreviation": _['team']['abbreviation'],
            })
    team = Team(
        espn_id=data[0]["espn_id"],
        display_name=data[0]["display_name"],
        abbreviation=data[0]["abbreviation"],
    )
    session.add(team)
    await session.commit()
    stmt = (select(Team).where(
        Team.espn_id == int(data[0]["espn_id"]),
        Team.abbreviation == data[0]["abbreviation"],
        Team.display_name == data[0]["display_name"],
    ))
    result = await session.execute(stmt)
    team_obj = result.scalars().one()
    pprint(team_obj)
    await session.rollback()


@pytest.mark.anyio
async def test_espn_client(aclient: httpxAsyncClient, session: SessionDep):
    r = await aclient.get(
        url="https://site.api.espn.com/apis/site/v2/sports/football/nfl/injuries",
        params={"lang": "en", "region": "us"},
        headers={
            "Accept": "application/json",
            "Accept-Language": "en-US,en;q=0.8",
            "Referrer": "https://www.google.com",
            # "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        },
    )
    assert status.HTTP_200_OK == r.status_code
    json_r = r.json()
    injury_data = json_r["injuries"]

    # data = {}
    # for teams in injury_data:
    #     for player in teams['injuries']:
    #         data.update({
    #             int(player['id']): f"{player['athlete']['firstName']} {player['athlete']['lastName']}"
    #         })

    team = injury_data[0]["displayName"]
    injuries_team = injury_data[0]["injuries"]



    # injuries = json_r["injuries"]
    # print(f"\n{len(injuries)=}")    # 32 teams
    # # for _ in injuries:
    # #     print(f"{_=}")
    #
    # # print(f"\n{injuries[0]['injuries']=}") # how many injuries for a particular team
    # print(f"\n{len(injuries[0]['injuries'])=}")
    # # print(f"\n{injuries[0]['injuries'][0]['athlete']=}")
    #
    #
    # for _ in injuries[0]['injuries']:
    #     print(
    #         f"{_['athlete']['displayName']} | "
    #         f"{_['athlete']['team']['name']} | "
    #         f"{_['athlete']['position']['name']} | "
    #         f"{_.get('details', 'N/A')}"
    #     )
    #     # breakpoint()
