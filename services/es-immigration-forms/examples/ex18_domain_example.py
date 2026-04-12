"""EX18 domain model example."""

from datetime import date
from pathlib import Path

from fill_form import fill_form_from_model
from app.models.ex18 import (
    EX18FormSchema,
    FilingRepresentativeDetails,
    ForeignerDetails,
    GenderEnum,
    MainRequestCategoryEnum,
    MaritalStatusEnum,
    NotificationAddress,
    OfficeDetails,
    RequestDetails,
    SignatureDetails,
    TemporaryResidenceGroundEnum,
)

foreigner = ForeignerDetails(
    passport="AB1234567",
    nie=None,
    first_surname="MARTIN",
    second_surname="GARCIA",
    name="ELENA",
    gender=GenderEnum.FEMALE,
    date_of_birth=date(1991, 7, 14),
    birth_place="Buenos Aires",
    birth_country="Argentina",
    nationality="Argentina",
    father_name="JUAN MARTIN",
    mother_name="ANA GARCIA",
    address="Calle Diputacion",
    address_number="15",
    floor_door="2B",
    city="Barcelona",
    postal_code="08015",
    province="Barcelona",
    mobile_phone="600111555",
    email="elena.martin@example.com",
    legal_guardian_name=None,
    legal_guardian_id=None,
    legal_guardian_title=None,
    marital_status=MaritalStatusEnum.SINGLE,
)

representative = FilingRepresentativeDetails(
    name_or_company="GESTORIA EUROPA SL",
    id_number="B77889900",
    address="Passeig de Gracia",
    address_number="90",
    floor_door="4",
    city="Barcelona",
    postal_code="08008",
    province="Barcelona",
    mobile_phone="931234567",
    email="tramites@gestoriaeuropa.es",
    legal_rep_name="MARTA RUIZ",
    legal_rep_id="44556677L",
    legal_rep_title="Apoderada",
)

notification = NotificationAddress(
    name_or_company="GESTORIA EUROPA SL",
    id_number="B77889900",
    address="Passeig de Gracia",
    address_number="90",
    floor_door="4",
    city="Barcelona",
    postal_code="08008",
    province="Barcelona",
    mobile_phone="931234567",
    email="notificaciones@gestoriaeuropa.es",
    consent_electronic_notifications=True,
)

request = RequestDetails(
    expected_residence_period="5 anos",
    residence_start_day="01",
    residence_start_month="05",
    residence_start_year="2026",
    residence_start_location="Barcelona",
    eu_citizen_document_id="X1234567L",
    relationship_with_eu_citizen="Conyuge",
    incapacity_with_spanish_spouse_text="",
    identity_document_change_text="",
    cause_specification="",
    category=MainRequestCategoryEnum.TEMPORARY_RESIDENCE,
    temporary_ground=TemporaryResidenceGroundEnum.EMPLOYEE,
    permanent_ground=None,
    permanent_other_text=None,
    modification_ground=None,
    modification_other_text=None,
    deregistration_cause=None,
    truth_statement_accepted=True,
)

signature = SignatureDetails(
    place="Barcelona",
    day="06",
    month="04",
    year="2026",
    eu_citizen_signature_name="JUAN PEREZ",
    applicant_signature_name="ELENA MARTIN GARCIA",
)

office = OfficeDetails(
    target_office="Oficina de Extranjeria de Barcelona",
    dir3_code="E04922001",
    province="Barcelona",
)

form = EX18FormSchema(
    foreigner_details=foreigner,
    filing_representative=representative,
    notification_address=notification,
    request_details=request,
    signature=signature,
    office=office,
)

output = fill_form_from_model(form, Path("forms/filled/EX18-domain-complete.pdf"))
print(f"Saved to: {output}")
