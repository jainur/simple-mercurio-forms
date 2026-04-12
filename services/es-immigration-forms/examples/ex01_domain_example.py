"""
EX-01 domain model example
Solicitud de autorización de residencia temporal no lucrativa.

Demonstrates filling the form as a *familiar del titular de los recursos
económicos* (family member of the economic resources holder), together
with a presenter (legal representative for filing purposes).
"""

from datetime import date
from pathlib import Path

from app.models.ex01 import (
    ApplicantRoleEnum,
    ApplicationCategoryEnum,
    EX01FormSchema,
    ForeignerDetails,
    GenderEnum,
    MaritalStatusEnum,
    NotificationAddress,
    OfficeDetails,
    PresenterDetails,
    RequestDetails,
    ResourceHolderDetails,
    SignatureDetails,
)
from fill_form import fill_form_from_model

# ---------------------------------------------------------------------------
# 1.  DATOS DE LA PERSONA EXTRANJERA SOLICITANTE
# ---------------------------------------------------------------------------
foreigner = ForeignerDetails(
    passport="AB1234567",
    nie=None,
    first_surname="GARCÍA",
    second_surname="LÓPEZ",
    name="MARÍA",
    gender=GenderEnum.FEMALE,
    date_of_birth=date(1990, 6, 15),
    birth_place="Buenos Aires",
    birth_country="Argentina",
    nationality="Argentina",
    marital_status=MaritalStatusEnum.SINGLE,
    father_name="CARLOS GARCÍA",
    mother_name="ANA LÓPEZ",
    address="Calle de Alcalá",
    address_number="100",
    floor_door="3º B",
    city="Madrid",
    postal_code="28009",
    province="Madrid",
    mobile_phone="+34 600 111 222",
    email="maria.garcia@example.com",
    children_in_school_age=False,
    legal_guardian_name=None,
    legal_guardian_id=None,
    legal_guardian_title=None,
)

# ---------------------------------------------------------------------------
# 2.  DATOS DEL FAMILIAR TITULAR DE LOS RECURSOS ECONÓMICOS
# ---------------------------------------------------------------------------
resource_holder = ResourceHolderDetails(
    passport="CD9876543",
    nie=None,
    first_surname="GARCÍA",
    second_surname="MARTÍNEZ",
    name="ROBERTO",
    gender=GenderEnum.MALE,
    date_of_birth=date(1955, 3, 22),
    birth_country="Argentina",
    father_name="PEDRO GARCÍA",
    mother_name="LUISA MARTÍNEZ",
    relationship="Padre",
    marital_status=MaritalStatusEnum.MARRIED,
)

# ---------------------------------------------------------------------------
# 3.  DATOS DEL REPRESENTANTE A EFECTOS DE PRESENTACIÓN
# ---------------------------------------------------------------------------
presenter = PresenterDetails(
    name_or_company="BUFETE INMIGRACIÓN SL",
    id_number="B12345678",
    address="Gran Vía",
    address_number="50",
    floor_door="4ª planta",
    city="Madrid",
    postal_code="28013",
    province="Madrid",
    mobile_phone="+34 912 345 678",
    email="gestion@bufete-inmigracion.es",
    legal_rep_name="LAURA SÁNCHEZ RUIZ",
    legal_rep_id="12345678Z",
    legal_rep_title="Abogada",
)

# ---------------------------------------------------------------------------
# 4.  DOMICILIO A EFECTOS DE NOTIFICACIONES
# ---------------------------------------------------------------------------
notification = NotificationAddress(
    name_or_company="BUFETE INMIGRACIÓN SL",
    id_number="B12345678",
    address="Gran Vía",
    address_number="50",
    floor_door="4ª planta",
    city="Madrid",
    postal_code="28013",
    province="Madrid",
    mobile_phone="+34 912 345 678",
    email="gestion@bufete-inmigracion.es",
    consent_electronic_notifications=True,
)

# ---------------------------------------------------------------------------
# 5.  TIPO DE AUTORIZACIÓN SOLICITADA
# ---------------------------------------------------------------------------
request = RequestDetails(
    application_category=ApplicationCategoryEnum.RESIDENCIA_INICIAL,
    applicant_role=ApplicantRoleEnum.FAMILIAR_TITULAR_RECURSOS,
)

# ---------------------------------------------------------------------------
# Office + Signature
# ---------------------------------------------------------------------------
office = OfficeDetails(
    target_office="Oficina de Extranjería de Madrid",
    dir3_code="E04921901",
    province="Madrid",
)

signature = SignatureDetails(
    place="Madrid",
    day="15",
    month="06",
    year="2025",
    name="MARÍA GARCÍA LÓPEZ",
)

# ---------------------------------------------------------------------------
# Build root schema and fill the form
# ---------------------------------------------------------------------------
form = EX01FormSchema(
    foreigner_details=foreigner,
    resource_holder=resource_holder,
    presenter_details=presenter,
    notification_address=notification,
    request_details=request,
    office=office,
    signature=signature,
)

output_path = Path("forms/filled/EX01-domain-complete.pdf")
result = fill_form_from_model(form, output_path)
print(f"Saved to: {result}")
