"""EX23 domain model example."""

from datetime import date
from pathlib import Path

from fill_form import fill_form_from_model
from models.ex23 import (
    ApplicantDetails,
    EX23FormSchema,
    FilingRepresentativeDetails,
    GenderEnum,
    MaritalStatusEnum,
    NotificationAddress,
    OfficeDetails,
    RequestDetails,
    ResidenceStatusEnum,
    SignatureDetails,
)

applicant = ApplicantDetails(
    passport="AB1234567",
    nie=None,
    first_surname="THOMAS",
    second_surname="BROWN",
    name="EMMA",
    date_of_birth=date(1991, 8, 14),
    birth_place="London",
    birth_country="United Kingdom",
    nationality="British",
    father_name="JOHN THOMAS",
    mother_name="ANNA BROWN",
    address="Calle Mayor",
    address_number="20",
    floor_door="3A",
    city="Madrid",
    postal_code="28013",
    province="Madrid",
    mobile_phone="600999111",
    email="emma.thomas@example.com",
    legal_guardian_name=None,
    legal_guardian_id=None,
    legal_guardian_title=None,
    gender=GenderEnum.FEMALE,
    marital_status=MaritalStatusEnum.SINGLE,
)

representative = FilingRepresentativeDetails(
    name_or_company="GESTORIA BREXIT MADRID SL",
    id_number="B22334455",
    address="Gran Via",
    address_number="40",
    floor_door="5",
    city="Madrid",
    postal_code="28013",
    province="Madrid",
    mobile_phone="910112233",
    email="tramites@gestoriabrexitmadrid.es",
    legal_rep_name="LAURA TORRES",
    legal_rep_id="44556677R",
    legal_rep_title="Apoderada",
)

notification = NotificationAddress(
    name_or_company="GESTORIA BREXIT MADRID SL",
    id_number="B22334455",
    address="Gran Via",
    address_number="40",
    floor_door="5",
    city="Madrid",
    postal_code="28013",
    province="Madrid",
    mobile_phone="910112233",
    email="notificaciones@gestoriabrexitmadrid.es",
    consent_electronic_notifications=True,
)

request = RequestDetails(
    residence_status=ResidenceStatusEnum.INITIAL_WITHOUT_PREVIOUS_REGISTRATION,
    other_status_text=None,
    additional_eu_registration_option=None,
)

signature = SignatureDetails(
    place="Madrid",
    day="06",
    month="04",
    year="2026",
    name="EMMA THOMAS BROWN",
)

office = OfficeDetails(
    target_office="Oficina de Extranjeria de Madrid",
    dir3_code="E04921901",
    province="Madrid",
)

form = EX23FormSchema(
    applicant_details=applicant,
    filing_representative=representative,
    notification_address=notification,
    request_details=request,
    signature=signature,
    office=office,
)

output = fill_form_from_model(form, Path("forms/filled/EX23-domain-complete.pdf"))
print(f"Saved to: {output}")
