import csv
import json
from time import strptime
from pathlib import Path
from typing import Iterator, Optional, Tuple, List
from datetime import datetime, date
from dataclasses import dataclass, field

Url = str
Metadata = Tuple[str, Url]


@dataclass
class Game:
    grouvee_id: int
    name: str
    url: str
    giantbomb_id: Optional[int] = None
    release_date: Optional[date] = None
    added: Optional[datetime] = None
    modified: Optional[datetime] = None
    rating: Optional[int] = None
    review: Optional[str] = None
    genres: List[Metadata] = field(default_factory=list)
    franchises: List[Metadata] = field(default_factory=list)
    developers: List[Metadata] = field(default_factory=list)
    publishers: List[Metadata] = field(default_factory=list)


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

            yield Game(
                grouvee_id=int(grouvee_id),
                name=name,
                rating=int(rating) if rating.strip() else None,
                release_date=rel,
                url=url,
                giantbomb_id=int(giantbomb_id) if giantbomb_id.strip() else None,
            )
