"""
Domain model for EX-06
Solicitud de autorización de residencia temporal y trabajo por cuenta ajena de duración determinada.
"""

from __future__ import annotations

from datetime import date
from enum import Enum
from typing import Optional

from pydantic import BaseModel, EmailStr, Field
from app.models.common_sections import FilingRepresentativeDetailsBase, ForeignerIdentitySectionBase, NotificationAddressBase, OfficeDetailsBase, SignatureFieldsBase
from app.models.shared_enums import GenderEnum, MaritalStatusEnum


class ApplicationTypeEnum(str, Enum):
    RESIDENCIA_INICIAL = "RESIDENCIA_INICIAL"
    PRIMER_LLAMAMIENTO = "PRIMER_LLAMAMIENTO"
    SEGUNDO_LLAMAMIENTO = "SEGUNDO_LLAMAMIENTO"
    TERCER_LLAMAMIENTO = "TERCER_LLAMAMIENTO"
    CAMBIO_EMPLEADOR = "CAMBIO_EMPLEADOR"
    PRORROGA_O_CONCATENACION = "PRORROGA_O_CONCATENACION"
    RENOVACION_PLURIANUAL = "RENOVACION_PLURIANUAL"


class ForeignerDetails(ForeignerIdentitySectionBase[GenderEnum, MaritalStatusEnum]):
    pass


class EmployerDetails(BaseModel):
    name_or_company: str
    id_number: str
    activity: str
    occupation: str
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


class FilingRepresentativeDetails(FilingRepresentativeDetailsBase):
    pass


class NotificationAddress(NotificationAddressBase):
    pass


class RequestDetails(BaseModel):
    application_type: ApplicationTypeEnum
    accepts_truth_responsibility: bool = True


class SignatureDetails(SignatureFieldsBase):
    name: Optional[str] = None


class OfficeDetails(OfficeDetailsBase):
    pass


class EX06FormSchema(BaseModel):
    foreigner_details: ForeignerDetails
    employer_details: EmployerDetails
    filing_representative: Optional[FilingRepresentativeDetails] = None
    notification_address: NotificationAddress
    request_details: RequestDetails
    signature: SignatureDetails
    office: OfficeDetails
