from typing import Literal, Optional
from pydantic import BaseModel, Field

Role = Literal["FILER", "SUPPLIER", "SUB_SUPPLIER", "DISTRIBUTOR", "CUSTOMER", "OTHER"]
Locus = Literal["TIER1_PROCESS", "SUBTIER_OR_MATERIAL", "DISTRIBUTOR_OR_SUBSTITUTE",
                "FILER_ASSEMBLY", "DESIGN_SPEC", "SOFTWARE", "UNDETERMINED"]
EventType = Literal["SUPPLIER_NOTICE", "FILER_AWARENESS", "INVESTIGATION_START",
                    "DECISION", "NHTSA_FILING", "OTHER"]
EvidenceStatus = Literal["SUPPORTED", "CONTRADICTED", "INSUFFICIENT", "NOT_REPORTED"]
Section = Literal["cause", "chronology", "components", "defect"]


class Evidence(BaseModel):
    section: Section
    quote: str = Field(max_length=300)


class Company(BaseModel):
    name: str
    role: Role
    status: EvidenceStatus
    evidence: Evidence


class Event(BaseModel):
    date_text: str
    type: EventType
    status: EvidenceStatus
    evidence: Evidence


class Extraction(BaseModel):
    companies: list[Company] = Field(max_length=8)
    supply_path: list[str] = Field(max_length=6)  # filer -> ... -> deepest named company
    locus: Locus
    locus_status: EvidenceStatus
    locus_evidence: Optional[Evidence] = None
    events: list[Event] = Field(max_length=12)
    cause_reported: bool  # False when the source says NR
    abstain_reason: Optional[Literal["NOT_REPORTED", "AMBIGUOUS"]] = None
