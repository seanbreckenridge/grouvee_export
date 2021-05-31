import csv
import json
from time import strptime
from pathlib import Path
import dataclasses
from typing import Iterator, Optional, Tuple, List, NamedTuple, Any, Iterable, Dict
from datetime import datetime, date, timezone

Url = str
MetadataTuple = Tuple[str, Url]
Metadata = Dict[str, Url]


class ShelfAction(NamedTuple):
    name: str
    added: datetime
    url: str


@dataclasses.dataclass
class Game:
    grouvee_id: int
    name: str
    url: str
    giantbomb_id: Optional[int] = None
    release_date: Optional[date] = None
    rating: Optional[int] = None
    review: Optional[str] = None
    shelves: List[ShelfAction] = dataclasses.field(default_factory=list)
    genres: Metadata = dataclasses.field(default_factory=dict)
    franchises: Metadata = dataclasses.field(default_factory=dict)
    developers: Metadata = dataclasses.field(default_factory=dict)
    publishers: Metadata = dataclasses.field(default_factory=dict)

    @property
    def datetimes(self) -> Iterator[datetime]:
        for v in self.shelves:
            yield v.added

    @property
    def added(self) -> Optional[datetime]:
        """
        When this Game was first added to a Shelf
        """
        dts = sorted(self.datetimes)
        if len(dts) == 0:
            return None
        return dts[0]

    @property
    def modified(self) -> Optional[datetime]:
        """
        When this Game was last moved on a shelf - edited
        """
        dts = sorted(self.datetimes)
        if len(dts) == 0:
            return None
        return dts[-1]


def _parse_grouvee_datetime(ds: str) -> datetime:
    return datetime.astimezone(datetime.fromisoformat(ds.rstrip("Z")), tz=timezone.utc)


def _parse_metadata(sdata: str) -> Iterator[MetadataTuple]:
    if sdata.strip():
        data = json.loads(sdata)
        for name, data in data.items():
            yield (name, data["url"])


def parse_export(path: Path) -> Iterator[Game]:
    with path.open("r") as f:
        csv_reader = csv.reader(f)
        next(csv_reader)  # ignore headers
        for line in csv_reader:
            (
                grouvee_id,
                name,
                shelves,
                _platforms,
                rating,
                review,
                _dates,
                statuses,
                genres,
                franchises,
                developers,
                publishers,
                release_date,
                url,
                giantbomb_id,
            ) = line

            rel: Optional[date] = None
            if release_date:
                d = strptime(release_date, r"%Y-%m-%d")
                rel = date(year=d.tm_year, month=d.tm_mon, day=d.tm_mday)

            sh: List[ShelfAction] = []
            if shelves:
                for shelf_name, data in json.loads(shelves).items():
                    sh.append(
                        ShelfAction(
                            name=shelf_name,
                            added=_parse_grouvee_datetime(data["date_added"]),
                            url=data["url"],
                        )
                    )

            metadata: Dict[str, Metadata] = {}
            for key, sdata in {
                "genres": genres,
                "franchises": franchises,
                "developers": developers,
                "publishers": publishers,
            }.items():
                metadata[key] = {k: v for (k, v) in _parse_metadata(sdata)}

            yield Game(
                grouvee_id=int(grouvee_id),
                name=name,
                rating=int(rating) if rating.strip() else None,
                review=review if review.strip() else None,
                release_date=rel,
                url=url,
                giantbomb_id=int(giantbomb_id) if giantbomb_id.strip() else None,
                shelves=sh,
                **metadata,
            )


def _default(data: Any) -> Any:
    if isinstance(data, datetime) or isinstance(data, date):
        return str(data)
    elif hasattr(data, "_asdict") and callable(data._asdict):
        return data._asdict()
    elif dataclasses.is_dataclass(data):
        return dataclasses.asdict(data)
    raise TypeError(f"Could not serialize {data} {data.__class__.__name__}")


def serialize_export(data: Iterable[Game]) -> str:
    return json.dumps(list(data), default=_default)
