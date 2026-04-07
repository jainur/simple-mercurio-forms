"""
Domain model for EX-19
Solicitud de tarjeta de residencia de familiar de ciudadano de la Union.
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


class ResidenceRequestTypeEnum(str, Enum):
    TEMPORARY_INITIAL = "TEMPORARY_INITIAL"
    PERMANENT = "PERMANENT"
    CARD_RENEWAL = "CARD_RENEWAL"
    MAINTAIN_PERSONAL_RIGHT = "MAINTAIN_PERSONAL_RIGHT"


class FamilyRelationshipEnum(str, Enum):
    SPOUSE = "SPOUSE"
    REGISTERED_PARTNER = "REGISTERED_PARTNER"
    STABLE_PARTNER = "STABLE_PARTNER"
    DESCENDANT_UNDER_21 = "DESCENDANT_UNDER_21"
    DESCENDANT_OVER_21_DEPENDENT = "DESCENDANT_OVER_21_DEPENDENT"
    ASCENDANT_DEPENDENT = "ASCENDANT_DEPENDENT"
    PARENT_OF_MINOR_EU_CITIZEN = "PARENT_OF_MINOR_EU_CITIZEN"
    OTHER_FAMILY_MEMBER = "OTHER_FAMILY_MEMBER"


class MaintainRightGroundEnum(str, Enum):
    DEATH_OF_EU_CITIZEN = "DEATH_OF_EU_CITIZEN"
    MARITAL_NULLITY_DIVORCE_OR_CANCELLED_PARTNERSHIP = "MARITAL_NULLITY_DIVORCE_OR_CANCELLED_PARTNERSHIP"
    VICTIM_OF_GENDER_OR_SEXUAL_VIOLENCE_OR_TRAFFICKING = "VICTIM_OF_GENDER_OR_SEXUAL_VIOLENCE_OR_TRAFFICKING"
    OTHER_CHILD_CUSTODY_OR_VISITATION = "OTHER_CHILD_CUSTODY_OR_VISITATION"


class ApplicantDetails(ApplicantGuardianMaritalSectionBase[GenderEnum, MaritalStatusEnum]):
    pass


class EuCitizenDetails(BaseModel):
    passport: Optional[str] = None
    nie: Optional[str] = None
    first_surname: str
    second_surname: Optional[str] = None
    name: str
    nationality: str
    address: str
    address_number: Optional[str] = None
    floor_door: Optional[str] = None
    city: str
    postal_code: str
    province: str


class FilingRepresentativeDetails(FilingRepresentativeDetailsBase):
    pass


class NotificationAddress(NotificationAddressBase):
    pass


class RequestDetails(BaseModel):
    request_type: ResidenceRequestTypeEnum
    family_relationship: Optional[FamilyRelationshipEnum] = None
    maintain_right_ground: Optional[MaintainRightGroundEnum] = None
    truth_statement_accepted: bool = True


class SignatureDetails(SignatureFieldsBase):
    eu_citizen_signature_name: Optional[str] = None
    applicant_signature_name: Optional[str] = None


class OfficeDetails(OfficeDetailsBase):
    pass


class EX19FormSchema(BaseModel):
    applicant_details: ApplicantDetails
    eu_citizen_details: EuCitizenDetails
    filing_representative: Optional[FilingRepresentativeDetails] = None
    notification_address: NotificationAddress
    request_details: RequestDetails
    signature: SignatureDetails
    office: OfficeDetails
