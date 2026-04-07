"""EX22 domain model example."""

from datetime import date
from pathlib import Path

from fill_form import fill_form_from_model
from models.ex22 import (
    ApplicantDetails,
    EmployerDetails,
    EX22FormSchema,
    FilingRepresentativeDetails,
    GenderEnum,
    MaritalStatusEnum,
    NotificationAddress,
    OfficeDetails,
    RequestCategoryEnum,
    RequestDetails,
    SignatureDetails,
    WorkModeEnum,
)

applicant = ApplicantDetails(
    passport="AB1234567",
    nie=None,
    first_surname="GOMEZ",
    second_surname="RUIZ",
    name="ELENA",
    date_of_birth=date(1992, 7, 21),
    birth_place="Quito",
    birth_country="Ecuador",
    nationality="Ecuatoriana",
    father_name="JORGE GOMEZ",
    mother_name="ANA RUIZ",
    mobile_phone="600555666",
    email="elena.gomez@example.com",
    legal_guardian_name=None,
    legal_guardian_id=None,
    legal_guardian_title=None,
    gender=GenderEnum.FEMALE,
    marital_status=MaritalStatusEnum.SINGLE,
)

employer = EmployerDetails(
    name_or_company="AGRO TEMPORAL SL",
    id_number="B44556677",
    activity="Agricultura",
    occupation="Peon agricola",
    address="Camino Rural 8",
    address_number="8",
    floor_door="",
    city="Murcia",
    postal_code="30001",
    province="Murcia",
)

representative = FilingRepresentativeDetails(
    name_or_company="GESTION MIGRA SL",
    id_number="B55667788",
    address="Gran Via",
    address_number="20",
    floor_door="4D",
    city="Madrid",
    postal_code="28013",
    province="Madrid",
    mobile_phone="910223344",
    email="tramites@gestionmigra.es",
    legal_rep_name="LAURA DIAZ",
    legal_rep_id="44556677P",
    legal_rep_title="Apoderada",
)

notification = NotificationAddress(
    name_or_company="GESTION MIGRA SL",
    id_number="B55667788",
    address="Gran Via",
    address_number="20",
    floor_door="4D",
    city="Madrid",
    postal_code="28013",
    province="Madrid",
    mobile_phone="910223344",
    email="notificaciones@gestionmigra.es",
    consent_electronic_notifications=True,
)

request = RequestDetails(
    category=RequestCategoryEnum.INITIAL,
    work_mode=WorkModeEnum.EMPLOYEE,
    modification_ground=None,
    identity_document_change_text="",
    cause_specification="",
    truth_statement_accepted=True,
)

office = OfficeDetails(
    target_office="Oficina de Extranjeria de Murcia",
    dir3_code="E04921902",
    province="Murcia",
)

signature = SignatureDetails(
    place="Murcia",
    day="06",
    month="04",
    year="2026",
    name="ELENA GOMEZ RUIZ",
)

form = EX22FormSchema(
    applicant_details=applicant,
    employer_details=employer,
    filing_representative=representative,
    notification_address=notification,
    request_details=request,
    office=office,
    signature=signature,
)

output = fill_form_from_model(form, Path("forms/filled/EX22-domain-complete.pdf"))
print(f"Saved to: {output}")
