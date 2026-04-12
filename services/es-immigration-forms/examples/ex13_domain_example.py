"""EX13 domain model example."""

from datetime import date
from pathlib import Path

from fill_form import fill_form_from_model
from app.models.ex13 import (
    EX13FormSchema,
    FilingRepresentativeDetails,
    ForeignerDetails,
    GenderEnum,
    MaritalStatusEnum,
    NotificationAddress,
    OfficeDetails,
    RequestDetails,
    ReturnAuthorizationGroundEnum,
    SignatureDetails,
)

foreigner = ForeignerDetails(
    passport="AB1234567",
    nie=None,
    first_surname="ORTEGA",
    second_surname="DIAZ",
    name="PAULA",
    gender=GenderEnum.FEMALE,
    date_of_birth=date(1994, 6, 21),
    birth_place="Quito",
    birth_country="Ecuador",
    nationality="Ecuatoriana",
    father_name="CARLOS ORTEGA",
    mother_name="LUCIA DIAZ",
    address="Calle del Sol",
    address_number="12",
    floor_door="2A",
    city="Sevilla",
    postal_code="41001",
    province="Sevilla",
    mobile_phone="600778899",
    email="paula.ortega@example.com",
    legal_guardian_name=None,
    legal_guardian_id=None,
    legal_guardian_title=None,
    marital_status=MaritalStatusEnum.SINGLE,
)

representative = FilingRepresentativeDetails(
    name_or_company="GESTORIA SUR SL",
    id_number="B55667788",
    address="Avenida de la Constitucion",
    address_number="33",
    floor_door="1",
    city="Sevilla",
    postal_code="41004",
    province="Sevilla",
    mobile_phone="954112233",
    email="tramites@gestoriasur.es",
    legal_rep_name="MARTA VEGA",
    legal_rep_id="44556677T",
    legal_rep_title="Apoderada",
)

notification = NotificationAddress(
    name_or_company="GESTORIA SUR SL",
    id_number="B55667788",
    address="Avenida de la Constitucion",
    address_number="33",
    floor_door="1",
    city="Sevilla",
    postal_code="41004",
    province="Sevilla",
    mobile_phone="954112233",
    email="notificaciones@gestoriasur.es",
    consent_electronic_notifications=True,
)

request = RequestDetails(
    ground=ReturnAuthorizationGroundEnum.RESIDENCE_RENEWAL_OR_EXTENSION_ART_5,
    other_reason_text_1=None,
    other_reason_text_2=None,
    other_reason_text_3=None,
)

signature = SignatureDetails(
    place="Sevilla",
    day="06",
    month="04",
    year="2026",
    name="PAULA ORTEGA DIAZ",
)

office = OfficeDetails(
    target_office="Oficina de Extranjeria de Sevilla",
    dir3_code="E04921903",
    province="Sevilla",
)

form = EX13FormSchema(
    foreigner_details=foreigner,
    filing_representative=representative,
    notification_address=notification,
    request_details=request,
    signature=signature,
    office=office,
)

output = fill_form_from_model(form, Path("forms/filled/EX13-domain-complete.pdf"))
print(f"Saved to: {output}")
