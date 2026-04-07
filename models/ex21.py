"""
Domain model for EX-21
Solicitud relativa al documento de residencia para familiares de nacionales del Reino Unido.
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


class MainRequestCategoryEnum(str, Enum):
    TEMPORARY_RESIDENCE = "TEMPORARY_RESIDENCE"
    PERMANENT_RESIDENCE = "PERMANENT_RESIDENCE"
    MODIFICATION = "MODIFICATION"
    CARD_RENEWAL = "CARD_RENEWAL"
    DEREGISTRATION = "DEREGISTRATION"


class FamilyRelationshipEnum(str, Enum):
    SPOUSE = "SPOUSE"
    REGISTERED_PARTNER = "REGISTERED_PARTNER"
    UNREGISTERED_PARTNER = "UNREGISTERED_PARTNER"
    DESCENDANT_UNDER_21 = "DESCENDANT_UNDER_21"
    DESCENDANT_OVER_21_DEPENDENT_OR_DISABLED = "DESCENDANT_OVER_21_DEPENDENT_OR_DISABLED"
    ASCENDANT_DEPENDENT = "ASCENDANT_DEPENDENT"
    OTHER_FAMILY_MEMBER = "OTHER_FAMILY_MEMBER"


class PermanentResidenceGroundEnum(str, Enum):
    CONTINUOUS_5_YEARS = "CONTINUOUS_5_YEARS"
    FAMILY_OF_BRITISH_WORKER_WITH_PERMANENT_RESIDENCE = "FAMILY_OF_BRITISH_WORKER_WITH_PERMANENT_RESIDENCE"
    WIDOW_WITH_2_YEARS_RESIDENCE = "WIDOW_WITH_2_YEARS_RESIDENCE"
    WIDOW_WORK_ACCIDENT_OR_PROF_DISEASE = "WIDOW_WORK_ACCIDENT_OR_PROF_DISEASE"
    WIDOW_ORIGINALLY_SPANISH = "WIDOW_ORIGINALLY_SPANISH"
    OTHER = "OTHER"


class ModificationGroundEnum(str, Enum):
    PERSONAL_DATA = "PERSONAL_DATA"
    ADDRESS = "ADDRESS"
    IDENTITY_DOCUMENT = "IDENTITY_DOCUMENT"
    STATUS_WIDOW = "STATUS_WIDOW"
    STATUS_CHILD_AND_PARENT_UNTIL_END_OF_STUDIES = "STATUS_CHILD_AND_PARENT_UNTIL_END_OF_STUDIES"
    OTHER = "OTHER"


class RenewalSubtypeEnum(str, Enum):
    TEMPORARY_HOLDER = "TEMPORARY_HOLDER"
    PERMANENT_HOLDER = "PERMANENT_HOLDER"


class ApplicantDetails(ApplicantGuardianMaritalSectionBase[GenderEnum, MaritalStatusEnum]):
    pass


class BritishNationalDetails(BaseModel):
    passport: Optional[str] = None
    nie: Optional[str] = None
    first_surname: str
    second_surname: Optional[str] = None
    name: str
    address: str
    city: str
    postal_code: str
    relationship_with_applicant: str
    nationality: str
    address_number: Optional[str] = None
    floor_door: Optional[str] = None
    province: str


class FilingRepresentativeDetails(FilingRepresentativeDetailsBase):
    pass


class NotificationAddress(NotificationAddressBase):
    pass


class RequestDetails(BaseModel):
    residence_start_day: str
    residence_start_month: str
    residence_start_year: str
    continuous_5_years_text: Optional[str] = None
    identity_document_change_text: Optional[str] = None
    cause_specification: Optional[str] = None

    category: MainRequestCategoryEnum
    family_relationship: Optional[FamilyRelationshipEnum] = None
    permanent_ground: Optional[PermanentResidenceGroundEnum] = None
    modification_ground: Optional[ModificationGroundEnum] = None
    renewal_subtype: Optional[RenewalSubtypeEnum] = None
    deregistration_cause_present: bool = False
    truth_statement_accepted: bool = True


class SignatureDetails(SignatureFieldsBase):
    british_national_signature_name: Optional[str] = None
    applicant_signature_name: Optional[str] = None


class OfficeDetails(OfficeDetailsBase):
    pass


class EX21FormSchema(BaseModel):
    applicant_details: ApplicantDetails
    british_national_details: BritishNationalDetails
    filing_representative: Optional[FilingRepresentativeDetails] = None
    notification_address: NotificationAddress
    request_details: RequestDetails
    signature: SignatureDetails
    office: OfficeDetails
