import pytest
from pprint import pprint

from httpx import AsyncClient as httpxAsyncClient
from sqlalchemy import func, select
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

    team_objs = []
    for t in teams:
        team_objs.append(Team(
            espn_id=t["team"]["id"],
            display_name=t["team"]["displayName"],
            nickname=t["team"]["nickname"],
            short_name=t["team"]["shortDisplayName"],
            abbreviation=t["team"]["abbreviation"],
            location=t["team"]["location"],
        ))
    session.add_all(team_objs)
    await session.commit()
    assert 32 == len(team_objs) == await session.scalar(select(func.count(Team.id)))
    # pprint(team_objs)


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
