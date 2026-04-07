"""EX30 domain model example."""

from datetime import date
from pathlib import Path

from fill_form import fill_form_from_model
from models.ex30 import (
    AuthorizationTypeEnum,
    ApplicantDetails,
    EmployerDetails,
    EX30FormSchema,
    FilingRepresentativeDetails,
    GenderEnum,
    MaritalStatusEnum,
    NotificationAddress,
    OfficeDetails,
    RequestDetails,
    SignatureDetails,
    TrainingCenterDetails,
)

applicant = ApplicantDetails(
    passport="PE4455667",
    nie="Y4567890T",
    first_surname="SALAS",
    second_surname="RUIZ",
    name="DIEGO",
    date_of_birth=date(1996, 8, 21),
    birth_place="Medellin",
    birth_country="Colombia",
    nationality="Colombiana",
    father_name="MIGUEL SALAS",
    mother_name="ELENA RUIZ",
    address="Calle Serrano",
    address_number="41",
    floor_door="1D",
    city="Madrid",
    postal_code="28001",
    province="Madrid",
    mobile_phone="600998877",
    email="diego.salas@example.com",
    legal_representative_name=None,
    legal_representative_id=None,
    legal_representative_title=None,
    gender=GenderEnum.MALE,
    marital_status=MaritalStatusEnum.SINGLE,
)

representative = FilingRepresentativeDetails(
    name_or_company="ASESORIA NUEVOS TRAMITES SL",
    id_number="B99887766",
    address="Calle Velazquez",
    address_number="18",
    floor_door="4A",
    city="Madrid",
    postal_code="28001",
    province="Madrid",
    mobile_phone="914445566",
    email="presentacion@nuevostramites.es",
    legal_representative_name="SARA LORENZO",
    legal_representative_id="33445566L",
    legal_representative_title="Apoderada",
)

notification = NotificationAddress(
    name_or_company="ASESORIA NUEVOS TRAMITES SL",
    id_number="B99887766",
    address="Calle Velazquez",
    address_number="18",
    floor_door="4A",
    city="Madrid",
    postal_code="28001",
    province="Madrid",
    mobile_phone="914445566",
    email="notificaciones@nuevostramites.es",
    consent_electronic_notifications=True,
)

employer = EmployerDetails(
    name_or_company="SERVICIOS URBANOS DEL CENTRO SL",
    tax_or_id_number="B55667788",
    activity="Servicios generales",
    cnae="8121",
    cno_spe_2011="95101016",
    registered_address="Paseo de las Delicias",
    address_number="120",
    floor_door="2",
    city="Madrid",
    postal_code="28045",
    province="Madrid",
    mobile_phone="915556677",
    email="rrhh@servicioscentro.es",
    representative_name="RAQUEL PASTOR",
    representative_id="28765432N",
    representative_title="Administradora",
)

training_center = TrainingCenterDetails(
    secondary_post_compulsory_education=False,
    professional_certificate=True,
    adult_mandatory_education_in_person=False,
    public_employment_service_training=True,
    provider_name="CENTRO FORMATIVO EMPLEA MADRID",
    training_name="Certificado profesional de operaciones auxiliares",
    course_code="CP-2026-001",
    provider_tax_id="G12345678",
    provider_address="Avenida de America 55, Madrid",
    province="Madrid",
    duration_hours="380",
    start_date="01/05/2026",
    end_date="30/09/2026",
    modality_presential=True,
    modality_non_presential=False,
    date_range_checkbox=True,
)

request = RequestDetails(
    authorization_type=AuthorizationTypeEnum.SOCIOFORMATIVO,
)

signature = SignatureDetails(
    place="Madrid",
    day="06",
    month="04",
    year="2026",
    signer_name="DIEGO SALAS RUIZ",
)

office = OfficeDetails(
    target_office="Oficina de Extranjeria de Madrid",
    dir3_code="EA0040721",
    province="Madrid",
)

form = EX30FormSchema(
    applicant_details=applicant,
    filing_representative=representative,
    notification_address=notification,
    employer_details=employer,
    training_center_details=training_center,
    request_details=request,
    signature=signature,
    office=office,
)

output = fill_form_from_model(form, Path("forms/filled/EX30-domain-complete.pdf"))
print(f"Saved to: {output}")