"""
Domain model for EX-09
Solicitud de autorización de residencia temporal con excepción de la autorización de trabajo.
"""

from __future__ import annotations

from datetime import date
from enum import Enum
from typing import Optional

from pydantic import BaseModel, EmailStr, Field
from models.common_sections import ApplicantGuardianMaritalWithChildrenSectionBase, FilingRepresentativeDetailsBase, NotificationAddressBase, OfficeDetailsBase, SignatureFieldsBase
from models.shared_enums import GenderEnum, MaritalStatusEnum


class ApplicationCategoryEnum(str, Enum):
    INITIAL_EXCEPTION = "INITIAL_EXCEPTION"
    EXTENSION = "EXTENSION"


class InitialExceptionSubtypeEnum(str, Enum):
    RELIGIOUS_MEMBER = "RELIGIOUS_MEMBER"
    OTHER = "OTHER"


class ForeignerDetails(ApplicantGuardianMaritalWithChildrenSectionBase[GenderEnum, MaritalStatusEnum]):
    pass


class ActivityEntityDetails(BaseModel):
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
    initial_subtype: Optional[InitialExceptionSubtypeEnum] = None
    other_initial_exception_details: Optional[str] = None


class SignatureDetails(SignatureFieldsBase):
    name: Optional[str] = None


class OfficeDetails(OfficeDetailsBase):
    pass


class EX09FormSchema(BaseModel):
    foreigner_details: ForeignerDetails
    activity_entity_details: ActivityEntityDetails
    filing_representative: Optional[FilingRepresentativeDetails] = None
    notification_address: NotificationAddress
    request_details: RequestDetails
    signature: SignatureDetails
    office: OfficeDetails
