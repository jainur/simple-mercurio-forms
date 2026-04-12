"""EX06 domain model example."""

from datetime import date
from pathlib import Path

from fill_form import fill_form_from_model
from app.models.ex06 import (
    ApplicationTypeEnum,
    EX06FormSchema,
    EmployerDetails,
    FilingRepresentativeDetails,
    ForeignerDetails,
    GenderEnum,
    MaritalStatusEnum,
    NotificationAddress,
    OfficeDetails,
    RequestDetails,
    SignatureDetails,
)

foreigner = ForeignerDetails(
    passport="AB1234567",
    nie=None,
    first_surname="GOMEZ",
    second_surname="RUIZ",
    name="ELENA",
    gender=GenderEnum.FEMALE,
    date_of_birth=date(1994, 7, 21),
    birth_place="Quito",
    birth_country="Ecuador",
    nationality="Ecuatoriana",
    marital_status=MaritalStatusEnum.SINGLE,
    father_name="JORGE GOMEZ",
    mother_name="ANA RUIZ",
    address="Calle Embajadores",
    address_number="45",
    floor_door="2C",
    city="Madrid",
    postal_code="28012",
    province="Madrid",
    mobile_phone="600555666",
    email="elena.gomez@example.com",
    legal_guardian_name=None,
    legal_guardian_id=None,
    legal_guardian_title=None,
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
    mobile_phone="968123456",
    email="rrhh@agrotemporal.es",
    legal_rep_name="PABLO SERRANO",
    legal_rep_id="33445566M",
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
    application_type=ApplicationTypeEnum.RESIDENCIA_INICIAL,
    accepts_truth_responsibility=True,
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
    name="PABLO SERRANO",
)

form = EX06FormSchema(
    foreigner_details=foreigner,
    employer_details=employer,
    filing_representative=representative,
    notification_address=notification,
    request_details=request,
    office=office,
    signature=signature,
)

output = fill_form_from_model(form, Path("forms/filled/EX06-domain-complete.pdf"))
print(f"Saved to: {output}")
