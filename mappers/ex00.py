"""
Mapper: EX00FormSchema → field_values dict understood by fill_form.fill_form()

Every PDF widget name is listed explicitly so the mapping is fully auditable
against the form definition (forms/definitions/EX00.json).
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any
from mappers.helpers import assign_checkboxes, coerce_str as _s, split_nie as _split_nie

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

    fv["Texto1"] = _s(fd.passport)

    if fd.nie:
        seg1, seg2, seg3 = _split_nie(fd.nie)
        fv["Texto2"] = seg1
        fv["Texto3"] = seg2
        fv["Texto4"] = seg3
    else:
        fv["Texto2"] = fv["Texto3"] = fv["Texto4"] = ""

    fv["Texto5"]  = fd.first_surname
    fv["Texto6"]  = _s(fd.second_surname)
    fv["Texto7"]  = fd.name
    fv["Texto8"]  = fd.date_of_birth.strftime("%d")
    fv["Texto9"]  = fd.date_of_birth.strftime("%m")
    fv["Texto10"] = fd.date_of_birth.strftime("%Y")
    fv["Texto11"] = fd.birth_place
    fv["Texto12"] = fd.birth_country
    fv["Texto13"] = fd.nationality
    fv["Texto14"] = _s(fd.father_name)
    fv["Texto15"] = _s(fd.mother_name)
    fv["Texto16"] = fd.address
    fv["Texto17"] = _s(fd.address_number)
    fv["Texto18"] = _s(fd.floor_door)
    fv["Texto19"] = fd.city
    fv["Texto20"] = fd.postal_code
    fv["Texto21"] = fd.province
    fv["Texto22"] = _s(fd.mobile_phone)
    fv["Texto23"] = _s(fd.email)
    fv["Texto24"] = _s(fd.legal_guardian_name)
    fv["Texto25"] = _s(fd.legal_guardian_id)
    fv["Texto26"] = _s(fd.legal_guardian_title)

    # Sexo (X = indeterminado/other)
    assign_checkboxes(fv, fd.gender.value, {
        "Casilla de verificación2": "X",
        "Casilla de verificación3": "H",
        "Casilla de verificación4": "M",
    })

    # Estado civil
    assign_checkboxes(fv, fd.marital_status.value, {
        "Casilla de verificación5": "S",
        "Casilla de verificación6": "C",
        "Casilla de verificación7": "V",
        "Casilla de verificación8": "D",
        "Casilla de verificación9": "Sp",
    })

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
    fv["Texto50"] = _s(emp.name_or_company) if emp else ""
    fv["Texto51"] = _s(emp.dni_nie_pas)     if emp else ""
    fv["Texto52"] = _s(emp.activity)        if emp else ""
    fv["Texto53"] = _s(emp.occupation)      if emp else ""
    fv["Texto54"] = _s(emp.address)         if emp else ""
    fv["Texto55"] = _s(emp.address_number)  if emp else ""
    fv["Texto56"] = _s(emp.floor_door)      if emp else ""
    fv["Texto57"] = _s(emp.city)            if emp else ""
    fv["Texto58"] = _s(emp.postal_code)     if emp else ""
    fv["Texto59"] = _s(emp.province)        if emp else ""
    fv["Texto60"] = _s(emp.mobile_phone)    if emp else ""
    fv["Texto61"] = _s(emp.email)           if emp else ""
    fv["Texto62"] = _s(emp.legal_rep_name)  if emp else ""
    fv["Texto63"] = _s(emp.legal_rep_id)    if emp else ""

    # -------------------------------------------------------------------------
    # Section 6 – DATOS DEL REPRESENTANTE (PRESENTACIÓN)
    # -------------------------------------------------------------------------
    pres = form.presenter_details
    fv["Texto64"] = _s(pres.name_or_company) if pres else ""
    fv["Texto65"] = _s(pres.id_number)       if pres else ""
    fv["Texto66"] = _s(pres.address)         if pres else ""
    fv["Texto67"] = _s(pres.address_number)  if pres else ""
    fv["Texto68"] = _s(pres.floor_door)      if pres else ""
    fv["Texto69"] = _s(pres.city)            if pres else ""
    fv["Texto70"] = _s(pres.postal_code)     if pres else ""
    fv["Texto71"] = _s(pres.province)        if pres else ""
    fv["Texto72"] = _s(pres.mobile_phone)    if pres else ""
    fv["Texto73"] = _s(pres.email)           if pres else ""
    fv["Texto74"] = _s(pres.legal_rep_name)  if pres else ""
    fv["Texto75"] = _s(pres.legal_rep_id)    if pres else ""
    fv["Texto76"] = _s(pres.legal_rep_title) if pres else ""

    # -------------------------------------------------------------------------
    # Section 7 – DOMICILIO A EFECTOS DE NOTIFICACIONES
    # -------------------------------------------------------------------------
    notif = form.notification_address
    fv["Texto77"] = notif.name_or_company
    fv["Texto78"] = notif.id_number
    fv["Texto79"] = notif.address
    fv["Texto80"] = _s(notif.address_number)
    fv["Texto81"] = _s(notif.floor_door)
    fv["Texto82"] = notif.city
    fv["Texto83"] = notif.postal_code
    fv["Texto84"] = notif.province
    fv["Texto85"] = _s(notif.mobile_phone)
    fv["Texto86"] = _s(notif.email)
    fv["Casilla de verificación17"] = notif.consent_electronic_notifications

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
