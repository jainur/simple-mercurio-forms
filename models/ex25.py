"""
Domain model for EX-25
Solicitud relativa a menores extranjeros.
"""

from __future__ import annotations

from datetime import date
from enum import Enum
from typing import Optional

from pydantic import BaseModel, EmailStr
from models.common_sections import FilingRepresentativeDetailsBase, NotificationAddressBase, OfficeDetailsBase, SignatureFieldsBase


class GenderEnum(str, Enum):
    OTHER = "X"
    MALE = "H"
    FEMALE = "M"


class MinorDetails(BaseModel):
    passport: Optional[str] = None
    nie: Optional[str] = None
    first_surname: str
    second_surname: Optional[str] = None
    name: str
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
    mobile_phone: Optional[str] = None
    postal_code: str
    province: str
    email: Optional[EmailStr] = None
    legal_guardian_name: Optional[str] = None
    legal_guardian_id: Optional[str] = None
    legal_guardian_title: Optional[str] = None
    representative_nature: Optional[str] = None
    relationship_with_minor: Optional[str] = None
    gender: GenderEnum


class GuardianOrEntityDetails(BaseModel):
    name_or_company: str
    id_number: str
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


class FilingRepresentativeDetails(FilingRepresentativeDetailsBase):
    pass


class NotificationAddress(NotificationAddressBase):
    pass


class RequestDetails(BaseModel):
    temporary_residence_minor_born_in_spain: bool = False
    temporary_residence_accompanied_disabled_minor_not_born_in_spain: bool = False
    temporary_residence_dana_2024_minor_with_guardian: bool = False

    temporary_initial_unaccompanied_minor: bool = False
    temporary_initial_former_ward_without_residence_at_majority: bool = False
    temporary_initial_displaced_minor_medical_treatment_extension_exhausted: bool = False
    temporary_initial_parent_or_guardian_medical_treatment_extension_exhausted: bool = False

    renewal_unaccompanied_minor_with_residence: bool = False
    renewal_former_ward_with_residence_at_majority: bool = False
    renewal_former_ward_without_residence_at_majority: bool = False
    renewal_displaced_minor_medical_treatment_exceptional: bool = False
    renewal_parent_or_guardian_medical_treatment_exceptional: bool = False

    humanitarian_program_minor_medical_treatment_stay: bool = False
    humanitarian_program_parent_or_guardian_medical_treatment_stay: bool = False
    humanitarian_program_minor_holiday_stay: bool = False
    humanitarian_program_monitor_holiday_stay: bool = False
    humanitarian_program_schooling_stay: bool = False

    humanitarian_extension_medical_treatment: bool = False
    humanitarian_extension_parent_or_guardian_medical_treatment: bool = False
    humanitarian_extension_schooling_exceptional_return_impediment: bool = False

    other_international_adoption: bool = False
    other_vacations_in_peace_program: bool = False


class SignatureDetails(BaseModel):
    day: str
    signer_1_id: Optional[str] = None
    signer_1_title: Optional[str] = None
    place: str = ""
    signer_2_id: Optional[str] = None
    signer_2_title: Optional[str] = None
    month: str = ""
    year: str = ""
    signer_1_name: Optional[str] = None
    signer_2_name: Optional[str] = None


class OfficeDetails(OfficeDetailsBase):
    pass


class EX25FormSchema(BaseModel):
    minor_details: MinorDetails
    guardian_or_entity_details: GuardianOrEntityDetails
    filing_representative: FilingRepresentativeDetails
    notification_address: NotificationAddress
    request_details: RequestDetails
    signature: SignatureDetails
    office: OfficeDetails
