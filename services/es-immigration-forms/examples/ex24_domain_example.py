"""EX24 domain model example."""

from datetime import date
from pathlib import Path

from fill_form import fill_form_from_model
from app.models.ex24 import (
    ApplicantDetails,
    EX24FormSchema,
    FilingRepresentativeDetails,
    GenderEnum,
    InitialRelationshipEnum,
    MaritalStatusEnum,
    NotificationAddress,
    OfficeDetails,
    RequestCategoryEnum,
    RequestDetails,
    SignatureDetails,
    SpanishNationalFamilyMemberDetails,
)

applicant = ApplicantDetails(
    passport="AB1234567",
    nie=None,
    first_surname="MORALES",
    second_surname="SUAREZ",
    name="LUCIA",
    date_of_birth=date(1991, 3, 18),
    birth_place="Lima",
    birth_country="Peru",
    nationality="Peruana",
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
    legal_guardian_name=None,
    legal_guardian_id=None,
    legal_guardian_title=None,
    gender=GenderEnum.FEMALE,
    marital_status=MaritalStatusEnum.SINGLE,
)

spanish_family = SpanishNationalFamilyMemberDetails(
    passport="CD7654321",
    dni="12345678Z",
    title="DNI",
    first_surname="GARCIA",
    second_surname="LOPEZ",
    name="MARIA",
    date_of_birth=date(1988, 5, 10),
    birth_country="España",
    father_name="JOSE GARCIA",
    mother_name="ELENA LOPEZ",
    address="Calle Alcala",
    address_number="40",
    floor_door="3A",
    city="Madrid",
    postal_code="28014",
    province="Madrid",
    relationship_with_applicant="Conyuge",
    gender=GenderEnum.FEMALE,
    marital_status=MaritalStatusEnum.MARRIED,
)

representative = FilingRepresentativeDetails(
    name_or_company="GESTORIA AUTORIZA SL",
    id_number="B22334455",
    address="Gran Via",
    address_number="12",
    floor_door="5",
    city="Madrid",
    postal_code="28013",
    province="Madrid",
    mobile_phone="910554433",
    email="tramites@gestoriaautoriza.es",
    legal_rep_name="MARTA ORTEGA",
    legal_rep_id="33445566R",
    legal_rep_title="Apoderada",
)

notification = NotificationAddress(
    name_or_company="GESTORIA AUTORIZA SL",
    id_number="B22334455",
    address="Gran Via",
    address_number="12",
    floor_door="5",
    city="Madrid",
    postal_code="28013",
    province="Madrid",
    mobile_phone="910554433",
    email="notificaciones@gestoriaautoriza.es",
    consent_electronic_notifications=True,
)

request = RequestDetails(
    category=RequestCategoryEnum.INITIAL_RESIDENCE,
    initial_relationship=InitialRelationshipEnum.SPOUSE_OR_REGISTERED_OR_STABLE_PARTNER,
    preservation_ground=None,
)

signature = SignatureDetails(
    place="Madrid",
    day="06",
    month="04",
    year="2026",
    name="LUCIA MORALES SUAREZ",
)

office = OfficeDetails(
    target_office="Oficina de Extranjeria de Madrid",
    dir3_code="E04921901",
    province="Madrid",
)

form = EX24FormSchema(
    applicant_details=applicant,
    spanish_family_member_details=spanish_family,
    filing_representative=representative,
    notification_address=notification,
    request_details=request,
    signature=signature,
    office=office,
)

output = fill_form_from_model(form, Path("forms/filled/EX24-domain-complete.pdf"))
print(f"Saved to: {output}")
