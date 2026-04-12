"""
Domain model for EX-22
Solicitud de documento para personas trabajadoras transfronterizas.
"""

from __future__ import annotations

from datetime import date
from enum import Enum
from typing import Optional

from pydantic import BaseModel, EmailStr
from app.models.common_sections import ApplicantGuardianMaritalNoAddressSectionBase, FilingRepresentativeDetailsBase, NotificationAddressBase, OfficeDetailsBase, SignatureFieldsBase
from app.models.shared_enums import GenderEnum, MaritalStatusEnum


class WorkModeEnum(str, Enum):
    EMPLOYEE = "EMPLOYEE"
    SELF_EMPLOYED = "SELF_EMPLOYED"


class RequestCategoryEnum(str, Enum):
    INITIAL = "INITIAL"
    RENEWED = "RENEWED"
    MODIFICATION = "MODIFICATION"
    DEREGISTRATION = "DEREGISTRATION"


class ModificationGroundEnum(str, Enum):
    PERSONAL_DATA = "PERSONAL_DATA"
    LABOR_OR_PROFESSIONAL_DATA = "LABOR_OR_PROFESSIONAL_DATA"
    ADDRESS_CHANGE = "ADDRESS_CHANGE"
    IDENTITY_DOCUMENT_CHANGE = "IDENTITY_DOCUMENT_CHANGE"
    OTHER = "OTHER"


class ApplicantDetails(ApplicantGuardianMaritalNoAddressSectionBase[GenderEnum, MaritalStatusEnum]):
    pass


class EmployerDetails(BaseModel):
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


class FilingRepresentativeDetails(FilingRepresentativeDetailsBase):
    pass


class NotificationAddress(NotificationAddressBase):
    pass


class RequestDetails(BaseModel):
    category: RequestCategoryEnum
    work_mode: Optional[WorkModeEnum] = None
    modification_ground: Optional[ModificationGroundEnum] = None
    identity_document_change_text: Optional[str] = None
    cause_specification: Optional[str] = None
    truth_statement_accepted: bool = True


class SignatureDetails(SignatureFieldsBase):
    name: Optional[str] = None


class OfficeDetails(OfficeDetailsBase):
    pass


class EX22FormSchema(BaseModel):
    applicant_details: ApplicantDetails
    employer_details: EmployerDetails
    filing_representative: Optional[FilingRepresentativeDetails] = None
    notification_address: NotificationAddress
    request_details: RequestDetails
    signature: SignatureDetails
    office: OfficeDetails
