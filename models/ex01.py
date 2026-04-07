"""
Domain model for EX-01
Solicitud de autorización de residencia temporal no lucrativa.

Sections
--------
1  DATOS DE LA PERSONA EXTRANJERA SOLICITANTE
2  DATOS DEL FAMILIAR TITULAR DE LOS RECURSOS ECONÓMICOS  (optional)
3  DATOS DEL REPRESENTANTE A EFECTOS DE PRESENTACIÓN      (optional)
4  DOMICILIO A EFECTOS DE NOTIFICACIONES
5  TIPO DE AUTORIZACIÓN SOLICITADA
"""

from __future__ import annotations

from datetime import date
from enum import Enum
from typing import Optional

from pydantic import BaseModel, EmailStr, Field
from models.common_sections import ApplicantGuardianMaritalWithChildrenSectionBase, FilingRepresentativeDetailsBase, NotificationAddressBase, OfficeDetailsBase, SignatureFieldsBase
from models.shared_enums import GenderEnum, MaritalStatusEnum


# ---------------------------------------------------------------------------
# Enums
# ---------------------------------------------------------------------------

class ApplicationCategoryEnum(str, Enum):
    RESIDENCIA_INICIAL = "RESIDENCIA_INICIAL"
    RENOVACION         = "RENOVACION"


class ApplicantRoleEnum(str, Enum):
    """Whether the applicant is the economic resources holder or their family member."""
    TITULAR_RECURSOS         = "TITULAR_RECURSOS"
    FAMILIAR_TITULAR_RECURSOS = "FAMILIAR_TITULAR_RECURSOS"


# ---------------------------------------------------------------------------
# Section sub-models
# ---------------------------------------------------------------------------

class ForeignerDetails(ApplicantGuardianMaritalWithChildrenSectionBase[GenderEnum, MaritalStatusEnum]):
    pass


class ResourceHolderDetails(BaseModel):
    """
    Section 2 – Datos del familiar titular de los recursos económicos.
    Required when applicant_role == FAMILIAR_TITULAR_RECURSOS.
    """

    passport: Optional[str] = Field(None, description="Número de Pasaporte del titular")
    nie: Optional[str] = Field(None, description="NIE del titular, e.g. X-1234567-L")
    first_surname: str = Field(..., description="1er Apellido")
    second_surname: Optional[str] = Field(None, description="2º Apellido")
    name: str = Field(..., description="Nombre")
    gender: GenderEnum = Field(..., description="Sexo")
    date_of_birth: date = Field(..., description="Fecha de nacimiento")
    birth_country: str = Field(..., description="País de nacimiento")
    father_name: Optional[str] = Field(None, description="Nombre del padre")
    mother_name: Optional[str] = Field(None, description="Nombre de la madre")
    relationship: str = Field(..., description="Parentesco con el solicitante")
    marital_status: MaritalStatusEnum = Field(..., description="Estado civil")
    name_or_company: Optional[str] = Field(None, description="Nombre o Razón Social (si persona jurídica)")
    id_number: Optional[str] = Field(None, description="DNI/NIE/PAS")
    address: Optional[str] = Field(None, description="Domicilio en España")
    address_number: Optional[str] = Field(None, description="Nº")
    floor_door: Optional[str] = Field(None, description="Piso / Puerta")
    city: Optional[str] = Field(None, description="Localidad")
    postal_code: Optional[str] = Field(None, description="C.P.")
    province: Optional[str] = Field(None, description="Provincia")
    mobile_phone: Optional[str] = Field(None, description="Teléfono móvil")
    email: Optional[EmailStr] = Field(None, description="E-mail")
    legal_rep_name: Optional[str] = Field(None, description="Representante legal, en su caso")
    legal_rep_id: Optional[str] = Field(None, description="DNI/NIE/PAS del representante legal")
    legal_rep_title: Optional[str] = Field(None, description="Título del representante legal")


class PresenterDetails(FilingRepresentativeDetailsBase):
    pass


class NotificationAddress(NotificationAddressBase):
    pass


class RequestDetails(BaseModel):
    """Section 5 – Tipo de autorización solicitada."""

    application_category: ApplicationCategoryEnum = Field(
        ..., description="RESIDENCIA_INICIAL o RENOVACION"
    )
    applicant_role: ApplicantRoleEnum = Field(
        ...,
        description="Si el solicitante es titular de los recursos o familiar del titular",
    )


class SignatureDetails(SignatureFieldsBase):
    name: Optional[str] = None


class OfficeDetails(OfficeDetailsBase):
    pass


class EX01FormSchema(BaseModel):
    """
    EX-01: Solicitud de autorización de residencia temporal no lucrativa.
    """

    foreigner_details: ForeignerDetails
    resource_holder: Optional[ResourceHolderDetails] = Field(
        None,
        description=(
            "Familiar titular de los recursos económicos (sección 2). "
            "Requerido cuando applicant_role == FAMILIAR_TITULAR_RECURSOS."
        ),
    )
    presenter_details: Optional[PresenterDetails] = Field(
        None, description="Representante para presentación (sección 3, opcional)"
    )
    notification_address: NotificationAddress
    request_details: RequestDetails
    office: OfficeDetails
    signature: SignatureDetails
