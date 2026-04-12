"""
Domain model for EX-03
Solicitud de autorización de residencia temporal y trabajo por cuenta ajena.
"""

from __future__ import annotations

from datetime import date
from enum import Enum
from typing import Optional

from pydantic import BaseModel, EmailStr, Field
from app.models.common_sections import ApplicantGuardianMaritalWithChildrenSectionBase, FilingRepresentativeDetailsBase, NotificationAddressBase, OfficeDetailsBase, SignatureFieldsBase
from app.models.shared_enums import GenderEnum, MaritalStatusEnum


class ApplicationPhaseEnum(str, Enum):
    INITIAL = "INITIAL"
    RENEWAL = "RENEWAL"


class InitialEligibilityEnum(str, Enum):
    INTERNATIONAL_AGREEMENTS_CHILE_PERU_ART_74_2 = "INTERNATIONAL_AGREEMENTS_CHILE_PERU_ART_74_2"
    EXEMPTION_ART_40_LO_4_2000 = "EXEMPTION_ART_40_LO_4_2000"
    HARD_TO_FILL_OCCUPATION_CATALOG = "HARD_TO_FILL_OCCUPATION_CATALOG"
    PUBLIC_EMPLOYMENT_SERVICE_OFFER = "PUBLIC_EMPLOYMENT_SERVICE_OFFER"
    COUNCIL_OF_MINISTERS_INSTRUCTIONS_DA2_1 = "COUNCIL_OF_MINISTERS_INSTRUCTIONS_DA2_1"
    PROFESSIONAL_ATHLETES_2005 = "PROFESSIONAL_ATHLETES_2005"
    MERCHANT_MARINE_2007 = "MERCHANT_MARINE_2007"
    FISHING_VESSEL_2019 = "FISHING_VESSEL_2019"
    THIRD_GRADE_OR_PAROLE_2005 = "THIRD_GRADE_OR_PAROLE_2005"
    INTERNATIONAL_AGREEMENTS_ANDORRA = "INTERNATIONAL_AGREEMENTS_ANDORRA"
    CROSS_BORDER_WORKER_ART_157 = "CROSS_BORDER_WORKER_ART_157"
    EMPLOYER_CHANGE_BREACH_ART_79_2 = "EMPLOYER_CHANGE_BREACH_ART_79_2"
    EMPLOYER_CHANGE_OVERRIDING_CIRCUMSTANCES_ART_79_3 = "EMPLOYER_CHANGE_OVERRIDING_CIRCUMSTANCES_ART_79_3"


class RenewalGroundEnum(str, Enum):
    GENERAL_ART_81_1 = "GENERAL_ART_81_1"
    UNEMPLOYMENT_BENEFIT = "UNEMPLOYMENT_BENEFIT"
    CROSS_BORDER_WORKER_ART_158 = "CROSS_BORDER_WORKER_ART_158"
    THIRD_GRADE_OR_PAROLE_2005 = "THIRD_GRADE_OR_PAROLE_2005"


class FilingPartyEnum(str, Enum):
    FOREIGN_WORKER = "FOREIGN_WORKER"
    EMPLOYER = "EMPLOYER"


class SignaturePartyEnum(str, Enum):
    LEGAL_REPRESENTATIVE_OR_FOREIGNER = "LEGAL_REPRESENTATIVE_OR_FOREIGNER"
    FOREIGN_WORKER = "FOREIGN_WORKER"
    EMPLOYER = "EMPLOYER"


class ForeignerDetails(ApplicantGuardianMaritalWithChildrenSectionBase[GenderEnum, MaritalStatusEnum]):
    pass


class EmployerDetails(BaseModel):
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
    legal_rep_name: Optional[str] = None
    legal_rep_id: Optional[str] = None
    legal_rep_title: Optional[str] = None


class JobOfferDetails(BaseModel):
    position_name: str
    contribution_group: Optional[str] = None
    cno_sepe_2011: Optional[str] = None
    convenio_code: Optional[str] = None
    convenio_name: Optional[str] = None
    contract_code: Optional[str] = None
    contract_name: Optional[str] = None
    social_security_account_code: Optional[str] = None
    gross_salary_eur: Optional[str] = None
    work_center_address: str
    work_center_number: Optional[str] = None
    work_center_floor_door: Optional[str] = None
    work_center_city: str
    work_center_postal_code: str
    work_center_province: str


class FilingRepresentativeDetails(FilingRepresentativeDetailsBase):
    pass


class NotificationAddress(NotificationAddressBase):
    pass


class RequestDetails(BaseModel):
    application_phase: ApplicationPhaseEnum
    initial_eligibility: Optional[InitialEligibilityEnum] = None
    renewal_ground: Optional[RenewalGroundEnum] = None
    filing_party: FilingPartyEnum
    signature_party: SignaturePartyEnum


class SignatureDetails(SignatureFieldsBase):
    name: Optional[str] = None


class OfficeDetails(OfficeDetailsBase):
    pass


class EX03FormSchema(BaseModel):
    foreigner_details: ForeignerDetails
    employer_details: EmployerDetails
    job_offer_details: JobOfferDetails
    filing_representative: Optional[FilingRepresentativeDetails] = None
    notification_address: NotificationAddress
    request_details: RequestDetails
    signature: SignatureDetails
    office: OfficeDetails
