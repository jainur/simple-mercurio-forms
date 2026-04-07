"""EX19 domain model example."""

from datetime import date
from pathlib import Path

from fill_form import fill_form_from_model
from models.ex19 import (
    ApplicantDetails,
    EX19FormSchema,
    EuCitizenDetails,
    FamilyRelationshipEnum,
    FilingRepresentativeDetails,
    GenderEnum,
    MaritalStatusEnum,
    NotificationAddress,
    OfficeDetails,
    RequestDetails,
    ResidenceRequestTypeEnum,
    SignatureDetails,
)

applicant = ApplicantDetails(
    passport="AB1234567",
    nie=None,
    first_surname="SANCHEZ",
    second_surname="LOPEZ",
    name="MARIA",
    gender=GenderEnum.FEMALE,
    date_of_birth=date(1994, 2, 11),
    birth_place="Quito",
    birth_country="Ecuador",
    nationality="Ecuatoriana",
    father_name="CARLOS SANCHEZ",
    mother_name="ANA LOPEZ",
    address="Calle Mayor",
    address_number="18",
    floor_door="2B",
    city="Madrid",
    postal_code="28013",
    province="Madrid",
    mobile_phone="600444555",
    email="maria.sanchez@example.com",
    legal_guardian_name=None,
    legal_guardian_id=None,
    legal_guardian_title=None,
    marital_status=MaritalStatusEnum.MARRIED,
)

eu_citizen = EuCitizenDetails(
    passport="CD7654321",
    nie=None,
    first_surname="PEREZ",
    second_surname="GARCIA",
    name="JUAN",
    nationality="Espanola",
    address="Calle Mayor",
    address_number="18",
    floor_door="2B",
    city="Madrid",
    postal_code="28013",
    province="Madrid",
)

representative = FilingRepresentativeDetails(
    name_or_company="GESTORIA UNION SL",
    id_number="B88990011",
    address="Gran Via",
    address_number="44",
    floor_door="5",
    city="Madrid",
    postal_code="28013",
    province="Madrid",
    mobile_phone="910223355",
    email="tramites@gestoriaunion.es",
    legal_rep_name="LAURA GOMEZ",
    legal_rep_id="55667788T",
    legal_rep_title="Apoderada",
)

notification = NotificationAddress(
    name_or_company="GESTORIA UNION SL",
    id_number="B88990011",
    address="Gran Via",
    address_number="44",
    floor_door="5",
    city="Madrid",
    postal_code="28013",
    province="Madrid",
    mobile_phone="910223355",
    email="notificaciones@gestoriaunion.es",
    consent_electronic_notifications=True,
)

request = RequestDetails(
    request_type=ResidenceRequestTypeEnum.TEMPORARY_INITIAL,
    family_relationship=FamilyRelationshipEnum.SPOUSE,
    maintain_right_ground=None,
    truth_statement_accepted=True,
)

signature = SignatureDetails(
    place="Madrid",
    day="06",
    month="04",
    year="2026",
    eu_citizen_signature_name="JUAN PEREZ GARCIA",
    applicant_signature_name="MARIA SANCHEZ LOPEZ",
)

office = OfficeDetails(
    target_office="Oficina de Extranjeria de Madrid",
    dir3_code="E04921901",
    province="Madrid",
)

form = EX19FormSchema(
    applicant_details=applicant,
    eu_citizen_details=eu_citizen,
    filing_representative=representative,
    notification_address=notification,
    request_details=request,
    signature=signature,
    office=office,
)

output = fill_form_from_model(form, Path("forms/filled/EX19-domain-complete.pdf"))
print(f"Saved to: {output}")
