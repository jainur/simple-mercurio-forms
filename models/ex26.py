"""
Domain model for EX-26
Solicitud de modificación de autorización de residencia o estancia.
"""

from __future__ import annotations

from datetime import date
from enum import Enum
from typing import Optional

from pydantic import BaseModel, EmailStr
from models.common_sections import ApplicantLegalRepresentativeWithChildrenSectionBase, FilingRepresentativeDetailsBase, NotificationAddressBase, OfficeDetailsBase, SignatureFieldsBase


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


class ApplicantDetails(ApplicantLegalRepresentativeWithChildrenSectionBase[GenderEnum, MaritalStatusEnum]):
    pass


class EmployerDetails(BaseModel):
    name_or_company: str
    tax_or_id_number: str
    activity: Optional[str] = None
    cnae: Optional[str] = None
    registered_address: str
    address_number: Optional[str] = None
    floor_door: Optional[str] = None
    city: str
    postal_code: str
    province: str
    mobile_phone: Optional[str] = None
    email: Optional[EmailStr] = None
    legal_representative_name: Optional[str] = None
    legal_representative_id: Optional[str] = None
    legal_representative_title: Optional[str] = None


class FilingRepresentativeDetails(FilingRepresentativeDetailsBase):
    pass


class NotificationAddress(NotificationAddressBase):
    pass


class RequestDetails(BaseModel):
    from_work_enabled_residence_less_than_one_year_to_employment: bool = False
    from_work_enabled_residence_one_year_to_employment_and_self_employment: bool = False
    from_seasonal_residence_to_employment: bool = False
    from_seasonal_residence_to_self_employment: bool = False

    from_non_work_residence_less_than_one_year_to_employment: bool = False
    from_non_work_residence_one_year_to_employment: bool = False
    from_non_work_residence_one_year_to_self_employment: bool = False

    modify_employment_scope_occupation_or_territory: bool = False
    modify_self_employment_scope_sector_or_territory: bool = False
    from_employment_to_employment_and_self_employment: bool = False

    from_family_member_residence_to_non_lucrative_residence: bool = False
    from_family_member_residence_to_employment: bool = False
    from_family_member_residence_to_self_employment: bool = False
    from_family_member_residence_to_work_exception_residence: bool = False

    from_study_stay_to_employment_article_190_2: bool = False
    from_study_stay_to_self_employment_article_190_3: bool = False
    from_study_stay_to_work_exception_residence_article_190_4: bool = False
    from_study_stay_to_family_reunification_residence: bool = False
    from_study_stay_to_job_search_or_business_project: bool = False


class SignatureDetails(SignatureFieldsBase):
    signer_name: Optional[str] = None

class OfficeDetails(OfficeDetailsBase):
    pass


class EX26FormSchema(BaseModel):
    applicant_details: ApplicantDetails
    employer_details: Optional[EmployerDetails] = None
    filing_representative: Optional[FilingRepresentativeDetails] = None
    notification_address: NotificationAddress
    request_details: RequestDetails
    signature: SignatureDetails
    office: OfficeDetails
