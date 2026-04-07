from pydantic import BaseModel, Field, EmailStr
from typing import Optional
from enum import Enum
from datetime import date

# --- Enums for categorical fields ---

class GenderEnum(str, Enum):
    MALE = "H"
    FEMALE = "M"

class MaritalStatusEnum(str, Enum):
    SINGLE = "S"
    MARRIED = "C"
    WIDOWED = "V"
    DIVORCED = "D"
    SEPARATED = "Sp"

class AuthorizationTypeEnum(str, Enum):
    LONG_TERM_GENERAL = "Larga Duración - Supuesto general 5 años"
    LONG_TERM_PENSIONER = "Larga Duración - Beneficiario de pensión"
    LONG_TERM_BORN_IN_SPAIN = "Larga Duración - Nacido en España y residente 3 años"
    LONG_TERM_SPANISH_ORIGIN = "Larga Duración - Español de origen"
    LONG_TERM_TUTELADO = "Larga Duración - Tutelado por entidad pública 5 años"
    LONG_TERM_EU_BLUE_CARD = "Larga Duración - Titular Tarjeta Azul UE"
    LONG_TERM_EU_GENERAL = "Larga Duración-UE - Supuesto general 5 años"

# --- Sub-models for distinct form sections ---

class ForeignerDetails(BaseModel):
    nie: Optional[str] = Field(None, description="Número de Identidad de Extranjero")
    passport: Optional[str] = Field(None, description="Número de Pasaporte")
    first_surname: str = Field(..., description="1er Apellido")
    second_surname: Optional[str] = Field(None, description="2º Apellido")
    name: str = Field(..., description="Nombre")
    gender: GenderEnum = Field(..., description="Sexo (H/M)")
    date_of_birth: date = Field(..., description="Fecha de nacimiento")
    place_of_birth: str = Field(..., description="Lugar de nacimiento")
    country_of_birth: str = Field(..., description="País de nacimiento")
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
    legal_rep_id: Optional[str] = Field(None, description="DNI/NIE/PAS del representante legal (menor/tutelado)")
    legal_rep_title: Optional[str] = Field(None, description="Título del representante legal")
    children_in_school_age: bool = Field(False, description="Hijas/os a cargo en edad de escolarización en España")

class PresenterDetails(BaseModel):
    name_or_company: str = Field(..., description="Nombre o Razón Social del presentador")
    id_number: str = Field(..., description="DNI/NIE/PAS del presentador")
    address: str = Field(..., description="Domicilio en España")
    address_number: Optional[str] = Field(None, description="Nº del domicilio")
    floor_door: Optional[str] = Field(None, description="Piso / Puerta")
    city: str = Field(..., description="Localidad")
    postal_code: str = Field(..., description="C.P.")
    province: str = Field(..., description="Provincia")
    mobile_phone: Optional[str] = Field(None, description="Teléfono móvil")
    email: Optional[EmailStr] = Field(None, description="E-mail")
    legal_rep_id: Optional[str] = Field(None, description="DNI/NIE/PAS del representante legal")
    legal_rep_title: Optional[str] = Field(None, description="Título del representante legal")

class NotificationAddress(BaseModel):
    name_or_company: str = Field(..., description="Nombre o Razón Social para notificaciones")
    id_number: str = Field(..., description="DNI/NIE/PAS")
    address: str = Field(..., description="Domicilio a efectos de notificaciones")
    address_number: Optional[str] = Field(None, description="Nº del domicilio")
    floor_door: Optional[str] = Field(None, description="Piso / Puerta")
    city: str = Field(..., description="Localidad")
    postal_code: str = Field(..., description="C.P.")
    province: str = Field(..., description="Provincia")
    mobile_phone: Optional[str] = Field(None, description="Teléfono móvil")
    email: Optional[EmailStr] = Field(None, description="E-mail")
    consent_electronic_notifications: bool = Field(
        default=False, 
        description="CONSIENTO que las comunicaciones se realicen mediante Dehú (Dirección electrónica habilitada Única)"
    )

class RequestDetails(BaseModel):
    target_office_dir3: Optional[str] = Field(None, description="Código DIR3 de la oficina a la que se dirige")
    target_province: str = Field(..., description="Provincia a la que se dirige")
    authorization_type: AuthorizationTypeEnum = Field(..., description="Tipo de autorización solicitada")

# --- Main Form Schema ---

class EX11FormSchema(BaseModel):
    """
    Main Schema for EX-11: Solicitud de autorización de residencia de larga duración o de larga duración-UE
    """
    foreigner_details: ForeignerDetails
    presenter_details: Optional[PresenterDetails] = Field(
        None, description="Datos del representante a efectos de presentación de la solicitud (if applicable)"
    )
    notification_address: NotificationAddress
    request_details: RequestDetails