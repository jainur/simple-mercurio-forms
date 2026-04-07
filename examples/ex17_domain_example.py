"""EX17 domain model example."""

from datetime import date
from pathlib import Path

from fill_form import fill_form_from_model
from models.ex17 import (
    CardRequestTypeEnum,
    EX17FormSchema,
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
    first_surname="NAVARRO",
    second_surname="SOTO",
    name="PAULA",
    gender=GenderEnum.FEMALE,
    date_of_birth=date(1992, 11, 4),
    birth_place="Lima",
    birth_country="Peru",
    nationality="Peruana",
    father_name="CARLOS NAVARRO",
    mother_name="ANA SOTO",
    address="Calle Marina",
    address_number="8",
    floor_door="2A",
    city="Valencia",
    postal_code="46002",
    province="Valencia",
    mobile_phone="600222444",
    email="paula.navarro@example.com",
    legal_guardian_name=None,
    legal_guardian_id=None,
    legal_guardian_title=None,
    marital_status=MaritalStatusEnum.SINGLE,
)

representative = FilingRepresentativeDetails(
    name_or_company="GESTORIA LEVANTE SL",
    id_number="B11223344",
    address="Calle Colon",
    address_number="50",
    floor_door="3",
    city="Valencia",
    postal_code="46004",
    province="Valencia",
    mobile_phone="963112233",
    email="tramites@gestorialevante.es",
    legal_rep_name="MARTA RUIZ",
    legal_rep_id="55667788Q",
    legal_rep_title="Apoderada",
)

notification = NotificationAddress(
    name_or_company="GESTORIA LEVANTE SL",
    id_number="B11223344",
    address="Calle Colon",
    address_number="50",
    floor_door="3",
    city="Valencia",
    postal_code="46004",
    province="Valencia",
    mobile_phone="963112233",
    email="notificaciones@gestorialevante.es",
    consent_electronic_notifications=True,
)

request = RequestDetails(
    card_request_type=CardRequestTypeEnum.INITIAL_CARD,
)

signature = SignatureDetails(
    place="Valencia",
    day="06",
    month="04",
    year="2026",
    name="PAULA NAVARRO SOTO",
)

office = OfficeDetails(
    target_office="Oficina de Extranjeria de Valencia",
    dir3_code="E04922005",
    province="Valencia",
)

form = EX17FormSchema(
    foreigner_details=foreigner,
    filing_representative=representative,
    notification_address=notification,
    request_details=request,
    signature=signature,
    office=office,
)

output = fill_form_from_model(form, Path("forms/filled/EX17-domain-complete.pdf"))
print(f"Saved to: {output}")
