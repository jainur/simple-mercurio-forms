"""EX21 domain model example."""

from datetime import date
from pathlib import Path

from fill_form import fill_form_from_model
from models.ex21 import (
    ApplicantDetails,
    BritishNationalDetails,
    EX21FormSchema,
    FamilyRelationshipEnum,
    FilingRepresentativeDetails,
    GenderEnum,
    MainRequestCategoryEnum,
    MaritalStatusEnum,
    NotificationAddress,
    OfficeDetails,
    RequestDetails,
    SignatureDetails,
)

applicant = ApplicantDetails(
    passport="AB1234567",
    nie=None,
    first_surname="LOPEZ",
    second_surname="GARCIA",
    name="MARTA",
    gender=GenderEnum.FEMALE,
    marital_status=MaritalStatusEnum.MARRIED,
    date_of_birth=date(1993, 6, 15),
    birth_place="Sevilla",
    nationality="Española",
    birth_country="España",
    father_name="JUAN LOPEZ",
    mother_name="ANA GARCIA",
    address="Calle Alcala",
    address_number="18",
    floor_door="2B",
    postal_code="28014",
    city="Madrid",
    mobile_phone="600111444",
    email="marta.lopez@example.com",
    legal_guardian_name=None,
    province="Madrid",
    legal_guardian_id=None,
    legal_guardian_title=None,
)

british = BritishNationalDetails(
    passport="CD7654321",
    nie="Y1234567Z",
    first_surname="BROWN",
    second_surname="SMITH",
    name="JAMES",
    address="Calle Alcala",
    city="Madrid",
    postal_code="28014",
    relationship_with_applicant="Conyuge",
    nationality="Británica",
    address_number="18",
    floor_door="2B",
    province="Madrid",
)

representative = FilingRepresentativeDetails(
    name_or_company="GESTORIA GLOBAL SL",
    address="Gran Via",
    city="Madrid",
    province="Madrid",
    postal_code="28013",
    mobile_phone="910223344",
    email="tramites@gestoriaglobal.es",
    legal_rep_name="LAURA TORRES",
    legal_rep_id="55667788R",
    legal_rep_title="Apoderada",
    id_number="B33445566",
    address_number="50",
    floor_door="4",
)

notification = NotificationAddress(
    name_or_company="GESTORIA GLOBAL SL",
    id_number="B33445566",
    address="Gran Via",
    address_number="50",
    floor_door="4",
    city="Madrid",
    postal_code="28013",
    province="Madrid",
    email="notificaciones@gestoriaglobal.es",
    mobile_phone="910223344",
    consent_electronic_notifications=True,
)

request = RequestDetails(
    residence_start_day="01",
    residence_start_month="01",
    residence_start_year="2021",
    continuous_5_years_text="",
    identity_document_change_text="",
    cause_specification="",
    category=MainRequestCategoryEnum.TEMPORARY_RESIDENCE,
    family_relationship=FamilyRelationshipEnum.SPOUSE,
    permanent_ground=None,
    modification_ground=None,
    renewal_subtype=None,
    deregistration_cause_present=False,
    truth_statement_accepted=True,
)

signature = SignatureDetails(
    place="Madrid",
    day="06",
    month="04",
    year="2026",
    british_national_signature_name="JAMES BROWN SMITH",
    applicant_signature_name="MARTA LOPEZ GARCIA",
)

office = OfficeDetails(
    target_office="Oficina de Extranjeria de Madrid",
    dir3_code="E04921901",
    province="Madrid",
)

form = EX21FormSchema(
    applicant_details=applicant,
    british_national_details=british,
    filing_representative=representative,
    notification_address=notification,
    request_details=request,
    signature=signature,
    office=office,
)

output = fill_form_from_model(form, Path("forms/filled/EX21-domain-complete.pdf"))
print(f"Saved to: {output}")
