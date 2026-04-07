"""
Domain model for EX-24
Solicitud de autorización de residencia temporal de familiar de personas con nacionalidad española.
"""

from __future__ import annotations

from datetime import date
from enum import Enum
from typing import Optional

from pydantic import BaseModel, EmailStr
from models.common_sections import ApplicantGuardianMaritalSectionBase, FilingRepresentativeDetailsBase, NotificationAddressBase, OfficeDetailsBase, SignatureFieldsBase
from models.shared_enums import GenderEnum, MaritalStatusEnum


class InitialRelationshipEnum(str, Enum):
    SPOUSE_OR_REGISTERED_OR_STABLE_PARTNER = "SPOUSE_OR_REGISTERED_OR_STABLE_PARTNER"
    CHILD_UNDER_26_OR_DISABLED = "CHILD_UNDER_26_OR_DISABLED"
    CHILD_OVER_26_DEPENDENT = "CHILD_OVER_26_DEPENDENT"
    FIRST_DEGREE_ASCENDANT = "FIRST_DEGREE_ASCENDANT"
    PARENT_OR_GUARDIAN_OF_SPANISH_MINOR = "PARENT_OR_GUARDIAN_OF_SPANISH_MINOR"
    CAREGIVER_UP_TO_SECOND_DEGREE = "CAREGIVER_UP_TO_SECOND_DEGREE"
    CHILD_OF_SPANISH_PARENT_BY_ORIGIN = "CHILD_OF_SPANISH_PARENT_BY_ORIGIN"
    OTHER_DEPENDENT_FAMILY_MEMBER = "OTHER_DEPENDENT_FAMILY_MEMBER"


class RequestCategoryEnum(str, Enum):
    INITIAL_RESIDENCE = "INITIAL_RESIDENCE"
    RENEWAL = "RENEWAL"
    INDEPENDENT_RESIDENCE_BY_PRESERVATION = "INDEPENDENT_RESIDENCE_BY_PRESERVATION"


class PreservationGroundEnum(str, Enum):
    DEATH_OF_SPANISH_NATIONAL = "DEATH_OF_SPANISH_NATIONAL"
    END_OF_EFFECTIVE_RESIDENCE_IN_SPAIN = "END_OF_EFFECTIVE_RESIDENCE_IN_SPAIN"
    NULLITY_DIVORCE_OR_CANCELLATION = "NULLITY_DIVORCE_OR_CANCELLATION"
    VICTIM_OF_GENDER_OR_SEXUAL_VIOLENCE_OR_FAMILY_VIOLENCE_OR_TRAFFICKING = "VICTIM_OF_GENDER_OR_SEXUAL_VIOLENCE_OR_FAMILY_VIOLENCE_OR_TRAFFICKING"


class ApplicantDetails(ApplicantGuardianMaritalSectionBase[GenderEnum, MaritalStatusEnum]):
    pass


class SpanishNationalFamilyMemberDetails(BaseModel):
    passport: Optional[str] = None
    dni: Optional[str] = None
    title: Optional[str] = None
    first_surname: str
    second_surname: Optional[str] = None
    name: str
    date_of_birth: date
    birth_country: str
    father_name: Optional[str] = None
    mother_name: Optional[str] = None
    address: str
    address_number: Optional[str] = None
    floor_door: Optional[str] = None
    city: str
    postal_code: str
    province: str
    relationship_with_applicant: str
    gender: GenderEnum
    marital_status: MaritalStatusEnum


class FilingRepresentativeDetails(FilingRepresentativeDetailsBase):
    pass


class NotificationAddress(NotificationAddressBase):
    pass


class RequestDetails(BaseModel):
    category: RequestCategoryEnum
    initial_relationship: Optional[InitialRelationshipEnum] = None
    preservation_ground: Optional[PreservationGroundEnum] = None


class SignatureDetails(SignatureFieldsBase):
    name: Optional[str] = None


class OfficeDetails(OfficeDetailsBase):
    pass


class EX24FormSchema(BaseModel):
    applicant_details: ApplicantDetails
    spanish_family_member_details: SpanishNationalFamilyMemberDetails
    filing_representative: Optional[FilingRepresentativeDetails] = None
    notification_address: NotificationAddress
    request_details: RequestDetails
    signature: SignatureDetails
    office: OfficeDetails
