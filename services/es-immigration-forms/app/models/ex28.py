"""
Domain model for EX-28.
Solicitud de aplicación de la disposición transitoria segunda del RD 1155/2024.
"""

from __future__ import annotations

from datetime import date
from enum import Enum
from typing import Optional

from pydantic import BaseModel, EmailStr
from app.models.common_sections import ApplicantLegalRepresentativeWithChildrenSectionBase, FilingRepresentativeDetailsBase, NotificationAddressBase, OfficeDetailsBase, SignatureFieldsBase
from app.models.shared_enums import GenderEnum, MaritalStatusEnum


class ApplicantDetails(ApplicantLegalRepresentativeWithChildrenSectionBase[GenderEnum, MaritalStatusEnum]):
    current_authorization_type: Optional[str] = None
    current_authorization_id: Optional[str] = None


class PendingApplicationDetails(BaseModel):
    case_number: str
    filing_date: str


class FilingRepresentativeDetails(FilingRepresentativeDetailsBase):
    pass


class NotificationAddress(NotificationAddressBase):
    pass


class RequestDetails(BaseModel):
    long_term_stay_from_study_or_mobility_or_volunteering: bool = False
    exceptional_circumstances_family_roots_to_parent_guardian_of_eu_minor: bool = False
    exceptional_circumstances_training_roots_to_sociotraining_roots: bool = False
    exceptional_circumstances_social_roots_employment_to_sociolabor_roots: bool = False
    exceptional_circumstances_social_roots_self_employment_to_social_roots: bool = False
    exceptional_circumstances_other_to_equivalent_title_vii: bool = False
    family_members_of_spanish_nationals_transition: bool = False
    temporary_residence_title_iv_to_equivalent_title_iv: bool = False
    temporary_residence_minor_child_or_ward_to_equivalent: bool = False
    long_term_residence_to_long_term_national: bool = False
    long_term_residence_to_long_term_eu: bool = False
    modification_of_situations_to_title_xi_equivalent: bool = False
    simultaneous_family_reunification_requests: bool = False


class SignatureDetails(SignatureFieldsBase):
    signer_name: Optional[str] = None

class OfficeDetails(OfficeDetailsBase):
    pass


class EX28FormSchema(BaseModel):
    applicant_details: ApplicantDetails
    pending_application: PendingApplicationDetails
    filing_representative: Optional[FilingRepresentativeDetails] = None
    notification_address: NotificationAddress
    request_details: RequestDetails
    signature: SignatureDetails
    office: OfficeDetails
