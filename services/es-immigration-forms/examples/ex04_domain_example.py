"""EX04 domain model example."""

from datetime import date
from pathlib import Path

from fill_form import fill_form_from_model
from app.models.ex04 import (
    ApplicationCategoryEnum,
    EX04FormSchema,
    FamilyAuthorizationPhaseEnum,
    FilingRepresentativeDetails,
    ForeignerDetails,
    GenderEnum,
    HostEntityDetails,
    InitialLocationEnum,
    MaritalStatusEnum,
    NotificationAddress,
    OfficeDetails,
    PracticeBasisEnum,
    RequestDetails,
    SignatureDetails,
)

foreigner = ForeignerDetails(
    passport="AB1234567",
    nie=None,
    first_surname="RAMIREZ",
    second_surname="LOPEZ",
    name="PAULA",
    gender=GenderEnum.FEMALE,
    date_of_birth=date(1998, 2, 10),
    birth_place="Santiago",
    birth_country="Chile",
    nationality="Chilena",
    father_name="JUAN RAMIREZ",
    mother_name="ANA LOPEZ",
    address="Calle Toledo",
    address_number="22",
    floor_door="1B",
    city="Madrid",
    postal_code="28005",
    province="Madrid",
    mobile_phone="600222333",
    email="paula.ramirez@example.com",
    marital_status=MaritalStatusEnum.SINGLE,
    legal_guardian_name=None,
    legal_guardian_id=None,
    legal_guardian_title=None,
)

host_entity = HostEntityDetails(
    name_or_company="INNOVA TECH SL",
    id_number="B33445566",
    activity="Desarrollo de software",
    occupation="Desarrolladora en practicas",
    address="Avenida Europa",
    address_number="14",
    floor_door="3",
    city="Madrid",
    postal_code="28023",
    province="Madrid",
    mobile_phone="911223344",
    email="rrhh@innovatech.es",
    legal_rep_name="CARLOS VEGA",
    legal_rep_id="12345678Z",
    legal_rep_title="Administrador",
)

representative = FilingRepresentativeDetails(
    name_or_company="GESTORIA GLOBAL SA",
    id_number="A99887766",
    address="Paseo Castellana",
    address_number="210",
    floor_door="7",
    city="Madrid",
    postal_code="28046",
    province="Madrid",
    mobile_phone="912334455",
    email="tramites@gestoriaglobal.es",
    legal_rep_name="LAURA TORRES",
    legal_rep_id="23456789X",
    legal_rep_title="Apoderada",
)

notification = NotificationAddress(
    name_or_company="GESTORIA GLOBAL SA",
    id_number="A99887766",
    address="Paseo Castellana",
    address_number="210",
    floor_door="7",
    city="Madrid",
    postal_code="28046",
    province="Madrid",
    mobile_phone="912334455",
    email="notificaciones@gestoriaglobal.es",
    consent_electronic_notifications=True,
)

request = RequestDetails(
    category=ApplicationCategoryEnum.INITIAL,
    initial_location=InitialLocationEnum.OUTSIDE_SPAIN,
    initial_basis=PracticeBasisEnum.EMPLOYMENT_CONTRACT,
    renewal_basis=None,
    family_phase=FamilyAuthorizationPhaseEnum.INITIAL,
    is_host_entity_legal_representative_signing=True,
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
    name="CARLOS VEGA",
)

form = EX04FormSchema(
    foreigner_details=foreigner,
    host_entity_details=host_entity,
    filing_representative=representative,
    notification_address=notification,
    request_details=request,
    office=office,
    signature=signature,
)

output = fill_form_from_model(form, Path("forms/filled/EX04-domain-complete.pdf"))
print(f"Saved to: {output}")
