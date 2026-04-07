"""EX10 domain model example."""

from datetime import date
from pathlib import Path

from fill_form import fill_form_from_model
from models.ex10 import (
    ApplicationRequestTypeEnum,
    AuthorizationTypeEnum,
    EX10FormSchema,
    EmployerDetails,
    EuFamilyDetails,
    FilingRepresentativeDetails,
    ForeignerDetails,
    GenderEnum,
    MaritalStatusEnum,
    NotificationAddress,
    OfficeDetails,
    RequestDetails,
    SignatureDetails,
    TrainingDetails,
    TrainingModeEnum,
)

foreigner = ForeignerDetails(
    passport="AB1234567",
    nie=None,
    first_surname="PEREZ",
    second_surname="LOPEZ",
    name="MARTA",
    gender=GenderEnum.FEMALE,
    date_of_birth=date(1995, 5, 12),
    birth_place="Lima",
    birth_country="Peru",
    nationality="Peruana",
    marital_status=MaritalStatusEnum.SINGLE,
    father_name="CARLOS PEREZ",
    mother_name="ANA LOPEZ",
    address="Calle Mayor",
    address_number="18",
    floor_door="2B",
    city="Madrid",
    postal_code="28013",
    province="Madrid",
    mobile_phone="600111222",
    email="marta.perez@example.com",
    legal_guardian_name=None,
    legal_guardian_id=None,
    legal_guardian_title=None,
)

family = EuFamilyDetails(
    passport="CD7654321",
    nie=None,
    first_surname="PEREZ",
    second_surname="GOMEZ",
    name="JUAN",
    gender=GenderEnum.MALE,
    marital_status=MaritalStatusEnum.MARRIED,
    date_of_birth=date(1970, 3, 20),
    birth_country="Espana",
    relationship_or_type="Familiar ciudadano UE",
    father_name="PEDRO PEREZ",
    mother_name="LUISA GOMEZ",
    address="Avenida America",
    address_number="10",
    floor_door="1A",
    city="Madrid",
    postal_code="28002",
    province="Madrid",
    relationship_with_applicant="Padre",
)

representative = FilingRepresentativeDetails(
    name_or_company="GESTORIA MIGRA SL",
    id_number="B33445566",
    address="Gran Via",
    address_number="50",
    floor_door="4",
    city="Madrid",
    postal_code="28013",
    province="Madrid",
    mobile_phone="910223344",
    email="tramites@gestoriamigra.es",
    legal_rep_name="LAURA TORRES",
    legal_rep_id="22334455R",
    legal_rep_title="Apoderada",
)

notification = NotificationAddress(
    name_or_company="GESTORIA MIGRA SL",
    id_number="B33445566",
    address="Gran Via",
    address_number="50",
    floor_door="4",
    city="Madrid",
    postal_code="28013",
    province="Madrid",
    mobile_phone="910223344",
    email="notificaciones@gestoriamigra.es",
)

employer = EmployerDetails(
    name_or_company="SERVICIOS CENTRALES SA",
    id_number="A99887766",
    activity="Servicios administrativos",
    cnae_code="8211",
    cno_spe_2011="4309",
    address="Paseo Castellana",
    address_number="200",
    floor_door="6",
    city="Madrid",
    postal_code="28046",
    province="Madrid",
    mobile_phone="911112233",
    email="rrhh@servicioscentrales.es",
    legal_rep_name="MARIO BLANCO",
    legal_rep_id="33445566K",
    legal_rep_title="Administrador",
)

training = TrainingDetails(
    training_name="Curso de insercion laboral",
    course_code_1="C-100",
    course_code_2="C-200",
    course_code_3="C-300",
    start_date="01/05/2026",
    end_date="31/10/2026",
    province="Madrid",
    duration_hours="240",
    training_mode=TrainingModeEnum.SECONDARY_POSTOBLIGATORY,
)

request = RequestDetails(
    has_valid_electronic_certificate_or_clave=True,
    request_type=ApplicationRequestTypeEnum.INITIAL,
    authorization_type=AuthorizationTypeEnum.SOCIOLABORAL_ART_127_B,
    humanitarian_option_1=False,
    humanitarian_option_2=False,
    humanitarian_option_3=False,
    humanitarian_option_4=False,
    humanitarian_option_5=False,
    public_interest_option_1=False,
    public_interest_option_2=False,
    gender_violence_woman_option_1=False,
    gender_violence_woman_option_2=False,
    parent_of_gender_violence_victim=False,
    sexual_violence_option_1=False,
    sexual_violence_option_2=False,
    parent_of_sexual_violence_option_1=False,
    parent_of_sexual_violence_option_2=False,
    parent_of_sexual_violence_option_3=False,
    parent_of_sexual_violence_option_4=False,
    parent_of_sexual_violence_option_5=False,
    parent_of_sexual_violence_option_6=False,
    unknown_option_148=False,
)

signature = SignatureDetails(
    signer_1="MARTA PEREZ LOPEZ",
    signer_2="",
    signer_3="",
    signer_4="",
    signer_5="",
)

office = OfficeDetails(
    target_office="Oficina de Extranjeria de Madrid",
    dir3_code="E04921901",
    province="Madrid",
)

form = EX10FormSchema(
    foreigner_details=foreigner,
    eu_family_details=family,
    filing_representative=representative,
    notification_address=notification,
    employer_details=employer,
    training_details=training,
    request_details=request,
    signature=signature,
    office=office,
)

output = fill_form_from_model(form, Path("forms/filled/EX10-domain-complete.pdf"))
print(f"Saved to: {output}")
