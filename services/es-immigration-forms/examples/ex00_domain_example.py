"""
EX00 domain-model filling example.

Run from the project root:
    .venv/bin/python examples/ex00_domain_example.py
"""

import sys
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from app.models.ex00 import (
    ApplicationCategoryEnum,
    AuthorizationSubtypeEnum,
    EX00FormSchema,
    EmployerDetails,
    FamilyMemberDetails,
    ForeignerDetails,
    GenderEnum,
    InstitutionDetails,
    InstitutionRecognitionTypeEnum,
    MaritalStatusEnum,
    NotificationAddress,
    OfficeDetails,
    PresenterDetails,
    ProgramDetails,
    RequestDetails,
    SignatureDetails,
    StudyModalityEnum,
)
from fill_form import fill_form_from_model

form = EX00FormSchema(
    # ------------------------------------------------------------------
    # Section 1 – Datos de la persona extranjera
    # ------------------------------------------------------------------
    foreigner_details=ForeignerDetails(
        passport="P1234567",
        nie="X1234567L",
        first_surname="GARCIA",
        second_surname="MARTIN",
        name="LUIS",
        gender=GenderEnum.MALE,
        date_of_birth=date(1995, 8, 20),
        birth_place="BOGOTÁ",
        birth_country="COLOMBIA",
        nationality="COLOMBIANA",
        marital_status=MaritalStatusEnum.SINGLE,
        father_name="JOSE GARCIA PEREZ",
        mother_name="MARIA MARTIN LOPEZ",
        address="CALLE GRAN VÍA",
        address_number="45",
        floor_door="2C",
        city="MADRID",
        postal_code="28013",
        province="MADRID",
        mobile_phone="612345678",
        email="luis.garcia@ejemplo.es",
        legal_guardian_name="MARIA DEL CARMEN GARCIA",
        legal_guardian_id="Y7654321K",
        legal_guardian_title="TUTORA LEGAL",
    ),

    # ------------------------------------------------------------------
    # Section 2 – Datos de institución / centro de estudios
    # ------------------------------------------------------------------
    institution_details=InstitutionDetails(
        denomination="UNIVERSIDAD COMPLUTENSE DE MADRID",
        nif="Q2818014H",
        recognition_type=InstitutionRecognitionTypeEnum.RUCT,
        other_type_name="CENTRO PRIVADO ACREDITADO",
        university_affiliation_name="UNIVERSIDAD AUTONOMA DE MADRID",
        other_official_recognition_name="REGISTRO AUTONOMICO DE FORMACION",
        dir3_code="L01280796",
        address="CALLE ISAAC PERAL",
        address_number="1",
        floor_door="1A",
        city="MADRID",
        postal_code="28040",
        province="MADRID",
        legal_rep_name="ANA RODRÍGUEZ FERNÁNDEZ",
        legal_rep_id="12345678Z",
        legal_rep_title="SECRETARIA GENERAL",
    ),

    # ------------------------------------------------------------------
    # Section 3 – Datos del programa de estudios
    # ------------------------------------------------------------------
    program_details=ProgramDetails(
        denomination="MÁSTER EN INTELIGENCIA ARTIFICIAL",
        dir3_code="EA0040721",
        start_date=date(2026, 9, 15),
        end_date=date(2027, 6, 30),
        modality=StudyModalityEnum.IN_PERSON,
    ),

    # ------------------------------------------------------------------
    # Section 4 – Familiar (not applicable)
    # ------------------------------------------------------------------
    family_member=FamilyMemberDetails(
        name="LAURA GARCIA MARTIN",
        nie_pas="Y1234567P",
        surnames="GARCIA MARTIN",
        relationship="HIJA",
    ),

    # ------------------------------------------------------------------
    # Section 5 – Empleador (not applicable for study authorization)
    # ------------------------------------------------------------------
    employer_details=EmployerDetails(
        name_or_company="INNOVA DATA SOLUTIONS SL",
        dni_nie_pas="B76543210",
        activity="DESARROLLO DE SOFTWARE",
        occupation="ANALISTA DE DATOS",
        address="PASEO DE LA CASTELLANA",
        address_number="210",
        floor_door="8B",
        city="MADRID",
        postal_code="28046",
        province="MADRID",
        mobile_phone="611223344",
        email="rrhh@innovadata.es",
        legal_rep_name="MARTA RUIZ GOMEZ",
        legal_rep_id="12345678A",
    ),

    # ------------------------------------------------------------------
    # Section 6 – Representante para presentación
    # ------------------------------------------------------------------
    presenter_details=PresenterDetails(
        name_or_company="RODRIGUEZ FERNANDEZ, ANA",
        id_number="12345678Z",
        address="CALLE GRAN VÍA",
        address_number="10",
        floor_door="2B",
        city="MADRID",
        postal_code="28013",
        province="MADRID",
        mobile_phone="698765432",
        email="ana.rodriguez@gestoria.es",
        legal_rep_name="LAURA SANCHEZ PEREZ",
        legal_rep_id="87654321B",
        legal_rep_title="GESTOR ADMINISTRATIVO",
    ),

    # ------------------------------------------------------------------
    # Section 7 – Domicilio a efectos de notificaciones
    # ------------------------------------------------------------------
    notification_address=NotificationAddress(
        name_or_company="GARCIA MARTIN, LUIS",
        id_number="P1234567",
        address="CALLE GRAN VÍA",
        address_number="45",
        floor_door="2C",
        city="MADRID",
        postal_code="28013",
        province="MADRID",
        mobile_phone="612345678",
        email="luis.garcia@ejemplo.es",
        consent_electronic_notifications=True,
    ),

    # ------------------------------------------------------------------
    # Section 8 – Tipo de autorización
    # ------------------------------------------------------------------
    request_details=RequestDetails(
        application_category=ApplicationCategoryEnum.INICIAL,
        authorization_subtype=AuthorizationSubtypeEnum.ESTUDIOS_SUPERIORES,
        requested_by_institution=False,
        legal_status_in_spain=False,
        work_mode=None,
    ),

    # ------------------------------------------------------------------
    # Office & signature
    # ------------------------------------------------------------------
    office=OfficeDetails(
        target_office="SUBDELEGACIÓN DEL GOBIERNO EN MADRID",
        dir3_code="L01280796",
        province="MADRID",
    ),
    signature=SignatureDetails(
        place="MADRID",
        day="06",
        month="04",
        year="2026",
        name="L. GARCIA MARTIN",
    ),
)

output = fill_form_from_model(form, Path("forms/filled/EX00-domain-complete.pdf"))
print(f"Filled PDF saved to: {output}")
