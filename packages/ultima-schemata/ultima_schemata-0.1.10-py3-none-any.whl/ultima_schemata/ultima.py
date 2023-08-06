import logging

# import httpx
from cvss import CVSS3
from datetime import datetime
from pydantic import UUID4, BaseModel, IPvAnyAddress, IPvAnyNetwork, validator, Field
from typing import Any, Optional
from enum import Enum
import os 
import json
from uuid import uuid4
# client = httpx.Client(
#     base_url=environ.get("CVE_SEARCH_API", "https://cve.circ.lu/api"),
#     timeout=float(environ.get("CVE_SEARCH_TIMEOUT", 10.0)),
#     transport=httpx.HTTPTransport(retries=environ.get("CVE_SEARCH_RETRIES", 3)),
#     headers={
#         "user-agent": environ.get("CVE_SEARCH_USER_AGENT", "ultima/0.1.0")
#     }
#     )

logger = logging.getLogger("schemas")


# def find(id: UUID4, col: Collection) -> Any:
#     return col.find_one({"_id": str(id)})


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
    hostname: str
    port: int = 0
    protocol: NetworkProtocol = NetworkProtocol.ICMP
    labels: list[str] = []
    notes: list[dict] = []

    @validator("port")
    def port_checks(cls, v):
        # assert v != 0, f"Invalid port number {v}"
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


class CWE(BaseModel):
    id: str
    summary: str = ""


class CVE(BaseModel):
    id: str
    year: int = 2000
    summary: str = ""
    score: Optional[float]
    cvss: str = ""
    

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.year = int(self.id.split("-")[1])

    @validator("id")
    def check_type(cls, v):
        assert v.upper().startswith("CVE-"), f"{v} does not start with CVE-"
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
    cwe: list[CWE] = []

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if self.score:
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
    


class KafkaHeader(BaseModel):
    module: str
    campaign: Optional[Campaign]
    services: Optional[list[Service]]
    assets: Optional[list[Asset]]

    def form(self) -> list[tuple[(str, bytes)]]:
        """Create headers suitable for Kafka messages"""
        items = json.loads(self.json()).items()
        headers = []
        for k, v in items:
            if isinstance(v, list):
                headers.append((k, json.dumps(v).encode('latin-1')))
            else:
                assert type(v) == str
                headers.append((k, v.encode('latin-1')))
        
        return headers
    
    def to_envars(self) -> list[tuple[(str, str)]]:
        return [
            {"name": "ULTIMA_CAMPAIGN", "value": json.dumps(self.campaign.show())},
            {"name": "ULTIMA_SERVICES", "value": json.dumps([service.show() for service in self.services])},
            {"name": "ULTIMA_ASSETS", "value": json.dumps([asset.show() for asset in self.assets])},
            {"name": "ULTIMA_MODULE", "value": self.module}
        ]


def envar_header(test: bool = False) -> KafkaHeader:
    if test: 
        os.environ.update(
            {
                "ULTIMA_MODULE": "test",
                "ULTIMA_CAMPAIGN": '{"created": "2022-10-27T20:30:09.710727", "updated": "2022-10-27T20:30:09.710727", "name": "test", "timeline": {"start": "2022-10-27T20:29:41.778647", "end": "2022-10-27T20:29:41.778657"}, "scope": {"ip_blocks": [], "names": []}, "_id": "cb493b40-e109-4b9f-8621-c88f232dcaf3"}',
                "ULTIMA_SERVICES": '[{"created": "2022-10-27T20:11:02.424313", "updated": "2022-10-27T20:11:02.424313", "campaign_id": "5c49d523-93e6-4a31-852a-8a569902e95c", "ip": null, "hostname": "example.com", "port": 0, "protocol": "ICMP", "labels": [], "notes": [], "_id": "1bdd83d8-a68f-4b88-9566-911a2b0d7e95"}]',
                "ULTIMA_ASSETS": '[{"created": "2022-10-27T20:28:05.444542", "updated": "2022-10-27T20:28:05.444542", "path": "/", "service_id": "eb4cc132-c625-44c2-9032-8fa12a1006db", "method": "GET", "url_parameters": [], "body_parameters": [], "labels": [], "notes": [], "_id": "de0815ed-3c11-4e24-aa05-27b1c0b0c117"}, {"created": "2022-10-27T20:28:13.685800", "updated": "2022-10-27T20:28:13.685800", "path": "/", "service_id": "80af7613-1a41-4d5d-bb09-5cddb8a7187d", "method": "GET", "url_parameters": [], "body_parameters": [], "labels": [], "notes": [], "_id": "96ddd1be-33d3-4302-8d0d-4b29b0c7518e"}]'
            }
        )
    module = os.environ["ULTIMA_MODULE"]
    
    try:
        campaign = Campaign(**json.loads(os.environ["ULTIMA_CAMPAIGN"]))
    except TypeError:
        campaign = None
    
    try:
        services = [Service(**service_dict) for service_dict in json.loads(os.environ["ULTIMA_SERVICES"])]
    except TypeError:
        services = None

    try:
        assets = [Asset(**asset_dict) for asset_dict in json.loads(os.environ["ULTIMA_ASSETS"])]
    except TypeError:
        assets = None    
        
    return KafkaHeader(
        module=module,
        campaign=campaign,
        services=services,
        assets=assets
    )
    
      