"""EX09 domain model example."""

from datetime import date
from pathlib import Path

from fill_form import fill_form_from_model
from models.ex09 import (
    ActivityEntityDetails,
    ApplicationCategoryEnum,
    EX09FormSchema,
    FilingRepresentativeDetails,
    ForeignerDetails,
    GenderEnum,
    InitialExceptionSubtypeEnum,
    MaritalStatusEnum,
    NotificationAddress,
    OfficeDetails,
    RequestDetails,
    SignatureDetails,
)

foreigner = ForeignerDetails(
    passport="AB1234567",
    nie=None,
    first_surname="LOPEZ",
    second_surname="MARTIN",
    name="SARA",
    gender=GenderEnum.FEMALE,
    date_of_birth=date(1990, 10, 3),
    birth_place="Bogota",
    birth_country="Colombia",
    nationality="Colombiana",
    father_name="CARLOS LOPEZ",
    mother_name="ANA MARTIN",
    address="Calle Mayor",
    address_number="20",
    floor_door="3B",
    city="Valencia",
    postal_code="46001",
    province="Valencia",
    mobile_phone="600998877",
    email="sara.lopez@example.com",
    marital_status=MaritalStatusEnum.SINGLE,
    children_in_school_age=False,
)

activity_entity = ActivityEntityDetails(
    name_or_company="COMUNIDAD RELIGIOSA SAN JUAN",
    id_number="R1234567A",
    activity="Actividad religiosa",
    occupation="Misionera",
    address="Avenida del Cid",
    address_number="12",
    floor_door="1",
    city="Valencia",
    postal_code="46018",
    province="Valencia",
    mobile_phone="961223344",
    email="administracion@sanjuan.es",
    legal_rep_name="MIGUEL ORTEGA",
    legal_rep_id="22334455L",
    legal_rep_title="Superior",
)

representative = FilingRepresentativeDetails(
    name_or_company="GESTORIA LEYEX SL",
    id_number="B33445566",
    address="Calle Colon",
    address_number="50",
    floor_door="4",
    city="Valencia",
    postal_code="46004",
    province="Valencia",
    mobile_phone="963334455",
    email="tramites@leyex.es",
    legal_rep_name="LAURA GIL",
    legal_rep_id="33445566P",
    legal_rep_title="Apoderada",
)

notification = NotificationAddress(
    name_or_company="GESTORIA LEYEX SL",
    id_number="B33445566",
    address="Calle Colon",
    address_number="50",
    floor_door="4",
    city="Valencia",
    postal_code="46004",
    province="Valencia",
    mobile_phone="963334455",
    email="notificaciones@leyex.es",
    consent_electronic_notifications=True,
)

request = RequestDetails(
    category=ApplicationCategoryEnum.INITIAL_EXCEPTION,
    initial_subtype=InitialExceptionSubtypeEnum.RELIGIOUS_MEMBER,
    other_initial_exception_details=None,
)

office = OfficeDetails(
    target_office="Oficina de Extranjeria de Valencia",
    dir3_code="E04922005",
    province="Valencia",
)

signature = SignatureDetails(
    place="Valencia",
    day="06",
    month="04",
    year="2026",
    name="MIGUEL ORTEGA",
)

form = EX09FormSchema(
    foreigner_details=foreigner,
    activity_entity_details=activity_entity,
    filing_representative=representative,
    notification_address=notification,
    request_details=request,
    office=office,
    signature=signature,
)

output = fill_form_from_model(form, Path("forms/filled/EX09-domain-complete.pdf"))
print(f"Saved to: {output}")
