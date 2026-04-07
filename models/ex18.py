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
from models.shared_enums import GenderEnum, MaritalStatusEnum
from models.shared_request_enums import MainRequestCategoryEnum, ModificationGroundEnum, PermanentResidenceGroundEnum


class TemporaryResidenceGroundEnum(str, Enum):
    EMPLOYEE = "EMPLOYEE"
    SELF_EMPLOYED = "SELF_EMPLOYED"
    INACTIVE_WITH_RESOURCES_AND_INSURANCE = "INACTIVE_WITH_RESOURCES_AND_INSURANCE"
    STUDENT_WITH_RESOURCES_AND_INSURANCE = "STUDENT_WITH_RESOURCES_AND_INSURANCE"
    EU_FAMILY_MEMBER = "EU_FAMILY_MEMBER"


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
