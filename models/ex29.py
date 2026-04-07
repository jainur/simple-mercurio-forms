"""
Domain model for EX-29.
Solicitud de prórroga de estancia de corta duración.
"""

from __future__ import annotations

from datetime import date
from enum import Enum
from typing import Optional

from pydantic import BaseModel, EmailStr
from models.common_sections import ApplicantLegalRepresentativeSectionBase, FilingRepresentativeDetailsBase, NotificationAddressBase, OfficeDetailsBase, SignatureFieldsBase


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


class ApplicantDetails(ApplicantLegalRepresentativeSectionBase[GenderEnum, MaritalStatusEnum]):
    pass


class FilingRepresentativeDetails(FilingRepresentativeDetailsBase):
    pass


class NotificationAddress(NotificationAddressBase):
    pass


class ExtensionRequestDetails(BaseModel):
    ordinary_stay_without_visa: bool = False
    short_stay_visa_holder: bool = False
    displaced_minor_medical_treatment: bool = False
    other: bool = False
    other_description: Optional[str] = None
    justification_and_extension_period: str


class SignatureDetails(SignatureFieldsBase):
    signer_name: Optional[str] = None

class OfficeDetails(OfficeDetailsBase):
    pass


class EX29FormSchema(BaseModel):
    applicant_details: ApplicantDetails
    filing_representative: Optional[FilingRepresentativeDetails] = None
    notification_address: NotificationAddress
    extension_request: ExtensionRequestDetails
    signature: SignatureDetails
    office: OfficeDetails
