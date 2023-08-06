import logging

# import httpx
from cvss import CVSS3
from datetime import datetime
from pydantic import UUID4, BaseModel, IPvAnyAddress, IPvAnyNetwork, validator, Field
from typing import Any, Optional
from enum import Enum
from os import environ
import json
from uuid import uuid4

from pymongo.collection import Collection

# client = httpx.Client(
#     base_url=environ.get("CVE_SEARCH_API", "https://cve.circ.lu/api"),
#     timeout=float(environ.get("CVE_SEARCH_TIMEOUT", 10.0)),
#     transport=httpx.HTTPTransport(retries=environ.get("CVE_SEARCH_RETRIES", 3)),
#     headers={
#         "user-agent": environ.get("CVE_SEARCH_USER_AGENT", "ultima/0.1.0")
#     }
#     )

logger = logging.getLogger("schemas")


def find(id: UUID4, col: Collection) -> Any:
    return col.find_one({"_id": str(id)})


class BaseSchema(BaseModel):
    def show(self):
        j = json.loads(self.json())

        try:
            j["_id"] = j.pop("id")
        except KeyError:
            pass

        return j


class ID(BaseSchema):
    id: UUID4 = Field(uuid4(), alias="_id")
    created: datetime = datetime.now()
    updated: datetime = datetime.now()
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.id = uuid4()
        self.created = datetime.now()
        self.updated = self.created
        


class Scope(BaseSchema):
    ip_blocks: list[IPvAnyNetwork] = []
    names: list[str] = []


class Timeline(BaseSchema):
    start: datetime
    end: datetime


class BaseCampaign(BaseSchema):
    name: str
    timeline: Timeline
    scope: Scope


class Campaign(BaseCampaign, ID):
    pass


class CampaignModify(BaseSchema):
    name: Optional[str]
    timeline: Optional[Timeline]
    scope: Optional[Scope]


class NetworkProtocol(str, Enum):
    TCP = "TCP"
    UDP = "UDP"
    ICMP = "ICMP"
    SCTP = "SCTP"


class HttpMethod(str, Enum):
    GET = "GET"
    POST = "POST"
    CONNECT = "CONNECT"
    PUT = "PUT"
    DELETE = "DELETE"
    PATCH = "PATCH"
    HEAD = "HEAD"
    OPTIONS = "OPTIONS"
    TRACE = "TRACE"
    LOCK = "LOCK"
    MKCOL = "MKCOL"
    MOVE = "MOVE"
    PROPFIND = "PROPFIND"
    PROPPATCH = "PROPPATCH"
    UNLOCK = "UNLOCK"
    NONE = "NONE"


class Author(BaseSchema):
    name: str


class BaseAsset(BaseSchema):
    path: str
    service_id: UUID4
    method: HttpMethod = HttpMethod.GET
    url_parameters: list[dict] = []
    body_parameters: list[dict] = []
    labels: list[str] = []
    notes: list[dict] = []
    
class Asset(BaseAsset, ID):
    pass


class BaseService(BaseSchema):
    campaign_id: UUID4
    ip: Optional[IPvAnyAddress]
    hostname: str = ""
    port: int = 0
    protocol: NetworkProtocol = NetworkProtocol.ICMP
    labels: list[str] = []
    notes: list[dict] = []

    @validator("port")
    def port_checks(cls, v):
        assert v != 0, f"Invalid port number {v}"
        return v % 65536


class Service(BaseService, ID):
    pass


class User(ID):
    username: str
    campaign: UUID4
    name: Optional[str]
    email: Optional[str]
    password: Optional[str]


class Severity(str, Enum):
    CRITICAL = "CRITICAL"
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"
    INFO = "INFO"


class CWE(ID):
    pass


class CVE(ID):
    identifier: str
    year: int = 2000
    summary: str = ""
    # cvss: CVSS3 = None
    cwe: CWE = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.year = int(self.identifier.split("-")[1])

    @validator("identifier")
    def check_type(cls, v):
        assert v.startswith("CVE-"), f"{v} does not start with CVE-"
        assert v.count("-") == 2
        assert datetime.now().year >= int(v.split("-")[1]) > 1970, f"Invalid year"
        return v

class BaseFinding(BaseSchema):
    service_id: UUID4    
    title: str 
    severity: Severity = Severity.INFO    
    cvss: str = None
    score: Optional[float]
    description: str = ""
    cve: list[CVE] = []

    # class Config:
    #     arbitrary_types_allowed = True

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if not self.score == None:
            if self.score == 0.0:
                self.severity = Severity.INFO
            elif self.score < 4.0:
                self.severity = Severity.LOW
            elif self.score < 7.0:
                self.severity = Severity.MEDIUM
            elif self.score < 9.0:
                self.severity = Severity.HIGH
            else:
                self.severity = Severity.CRITICAL

    @validator("score")
    def check_range(cls, v):
        assert 0.0 <= v <= 10.0, f"Value not between 0 and 10"
        return v
    

class Finding(BaseFinding, ID):
    pass
    # class Config:
    #     arbitrary_types_allowed = True
    

class RawResultHeader(BaseSchema):
    service_id: Optional[UUID4]
    campaign_id: Optional[UUID4]
    asset_id: Optional[UUID4]
    module: str


class ContainerUsage(BaseSchema):
    cpu: str 
    mem: str

class ModuleSpec(BaseSchema):
    name: str 
    container: str 
    limits: ContainerUsage
    resources: ContainerUsage
    labels: dict
    env: list[dict[str, str]]
    

class CampaignModule(BaseSchema):
    """A user-specified module scoped to a single campaign"""
    name: str 
    campaign_id: UUID4
