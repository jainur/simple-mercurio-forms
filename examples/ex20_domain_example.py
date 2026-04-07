"""EX20 domain model example."""

from datetime import date
from pathlib import Path

from fill_form import fill_form_from_model
from models.ex20 import (
    EX20FormSchema,
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
    first_surname="BROWN",
    second_surname="SMITH",
    name="EMMA",
    gender=GenderEnum.FEMALE,
    date_of_birth=date(1990, 9, 12),
    birth_place="London",
    birth_country="United Kingdom",
    nationality="British",
    father_name="JOHN BROWN",
    mother_name="ANNA SMITH",
    address="Calle Balmes",
    address_number="30",
    floor_door="2A",
    city="Barcelona",
    postal_code="08007",
    province="Barcelona",
    mobile_phone="600987654",
    email="emma.brown@example.com",
    legal_guardian_name=None,
    legal_guardian_id=None,
    legal_guardian_title=None,
    marital_status=MaritalStatusEnum.MARRIED,
)

representative = FilingRepresentativeDetails(
    name_or_company="GESTORIA BREXIT SL",
    id_number="B99001122",
    address="Passeig de Gracia",
    address_number="88",
    floor_door="4",
    city="Barcelona",
    postal_code="08008",
    province="Barcelona",
    mobile_phone="931234890",
    email="tramites@gestoriabrexit.es",
    legal_rep_name="LAURA CAMPOS",
    legal_rep_id="66778899V",
    legal_rep_title="Apoderada",
)

notification = NotificationAddress(
    name_or_company="GESTORIA BREXIT SL",
    id_number="B99001122",
    address="Passeig de Gracia",
    address_number="88",
    floor_door="4",
    city="Barcelona",
    postal_code="08008",
    province="Barcelona",
    mobile_phone="931234890",
    email="notificaciones@gestoriabrexit.es",
    consent_electronic_notifications=True,
)

request = RequestDetails(
    residence_start_segment_1="01",
    residence_start_segment_2="05",
    residence_start_segment_3="2021",
    residence_start_segment_4="Barcelona",
    uk_national_document_id="Y1234567X",
    relationship_with_uk_national="Conyuge",
    incapacity_with_spanish_spouse_text="",
    identity_document_change_text="",
    cause_specification="",
    category=MainRequestCategoryEnum.TEMPORARY_RESIDENCE,
    temporary_ground=TemporaryResidenceGroundEnum.EMPLOYEE,
    permanent_ground=None,
    modification_ground=None,
    permanent_other_text=None,
    modification_other_text=None,
    deregistration_cause=None,
    truth_statement_accepted=True,
)

signature = SignatureDetails(
    place="Barcelona",
    day="06",
    month="04",
    year="2026",
    uk_national_signature_name="JAMES BROWN",
    applicant_signature_name="EMMA BROWN SMITH",
)

office = OfficeDetails(
    target_office="Oficina de Extranjeria de Barcelona",
    dir3_code="E04922001",
    province="Barcelona",
)

form = EX20FormSchema(
    foreigner_details=foreigner,
    filing_representative=representative,
    notification_address=notification,
    request_details=request,
    signature=signature,
    office=office,
)

output = fill_form_from_model(form, Path("forms/filled/EX20-domain-complete.pdf"))
print(f"Saved to: {output}")
