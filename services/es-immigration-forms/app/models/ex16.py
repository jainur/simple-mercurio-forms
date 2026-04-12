"""
Domain model for EX-16
Solicitud de autorización de viaje para personas extranjeras.
"""

from __future__ import annotations

from datetime import date
from enum import Enum
from typing import Optional

from pydantic import BaseModel, EmailStr
from app.models.common_sections import FilingRepresentativeDetailsBase, ForeignerIdentitySectionBase, NotificationAddressBase, OfficeDetailsBase, SignatureFieldsBase
from app.models.shared_enums import GenderEnum, MaritalStatusEnum


class AuthorizationStageEnum(str, Enum):
    INITIAL = "INITIAL"
    RENEWAL = "RENEWAL"


class TravelDocumentTypeEnum(str, Enum):
    TRAVEL_AUTHORIZATION = "TRAVEL_AUTHORIZATION"
    TRAVEL_TITLE = "TRAVEL_TITLE"


class ReturnModeEnum(str, Enum):
    WITH_RETURN = "WITH_RETURN"
    WITHOUT_RETURN = "WITHOUT_RETURN"


class ForeignerDetails(ForeignerIdentitySectionBase[GenderEnum, MaritalStatusEnum]):
    pass


class FilingRepresentativeDetails(FilingRepresentativeDetailsBase):
    pass


class NotificationAddress(NotificationAddressBase):
    pass


class RequestDetails(BaseModel):
    destination: str

    reason_humanitarian: bool = False
    reason_public_interest: bool = False
    reason_spain_commitments: bool = False
    reason_exceptional_circumstances: bool = False

    stage: AuthorizationStageEnum
    document_type: TravelDocumentTypeEnum
    return_mode: ReturnModeEnum

    title_reason_humanitarian: bool = False
    title_reason_public_interest: bool = False
    title_motivos_checkbox: bool = False


class SignatureDetails(SignatureFieldsBase):
    name: Optional[str] = None


class OfficeDetails(OfficeDetailsBase):
    pass


class EX16FormSchema(BaseModel):
    foreigner_details: ForeignerDetails
    filing_representative: Optional[FilingRepresentativeDetails] = None
    notification_address: NotificationAddress
    request_details: RequestDetails
    signature: SignatureDetails
    office: OfficeDetails
