"""
Domain model for EX-13
Solicitud de autorización de regreso.
"""

from __future__ import annotations

from datetime import date
from enum import Enum
from typing import Optional

from pydantic import BaseModel, EmailStr
from models.common_sections import FilingRepresentativeDetailsBase, ForeignerIdentitySectionBase, NotificationAddressBase, OfficeDetailsBase, SignatureFieldsBase
from models.shared_enums import GenderEnum, MaritalStatusEnum


class ReturnAuthorizationGroundEnum(str, Enum):
    RESIDENCE_RENEWAL_OR_EXTENSION_ART_5 = "RESIDENCE_RENEWAL_OR_EXTENSION_ART_5"
    STAY_EXTENSION_ART_5 = "STAY_EXTENSION_ART_5"
    TIE_DUPLICATE_THEFT_LOSS_DAMAGE_ART_5 = "TIE_DUPLICATE_THEFT_LOSS_DAMAGE_ART_5"
    INITIAL_RESIDENCE_TIE_ISSUANCE_EXCEPTIONAL_REASONS_ART_5 = "INITIAL_RESIDENCE_TIE_ISSUANCE_EXCEPTIONAL_REASONS_ART_5"
    INITIAL_STAY_TIE_ISSUANCE_EXCEPTIONAL_REASONS_ART_5 = "INITIAL_STAY_TIE_ISSUANCE_EXCEPTIONAL_REASONS_ART_5"
    OTHER = "OTHER"


class ForeignerDetails(ForeignerIdentitySectionBase[GenderEnum, MaritalStatusEnum]):
    pass


class FilingRepresentativeDetails(FilingRepresentativeDetailsBase):
    pass


class NotificationAddress(NotificationAddressBase):
    pass


class RequestDetails(BaseModel):
    ground: ReturnAuthorizationGroundEnum
    other_reason_text_1: Optional[str] = None
    other_reason_text_2: Optional[str] = None
    other_reason_text_3: Optional[str] = None


class SignatureDetails(SignatureFieldsBase):
    name: Optional[str] = None


class OfficeDetails(OfficeDetailsBase):
    pass


class EX13FormSchema(BaseModel):
    foreigner_details: ForeignerDetails
    filing_representative: Optional[FilingRepresentativeDetails] = None
    notification_address: NotificationAddress
    request_details: RequestDetails
    signature: SignatureDetails
    office: OfficeDetails
