"""EX11 domain model example."""

from datetime import date
from pathlib import Path

from fill_form import fill_form_from_model
from models.ex11 import (
    AuthorizationFamilyEnum,
    EX11FormSchema,
    FilingRepresentativeDetails,
    ForeignerDetails,
    GenderEnum,
    LdSubtypeEnum,
    MaritalStatusEnum,
    NotificationAddress,
    OfficeDetails,
    RequestDetails,
    SignatureDetails,
)

foreigner = ForeignerDetails(
    passport="AB1234567",
    nie=None,
    first_surname="GARCIA",
    second_surname="LOPEZ",
    name="ANA",
    gender=GenderEnum.FEMALE,
    date_of_birth=date(1988, 4, 16),
    birth_place="Quito",
    birth_country="Ecuador",
    nationality="Ecuatoriana",
    father_name="CARLOS GARCIA",
    mother_name="MARTA LOPEZ",
    address="Calle Serrano",
    address_number="45",
    floor_door="2A",
    city="Madrid",
    postal_code="28001",
    province="Madrid",
    mobile_phone="600111999",
    email="ana.garcia@example.com",
    legal_guardian_name=None,
    legal_guardian_id=None,
    legal_guardian_title=None,
    marital_status=MaritalStatusEnum.SINGLE,
    children_in_school_age=False,
)

representative = FilingRepresentativeDetails(
    name_or_company="GESTORIA INTEGRAL SL",
    id_number="B22446688",
    address="Paseo de la Castellana",
    address_number="100",
    floor_door="5",
    city="Madrid",
    postal_code="28046",
    province="Madrid",
    mobile_phone="911223344",
    email="tramites@gestoriaintegral.es",
    legal_rep_name="LAURA RAMOS",
    legal_rep_id="11223344Z",
    legal_rep_title="Apoderada",
)

notification = NotificationAddress(
    name_or_company="GESTORIA INTEGRAL SL",
    id_number="B22446688",
    address="Paseo de la Castellana",
    address_number="100",
    floor_door="5",
    city="Madrid",
    postal_code="28046",
    province="Madrid",
    mobile_phone="911223344",
    email="notificaciones@gestoriaintegral.es",
    consent_electronic_notifications=True,
)

request = RequestDetails(
    authorization_family=AuthorizationFamilyEnum.RESIDENCIA_LARGA_DURACION,
    ld_subtype=LdSubtypeEnum.GENERAL_5_YEARS_ART_183_1,
    ld_ue_subtype=None,
)

signature = SignatureDetails(
    place="Madrid",
    day="06",
    month="04",
    year="2026",
    name="ANA GARCIA LOPEZ",
)

office = OfficeDetails(
    target_office="Oficina de Extranjeria de Madrid",
    dir3_code="E04921901",
    province="Madrid",
)

form = EX11FormSchema(
    foreigner_details=foreigner,
    filing_representative=representative,
    notification_address=notification,
    request_details=request,
    signature=signature,
    office=office,
)

output = fill_form_from_model(form, Path("forms/filled/EX11-domain-complete.pdf"))
print(f"Saved to: {output}")
