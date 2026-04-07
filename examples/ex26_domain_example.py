"""EX26 domain model example."""

from datetime import date
from pathlib import Path

from fill_form import fill_form_from_model
from models.ex26 import (
    EX26FormSchema,
    ApplicantDetails,
    EmployerDetails,
    FilingRepresentativeDetails,
    GenderEnum,
    MaritalStatusEnum,
    NotificationAddress,
    OfficeDetails,
    RequestDetails,
    SignatureDetails,
)

applicant = ApplicantDetails(
    passport="PA9988776",
    nie="Y1234567X",
    first_surname="BENITEZ",
    second_surname="ROJAS",
    name="MARIO",
    date_of_birth=date(1998, 9, 14),
    birth_place="Bogota",
    birth_country="Colombia",
    nationality="Colombiana",
    father_name="JORGE BENITEZ",
    mother_name="SANDRA ROJAS",
    address="Calle Feria",
    address_number="18",
    floor_door="2B",
    city="Sevilla",
    postal_code="41003",
    province="Sevilla",
    mobile_phone="600987654",
    email="mario.benitez@example.com",
    legal_representative_name=None,
    legal_representative_id=None,
    legal_representative_title=None,
    gender=GenderEnum.MALE,
    marital_status=MaritalStatusEnum.SINGLE,
    has_school_age_children_in_spain=False,
)

employer = EmployerDetails(
    name_or_company="SERVICIOS HOSTELEROS DEL SUR SL",
    tax_or_id_number="B91827364",
    activity="Hosteleria",
    cnae="5610",
    registered_address="Avenida de la Innovacion",
    address_number="21",
    floor_door="4",
    city="Sevilla",
    postal_code="41020",
    province="Sevilla",
    mobile_phone="954555111",
    email="rrhh@hosteleriadelsur.es",
    legal_representative_name="ELENA PRIETO",
    legal_representative_id="28765432T",
    legal_representative_title="Administradora unica",
)

representative = FilingRepresentativeDetails(
    name_or_company="GESTION MIGRATORIA ANDALUZA SL",
    id_number="B44556677",
    address="Calle Imagen",
    address_number="7",
    floor_door="1C",
    city="Sevilla",
    postal_code="41003",
    province="Sevilla",
    mobile_phone="954888222",
    email="presentacion@gestionmigratoria.es",
    legal_representative_name="INES CAMPOS",
    legal_representative_id="44556677R",
    legal_representative_title="Apoderada",
)

notification = NotificationAddress(
    name_or_company="GESTION MIGRATORIA ANDALUZA SL",
    id_number="B44556677",
    address="Calle Imagen",
    address_number="7",
    floor_door="1C",
    city="Sevilla",
    postal_code="41003",
    province="Sevilla",
    mobile_phone="954888222",
    email="notificaciones@gestionmigratoria.es",
    consent_electronic_notifications=True,
)

request = RequestDetails(
    from_work_enabled_residence_less_than_one_year_to_employment=False,
    from_work_enabled_residence_one_year_to_employment_and_self_employment=False,
    from_seasonal_residence_to_employment=False,
    from_seasonal_residence_to_self_employment=False,
    from_non_work_residence_less_than_one_year_to_employment=False,
    from_non_work_residence_one_year_to_employment=True,
    from_non_work_residence_one_year_to_self_employment=False,
    modify_employment_scope_occupation_or_territory=False,
    modify_self_employment_scope_sector_or_territory=False,
    from_employment_to_employment_and_self_employment=False,
    from_family_member_residence_to_non_lucrative_residence=False,
    from_family_member_residence_to_employment=False,
    from_family_member_residence_to_self_employment=False,
    from_family_member_residence_to_work_exception_residence=False,
    from_study_stay_to_employment_article_190_2=False,
    from_study_stay_to_self_employment_article_190_3=False,
    from_study_stay_to_work_exception_residence_article_190_4=False,
    from_study_stay_to_family_reunification_residence=False,
    from_study_stay_to_job_search_or_business_project=False,
)

signature = SignatureDetails(
    place="Sevilla",
    day="06",
    month="04",
    year="2026",
    signer_name="MARIO BENITEZ ROJAS",
)

office = OfficeDetails(
    target_office="Oficina de Extranjeria de Sevilla",
    dir3_code="EA0041234",
    province="Sevilla",
)

form = EX26FormSchema(
    applicant_details=applicant,
    employer_details=employer,
    filing_representative=representative,
    notification_address=notification,
    request_details=request,
    signature=signature,
    office=office,
)

output = fill_form_from_model(form, Path("forms/filled/EX26-domain-complete.pdf"))
print(f"Saved to: {output}")