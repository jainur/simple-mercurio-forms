"""EX28 domain model example."""

from datetime import date
from pathlib import Path

from fill_form import fill_form_from_model
from models.ex28 import (
    EX28FormSchema,
    ApplicantDetails,
    FilingRepresentativeDetails,
    GenderEnum,
    MaritalStatusEnum,
    NotificationAddress,
    OfficeDetails,
    PendingApplicationDetails,
    RequestDetails,
    SignatureDetails,
)

applicant = ApplicantDetails(
    passport="PZ3344556",
    nie="Y7654321Z",
    first_surname="MENDOZA",
    second_surname="GIL",
    name="LUCIA",
    date_of_birth=date(1999, 2, 18),
    birth_place="Lima",
    birth_country="Peru",
    nationality="Peruana",
    father_name="RAUL MENDOZA",
    mother_name="PILAR GIL",
    address="Calle San Luis",
    address_number="14",
    floor_door="2D",
    city="Valencia",
    postal_code="46006",
    province="Valencia",
    mobile_phone="600112233",
    email="lucia.mendoza@example.com",
    current_authorization_type="Autorizacion de estancia por estudios",
    current_authorization_id="Y7654321Z",
    legal_representative_name=None,
    legal_representative_id=None,
    legal_representative_title=None,
    gender=GenderEnum.FEMALE,
    marital_status=MaritalStatusEnum.SINGLE,
    has_school_age_children_in_spain=False,
)

pending_application = PendingApplicationDetails(
    case_number="EXP-2025-VAL-001234",
    filing_date="15/05/2025",
)

representative = FilingRepresentativeDetails(
    name_or_company="ASESORIA MIGRATORIA LEVANTE SL",
    id_number="B55443322",
    address="Gran Via Germanias",
    address_number="28",
    floor_door="5A",
    city="Valencia",
    postal_code="46004",
    province="Valencia",
    mobile_phone="963445566",
    email="presentacion@asesorialevante.es",
    legal_representative_name="ALBA FERRER",
    legal_representative_id="25444333J",
    legal_representative_title="Apoderada",
)

notification = NotificationAddress(
    name_or_company="ASESORIA MIGRATORIA LEVANTE SL",
    id_number="B55443322",
    address="Gran Via Germanias",
    address_number="28",
    floor_door="5A",
    city="Valencia",
    postal_code="46004",
    province="Valencia",
    mobile_phone="963445566",
    email="notificaciones@asesorialevante.es",
    consent_electronic_notifications=True,
)

request = RequestDetails(
    long_term_stay_from_study_or_mobility_or_volunteering=True,
    exceptional_circumstances_family_roots_to_parent_guardian_of_eu_minor=False,
    exceptional_circumstances_training_roots_to_sociotraining_roots=False,
    exceptional_circumstances_social_roots_employment_to_sociolabor_roots=False,
    exceptional_circumstances_social_roots_self_employment_to_social_roots=False,
    exceptional_circumstances_other_to_equivalent_title_vii=False,
    family_members_of_spanish_nationals_transition=False,
    temporary_residence_title_iv_to_equivalent_title_iv=False,
    temporary_residence_minor_child_or_ward_to_equivalent=False,
    long_term_residence_to_long_term_national=False,
    long_term_residence_to_long_term_eu=False,
    modification_of_situations_to_title_xi_equivalent=False,
    simultaneous_family_reunification_requests=False,
)

signature = SignatureDetails(
    place="Valencia",
    day="06",
    month="04",
    year="2026",
    signer_name="LUCIA MENDOZA GIL",
)

office = OfficeDetails(
    target_office="Oficina de Extranjeria de Valencia",
    dir3_code="EA0041208",
    province="Valencia",
)

form = EX28FormSchema(
    applicant_details=applicant,
    pending_application=pending_application,
    filing_representative=representative,
    notification_address=notification,
    request_details=request,
    signature=signature,
    office=office,
)

output = fill_form_from_model(form, Path("forms/filled/EX28-domain-complete.pdf"))
print(f"Saved to: {output}")