from typing import Optional, Any
from datetime import datetime
from dataclasses import dataclass

from .util import query_api
from .constants import API_SEARCH_LIMIT, API_LIST_LIMIT


@dataclass
class Episode:
    title: str
    description: str
    number: int
    publish_date: datetime

    image_url: str
    presentation_url: str

    slug: str
    urn: str

    @property
    def metadata(self):
        return {"title" : self.title,
                "description" : self.description,
                "episode-number" : self.number,
                "publish-date" : self.publish_date,
                "drdk-urn" : self.urn,
                }

    @classmethod
    def from_api_json(cls, data: dict[str, Any], number: int):
        return cls(
            data["Title"],
            data["Description"],
            data["EpisodeNumber"] if "EpisodeNumber" in data else number,
            datetime.strptime(data["SortDateTime"], "%Y-%m-%dT%H:%M:%SZ"),
            data["PrimaryImageUri"],
            data["PresentationUri"],
            data["Slug"],
            data["Urn"],
        )


@dataclass
class Season:
    title: str
    number: int

    slug: str
    urn: str

    episodes: Optional[list[Episode]] = None

    def get_episodes(self) -> None:
        episode_data: dict[str, Any] = query_api(
            "/list/view/season",
            {"id": self.urn, "limit": API_LIST_LIMIT},
        )

        self.episodes: list[Episode] = [
            Episode.from_api_json(episode, i) for i, episode in enumerate(episode_data)
        ]

    @classmethod
    def from_api_json(cls, data: dict[str, Any]):
        data: dict[str, Any] = data["Episodes"]["Items"][0]
        return cls(
            data["SeasonTitle"],
            data["SeasonNumber"],
            data["SeasonSlug"],
            data["SeasonUrn"],
        )


@dataclass
class Series:
    title: str
    slug: str
    urn: str

    seasons: Optional[list[Season]] = None

    def get_seasons(self) -> None:
        season_data: dict[str, Any] = query_api(
            "/list/view/seasons",
            {"id": self.urn, "onlyIncludeFirstEpisode": True, "limit": API_LIST_LIMIT},
        )
        self.seasons = [Season.from_api_json(season) for season in season_data]

    def get_content(self) -> None:
        self.get_seasons()

        for season in self.seasons:
            season.get_episodes()

    @classmethod
    def from_urn(cls, urn: str):
        series_data: dict[str, Any] = query_api(
            f"/list/{urn}", {"limit": 1}, paging=False
        )[0]

        return cls(
            series_data["SeriesTitle"],
            series_data["SeriesSlug"],
            series_data["SeriesUrn"],
        )

    @classmethod
    def from_json(cls, data: list[dict[str, str]]):
        return [cls(series["title"], series["slug"], series["urn"]) for series in data]

    @classmethod
    def search_series(
        cls, search_query: str
    ):  # Make return type the Self type once python 3.11 is released
        series_data: dict[str, Any] = query_api(
            f"/search/tv/programcards-latest-episode-with-broadcast/series-title/{search_query}",
            {"limit": API_SEARCH_LIMIT},
        )

        return [
            cls(series["SeriesTitle"], series["SeriesSlug"], series["SeriesUrn"])
            for series in series_data
        ]
