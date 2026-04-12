"""
Domain model for EX-20
Solicitud de documento de residencia para nacionales del Reino Unido y sus familiares.
"""

from __future__ import annotations

from datetime import date
from enum import Enum
from typing import Optional

from pydantic import BaseModel, EmailStr
from app.models.common_sections import FilingRepresentativeDetailsBase, ForeignerIdentitySectionBase, NotificationAddressBase, OfficeDetailsBase, SignatureFieldsBase
from app.models.shared_enums import GenderEnum, MaritalStatusEnum
from app.models.shared_request_enums import MainRequestCategoryEnum, ModificationGroundEnum, PermanentResidenceGroundEnum


class TemporaryResidenceGroundEnum(str, Enum):
    EMPLOYEE = "EMPLOYEE"
    SELF_EMPLOYED = "SELF_EMPLOYED"
    INACTIVE_WITH_RESOURCES_AND_INSURANCE = "INACTIVE_WITH_RESOURCES_AND_INSURANCE"
    STUDENT_WITH_RESOURCES_AND_INSURANCE = "STUDENT_WITH_RESOURCES_AND_INSURANCE"
    UK_FAMILY_MEMBER = "UK_FAMILY_MEMBER"


class ForeignerDetails(ForeignerIdentitySectionBase[GenderEnum, MaritalStatusEnum]):
    pass


class FilingRepresentativeDetails(FilingRepresentativeDetailsBase):
    pass


class NotificationAddress(NotificationAddressBase):
    pass


class RequestDetails(BaseModel):
    residence_start_segment_1: str
    residence_start_segment_2: str
    residence_start_segment_3: str
    residence_start_segment_4: str
    uk_national_document_id: Optional[str] = None
    relationship_with_uk_national: Optional[str] = None
    incapacity_with_spanish_spouse_text: Optional[str] = None
    identity_document_change_text: Optional[str] = None
    cause_specification: Optional[str] = None

    category: MainRequestCategoryEnum
    temporary_ground: Optional[TemporaryResidenceGroundEnum] = None
    permanent_ground: Optional[PermanentResidenceGroundEnum] = None
    modification_ground: Optional[ModificationGroundEnum] = None
    permanent_other_text: Optional[str] = None
    modification_other_text: Optional[str] = None
    deregistration_cause: Optional[str] = None
    truth_statement_accepted: bool = True


class SignatureDetails(SignatureFieldsBase):
    uk_national_signature_name: Optional[str] = None
    applicant_signature_name: Optional[str] = None


class OfficeDetails(OfficeDetailsBase):
    pass


class EX20FormSchema(BaseModel):
    foreigner_details: ForeignerDetails
    filing_representative: Optional[FilingRepresentativeDetails] = None
    notification_address: NotificationAddress
    request_details: RequestDetails
    signature: SignatureDetails
    office: OfficeDetails
