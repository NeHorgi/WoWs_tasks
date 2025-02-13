from dataclasses import dataclass


@dataclass
class CompanyInfo:
    name: str
    popularity: int
    front: str
    back: str
    database: str
    notes: str = None
