"""
Domain model for EX-18
Solicitud de inscripción en el Registro Central de Extranjeros / residencia de ciudadano UE-EEE-Suiza.
"""

from __future__ import annotations

from datetime import date
from enum import Enum
from typing import Optional

from pydantic import BaseModel, EmailStr
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


class MainRequestCategoryEnum(str, Enum):
    TEMPORARY_RESIDENCE = "TEMPORARY_RESIDENCE"
    PERMANENT_RESIDENCE = "PERMANENT_RESIDENCE"
    MODIFICATION = "MODIFICATION"
    DEREGISTRATION = "DEREGISTRATION"


class TemporaryResidenceGroundEnum(str, Enum):
    EMPLOYEE = "EMPLOYEE"
    SELF_EMPLOYED = "SELF_EMPLOYED"
    INACTIVE_WITH_RESOURCES_AND_INSURANCE = "INACTIVE_WITH_RESOURCES_AND_INSURANCE"
    STUDENT_WITH_RESOURCES_AND_INSURANCE = "STUDENT_WITH_RESOURCES_AND_INSURANCE"
    EU_FAMILY_MEMBER = "EU_FAMILY_MEMBER"


class PermanentResidenceGroundEnum(str, Enum):
    CONTINUOUS_5_YEARS = "CONTINUOUS_5_YEARS"
    RETIREMENT_WITH_12_MONTHS_AND_3_YEARS = "RETIREMENT_WITH_12_MONTHS_AND_3_YEARS"
    RETIREMENT_WITH_SPANISH_SPOUSE = "RETIREMENT_WITH_SPANISH_SPOUSE"
    RETIREMENT_WITH_SPOUSE_LOST_SPANISH_NATIONALITY = "RETIREMENT_WITH_SPOUSE_LOST_SPANISH_NATIONALITY"
    EARLY_RETIREMENT_WITH_12_MONTHS_AND_3_YEARS = "EARLY_RETIREMENT_WITH_12_MONTHS_AND_3_YEARS"
    EARLY_RETIREMENT_WITH_SPANISH_SPOUSE = "EARLY_RETIREMENT_WITH_SPANISH_SPOUSE"
    EARLY_RETIREMENT_WITH_SPOUSE_LOST_SPANISH_NATIONALITY = "EARLY_RETIREMENT_WITH_SPOUSE_LOST_SPANISH_NATIONALITY"
    PERMANENT_DISABILITY_AFTER_2_YEARS = "PERMANENT_DISABILITY_AFTER_2_YEARS"
    PERMANENT_DISABILITY_WORK_ACCIDENT = "PERMANENT_DISABILITY_WORK_ACCIDENT"
    PERMANENT_DISABILITY_WITH_SPANISH_SPOUSE = "PERMANENT_DISABILITY_WITH_SPANISH_SPOUSE"
    PERMANENT_DISABILITY_WITH_SPOUSE_LOST_SPANISH_NATIONALITY = "PERMANENT_DISABILITY_WITH_SPOUSE_LOST_SPANISH_NATIONALITY"
    WORK_IN_OTHER_MEMBER_STATE_KEEPING_RESIDENCE = "WORK_IN_OTHER_MEMBER_STATE_KEEPING_RESIDENCE"
    OTHER = "OTHER"


class ModificationGroundEnum(str, Enum):
    PERSONAL_DATA = "PERSONAL_DATA"
    ADDRESS_CHANGE = "ADDRESS_CHANGE"
    IDENTITY_DOCUMENT_CHANGE = "IDENTITY_DOCUMENT_CHANGE"
    OTHER = "OTHER"


class ForeignerDetails(ForeignerIdentitySectionBase[GenderEnum, MaritalStatusEnum]):
    pass


class FilingRepresentativeDetails(FilingRepresentativeDetailsBase):
    pass


class NotificationAddress(NotificationAddressBase):
    pass


class RequestDetails(BaseModel):
    expected_residence_period: str
    residence_start_day: str
    residence_start_month: str
    residence_start_year: str
    residence_start_location: str
    eu_citizen_document_id: Optional[str] = None
    relationship_with_eu_citizen: Optional[str] = None
    incapacity_with_spanish_spouse_text: Optional[str] = None
    identity_document_change_text: Optional[str] = None
    cause_specification: Optional[str] = None

    category: MainRequestCategoryEnum
    temporary_ground: Optional[TemporaryResidenceGroundEnum] = None
    permanent_ground: Optional[PermanentResidenceGroundEnum] = None
    permanent_other_text: Optional[str] = None
    modification_ground: Optional[ModificationGroundEnum] = None
    modification_other_text: Optional[str] = None
    deregistration_cause: Optional[str] = None
    truth_statement_accepted: bool = True


class SignatureDetails(SignatureFieldsBase):
    eu_citizen_signature_name: Optional[str] = None
    applicant_signature_name: Optional[str] = None


class OfficeDetails(OfficeDetailsBase):
    pass


class EX18FormSchema(BaseModel):
    foreigner_details: ForeignerDetails
    filing_representative: Optional[FilingRepresentativeDetails] = None
    notification_address: NotificationAddress
    request_details: RequestDetails
    signature: SignatureDetails
    office: OfficeDetails
