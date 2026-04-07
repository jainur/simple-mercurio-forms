"""
Mapper: EX01FormSchema → field_values dict understood by fill_form.fill_form()

Every PDF widget name is mapped explicitly, auditable against
forms/definitions/EX01.json (96 fields).
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any
from mappers.helpers import apply_enum_registry as _apply_enum_registry, coerce_str as _s, map_identity_person_block as _map_identity_person_block, map_notification_block as _map_notification_block, map_optional_object_fields as _map_optional_object_fields, split_nie as _split_nie

if TYPE_CHECKING:
    from models.ex01 import EX01FormSchema



def to_field_values(form: EX01FormSchema) -> dict[str, Any]:
    from models.ex01 import ApplicationCategoryEnum, ApplicantRoleEnum

    fv: dict[str, Any] = {}

    # -------------------------------------------------------------------------
    # Section 1 – DATOS DE LA PERSONA EXTRANJERA SOLICITANTE
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
            "Casilla de verificación9": "Sp",
            "Casilla de verificación8": "D",
        },
    )

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
    _apply_enum_registry(fv, rh.gender if rh else None, {
        "Casilla de verificación12": "X",
        "Casilla de verificación13": "H",
        "Casilla de verificación14": "M",
    })
    _apply_enum_registry(fv, rh.marital_status if rh else None, {
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
    _map_optional_object_fields(
        fv,
        pres,
        text_fields={
            "name_or_company": "Texto41",
            "id_number": "Texto42",
            "address": "Texto43",
            "address_number": "Texto44",
            "floor_door": "Texto45",
            "city": "Texto46",
            "postal_code": "Texto47",
            "province": "Texto48",
            "mobile_phone": "Texto49",
            "email": "Texto50",
            "legal_rep_name": "Texto51",
            "legal_rep_id": "Texto52",
            "legal_rep_title": "Texto53",
        },
    )

    # -------------------------------------------------------------------------
    # Section 4 – DOMICILIO A EFECTOS DE NOTIFICACIONES
    # -------------------------------------------------------------------------
    notif = form.notification_address
    _map_notification_block(
        fv,
        notif,
        text_fields={
            "name_or_company": "Texto54",
            "id_number": "Texto55",
            "address": "Texto56",
            "address_number": "Texto57",
            "floor_door": "Texto58",
            "city": "Texto59",
            "postal_code": "Texto60",
            "province": "Texto61",
            "mobile_phone": "Texto62",
            "email": "Texto63",
        },
        consent_field="Casilla de verificación20",
    )

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

    _apply_enum_registry(fv, cat, {
        "Casilla de verificación21": ApplicationCategoryEnum.RESIDENCIA_INICIAL,
        "Casilla de verificación24": ApplicationCategoryEnum.RENOVACION,
    })
    _apply_enum_registry(fv, role, {
        "Casilla de verificación22": ApplicantRoleEnum.TITULAR_RECURSOS,
        "Casilla de verificación23": ApplicantRoleEnum.FAMILIAR_TITULAR_RECURSOS,
    }, enabled=is_inicial)
    _apply_enum_registry(fv, role, {
        "Casilla de verificación25": ApplicantRoleEnum.TITULAR_RECURSOS,
        "Casilla de verificación26": ApplicantRoleEnum.FAMILIAR_TITULAR_RECURSOS,
    }, enabled=is_renovacion)

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
