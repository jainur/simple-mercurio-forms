"""Mapper for EX06 domain model to PDF field values."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any
from app.mappers.helpers import apply_enum_registry as _apply_enum_registry, coerce_str as _s, map_identity_person_block as _map_identity_person_block, map_notification_block as _map_notification_block, map_optional_object_fields as _map_optional_object_fields

if TYPE_CHECKING:
    from models.ex06 import EX06FormSchema


def to_field_values(form: EX06FormSchema) -> dict[str, Any]:
    from models.ex06 import ApplicationTypeEnum

    fv: dict[str, Any] = {}

    # Section 1: Foreigner
    f = form.foreigner_details
    _map_identity_person_block(
        fv,
        f,
        passport_field="Texto1",
        nie_fields=("Texto3", "Texto4", "Texto5"),
        date_fields=("Texto12", "Texto13", "Texto14"),
        text_fields={
            "first_surname": "Texto6",
            "second_surname": "Texto7",
            "name": "Texto8",
            "birth_place": "Texto15",
            "birth_country": "Texto16",
            "nationality": "Texto17",
            "father_name": "Texto23",
            "mother_name": "Texto24",
            "address": "Texto25",
            "address_number": "Texto26",
            "floor_door": "Texto27",
            "city": "Texto28",
            "postal_code": "Texto29",
            "province": "Texto30",
            "mobile_phone": "Texto31",
            "email": "Texto32",
            "legal_guardian_name": "Texto33",
            "legal_guardian_id": "Texto34",
            "legal_guardian_title": "Texto35",
        },
        gender_checkbox_map={
            "Casilla de verificación9": "X",
            "Casilla de verificación10": "H",
            "Casilla de verificación11": "M",
        },
        marital_checkbox_map={
            "Casilla de verificación18": "S",
            "Casilla de verificación19": "C",
            "Casilla de verificación20": "V",
            "Casilla de verificación21": "D",
            "Casilla de verificación22": "Sp",
        },
    )

    # Section 2: Employer
    e = form.employer_details
    fv["Texto36"] = e.name_or_company
    fv["Texto37"] = e.id_number
    fv["Texto38"] = e.activity
    fv["Texto39"] = e.occupation
    fv["Texto40"] = e.address
    fv["Texto41"] = _s(e.address_number)
    fv["Texto42"] = _s(e.floor_door)
    fv["Texto43"] = e.city
    fv["Texto44"] = e.postal_code
    fv["Texto45"] = e.province
    fv["Texto46"] = _s(e.mobile_phone)
    fv["Texto47"] = _s(e.email)
    fv["Texto48"] = _s(e.legal_rep_name)
    fv["Texto49"] = _s(e.legal_rep_id)

    # Section 3: Filing representative
    r = form.filing_representative
    _map_optional_object_fields(
        fv,
        r,
        text_fields={
            "name_or_company": "Texto50",
            "id_number": "Texto51",
            "address": "Texto52",
            "address_number": "Texto53",
            "floor_door": "Texto54",
            "city": "Texto55",
            "postal_code": "Texto56",
            "province": "Texto57",
            "mobile_phone": "Texto58",
            "email": "Texto59",
            "legal_rep_name": "Texto60",
            "legal_rep_id": "Texto61",
            "legal_rep_title": "Texto62",
        },
    )

    # Section 4: Notification
    n = form.notification_address
    _map_notification_block(
        fv,
        n,
        text_fields={
            "name_or_company": "Texto63",
            "id_number": "Texto64",
            "address": "Texto65",
            "address_number": "Texto66",
            "floor_door": "Texto67",
            "city": "Texto68",
            "postal_code": "Texto69",
            "province": "Texto70",
            "mobile_phone": "Texto71",
            "email": "Texto72",
        },
        consent_field="Casilla de verificación73",
    )

    # Section 5: Request + signature + office
    req = form.request_details
    _apply_enum_registry(fv, req.application_type, {
        "Casilla de verificación74": ApplicationTypeEnum.RESIDENCIA_INICIAL,
        "Casilla de verificación75": ApplicationTypeEnum.PRIMER_LLAMAMIENTO,
        "Casilla de verificación76": ApplicationTypeEnum.SEGUNDO_LLAMAMIENTO,
        "Casilla de verificación77": ApplicationTypeEnum.TERCER_LLAMAMIENTO,
        "Casilla de verificación78": ApplicationTypeEnum.CAMBIO_EMPLEADOR,
        "Casilla de verificación79": ApplicationTypeEnum.PRORROGA_O_CONCATENACION,
        "Casilla de verificación80": ApplicationTypeEnum.RENOVACION_PLURIANUAL,
    })
    fv["Casilla de verificación81"] = req.accepts_truth_responsibility

    s = form.signature
    fv["Texto82"] = s.place
    fv["Texto83"] = s.day
    fv["Texto84"] = s.month
    fv["Texto85"] = s.year
    fv["Texto86"] = _s(s.name)

    o = form.office
    fv["Texto87"] = _s(o.target_office)
    fv["Texto88"] = _s(o.dir3_code)
    fv["Texto89"] = o.province

    return fv
