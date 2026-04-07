"""
Domain model for EX-04
Solicitud de autorización de residencia para prácticas.
"""

from __future__ import annotations

from datetime import date
from enum import Enum
from typing import Optional

from pydantic import BaseModel, EmailStr, Field
from models.common_sections import FilingRepresentativeDetailsBase, ForeignerIdentitySectionBase, NotificationAddressBase, OfficeDetailsBase, SignatureFieldsBase


class GenderEnum(str, Enum):
    OTHER = "X"
    MALE = "H"
    FEMALE = "M"


class MaritalStatusEnum(str, Enum):
    SINGLE = "S"
    MARRIED = "C"
    WIDOWED = "V"
    DIVORCED = "D"
    SEPARATED = "Sp"


class ApplicationCategoryEnum(str, Enum):
    INITIAL = "INITIAL"
    RENEWAL = "RENEWAL"
    FAMILY = "FAMILY"


class InitialLocationEnum(str, Enum):
    OUTSIDE_SPAIN = "OUTSIDE_SPAIN"
    IN_SPAIN = "IN_SPAIN"


class PracticeBasisEnum(str, Enum):
    AGREEMENT = "AGREEMENT"
    EMPLOYMENT_CONTRACT = "EMPLOYMENT_CONTRACT"


class FamilyAuthorizationPhaseEnum(str, Enum):
    INITIAL = "INITIAL"
    RENEWED = "RENEWED"


class ForeignerDetails(ForeignerIdentitySectionBase[GenderEnum, MaritalStatusEnum]):
    pass


class HostEntityDetails(BaseModel):
    name_or_company: str
    id_number: str
    activity: str
    occupation: str
    address: str
    address_number: Optional[str] = None
    floor_door: Optional[str] = None
    city: str
    postal_code: str
    province: str
    mobile_phone: Optional[str] = None
    email: Optional[EmailStr] = None
    legal_rep_name: Optional[str] = None
    legal_rep_id: Optional[str] = None
    legal_rep_title: Optional[str] = None


class FilingRepresentativeDetails(FilingRepresentativeDetailsBase):
    pass


class NotificationAddress(NotificationAddressBase):
    pass


class RequestDetails(BaseModel):
    category: ApplicationCategoryEnum

    initial_location: Optional[InitialLocationEnum] = None
    initial_basis: Optional[PracticeBasisEnum] = None

    renewal_basis: Optional[PracticeBasisEnum] = None

    family_phase: Optional[FamilyAuthorizationPhaseEnum] = None

    is_host_entity_legal_representative_signing: bool = False


class SignatureDetails(SignatureFieldsBase):
    name: Optional[str] = None


class OfficeDetails(OfficeDetailsBase):
    pass


class EX04FormSchema(BaseModel):
    foreigner_details: ForeignerDetails
    host_entity_details: HostEntityDetails
    filing_representative: Optional[FilingRepresentativeDetails] = None
    notification_address: NotificationAddress
    request_details: RequestDetails
    signature: SignatureDetails
    office: OfficeDetails
