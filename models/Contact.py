from dataclasses import dataclass
from typing import List, Optional


@dataclass
class Name:
    first: str
    last: str
    full: str


@dataclass
class JobTitle:
    title: str
    seniority: str
    departments: Optional[List[str]]


@dataclass
class Email:
    address: str
    label: str


@dataclass
class Phone:
    country_code: int
    number: Optional[str]


@dataclass
class Location:
    continent: str
    country: str
    country_iso2: str


@dataclass
class Contact:
    id: str
    contactId: str
    name: Name
    job_title: JobTitle
    social_link: str
    emails: List[Email]
    phones: List[Phone]
    location: Location

    def is_not_shown(self):
        return any(['...' in email.address for email in self.emails]) or\
               any(['...' in phone.number for phone in self.phones])
