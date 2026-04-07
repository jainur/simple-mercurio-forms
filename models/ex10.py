"""
Domain model for EX-10
Solicitud de autorización de residencia temporal por circunstancias excepcionales.
"""

from __future__ import annotations

from datetime import date
from enum import Enum
from typing import Optional

from pydantic import BaseModel, EmailStr, Field
from models.common_sections import FilingRepresentativeDetailsBase, ForeignerIdentitySectionBase, NotificationAddressBase, OfficeDetailsBase, SignatureFieldsBase
from models.shared_enums import GenderEnum, MaritalStatusEnum


class ApplicationRequestTypeEnum(str, Enum):
    INITIAL = "INITIAL"
    EXTENSION = "EXTENSION"


class AuthorizationTypeEnum(str, Enum):
    SECOND_OPPORTUNITY_ART_127_A = "SECOND_OPPORTUNITY_ART_127_A"
    SOCIOLABORAL_ART_127_B = "SOCIOLABORAL_ART_127_B"
    SOCIAL_ART_127_C = "SOCIAL_ART_127_C"
    SOCIOFORMATIVO_ART_127_D = "SOCIOFORMATIVO_ART_127_D"
    FAMILY_ART_127_E = "FAMILY_ART_127_E"


class TrainingModeEnum(str, Enum):
    SECONDARY_POSTOBLIGATORY = "SECONDARY_POSTOBLIGATORY"
    PROFESSIONAL_CERTIFICATE_LEVEL_1 = "PROFESSIONAL_CERTIFICATE_LEVEL_1"
    PROFESSIONAL_CERTIFICATE_LEVEL_2 = "PROFESSIONAL_CERTIFICATE_LEVEL_2"
    MIXED = "MIXED"
    IN_PERSON_OR_DISTANCE = "IN_PERSON_OR_DISTANCE"


class ForeignerDetails(ForeignerIdentitySectionBase[GenderEnum, MaritalStatusEnum]):
    pass


class EuFamilyDetails(BaseModel):
    passport: Optional[str] = None
    nie: Optional[str] = None
    first_surname: str
    second_surname: Optional[str] = None
    name: str
    gender: GenderEnum
    marital_status: MaritalStatusEnum
    date_of_birth: date
    birth_country: str
    relationship_or_type: Optional[str] = None
    father_name: Optional[str] = None
    mother_name: Optional[str] = None
    address: str
    address_number: Optional[str] = None
    floor_door: Optional[str] = None
    city: str
    postal_code: str
    province: str
    relationship_with_applicant: str


class FilingRepresentativeDetails(FilingRepresentativeDetailsBase):
    pass


class NotificationAddress(NotificationAddressBase):
    pass


class EmployerDetails(BaseModel):
    name_or_company: str
    id_number: str
    activity: str
    cnae_code: Optional[str] = None
    cno_spe_2011: Optional[str] = None
    address: str
    address_number: Optional[str] = None
    floor_door: Optional[str] = None
    city: str
    postal_code: str
    province: str
    mobile_phone: Optional[str] = None
    email: Optional[EmailStr] = None
    legal_rep_name: Optional[str] = None
    legal_rep_id: Optional[str] = None
    legal_rep_title: Optional[str] = None


class TrainingDetails(BaseModel):
    training_name: Optional[str] = None
    course_code_1: Optional[str] = None
    course_code_2: Optional[str] = None
    course_code_3: Optional[str] = None
    province: Optional[str] = None
    duration_hours: Optional[str] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    training_mode: Optional[TrainingModeEnum] = None


class RequestDetails(BaseModel):
    has_valid_electronic_certificate_or_clave: bool = False
    request_type: ApplicationRequestTypeEnum
    authorization_type: AuthorizationTypeEnum

    humanitarian_option_1: bool = False
    humanitarian_option_2: bool = False
    humanitarian_option_3: bool = False
    humanitarian_option_4: bool = False
    humanitarian_option_5: bool = False

    public_interest_option_1: bool = False
    public_interest_option_2: bool = False

    gender_violence_woman_option_1: bool = False
    gender_violence_woman_option_2: bool = False
    parent_of_gender_violence_victim: bool = False

    sexual_violence_option_1: bool = False
    sexual_violence_option_2: bool = False

    parent_of_sexual_violence_option_1: bool = False
    parent_of_sexual_violence_option_2: bool = False
    parent_of_sexual_violence_option_3: bool = False
    parent_of_sexual_violence_option_4: bool = False
    parent_of_sexual_violence_option_5: bool = False
    parent_of_sexual_violence_option_6: bool = False

    unknown_option_148: bool = False


class SignatureDetails(BaseModel):
    signer_1: Optional[str] = None
    signer_2: Optional[str] = None
    signer_3: Optional[str] = None
    signer_4: Optional[str] = None
    signer_5: Optional[str] = None


class OfficeDetails(OfficeDetailsBase):
    pass


class EX10FormSchema(BaseModel):
    foreigner_details: ForeignerDetails
    eu_family_details: Optional[EuFamilyDetails] = None
    filing_representative: Optional[FilingRepresentativeDetails] = None
    notification_address: NotificationAddress
    employer_details: EmployerDetails
    training_details: TrainingDetails
    request_details: RequestDetails
    signature: SignatureDetails
    office: OfficeDetails
