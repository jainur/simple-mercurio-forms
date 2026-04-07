from __future__ import annotations

from datetime import date
from enum import Enum
from typing import Generic, Optional, TypeVar

from pydantic import BaseModel, EmailStr

TGender = TypeVar("TGender", bound=Enum)
TMarital = TypeVar("TMarital", bound=Enum)


class _IdentityCoreBase(BaseModel, Generic[TGender, TMarital]):
    passport: Optional[str] = None
    nie: Optional[str] = None
    first_surname: str
    second_surname: Optional[str] = None
    name: str
    gender: TGender
    marital_status: TMarital
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
    mobile_phone: Optional[str] = None
    email: Optional[EmailStr] = None
    legal_guardian_name: Optional[str] = None
    legal_guardian_id: Optional[str] = None
    legal_guardian_title: Optional[str] = None


class ForeignerIdentitySectionBase(_IdentityCoreBase[TGender, TMarital], Generic[TGender, TMarital]):
    pass


class ApplicantGuardianMaritalSectionBase(_IdentityCoreBase[TGender, TMarital], Generic[TGender, TMarital]):
    pass


class ApplicantGuardianMaritalNoAddressSectionBase(_IdentityCoreBase[TGender, TMarital], Generic[TGender, TMarital]):
    address: Optional[str] = None
    address_number: Optional[str] = None
    floor_door: Optional[str] = None
    city: Optional[str] = None
    postal_code: Optional[str] = None
    province: Optional[str] = None


class ApplicantGuardianMaritalWithChildrenSectionBase(
    ApplicantGuardianMaritalSectionBase[TGender, TMarital],
    Generic[TGender, TMarital],
):
    has_school_age_children_in_spain: Optional[bool] = None
    children_in_school_age: Optional[str] = None


class ApplicantLegalRepresentativeSectionBase(_IdentityCoreBase[TGender, TMarital], Generic[TGender, TMarital]):
    legal_representative_name: Optional[str] = None
    legal_representative_id: Optional[str] = None
    legal_representative_title: Optional[str] = None


class ApplicantLegalRepresentativeWithChildrenSectionBase(
    ApplicantLegalRepresentativeSectionBase[TGender, TMarital],
    Generic[TGender, TMarital],
):
    has_school_age_children_in_spain: Optional[bool] = None
    children_in_school_age: Optional[str] = None


class FilingRepresentativeDetailsBase(BaseModel):
    name_or_company: str
    id_number: str
    address: str
    address_number: Optional[str] = None
    floor_door: Optional[str] = None
    city: str
    postal_code: str
    province: str
    mobile_phone: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[EmailStr] = None
    legal_rep_name: Optional[str] = None
    legal_rep_id: Optional[str] = None
    legal_rep_title: Optional[str] = None
    legal_representative_name: Optional[str] = None
    legal_representative_id: Optional[str] = None
    legal_representative_title: Optional[str] = None


class NotificationAddressBase(BaseModel):
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
    consent_electronic_notifications: bool = False


class OfficeDetailsBase(BaseModel):
    target_office: Optional[str] = None
    dir3_code: Optional[str] = None
    province: str


class SignatureFieldsBase(BaseModel):
    place: str
    day: str
    month: str
    year: str
