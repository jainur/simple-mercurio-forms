"""
Domain model for EX-23
Solicitud de documento de residencia para nacionales del Reino Unido y sus familiares en distintos supuestos de residencia.
"""

from __future__ import annotations

from datetime import date
from enum import Enum
from typing import Optional

from pydantic import BaseModel, EmailStr
from models.common_sections import ApplicantGuardianMaritalSectionBase, FilingRepresentativeDetailsBase, NotificationAddressBase, OfficeDetailsBase, SignatureFieldsBase


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


class ResidenceStatusEnum(str, Enum):
    INITIAL_WITHOUT_PREVIOUS_REGISTRATION = "INITIAL_WITHOUT_PREVIOUS_REGISTRATION"
    WITH_EU_REGISTRATION_CERTIFICATE = "WITH_EU_REGISTRATION_CERTIFICATE"
    TEMPORARY_WITH_UK_FAMILY_CARD = "TEMPORARY_WITH_UK_FAMILY_CARD"
    PERMANENT_WITH_UK_FAMILY_CARD = "PERMANENT_WITH_UK_FAMILY_CARD"
    OTHER = "OTHER"


class AdditionalEuRegistrationOptionEnum(str, Enum):
    OPTION_15 = "OPTION_15"
    OPTION_16 = "OPTION_16"
    OPTION_17 = "OPTION_17"


class ApplicantDetails(ApplicantGuardianMaritalSectionBase[GenderEnum, MaritalStatusEnum]):
    pass


class FilingRepresentativeDetails(FilingRepresentativeDetailsBase):
    pass


class NotificationAddress(NotificationAddressBase):
    pass


class RequestDetails(BaseModel):
    residence_status: ResidenceStatusEnum
    other_status_text: Optional[str] = None
    additional_eu_registration_option: Optional[AdditionalEuRegistrationOptionEnum] = None


class SignatureDetails(SignatureFieldsBase):
    name: Optional[str] = None


class OfficeDetails(OfficeDetailsBase):
    pass


class EX23FormSchema(BaseModel):
    applicant_details: ApplicantDetails
    filing_representative: Optional[FilingRepresentativeDetails] = None
    notification_address: NotificationAddress
    request_details: RequestDetails
    signature: SignatureDetails
    office: OfficeDetails
