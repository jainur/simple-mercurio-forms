"""
Domain model for EX-30.
Solicitud de aplicación de la disposición transitoria quinta del RD 1155/2024.
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


class AuthorizationTypeEnum(str, Enum):
    SECOND_CHANCE = "SECOND_CHANCE"
    SOCIOLABORAL = "SOCIOLABORAL"
    SOCIAL = "SOCIAL"
    SOCIOFORMATIVO = "SOCIOFORMATIVO"


class ApplicantDetails(ApplicantLegalRepresentativeSectionBase[GenderEnum, MaritalStatusEnum]):
    pass


class FilingRepresentativeDetails(FilingRepresentativeDetailsBase):
    pass


class NotificationAddress(NotificationAddressBase):
    pass


class EmployerDetails(BaseModel):
    name_or_company: str
    tax_or_id_number: str
    activity: Optional[str] = None
    cnae: Optional[str] = None
    cno_spe_2011: Optional[str] = None
    registered_address: str
    address_number: Optional[str] = None
    floor_door: Optional[str] = None
    city: str
    postal_code: str
    province: str
    mobile_phone: Optional[str] = None
    email: Optional[EmailStr] = None
    representative_name: Optional[str] = None
    representative_id: Optional[str] = None
    representative_title: Optional[str] = None


class TrainingCenterDetails(BaseModel):
    provider_name: str
    training_name: str
    course_code: Optional[str] = None
    provider_tax_id: Optional[str] = None
    provider_address: str
    province: str
    duration_hours: Optional[str] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    secondary_post_compulsory_education: bool = False
    professional_certificate: bool = False
    adult_mandatory_education_in_person: bool = False
    public_employment_service_training: bool = False
    modality_presential: bool = False
    modality_non_presential: bool = False
    date_range_checkbox: bool = False


class RequestDetails(BaseModel):
    authorization_type: AuthorizationTypeEnum


class SignatureDetails(SignatureFieldsBase):
    signer_name: Optional[str] = None

class OfficeDetails(OfficeDetailsBase):
    pass


class EX30FormSchema(BaseModel):
    applicant_details: ApplicantDetails
    employer_details: Optional[EmployerDetails] = None
    training_center_details: Optional[TrainingCenterDetails] = None
    filing_representative: Optional[FilingRepresentativeDetails] = None
    notification_address: NotificationAddress
    request_details: RequestDetails
    signature: SignatureDetails
    office: OfficeDetails
