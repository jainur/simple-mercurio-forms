"""EX03 domain model example."""

from datetime import date
from pathlib import Path

from fill_form import fill_form_from_model
from models.ex03 import (
    ApplicationPhaseEnum,
    EmployerDetails,
    EX03FormSchema,
    FilingPartyEnum,
    FilingRepresentativeDetails,
    ForeignerDetails,
    GenderEnum,
    InitialEligibilityEnum,
    JobOfferDetails,
    MaritalStatusEnum,
    NotificationAddress,
    OfficeDetails,
    RequestDetails,
    SignatureDetails,
    SignaturePartyEnum,
)

foreigner = ForeignerDetails(
    passport="AB1234567",
    nie=None,
    first_surname="GARCIA",
    second_surname="LOPEZ",
    name="MARTA",
    gender=GenderEnum.FEMALE,
    date_of_birth=date(1993, 9, 11),
    birth_place="Lima",
    birth_country="Peru",
    nationality="Peruana",
    father_name="JOSE GARCIA",
    mother_name="ANA LOPEZ",
    address="Calle Atocha",
    address_number="15",
    floor_door="2A",
    city="Madrid",
    postal_code="28012",
    province="Madrid",
    mobile_phone="600123123",
    email="marta.garcia@example.com",
    marital_status=MaritalStatusEnum.SINGLE,
    children_in_school_age=False,
    legal_guardian_name=None,
    legal_guardian_id=None,
    legal_guardian_title=None,
)

employer = EmployerDetails(
    name_or_company="HOSTELERIA CENTRO SL",
    id_number="B23456789",
    activity="Restauracion",
    cnae_code="5610",
    address="Calle Fuencarral",
    address_number="100",
    floor_door="",
    city="Madrid",
    postal_code="28004",
    province="Madrid",
    mobile_phone="910111222",
    email="rrhh@hosteleriacentro.es",
    legal_rep_name="CARLOS MENDEZ",
    legal_rep_id="12345678A",
    legal_rep_title="Administrador",
)

job = JobOfferDetails(
    position_name="Camarera",
    contribution_group="08",
    cno_sepe_2011="5120",
    convenio_code="28000105011982",
    convenio_name="Hosteleria Madrid",
    contract_code="100",
    contract_name="Indefinido a tiempo completo",
    social_security_account_code="281234567890",
    gross_salary_eur="18000",
    work_center_address="Calle Fuencarral",
    work_center_number="100",
    work_center_floor_door="",
    work_center_city="Madrid",
    work_center_postal_code="28004",
    work_center_province="Madrid",
)

representative = FilingRepresentativeDetails(
    name_or_company="GESTORIA LEGAL SA",
    id_number="A11223344",
    address="Paseo de la Castellana",
    address_number="55",
    floor_door="5",
    city="Madrid",
    postal_code="28046",
    province="Madrid",
    phone="913334444",
    email="tramites@gestorialegal.es",
    legal_rep_name="LAURA TORRES",
    legal_rep_id="22334455B",
    legal_rep_title="Apoderada",
)

notification = NotificationAddress(
    name_or_company="GESTORIA LEGAL SA",
    id_number="A11223344",
    address="Paseo de la Castellana",
    address_number="55",
    floor_door="5",
    city="Madrid",
    postal_code="28046",
    province="Madrid",
    mobile_phone="913334444",
    email="notificaciones@gestorialegal.es",
    consent_electronic_notifications=True,
)

request = RequestDetails(
    application_phase=ApplicationPhaseEnum.INITIAL,
    initial_eligibility=InitialEligibilityEnum.INTERNATIONAL_AGREEMENTS_CHILE_PERU_ART_74_2,
    renewal_ground=None,
    filing_party=FilingPartyEnum.EMPLOYER,
    signature_party=SignaturePartyEnum.EMPLOYER,
)

office = OfficeDetails(
    target_office="Oficina de Extranjeria de Madrid",
    dir3_code="E04921901",
    province="Madrid",
)

signature = SignatureDetails(
    place="Madrid",
    day="06",
    month="04",
    year="2026",
    name="CARLOS MENDEZ",
)

form = EX03FormSchema(
    foreigner_details=foreigner,
    employer_details=employer,
    job_offer_details=job,
    filing_representative=representative,
    notification_address=notification,
    request_details=request,
    office=office,
    signature=signature,
)

output = fill_form_from_model(form, Path("forms/filled/EX03-domain-complete.pdf"))
print(f"Saved to: {output}")
