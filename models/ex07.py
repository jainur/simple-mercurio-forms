"""
Domain model for EX-07
Solicitud de autorización de residencia temporal y trabajo por cuenta propia.
"""

from __future__ import annotations

from datetime import date
from enum import Enum
from typing import Optional

from pydantic import BaseModel, EmailStr, Field
from models.common_sections import ApplicantGuardianMaritalWithChildrenSectionBase, FilingRepresentativeDetailsBase, NotificationAddressBase, OfficeDetailsBase, SignatureFieldsBase


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


class ApplicationCategoryEnum(str, Enum):
    INITIAL = "INITIAL"
    RENEWAL = "RENEWAL"
    TERRITORIAL_SCOPE_EXTENSION = "TERRITORIAL_SCOPE_EXTENSION"


class InitialGroundEnum(str, Enum):
    GENERAL_RESIDENT_OUTSIDE_SPAIN_ART_85 = "GENERAL_RESIDENT_OUTSIDE_SPAIN_ART_85"
    INTERNATIONAL_AGREEMENTS_ANDORRA = "INTERNATIONAL_AGREEMENTS_ANDORRA"
    CROSS_BORDER_SELF_EMPLOYED_ART_157 = "CROSS_BORDER_SELF_EMPLOYED_ART_157"


class RenewalGroundEnum(str, Enum):
    CONTINUITY_ART_86 = "CONTINUITY_ART_86"
    OTHER_CASES_ART_86 = "OTHER_CASES_ART_86"
    CROSS_BORDER_SELF_EMPLOYED_ART_158 = "CROSS_BORDER_SELF_EMPLOYED_ART_158"


class TerritorialScopeGroundEnum(str, Enum):
    SAME_ACTIVITY_MULTIPLE_AUTONOMOUS_COMMUNITIES_ART_85_6 = "SAME_ACTIVITY_MULTIPLE_AUTONOMOUS_COMMUNITIES_ART_85_6"


class SignerRoleEnum(str, Enum):
    FOREIGNER = "FOREIGNER"
    REPRESENTATIVE = "REPRESENTATIVE"


class ForeignerDetails(ApplicantGuardianMaritalWithChildrenSectionBase[GenderEnum, MaritalStatusEnum]):
    pass


class SelfEmploymentDetails(BaseModel):
    name_or_company: str
    id_number: str
    activity: str
    cnae_code: Optional[str] = None
    address: str
    address_number: Optional[str] = None
    floor_door: Optional[str] = None
    city: str
    postal_code: str
    province: str
    mobile_phone: Optional[str] = None
    email: Optional[EmailStr] = None


class FilingRepresentativeDetails(FilingRepresentativeDetailsBase):
    pass


class NotificationAddress(NotificationAddressBase):
    pass


class RequestDetails(BaseModel):
    category: ApplicationCategoryEnum
    initial_ground: Optional[InitialGroundEnum] = None
    renewal_ground: Optional[RenewalGroundEnum] = None
    territorial_scope_ground: Optional[TerritorialScopeGroundEnum] = None
    signer_role: SignerRoleEnum


class SignatureDetails(SignatureFieldsBase):
    name: Optional[str] = None


class OfficeDetails(OfficeDetailsBase):
    pass


class EX07FormSchema(BaseModel):
    foreigner_details: ForeignerDetails
    self_employment_details: SelfEmploymentDetails
    filing_representative: Optional[FilingRepresentativeDetails] = None
    notification_address: NotificationAddress
    request_details: RequestDetails
    signature: SignatureDetails
    office: OfficeDetails
