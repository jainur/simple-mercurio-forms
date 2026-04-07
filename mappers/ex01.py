"""
Mapper: EX01FormSchema → field_values dict understood by fill_form.fill_form()

Every PDF widget name is mapped explicitly, auditable against
forms/definitions/EX01.json (96 fields).
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any
from mappers.helpers import assign_checkboxes, coerce_str as _s, split_nie as _split_nie

if TYPE_CHECKING:
    from models.ex01 import EX01FormSchema



def to_field_values(form: EX01FormSchema) -> dict[str, Any]:
    from models.ex01 import ApplicationCategoryEnum, ApplicantRoleEnum

    fv: dict[str, Any] = {}

    # -------------------------------------------------------------------------
    # Section 1 – DATOS DE LA PERSONA EXTRANJERA SOLICITANTE
    # -------------------------------------------------------------------------
    fd = form.foreigner_details

    fv["Texto1"] = _s(fd.passport)

    if fd.nie:
        s1, s2, s3 = _split_nie(fd.nie)
        fv["Texto2"], fv["Texto3"], fv["Texto4"] = s1, s2, s3
    else:
        fv["Texto2"] = fv["Texto3"] = fv["Texto4"] = ""

    fv["Texto5"]  = fd.first_surname
    fv["Texto6"]  = _s(fd.second_surname)
    fv["Texto7"]  = fd.name

    # Sexo
    assign_checkboxes(fv, fd.gender.value, {
        "Casilla de verificación2": "X",
        "Casilla de verificación3": "H",
        "Casilla de verificación4": "M",
    })

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

    # Estado civil (section 1 row)
    assign_checkboxes(fv, fd.marital_status.value, {
        "Casilla de verificación5": "S",
        "Casilla de verificación6": "C",
        "Casilla de verificación7": "V",
        "Casilla de verificación9": "Sp",
        "Casilla de verificación8": "D",
    })

    # Hijas/os a cargo
    fv["Casilla de verificación10"] = fd.children_in_school_age          # SÍ
    fv["Casilla de verificación11"] = not fd.children_in_school_age      # NO

    # -------------------------------------------------------------------------
    # Section 2 – DATOS DEL FAMILIAR TITULAR DE LOS RECURSOS ECONÓMICOS
    # -------------------------------------------------------------------------
    rh = form.resource_holder

    fv["Texto27"] = _s(rh.passport) if rh else ""
    if rh and rh.nie:
        s1, s2, s3 = _split_nie(rh.nie)
        fv["Texto28"], fv["Texto29"], fv["Texto30"] = s1, s2, s3
    else:
        fv["Texto28"] = fv["Texto29"] = fv["Texto30"] = ""

    fv["Texto31"] = rh.first_surname           if rh else ""
    fv["Texto32"] = _s(rh.second_surname)      if rh else ""
    fv["Texto33"] = rh.name                    if rh else ""
    fv["Texto34"] = rh.date_of_birth.strftime("%d") if rh else ""
    fv["Texto35"] = rh.date_of_birth.strftime("%m") if rh else ""
    fv["Texto36"] = rh.date_of_birth.strftime("%Y") if rh else ""
    fv["Texto37"] = rh.birth_country           if rh else ""
    fv["Texto38"] = _s(rh.father_name)         if rh else ""
    fv["Texto39"] = _s(rh.mother_name)         if rh else ""
    fv["Texto40"] = rh.relationship            if rh else ""

    # Sexo / Estado civil of resource holder
    assign_checkboxes(fv, rh.gender.value if rh else None, {
        "Casilla de verificación12": "X",
        "Casilla de verificación13": "H",
        "Casilla de verificación14": "M",
    })
    assign_checkboxes(fv, rh.marital_status.value if rh else None, {
        "Casilla de verificación15": "S",
        "Casilla de verificación16": "C",
        "Casilla de verificación17": "V",
        "Casilla de verificación18": "D",
        "Casilla de verificación19": "Sp",
    })

    # -------------------------------------------------------------------------
    # Section 3 – DATOS DEL REPRESENTANTE A EFECTOS DE PRESENTACIÓN
    # -------------------------------------------------------------------------
    pres = form.presenter_details
    fv["Texto41"] = _s(pres.name_or_company) if pres else ""
    fv["Texto42"] = _s(pres.id_number)       if pres else ""
    fv["Texto43"] = _s(pres.address)         if pres else ""
    fv["Texto44"] = _s(pres.address_number)  if pres else ""
    fv["Texto45"] = _s(pres.floor_door)      if pres else ""
    fv["Texto46"] = _s(pres.city)            if pres else ""
    fv["Texto47"] = _s(pres.postal_code)     if pres else ""
    fv["Texto48"] = _s(pres.province)        if pres else ""
    fv["Texto49"] = _s(pres.mobile_phone)    if pres else ""
    fv["Texto50"] = _s(pres.email)           if pres else ""
    fv["Texto51"] = _s(pres.legal_rep_name)  if pres else ""
    fv["Texto52"] = _s(pres.legal_rep_id)    if pres else ""
    fv["Texto53"] = _s(pres.legal_rep_title) if pres else ""

    # -------------------------------------------------------------------------
    # Section 4 – DOMICILIO A EFECTOS DE NOTIFICACIONES
    # -------------------------------------------------------------------------
    notif = form.notification_address
    fv["Texto54"] = notif.name_or_company
    fv["Texto55"] = notif.id_number
    fv["Texto56"] = notif.address
    fv["Texto57"] = _s(notif.address_number)
    fv["Texto58"] = _s(notif.floor_door)
    fv["Texto59"] = notif.city
    fv["Texto60"] = notif.postal_code
    fv["Texto61"] = notif.province
    fv["Texto62"] = _s(notif.mobile_phone)
    fv["Texto63"] = _s(notif.email)
    fv["Casilla de verificación20"] = notif.consent_electronic_notifications

    # -------------------------------------------------------------------------
    # Section 5 – TIPO DE AUTORIZACIÓN SOLICITADA
    # -------------------------------------------------------------------------
    req = form.request_details
    cat = req.application_category
    role = req.applicant_role

    is_inicial   = cat == ApplicationCategoryEnum.RESIDENCIA_INICIAL
    is_renovacion = cat == ApplicationCategoryEnum.RENOVACION
    is_titular   = role == ApplicantRoleEnum.TITULAR_RECURSOS
    is_familiar  = role == ApplicantRoleEnum.FAMILIAR_TITULAR_RECURSOS

    fv["Casilla de verificación21"] = is_inicial
    fv["Casilla de verificación22"] = is_inicial and is_titular
    fv["Casilla de verificación23"] = is_inicial and is_familiar
    fv["Casilla de verificación24"] = is_renovacion
    fv["Casilla de verificación25"] = is_renovacion and is_titular
    fv["Casilla de verificación26"] = is_renovacion and is_familiar

    # -------------------------------------------------------------------------
    # Signature footer
    # -------------------------------------------------------------------------
    sig = form.signature
    fv["Texto64"] = sig.place
    fv["Texto65"] = sig.day
    fv["Texto66"] = sig.month
    fv["Texto67"] = sig.year
    fv["Texto68"] = _s(sig.name)

    # -------------------------------------------------------------------------
    # Office (DIRIGIDA A / DIR3 / PROVINCIA)
    # -------------------------------------------------------------------------
    off = form.office
    fv["Texto69"] = _s(off.target_office)
    fv["Texto70"] = _s(off.dir3_code)
    fv["Texto71"] = off.province

    return fv
