"""
Domain model for EX-00
Solicitud de autorización de estancia por estudios, movilidad de alumnos,
prácticas no laborales y formación.

Sections
--------
1  DATOS DE LA PERSONA EXTRANJERA
2  DATOS DE INSTITUCIÓN/CENTRO DE ESTUDIOS, FORMACIÓN O VOLUNTARIADO
3  DATOS DEL PROGRAMA DE ESTUDIOS O FORMACIÓN
4  DATOS DEL FAMILIAR ESTUDIANTE AL QUE ACOMPAÑA          (optional)
5  DATOS DEL EMPLEADOR/A                                   (optional)
6  DATOS DEL REPRESENTANTE A EFECTOS DE LA PRESENTACIÓN   (optional)
7  DOMICILIO A EFECTOS DE NOTIFICACIONES
8  TIPO DE AUTORIZACIÓN DE ESTANCIA SOLICITADA
"""

from __future__ import annotations

from datetime import date
from enum import Enum
from typing import Optional

from pydantic import BaseModel, EmailStr, Field
from app.models.shared_enums import GenderEnum, MaritalStatusEnum


# ---------------------------------------------------------------------------
# Enums
# ---------------------------------------------------------------------------

class InstitutionRecognitionTypeEnum(str, Enum):
    """Recognition type for the study institution (section 2 checkboxes)."""
    RUCT                   = "RUCT"
    RCD                    = "RCD"
    OTHER                  = "OTRO"
    UNIVERSITY_AFFILIATION = "ADSCRIPCION_UNIVERSIDAD"
    OTHER_OFFICIAL         = "OTRO_RECONOCIMIENTO_OFICIAL"


class StudyModalityEnum(str, Enum):
    IN_PERSON = "PRESENCIAL"
    HYBRID    = "HIBRIDA"


class ApplicationCategoryEnum(str, Enum):
    INICIAL              = "INICIAL"
    PRORROGA             = "PRORROGA"
    AUTORIZACION_TRABAJO = "AUTORIZACION_TRABAJO"


class AuthorizationSubtypeEnum(str, Enum):
    """
    Specific authorization subtype within INICIAL.
    Maps directly to one of the article checkboxes in section 8.
    """
    ESTUDIOS_SUPERIORES         = "ESTUDIOS_SUPERIORES"           # art. 52.1.a
    EDUCACION_SECUNDARIA        = "EDUCACION_SECUNDARIA"          # art. 52.1.b
    MOVILIDAD_SECUNDARIA        = "MOVILIDAD_SECUNDARIA"          # art. 52.1.c
    VOLUNTARIADO                = "VOLUNTARIADO"                  # art. 52.1.d
    ACTIVIDADES_FORMATIVAS      = "ACTIVIDADES_FORMATIVAS"        # art. 52.1.e
    AUXILIAR_CONVERSACION       = "AUXILIAR_CONVERSACION"         # art. 52.1.e.1º
    ESTUDIOS_IDIOMATICOS        = "ESTUDIOS_IDIOMATICOS"          # art. 52.1.e.2º
    CURSOS_PREPARATORIOS        = "CURSOS_PREPARATORIOS"          # art. 52.1.e.3º
    CERTIFICACION_APTITUD       = "CERTIFICACION_APTITUD"         # art. 52.1.e.4º
    CERTIFICADO_PROFESIONAL     = "CERTIFICADO_PROFESIONAL"       # art. 52.1.e.5º
    FORMACION_SANITARIA         = "FORMACION_SANITARIA"           # art. 58
    MOVILIDAD_PROGRAMA_UE       = "MOVILIDAD_PROGRAMA_UE"         # art. 59.2
    MOVILIDAD_SIN_PROGRAMA_UE   = "MOVILIDAD_SIN_PROGRAMA_UE"    # art. 59.3
    CONVENIO_ANDORRA            = "CONVENIO_ANDORRA"
    FAMILIAR_ESTUDIOS_SUPERIORES = "FAMILIAR_ESTUDIOS_SUPERIORES" # art. 56
    FAMILIAR_FORMACION_SANITARIA = "FAMILIAR_FORMACION_SANITARIA" # art. 56
    FAMILIAR_ANDORRA             = "FAMILIAR_ANDORRA"
    HIJO_NACIDO_ESPANA           = "HIJO_NACIDO_ESPANA"           # art. 56.7


class WorkModeEnum(str, Enum):
    """Mode of work authorization (section 8, when category == AUTORIZACION_TRABAJO)."""
    EMPLOYED      = "CUENTA_AJENA"
    SELF_EMPLOYED = "CUENTA_PROPIA"


# ---------------------------------------------------------------------------
# Section sub-models
# ---------------------------------------------------------------------------

class ForeignerDetails(BaseModel):
    """Section 1 – Datos de la persona extranjera."""

    passport: Optional[str] = Field(None, description="Número de Pasaporte")
    nie: Optional[str] = Field(
        None, description="Número de Identidad de Extranjero, e.g. X-1234567-L"
    )
    first_surname: str  = Field(..., description="1er Apellido")
    second_surname: Optional[str] = Field(None, description="2º Apellido")
    name: str = Field(..., description="Nombre")
    gender: GenderEnum = Field(..., description="Sexo")
    date_of_birth: date = Field(..., description="Fecha de nacimiento")
    birth_place: str = Field(..., description="Lugar de nacimiento")
    birth_country: str = Field(..., description="País de nacimiento")
    nationality: str = Field(..., description="Nacionalidad")
    marital_status: MaritalStatusEnum = Field(..., description="Estado civil")
    father_name: Optional[str] = Field(None, description="Nombre del padre")
    mother_name: Optional[str] = Field(None, description="Nombre de la madre")
    address: str = Field(..., description="Domicilio en España")
    address_number: Optional[str] = Field(None, description="Nº del domicilio")
    floor_door: Optional[str] = Field(None, description="Piso / Puerta")
    city: str = Field(..., description="Localidad")
    postal_code: str = Field(..., description="C.P.")
    province: str = Field(..., description="Provincia")
    mobile_phone: Optional[str] = Field(None, description="Teléfono móvil")
    email: Optional[EmailStr] = Field(None, description="E-mail")
    legal_guardian_name: Optional[str] = Field(
        None, description="Representante legal (menor/tutelado), en su caso"
    )
    legal_guardian_id: Optional[str] = Field(
        None, description="DNI/NIE/PAS del representante legal"
    )
    legal_guardian_title: Optional[str] = Field(
        None, description="Título del representante legal"
    )


class InstitutionDetails(BaseModel):
    """Section 2 – Datos de institución/centro de estudios."""

    denomination: str = Field(..., description="Denominación del centro / institución")
    nif: Optional[str] = Field(None, description="NIF")
    recognition_type: InstitutionRecognitionTypeEnum = Field(
        ..., description="Tipo de registro/reconocimiento del centro"
    )
    other_type_name: Optional[str] = Field(
        None, description="Descripción si recognition_type == OTHER"
    )
    university_affiliation_name: Optional[str] = Field(
        None, description="Universidad de adscripción (si recognition_type == UNIVERSITY_AFFILIATION)"
    )
    other_official_recognition_name: Optional[str] = Field(
        None, description="Otro reconocimiento oficial (DT única)"
    )
    dir3_code: Optional[str] = Field(None, description="Código DIR3")
    address: str = Field(..., description="Dirección")
    address_number: Optional[str] = Field(None, description="Nº")
    floor_door: Optional[str] = Field(None, description="Piso")
    city: str = Field(..., description="Localidad")
    postal_code: str = Field(..., description="C.P.")
    province: str = Field(..., description="Provincia")
    legal_rep_name: Optional[str] = Field(None, description="Representante legal, en su caso")
    legal_rep_id: Optional[str] = Field(None, description="DNI/NIE/PAS del representante legal")
    legal_rep_title: Optional[str] = Field(None, description="Título del representante legal")


class ProgramDetails(BaseModel):
    """Section 3 – Datos del programa de estudios o formación."""

    denomination: str = Field(..., description="Denominación del programa")
    dir3_code: Optional[str] = Field(None, description="Código DIR3 del programa")
    start_date: date = Field(..., description="Fecha de inicio")
    end_date: date = Field(..., description="Fecha de finalización")
    modality: StudyModalityEnum = Field(..., description="Modalidad: presencial o híbrida/semipresencial")


class FamilyMemberDetails(BaseModel):
    """Section 4 – Datos del familiar estudiante al que acompaña (optional)."""

    name: str = Field(..., description="Nombre del familiar")
    nie_pas: Optional[str] = Field(None, description="NIE / PAS del familiar")
    surnames: str = Field(..., description="Apellidos del familiar")
    relationship: str = Field(..., description="Parentesco")


class EmployerDetails(BaseModel):
    """Section 5 – Datos del empleador/a (only when applying for work authorization)."""

    name_or_company: str = Field(..., description="Nombre o Razón Social")
    dni_nie_pas: Optional[str] = Field(None, description="DNI/NIE/PAS")
    activity: Optional[str] = Field(None, description="Actividad")
    occupation: Optional[str] = Field(None, description="Ocupación")
    address: str = Field(..., description="Domicilio en España")
    address_number: Optional[str] = Field(None, description="Nº")
    floor_door: Optional[str] = Field(None, description="Piso")
    city: str = Field(..., description="Localidad")
    postal_code: str = Field(..., description="C.P.")
    province: str = Field(..., description="Provincia")
    mobile_phone: Optional[str] = Field(None, description="Teléfono móvil")
    email: Optional[EmailStr] = Field(None, description="E-mail")
    legal_rep_name: Optional[str] = Field(None, description="Representante legal, en su caso")
    legal_rep_id: Optional[str] = Field(None, description="DNI/NIE/PAS del representante legal")


class PresenterDetails(BaseModel):
    """Section 6 – Datos del representante a efectos de presentación (optional)."""

    name_or_company: str = Field(..., description="Nombre o Razón Social")
    id_number: str = Field(..., description="DNI/NIE/PAS")
    address: str = Field(..., description="Domicilio en España")
    address_number: Optional[str] = Field(None, description="Nº")
    floor_door: Optional[str] = Field(None, description="Piso")
    city: str = Field(..., description="Localidad")
    postal_code: str = Field(..., description="C.P.")
    province: str = Field(..., description="Provincia")
    mobile_phone: Optional[str] = Field(None, description="Teléfono móvil")
    email: Optional[EmailStr] = Field(None, description="E-mail")
    legal_rep_name: Optional[str] = Field(None, description="Representante legal, en su caso")
    legal_rep_id: Optional[str] = Field(None, description="DNI/NIE/PAS del representante legal")
    legal_rep_title: Optional[str] = Field(None, description="Título (4)")


class NotificationAddress(BaseModel):
    """Section 7 – Domicilio a efectos de notificaciones."""

    name_or_company: str = Field(..., description="Nombre o Razón Social")
    id_number: str = Field(..., description="DNI/NIE/PAS")
    address: str = Field(..., description="Domicilio")
    address_number: Optional[str] = Field(None, description="Nº")
    floor_door: Optional[str] = Field(None, description="Piso")
    city: str = Field(..., description="Localidad")
    postal_code: str = Field(..., description="C.P.")
    province: str = Field(..., description="Provincia")
    mobile_phone: Optional[str] = Field(None, description="Teléfono móvil")
    email: Optional[EmailStr] = Field(None, description="E-mail")
    consent_electronic_notifications: bool = Field(
        default=False,
        description="CONSIENTO notificaciones mediante Dirección electrónica habilitada Única (Dehú)",
    )


class RequestDetails(BaseModel):
    """Section 8 – Tipo de autorización de estancia solicitada."""

    application_category: ApplicationCategoryEnum = Field(
        ..., description="Categoría: INICIAL, PRÓRROGA o AUTORIZACIÓN PARA TRABAJAR"
    )
    authorization_subtype: Optional[AuthorizationSubtypeEnum] = Field(
        None, description="Subtipo de autorización (aplica cuando category == INICIAL)"
    )
    requested_by_institution: bool = Field(
        False, description="Solicitada por institución (checkbox dentro de INICIAL)"
    )
    legal_status_in_spain: bool = Field(
        False, description="Situación regular en España (checkbox auxiliar)"
    )
    work_mode: Optional[WorkModeEnum] = Field(
        None,
        description="Modo de trabajo: cuenta ajena / cuenta propia (solo con AUTORIZACION_TRABAJO)",
    )


class OfficeDetails(BaseModel):
    """Office the application is addressed to (bottom of last page)."""

    target_office: Optional[str] = Field(None, description="Nombre de la oficina (DIRIGIDA A)")
    dir3_code: Optional[str] = Field(None, description="Código DIR3 de la oficina")
    province: str = Field(..., description="Provincia")


class SignatureDetails(BaseModel):
    place: str = Field(..., description="Lugar de la firma")
    day: str = Field(..., description="Día")
    month: str = Field(..., description="Mes")
    year: str = Field(..., description="Año")
    name: Optional[str] = Field(None, description="Nombre del firmante (campo firma)")


# ---------------------------------------------------------------------------
# Root schema
# ---------------------------------------------------------------------------

class EX00FormSchema(BaseModel):
    """
    EX-00: Solicitud de autorización de estancia por estudios, movilidad de
    alumnos, prácticas no laborales y formación.
    """

    foreigner_details: ForeignerDetails
    institution_details: InstitutionDetails
    program_details: ProgramDetails
    family_member: Optional[FamilyMemberDetails] = Field(
        None, description="Familiar al que acompaña (sección 4, opcional)"
    )
    employer_details: Optional[EmployerDetails] = Field(
        None, description="Datos del empleador (sección 5, solo con autorización de trabajo)"
    )
    presenter_details: Optional[PresenterDetails] = Field(
        None, description="Datos del representante para presentación (sección 6, opcional)"
    )
    notification_address: NotificationAddress
    request_details: RequestDetails
    office: OfficeDetails
    signature: SignatureDetails
