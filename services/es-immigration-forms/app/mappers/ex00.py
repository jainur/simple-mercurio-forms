"""
Mapper: EX00FormSchema → field_values dict understood by fill_form.fill_form()

Every PDF widget name is listed explicitly so the mapping is fully auditable
against the form definition (forms/definitions/EX00.json).
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any
from app.mappers.helpers import apply_enum_registry as _apply_enum_registry, coerce_str as _s, map_identity_person_block as _map_identity_person_block, map_notification_block as _map_notification_block, map_optional_object_fields as _map_optional_object_fields

if TYPE_CHECKING:
    from models.ex00 import EX00FormSchema



def to_field_values(form: EX00FormSchema) -> dict[str, Any]:
    """
    Convert an EX00FormSchema domain object to a flat field_values dict.
    Keys are PDF widget names; values are str (text fields) or bool (checkboxes).
    """
    from models.ex00 import (
        ApplicationCategoryEnum,
        AuthorizationSubtypeEnum,
        InstitutionRecognitionTypeEnum,
        StudyModalityEnum,
        WorkModeEnum,
    )

    fv: dict[str, Any] = {}

    # -------------------------------------------------------------------------
    # Section 1 – DATOS DE LA PERSONA EXTRANJERA
    # -------------------------------------------------------------------------
    fd = form.foreigner_details

    _map_identity_person_block(
        fv,
        fd,
        passport_field="Texto1",
        nie_fields=("Texto2", "Texto3", "Texto4"),
        date_fields=("Texto8", "Texto9", "Texto10"),
        text_fields={
            "first_surname": "Texto5",
            "second_surname": "Texto6",
            "name": "Texto7",
            "birth_place": "Texto11",
            "birth_country": "Texto12",
            "nationality": "Texto13",
            "father_name": "Texto14",
            "mother_name": "Texto15",
            "address": "Texto16",
            "address_number": "Texto17",
            "floor_door": "Texto18",
            "city": "Texto19",
            "postal_code": "Texto20",
            "province": "Texto21",
            "mobile_phone": "Texto22",
            "email": "Texto23",
            "legal_guardian_name": "Texto24",
            "legal_guardian_id": "Texto25",
            "legal_guardian_title": "Texto26",
        },
        gender_checkbox_map={
            "Casilla de verificación2": "X",
            "Casilla de verificación3": "H",
            "Casilla de verificación4": "M",
        },
        marital_checkbox_map={
            "Casilla de verificación5": "S",
            "Casilla de verificación6": "C",
            "Casilla de verificación7": "V",
            "Casilla de verificación8": "D",
            "Casilla de verificación9": "Sp",
        },
    )

    # -------------------------------------------------------------------------
    # Section 2 – DATOS DE INSTITUCIÓN / CENTRO DE ESTUDIOS
    # -------------------------------------------------------------------------
    inst = form.institution_details

    fv["Texto27"] = inst.denomination
    fv["Texto28"] = _s(inst.nif)
    fv["Texto29"] = _s(inst.other_type_name)
    fv["Texto30"] = _s(inst.university_affiliation_name)
    fv["Texto31"] = _s(inst.other_official_recognition_name)
    fv["Texto32"] = _s(inst.dir3_code)
    fv["Texto33"] = inst.address
    fv["Texto34"] = _s(inst.address_number)
    fv["Texto35"] = _s(inst.floor_door)
    fv["Texto36"] = inst.city
    fv["Texto37"] = inst.postal_code
    fv["Texto38"] = inst.province
    fv["Texto39"] = _s(inst.legal_rep_name)
    fv["Texto40"] = _s(inst.legal_rep_id)
    fv["Texto41"] = _s(inst.legal_rep_title)

    fv["Casilla de verificación10"] = inst.recognition_type == InstitutionRecognitionTypeEnum.RUCT
    fv["Casilla de verificación11"] = inst.recognition_type == InstitutionRecognitionTypeEnum.RCD
    fv["Casilla de verificación12"] = inst.recognition_type == InstitutionRecognitionTypeEnum.OTHER
    fv["Casilla de verificación13"] = inst.recognition_type == InstitutionRecognitionTypeEnum.UNIVERSITY_AFFILIATION
    fv["Casilla de verificación14"] = inst.recognition_type == InstitutionRecognitionTypeEnum.OTHER_OFFICIAL

    # -------------------------------------------------------------------------
    # Section 3 – DATOS DEL PROGRAMA DE ESTUDIOS O FORMACIÓN
    # -------------------------------------------------------------------------
    prog = form.program_details

    fv["Texto42"] = prog.denomination
    fv["Texto43"] = _s(prog.dir3_code)
    fv["Texto44"] = prog.start_date.strftime("%d/%m/%Y")
    fv["Texto45"] = prog.end_date.strftime("%d/%m/%Y")

    fv["Casilla de verificación15"] = prog.modality == StudyModalityEnum.IN_PERSON
    fv["Casilla de verificación16"] = prog.modality == StudyModalityEnum.HYBRID

    # -------------------------------------------------------------------------
    # Section 4 – DATOS DEL FAMILIAR ESTUDIANTE AL QUE ACOMPAÑA
    # -------------------------------------------------------------------------
    fam = form.family_member
    fv["Texto46"] = fam.name     if fam else ""
    fv["Texto47"] = _s(fam.nie_pas)  if fam else ""
    fv["Texto48"] = fam.surnames if fam else ""
    fv["Texto49"] = fam.relationship if fam else ""

    # -------------------------------------------------------------------------
    # Section 5 – DATOS DEL EMPLEADOR/A
    # -------------------------------------------------------------------------
    emp = form.employer_details
    _map_optional_object_fields(
        fv,
        emp,
        text_fields={
            "name_or_company": "Texto50",
            "dni_nie_pas": "Texto51",
            "activity": "Texto52",
            "occupation": "Texto53",
            "address": "Texto54",
            "address_number": "Texto55",
            "floor_door": "Texto56",
            "city": "Texto57",
            "postal_code": "Texto58",
            "province": "Texto59",
            "mobile_phone": "Texto60",
            "email": "Texto61",
            "legal_rep_name": "Texto62",
            "legal_rep_id": "Texto63",
        },
    )

    # -------------------------------------------------------------------------
    # Section 6 – DATOS DEL REPRESENTANTE (PRESENTACIÓN)
    # -------------------------------------------------------------------------
    pres = form.presenter_details
    _map_optional_object_fields(
        fv,
        pres,
        text_fields={
            "name_or_company": "Texto64",
            "id_number": "Texto65",
            "address": "Texto66",
            "address_number": "Texto67",
            "floor_door": "Texto68",
            "city": "Texto69",
            "postal_code": "Texto70",
            "province": "Texto71",
            "mobile_phone": "Texto72",
            "email": "Texto73",
            "legal_rep_name": "Texto74",
            "legal_rep_id": "Texto75",
            "legal_rep_title": "Texto76",
        },
    )

    # -------------------------------------------------------------------------
    # Section 7 – DOMICILIO A EFECTOS DE NOTIFICACIONES
    # -------------------------------------------------------------------------
    notif = form.notification_address
    _map_notification_block(
        fv,
        notif,
        text_fields={
            "name_or_company": "Texto77",
            "id_number": "Texto78",
            "address": "Texto79",
            "address_number": "Texto80",
            "floor_door": "Texto81",
            "city": "Texto82",
            "postal_code": "Texto83",
            "province": "Texto84",
            "mobile_phone": "Texto85",
            "email": "Texto86",
        },
        consent_field="Casilla de verificación17",
    )

    # -------------------------------------------------------------------------
    # Signature footer
    # -------------------------------------------------------------------------
    sig = form.signature
    fv["Texto87"] = sig.place
    fv["Texto88"] = sig.day
    fv["Texto89"] = sig.month
    fv["Texto90"] = sig.year
    fv["Texto91"] = _s(sig.name)

    # -------------------------------------------------------------------------
    # Office (DIRIGIDA A / DIR3 / PROVINCIA)
    # -------------------------------------------------------------------------
    off = form.office
    fv["Texto92"] = _s(off.target_office)
    fv["Texto93"] = _s(off.dir3_code)
    fv["Texto94"] = off.province

    # -------------------------------------------------------------------------
    # Section 8 – TIPO DE AUTORIZACIÓN DE ESTANCIA SOLICITADA
    # -------------------------------------------------------------------------
    req = form.request_details
    cat = req.application_category
    sub = req.authorization_subtype

    fv["Casilla de verificación18"] = cat == ApplicationCategoryEnum.INICIAL
    fv["Casilla de verificación39"] = cat == ApplicationCategoryEnum.PRORROGA
    fv["Casilla de verificación40"] = cat == ApplicationCategoryEnum.AUTORIZACION_TRABAJO

    # Authorization subtypes (only one of 19-38 is typically checked)
    fv["Casilla de verificación19"] = sub == AuthorizationSubtypeEnum.ESTUDIOS_SUPERIORES
    fv["Casilla de verificación20"] = req.requested_by_institution
    fv["Casilla de verificación21"] = req.legal_status_in_spain
    fv["Casilla de verificación22"] = sub == AuthorizationSubtypeEnum.EDUCACION_SECUNDARIA
    fv["Casilla de verificación23"] = sub == AuthorizationSubtypeEnum.MOVILIDAD_SECUNDARIA
    fv["Casilla de verificación24"] = sub == AuthorizationSubtypeEnum.VOLUNTARIADO
    fv["Casilla de verificación25"] = sub == AuthorizationSubtypeEnum.ACTIVIDADES_FORMATIVAS
    fv["Casilla de verificación26"] = sub == AuthorizationSubtypeEnum.AUXILIAR_CONVERSACION
    fv["Casilla de verificación27"] = sub == AuthorizationSubtypeEnum.ESTUDIOS_IDIOMATICOS
    fv["Casilla de verificación28"] = sub == AuthorizationSubtypeEnum.CURSOS_PREPARATORIOS
    fv["Casilla de verificación29"] = sub == AuthorizationSubtypeEnum.CERTIFICACION_APTITUD
    fv["Casilla de verificación30"] = sub == AuthorizationSubtypeEnum.CERTIFICADO_PROFESIONAL
    fv["Casilla de verificación31"] = sub == AuthorizationSubtypeEnum.FORMACION_SANITARIA
    fv["Casilla de verificación32"] = sub == AuthorizationSubtypeEnum.MOVILIDAD_PROGRAMA_UE
    fv["Casilla de verificación33"] = sub == AuthorizationSubtypeEnum.MOVILIDAD_SIN_PROGRAMA_UE
    fv["Casilla de verificación34"] = sub == AuthorizationSubtypeEnum.CONVENIO_ANDORRA
    fv["Casilla de verificación35"] = sub == AuthorizationSubtypeEnum.FAMILIAR_ESTUDIOS_SUPERIORES
    fv["Casilla de verificación36"] = sub == AuthorizationSubtypeEnum.FAMILIAR_FORMACION_SANITARIA
    fv["Casilla de verificación37"] = sub == AuthorizationSubtypeEnum.FAMILIAR_ANDORRA
    fv["Casilla de verificación38"] = sub == AuthorizationSubtypeEnum.HIJO_NACIDO_ESPANA

    # Work mode (for AUTORIZACION_TRABAJO)
    wm = req.work_mode
    fv["Casilla de verificación41"] = wm == WorkModeEnum.EMPLOYED
    fv["Casilla de verificación42"] = wm == WorkModeEnum.SELF_EMPLOYED

    return fv
