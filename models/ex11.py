"""
Domain model for EX-11
Solicitud de autorización de residencia de larga duración o larga duración-UE.
"""

from __future__ import annotations

from datetime import date
from enum import Enum
from typing import Optional

from pydantic import BaseModel, EmailStr
from models.common_sections import ApplicantGuardianMaritalWithChildrenSectionBase, FilingRepresentativeDetailsBase, NotificationAddressBase, OfficeDetailsBase, SignatureFieldsBase
from models.shared_enums import GenderEnum, MaritalStatusEnum


class AuthorizationFamilyEnum(str, Enum):
    RESIDENCIA_LARGA_DURACION = "RESIDENCIA_LARGA_DURACION"
    RESIDENCIA_LARGA_DURACION_UE = "RESIDENCIA_LARGA_DURACION_UE"


class LdSubtypeEnum(str, Enum):
    GENERAL_5_YEARS_ART_183_1 = "GENERAL_5_YEARS_ART_183_1"
    PENSION_OR_PERMANENT_DISABILITY_ART_183_3 = "PENSION_OR_PERMANENT_DISABILITY_ART_183_3"
    BORN_IN_SPAIN_AND_3_YEARS_RESIDENCE_ART_183_3_C = "BORN_IN_SPAIN_AND_3_YEARS_RESIDENCE_ART_183_3_C"
    FORMER_SPANISH_NATIONAL_ART_183_3_D = "FORMER_SPANISH_NATIONAL_ART_183_3_D"
    FORMER_PUBLIC_GUARDIANSHIP_ART_183_3_E = "FORMER_PUBLIC_GUARDIANSHIP_ART_183_3_E"
    STATELESS_OR_REFUGEE_ART_183_3_F = "STATELESS_OR_REFUGEE_ART_183_3_F"
    FAMILY_REUNIFICATION_WITH_LTR_SPONSOR = "FAMILY_REUNIFICATION_WITH_LTR_SPONSOR"
    EU_LTR_HOLDER_IN_OTHER_MEMBER_STATE_ART_179 = "EU_LTR_HOLDER_IN_OTHER_MEMBER_STATE_ART_179"
    RECOVERY_AFTER_LOSS_ART_188 = "RECOVERY_AFTER_LOSS_ART_188"


class LdUeSubtypeEnum(str, Enum):
    GENERAL_5_YEARS_WITH_RESOURCES_AND_INSURANCE_ART_176_1_A = "GENERAL_5_YEARS_WITH_RESOURCES_AND_INSURANCE_ART_176_1_A"
    STUDIES_EXCHANGE_PRACTICES_COMPUTED_50_ART_176_A = "STUDIES_EXCHANGE_PRACTICES_COMPUTED_50_ART_176_A"
    TWO_YEARS_SPAIN_PLUS_THREE_YEARS_BLUE_CARD_EU_ART_176_A = "TWO_YEARS_SPAIN_PLUS_THREE_YEARS_BLUE_CARD_EU_ART_176_A"
    OTHER_MEMBER_STATE_EU_LTR_RENUNCIATION_ART_181 = "OTHER_MEMBER_STATE_EU_LTR_RENUNCIATION_ART_181"
    RECOVERY_AFTER_LOSS_ART_186 = "RECOVERY_AFTER_LOSS_ART_186"


class ForeignerDetails(ApplicantGuardianMaritalWithChildrenSectionBase[GenderEnum, MaritalStatusEnum]):
    pass


class FilingRepresentativeDetails(FilingRepresentativeDetailsBase):
    pass


class NotificationAddress(NotificationAddressBase):
    pass


class RequestDetails(BaseModel):
    authorization_family: AuthorizationFamilyEnum
    ld_subtype: Optional[LdSubtypeEnum] = None
    ld_ue_subtype: Optional[LdUeSubtypeEnum] = None


class SignatureDetails(SignatureFieldsBase):
    name: Optional[str] = None


class OfficeDetails(OfficeDetailsBase):
    pass


class EX11FormSchema(BaseModel):
    foreigner_details: ForeignerDetails
    filing_representative: Optional[FilingRepresentativeDetails] = None
    notification_address: NotificationAddress
    request_details: RequestDetails
    signature: SignatureDetails
    office: OfficeDetails
