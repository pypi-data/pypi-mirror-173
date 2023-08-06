from dataclasses import dataclass
from typing import List
from enum import Enum


class Region(Enum):
    Europe = 1
    America = 2
    Switzerland = 3
    Singapore = 4
    Custom = 5


@dataclass(init=True)
class RegionUri:
    region: Region
    ha_uri: str
    urls: List[str]


def region_resolve(region: Region, uris: List[RegionUri]) -> RegionUri:
    if region == Region.Europe:
        return uris[0]
    elif region == Region.America:
        return uris[1]
    elif region == Region.Switzerland:
        return uris[2]
    elif region == Region.Singapore:
        return uris[3]
    return None
