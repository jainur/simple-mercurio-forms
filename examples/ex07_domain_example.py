"""EX07 domain model example."""

from datetime import date
from pathlib import Path

from fill_form import fill_form_from_model
from models.ex07 import (
    ApplicationCategoryEnum,
    EX07FormSchema,
    FilingRepresentativeDetails,
    ForeignerDetails,
    GenderEnum,
    InitialGroundEnum,
    MaritalStatusEnum,
    NotificationAddress,
    OfficeDetails,
    RequestDetails,
    SelfEmploymentDetails,
    SignatureDetails,
    SignerRoleEnum,
)

foreigner = ForeignerDetails(
    passport="AB1234567",
    nie=None,
    first_surname="MORALES",
    second_surname="SUAREZ",
    name="LUCIA",
    gender=GenderEnum.FEMALE,
    date_of_birth=date(1991, 3, 18),
    birth_place="Lima",
    birth_country="Peru",
    nationality="Peruana",
    marital_status=MaritalStatusEnum.SINGLE,
    father_name="JORGE MORALES",
    mother_name="ANA SUAREZ",
    address="Calle Alcala",
    address_number="40",
    floor_door="3A",
    city="Madrid",
    postal_code="28014",
    province="Madrid",
    mobile_phone="600112233",
    email="lucia.morales@example.com",
    children_in_school_age=False,
    legal_guardian_name=None,
    legal_guardian_id=None,
    legal_guardian_title=None,
)

self_employment = SelfEmploymentDetails(
    name_or_company="LUCIA MORALES",
    id_number="Y1234567K",
    activity="Servicios de diseno grafico",
    cnae_code="7410",
    address="Calle Alcala",
    address_number="40",
    floor_door="3A",
    city="Madrid",
    postal_code="28014",
    province="Madrid",
    mobile_phone="600112233",
    email="lucia.morales@example.com",
)

representative = FilingRepresentativeDetails(
    name_or_company="GESTORIA AUTONOMOS SL",
    id_number="B22334455",
    address="Gran Via",
    address_number="12",
    floor_door="5",
    city="Madrid",
    postal_code="28013",
    province="Madrid",
    mobile_phone="910554433",
    email="tramites@gestoria-autonomos.es",
    legal_rep_name="MARTA ORTEGA",
    legal_rep_id="33445566R",
    legal_rep_title="Apoderada",
)

notification = NotificationAddress(
    name_or_company="GESTORIA AUTONOMOS SL",
    id_number="B22334455",
    address="Gran Via",
    address_number="12",
    floor_door="5",
    city="Madrid",
    postal_code="28013",
    province="Madrid",
    mobile_phone="910554433",
    email="notificaciones@gestoria-autonomos.es",
    consent_electronic_notifications=True,
)

request = RequestDetails(
    category=ApplicationCategoryEnum.INITIAL,
    initial_ground=InitialGroundEnum.GENERAL_RESIDENT_OUTSIDE_SPAIN_ART_85,
    renewal_ground=None,
    territorial_scope_ground=None,
    signer_role=SignerRoleEnum.REPRESENTATIVE,
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
    name="MARTA ORTEGA",
)

form = EX07FormSchema(
    foreigner_details=foreigner,
    self_employment_details=self_employment,
    filing_representative=representative,
    notification_address=notification,
    request_details=request,
    office=office,
    signature=signature,
)

output = fill_form_from_model(form, Path("forms/filled/EX07-domain-complete.pdf"))
print(f"Saved to: {output}")
