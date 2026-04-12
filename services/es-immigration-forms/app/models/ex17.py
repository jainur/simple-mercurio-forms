"""
Domain model for EX-17
Solicitud de tarjeta de identidad de extranjero (TIE).
"""

from __future__ import annotations

from datetime import date
from enum import Enum
from typing import Optional

from pydantic import BaseModel, EmailStr
from app.models.common_sections import FilingRepresentativeDetailsBase, ForeignerIdentitySectionBase, NotificationAddressBase, OfficeDetailsBase, SignatureFieldsBase
from app.models.shared_enums import GenderEnum, MaritalStatusEnum


class CardRequestTypeEnum(str, Enum):
    INITIAL_CARD = "INITIAL_CARD"
    CARD_RENEWAL = "CARD_RENEWAL"
    DUPLICATE_LOSS_THEFT_DAMAGE_OR_DATA_CHANGE = "DUPLICATE_LOSS_THEFT_DAMAGE_OR_DATA_CHANGE"


class ForeignerDetails(ForeignerIdentitySectionBase[GenderEnum, MaritalStatusEnum]):
    pass


class FilingRepresentativeDetails(FilingRepresentativeDetailsBase):
    pass


class NotificationAddress(NotificationAddressBase):
    pass


class RequestDetails(BaseModel):
    card_request_type: CardRequestTypeEnum


class SignatureDetails(SignatureFieldsBase):
    name: Optional[str] = None


class OfficeDetails(OfficeDetailsBase):
    pass


class EX17FormSchema(BaseModel):
    foreigner_details: ForeignerDetails
    filing_representative: Optional[FilingRepresentativeDetails] = None
    notification_address: NotificationAddress
    request_details: RequestDetails
    signature: SignatureDetails
    office: OfficeDetails
