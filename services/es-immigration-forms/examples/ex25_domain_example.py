"""EX25 domain model example."""

from datetime import date
from pathlib import Path

from fill_form import fill_form_from_model
from app.models.ex25 import (
    EX25FormSchema,
    FilingRepresentativeDetails,
    GenderEnum,
    GuardianOrEntityDetails,
    MinorDetails,
    NotificationAddress,
    OfficeDetails,
    RequestDetails,
    SignatureDetails,
)

minor = MinorDetails(
    passport="AB1234567",
    nie=None,
    first_surname="LOPEZ",
    second_surname="MARTIN",
    name="DANIEL",
    date_of_birth=date(2012, 5, 4),
    birth_place="Quito",
    birth_country="Ecuador",
    nationality="Ecuatoriana",
    father_name="CARLOS LOPEZ",
    mother_name="ANA MARTIN",
    address="Calle Sol",
    address_number="12",
    floor_door="1A",
    city="Sevilla",
    mobile_phone="600123456",
    postal_code="41001",
    province="Sevilla",
    email="familia@example.com",
    legal_guardian_name="MARTA LOPEZ",
    legal_guardian_id="X1234567L",
    legal_guardian_title="Madre",
    representative_nature="Representante legal",
    relationship_with_minor="Madre",
    gender=GenderEnum.MALE,
)

guardian_entity = GuardianOrEntityDetails(
    name_or_company="ASOCIACION PROTECCION MENOR",
    id_number="G12345678",
    address="Avenida Constitucion",
    address_number="5",
    floor_door="2",
    city="Sevilla",
    postal_code="41004",
    province="Sevilla",
    mobile_phone="954123456",
    email="info@proteccionmenor.es",
    legal_rep_name="LUIS RAMOS",
    legal_rep_id="22334455K",
    legal_rep_title="Director",
)

representative = FilingRepresentativeDetails(
    name_or_company="GESTORIA INFANCIA SL",
    id_number="B33445566",
    address="Calle Sierpes",
    address_number="40",
    floor_door="3",
    city="Sevilla",
    postal_code="41004",
    province="Sevilla",
    mobile_phone="954223344",
    email="tramites@gestoriainfancia.es",
    legal_rep_name="LAURA VEGA",
    legal_rep_id="33445566P",
    legal_rep_title="Apoderada",
)

notification = NotificationAddress(
    name_or_company="GESTORIA INFANCIA SL",
    id_number="B33445566",
    address="Calle Sierpes",
    address_number="40",
    floor_door="3",
    city="Sevilla",
    postal_code="41004",
    province="Sevilla",
    mobile_phone="954223344",
    email="notificaciones@gestoriainfancia.es",
    consent_electronic_notifications=True,
)

request = RequestDetails(
    temporary_residence_minor_born_in_spain=True,
    temporary_residence_accompanied_disabled_minor_not_born_in_spain=False,
    temporary_residence_dana_2024_minor_with_guardian=False,
    temporary_initial_unaccompanied_minor=False,
    temporary_initial_former_ward_without_residence_at_majority=False,
    temporary_initial_displaced_minor_medical_treatment_extension_exhausted=False,
    temporary_initial_parent_or_guardian_medical_treatment_extension_exhausted=False,
    renewal_unaccompanied_minor_with_residence=False,
    renewal_former_ward_with_residence_at_majority=False,
    renewal_former_ward_without_residence_at_majority=False,
    renewal_displaced_minor_medical_treatment_exceptional=False,
    renewal_parent_or_guardian_medical_treatment_exceptional=False,
    humanitarian_program_minor_medical_treatment_stay=False,
    humanitarian_program_parent_or_guardian_medical_treatment_stay=False,
    humanitarian_program_minor_holiday_stay=False,
    humanitarian_program_monitor_holiday_stay=False,
    humanitarian_program_schooling_stay=False,
    humanitarian_extension_medical_treatment=False,
    humanitarian_extension_parent_or_guardian_medical_treatment=False,
    humanitarian_extension_schooling_exceptional_return_impediment=False,
    other_international_adoption=False,
    other_vacations_in_peace_program=False,
)

signature = SignatureDetails(
    day="06",
    signer_1_id="X1234567L",
    signer_1_title="Madre",
    place="Sevilla",
    signer_2_id="22334455K",
    signer_2_title="Director",
    month="04",
    year="2026",
    signer_1_name="MARTA LOPEZ",
    signer_2_name="LUIS RAMOS",
)

office = OfficeDetails(
    target_office="Oficina de Extranjeria de Sevilla",
    dir3_code="E04921903",
    province="Sevilla",
)

form = EX25FormSchema(
    minor_details=minor,
    guardian_or_entity_details=guardian_entity,
    filing_representative=representative,
    notification_address=notification,
    request_details=request,
    signature=signature,
    office=office,
)

output = fill_form_from_model(form, Path("forms/filled/EX25-domain-complete.pdf"))
print(f"Saved to: {output}")
