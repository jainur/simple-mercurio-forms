"""
Domain model for EX-02
Solicitud de autorización de residencia temporal por reagrupación familiar.
"""

from __future__ import annotations

from datetime import date
from enum import Enum
from typing import Optional

from pydantic import BaseModel, EmailStr, Field
from models.common_sections import ApplicantGuardianMaritalWithChildrenSectionBase, FilingRepresentativeDetailsBase, NotificationAddressBase, OfficeDetailsBase, SignatureFieldsBase
from models.shared_enums import GenderEnum, MaritalStatusEnum


class FamilyRelationshipEnum(str, Enum):
    SPOUSE = "SPOUSE"
    REGISTERED_PARTNER = "REGISTERED_PARTNER"
    MINOR_LEGALLY_REPRESENTED = "MINOR_LEGALLY_REPRESENTED"
    DISABLED_ADULT_LEGALLY_REPRESENTED = "DISABLED_ADULT_LEGALLY_REPRESENTED"
    ADULT_CHILD_CAREGIVER = "ADULT_CHILD_CAREGIVER"
    MINOR_CHILD = "MINOR_CHILD"
    DISABLED_ADULT_CHILD = "DISABLED_ADULT_CHILD"
    UNREGISTERED_PARTNER = "UNREGISTERED_PARTNER"
    ASCENDANT_OVER_65 = "ASCENDANT_OVER_65"
    ASCENDANT_UNDER_65 = "ASCENDANT_UNDER_65"
    ADULT_CHILD_RENEWAL_ONLY = "ADULT_CHILD_RENEWAL_ONLY"


class AuthorizationTypeEnum(str, Enum):
    INITIAL_ART_65 = "INITIAL_ART_65"
    INITIAL_UE_LONG_TERM_FAMILY = "INITIAL_UE_LONG_TERM_FAMILY"
    RENEWAL_ART_71 = "RENEWAL_ART_71"
    CHILDREN_CHAPTER_IV_ART_147 = "CHILDREN_CHAPTER_IV_ART_147"
    CHILDREN_CHAPTER_V_ART_155 = "CHILDREN_CHAPTER_V_ART_155"


class IndependentResidenceReasonEnum(str, Enum):
    INDEPENDENT_MEANS_ART_69_1 = "INDEPENDENT_MEANS_ART_69_1"
    BREAKUP_ART_69_2_A = "BREAKUP_ART_69_2_A"
    VICTIM_ART_69_2_B = "VICTIM_ART_69_2_B"
    DEATH_ART_69_2_C = "DEATH_ART_69_2_C"
    MAJORITY_OR_END_OF_REPRESENTATION_ART_69_4 = "MAJORITY_OR_END_OF_REPRESENTATION_ART_69_4"
    EU_RESIDENCE_BLUE_CARD_CONTEXT_ART_69_5 = "EU_RESIDENCE_BLUE_CARD_CONTEXT_ART_69_5"
    ASCENDANT_WITH_WORK_AUTH_ART_69_6 = "ASCENDANT_WITH_WORK_AUTH_ART_69_6"


class WorkModeEnum(str, Enum):
    CUENTA_AJENA = "CUENTA_AJENA"
    CUENTA_PROPIA = "CUENTA_PROPIA"


class ApplicantDetails(ApplicantGuardianMaritalWithChildrenSectionBase[GenderEnum, MaritalStatusEnum]):
    current_authorization: Optional[str] = Field(None, description="Autorización de la que es titular")
    current_authorization_document: Optional[str] = Field(None, description="DNI/NIE/PAS del título")
    current_authorization_title: Optional[str] = Field(None, description="Título")


class SponsorDetails(BaseModel):
    passport: Optional[str] = None
    nie: Optional[str] = None
    first_surname: str
    second_surname: Optional[str] = None
    name: str
    gender: GenderEnum
    date_of_birth: date
    birth_place: str
    birth_country: str
    nationality: str
    father_name: Optional[str] = None
    mother_name: Optional[str] = None
    address: str
    address_number: Optional[str] = None
    floor_door: Optional[str] = None
    city: str
    postal_code: str
    province: str
    marital_status: MaritalStatusEnum


class PresenterDetails(FilingRepresentativeDetailsBase):
    pass


class NotificationAddress(NotificationAddressBase):
    pass


class RequestDetails(BaseModel):
    family_relationship: FamilyRelationshipEnum
    authorization_type: AuthorizationTypeEnum

    request_independent_residence: bool = False
    independent_residence_reason: Optional[IndependentResidenceReasonEnum] = None

    request_ascendant_work_authorization: bool = False
    work_mode: Optional[WorkModeEnum] = None

    simultaneous_other_family_reunification_requests: bool = False


class SignatureDetails(SignatureFieldsBase):
    name: Optional[str] = None


class OfficeDetails(OfficeDetailsBase):
    pass


class EX02FormSchema(BaseModel):
    applicant_details: ApplicantDetails
    sponsor_details: SponsorDetails
    presenter_details: Optional[PresenterDetails] = None
    notification_address: NotificationAddress
    request_details: RequestDetails
    signature: SignatureDetails
    office: OfficeDetails
