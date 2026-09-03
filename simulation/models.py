from dataclasses import dataclass
from enum import Enum


class AmbulanceStatus(str, Enum):
    AVAILABLE = "AVAILABLE"
    EN_ROUTE = "EN_ROUTE"
    AT_SCENE = "AT_SCENE"
    TRANSPORTING = "TRANSPORTING"
    OFFLINE = "OFFLINE"


class EmergencySeverity(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


@dataclass
class Ambulance:
    id: str
    latitude: float
    longitude: float
    status: AmbulanceStatus = AmbulanceStatus.AVAILABLE


@dataclass
class Hospital:
    id: str
    name: str
    latitude: float
    longitude: float
    total_beds: int
    available_beds: int
    icu_total: int
    icu_available: int


@dataclass
class Emergency:
    id: str
    latitude: float
    longitude: float
    severity: EmergencySeverity