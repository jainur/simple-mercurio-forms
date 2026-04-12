"""EX02 domain model example."""

from datetime import date
from pathlib import Path

from fill_form import fill_form_from_model
from app.models.ex02 import (
    ApplicantDetails,
    AuthorizationTypeEnum,
    EX02FormSchema,
    FamilyRelationshipEnum,
    GenderEnum,
    MaritalStatusEnum,
    NotificationAddress,
    OfficeDetails,
    PresenterDetails,
    RequestDetails,
    SignatureDetails,
    SponsorDetails,
)

applicant = ApplicantDetails(
    passport="AB1234567",
    nie=None,
    first_surname="PEREZ",
    second_surname="LOPEZ",
    name="LAURA",
    gender=GenderEnum.FEMALE,
    date_of_birth=date(1992, 8, 14),
    birth_place="Bogota",
    birth_country="Colombia",
    nationality="Colombiana",
    father_name="JORGE PEREZ",
    mother_name="MARTA LOPEZ",
    address="Calle Mayor",
    address_number="10",
    floor_door="2B",
    city="Madrid",
    postal_code="28013",
    province="Madrid",
    mobile_phone="600111222",
    email="laura.perez@example.com",
    marital_status=MaritalStatusEnum.MARRIED,
    children_in_school_age=True,
    current_authorization="Residencia temporal",
    current_authorization_document="Y1234567X",
    current_authorization_title="Tarjeta de residencia",
    legal_guardian_name=None,
    legal_guardian_id=None,
    legal_guardian_title=None,
)

sponsor = SponsorDetails(
    passport="CD7654321",
    nie="X-1234567-L",
    first_surname="PEREZ",
    second_surname="GOMEZ",
    name="CARLOS",
    gender=GenderEnum.MALE,
    date_of_birth=date(1987, 5, 5),
    birth_place="Madrid",
    birth_country="Espana",
    nationality="Espanola",
    father_name="JOSE PEREZ",
    mother_name="ELENA GOMEZ",
    address="Avenida de America",
    address_number="25",
    floor_door="1A",
    city="Madrid",
    postal_code="28002",
    province="Madrid",
    marital_status=MaritalStatusEnum.MARRIED,
)

presenter = PresenterDetails(
    name_or_company="GESTORIA CENTRAL SL",
    id_number="B12345678",
    address="Paseo de la Castellana",
    address_number="80",
    floor_door="3",
    city="Madrid",
    postal_code="28046",
    province="Madrid",
    mobile_phone="911234567",
    email="tramites@gestoriacentral.es",
    legal_rep_name="ANA TORRES",
    legal_rep_id="12345678Z",
    legal_rep_title="Administradora",
)

notification = NotificationAddress(
    name_or_company="GESTORIA CENTRAL SL",
    id_number="B12345678",
    address="Paseo de la Castellana",
    address_number="80",
    floor_door="3",
    city="Madrid",
    postal_code="28046",
    province="Madrid",
    mobile_phone="911234567",
    email="notificaciones@gestoriacentral.es",
    consent_electronic_notifications=True,
)

request = RequestDetails(
    family_relationship=FamilyRelationshipEnum.SPOUSE,
    authorization_type=AuthorizationTypeEnum.INITIAL_ART_65,
    request_independent_residence=False,
    independent_residence_reason=None,
    request_ascendant_work_authorization=False,
    work_mode=None,
    simultaneous_other_family_reunification_requests=False,
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
    name="LAURA PEREZ LOPEZ",
)

form = EX02FormSchema(
    applicant_details=applicant,
    sponsor_details=sponsor,
    presenter_details=presenter,
    notification_address=notification,
    request_details=request,
    office=office,
    signature=signature,
)

output = fill_form_from_model(form, Path("forms/filled/EX02-domain-complete.pdf"))
print(f"Saved to: {output}")
