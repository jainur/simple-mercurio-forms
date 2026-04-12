"""EX16 domain model example."""

from datetime import date
from pathlib import Path

from fill_form import fill_form_from_model
from app.models.ex16 import (
    AuthorizationStageEnum,
    EX16FormSchema,
    FilingRepresentativeDetails,
    ForeignerDetails,
    GenderEnum,
    MaritalStatusEnum,
    NotificationAddress,
    OfficeDetails,
    RequestDetails,
    ReturnModeEnum,
    SignatureDetails,
    TravelDocumentTypeEnum,
)

foreigner = ForeignerDetails(
    passport="AB1234567",
    nie=None,
    first_surname="RUIZ",
    second_surname="MARTIN",
    name="LAURA",
    gender=GenderEnum.FEMALE,
    date_of_birth=date(1993, 8, 10),
    birth_place="Bogota",
    birth_country="Colombia",
    nationality="Colombiana",
    father_name="CARLOS RUIZ",
    mother_name="ANA MARTIN",
    address="Calle Primavera",
    address_number="7",
    floor_door="1B",
    city="Barcelona",
    postal_code="08001",
    province="Barcelona",
    mobile_phone="600123789",
    email="laura.ruiz@example.com",
    legal_guardian_name=None,
    legal_guardian_id=None,
    legal_guardian_title=None,
    marital_status=MaritalStatusEnum.SINGLE,
)

representative = FilingRepresentativeDetails(
    name_or_company="GESTORIA BARCELONA SL",
    id_number="B66778899",
    address="Gran Via",
    address_number="120",
    floor_door="3",
    city="Barcelona",
    postal_code="08011",
    province="Barcelona",
    mobile_phone="931112233",
    email="tramites@gestoriabarcelona.es",
    legal_rep_name="MARTA LOPEZ",
    legal_rep_id="55667788P",
    legal_rep_title="Apoderada",
)

notification = NotificationAddress(
    name_or_company="GESTORIA BARCELONA SL",
    id_number="B66778899",
    address="Gran Via",
    address_number="120",
    floor_door="3",
    city="Barcelona",
    postal_code="08011",
    province="Barcelona",
    mobile_phone="931112233",
    email="notificaciones@gestoriabarcelona.es",
    consent_electronic_notifications=True,
)

request = RequestDetails(
    destination="Colombia",
    reason_humanitarian=True,
    reason_public_interest=False,
    reason_spain_commitments=False,
    reason_exceptional_circumstances=False,
    stage=AuthorizationStageEnum.INITIAL,
    document_type=TravelDocumentTypeEnum.TRAVEL_AUTHORIZATION,
    return_mode=ReturnModeEnum.WITH_RETURN,
    title_reason_humanitarian=False,
    title_reason_public_interest=False,
    title_motivos_checkbox=False,
)

signature = SignatureDetails(
    place="Barcelona",
    day="06",
    month="04",
    year="2026",
    name="LAURA RUIZ MARTIN",
)

office = OfficeDetails(
    target_office="Oficina de Extranjeria de Barcelona",
    dir3_code="E04922001",
    province="Barcelona",
)

form = EX16FormSchema(
    foreigner_details=foreigner,
    filing_representative=representative,
    notification_address=notification,
    request_details=request,
    signature=signature,
    office=office,
)

output = fill_form_from_model(form, Path("forms/filled/EX16-domain-complete.pdf"))
print(f"Saved to: {output}")
