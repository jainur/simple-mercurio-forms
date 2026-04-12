"""EX29 domain model example."""

from datetime import date
from pathlib import Path

from fill_form import fill_form_from_model
from app.models.ex29 import (
    EX29FormSchema,
    ApplicantDetails,
    ExtensionRequestDetails,
    FilingRepresentativeDetails,
    GenderEnum,
    MaritalStatusEnum,
    NotificationAddress,
    OfficeDetails,
    SignatureDetails,
)

applicant = ApplicantDetails(
    passport="PC1122334",
    nie="X2345678M",
    first_surname="ORTEGA",
    second_surname="NARANJO",
    name="PAULA",
    date_of_birth=date(1997, 11, 3),
    birth_place="Quito",
    birth_country="Ecuador",
    nationality="Ecuatoriana",
    father_name="JORGE ORTEGA",
    mother_name="LUCIA NARANJO",
    address="Calle Mayor",
    address_number="9",
    floor_door="3A",
    city="Madrid",
    postal_code="28013",
    province="Madrid",
    mobile_phone="600554433",
    email="paula.ortega@example.com",
    legal_representative_name=None,
    legal_representative_id=None,
    legal_representative_title=None,
    gender=GenderEnum.FEMALE,
    marital_status=MaritalStatusEnum.SINGLE,
)

representative = FilingRepresentativeDetails(
    name_or_company="TRAMITES MIGRATORIOS CENTRO SL",
    id_number="B66778899",
    address="Calle Atocha",
    address_number="77",
    floor_door="2B",
    city="Madrid",
    postal_code="28012",
    province="Madrid",
    mobile_phone="915554433",
    email="presentacion@tramitescentro.es",
    legal_representative_name="ANA PRIETO",
    legal_representative_id="44556677P",
    legal_representative_title="Apoderada",
)

notification = NotificationAddress(
    name_or_company="TRAMITES MIGRATORIOS CENTRO SL",
    id_number="B66778899",
    address="Calle Atocha",
    address_number="77",
    floor_door="2B",
    city="Madrid",
    postal_code="28012",
    province="Madrid",
    mobile_phone="915554433",
    email="notificaciones@tramitescentro.es",
    consent_electronic_notifications=True,
)

extension_request = ExtensionRequestDetails(
    ordinary_stay_without_visa=False,
    short_stay_visa_holder=True,
    displaced_minor_medical_treatment=False,
    other=False,
    other_description=None,
    justification_and_extension_period="Retraso en la finalizacion del programa turistico por cancelacion de vuelo. Solicita prorroga de 15 dias.",
)

signature = SignatureDetails(
    place="Madrid",
    day="06",
    month="04",
    year="2026",
    signer_name="PAULA ORTEGA NARANJO",
)

office = OfficeDetails(
    target_office="Oficina de Extranjeria de Madrid",
    dir3_code="EA0040721",
    province="Madrid",
)

form = EX29FormSchema(
    applicant_details=applicant,
    filing_representative=representative,
    notification_address=notification,
    extension_request=extension_request,
    signature=signature,
    office=office,
)

output = fill_form_from_model(form, Path("forms/filled/EX29-domain-complete.pdf"))
print(f"Saved to: {output}")