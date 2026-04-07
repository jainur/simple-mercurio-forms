"""Mapper for EX22 domain model to PDF field values."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any
from mappers.helpers import apply_enum_registry as _apply_enum_registry, coerce_str as _s, map_identity_person_block as _map_identity_person_block, map_notification_block as _map_notification_block, map_optional_object_fields as _map_optional_object_fields

if TYPE_CHECKING:
    from models.ex22 import EX22FormSchema


def to_field_values(form: EX22FormSchema) -> dict[str, Any]:
    from models.ex22 import ModificationGroundEnum, RequestCategoryEnum, WorkModeEnum

    fv: dict[str, Any] = {}

    a = form.applicant_details
    _map_identity_person_block(
        fv,
        a,
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
            "mobile_phone": "Texto16",
            "email": "Texto17",
            "legal_guardian_name": "Texto18",
            "legal_guardian_id": "Texto19",
            "legal_guardian_title": "Texto20",
        },
        gender_checkbox_map={
            "Casilla de verificación64": "X",
            "Casilla de verificación65": "H",
            "Casilla de verificación66": "M",
        },
        marital_checkbox_map={
            "Casilla de verificación67": "S",
            "Casilla de verificación68": "C",
            "Casilla de verificación69": "V",
            "Casilla de verificación70": "D",
            "Casilla de verificación71": "Sp",
        },
    )

    e = form.employer_details
    fv["Texto21"] = e.name_or_company
    fv["Texto22"] = e.id_number
    fv["Texto23"] = e.activity
    fv["Texto24"] = e.occupation
    fv["Texto25"] = e.address
    fv["Texto26"] = _s(e.address_number)
    fv["Texto27"] = _s(e.floor_door)
    fv["Texto28"] = e.city
    fv["Texto29"] = e.postal_code
    fv["Texto30"] = e.province

    r = form.filing_representative
    _map_optional_object_fields(
        fv,
        r,
        text_fields={
            "name_or_company": "Texto31",
            "id_number": "Texto32",
            "address": "Texto33",
            "address_number": "Texto34",
            "floor_door": "Texto35",
            "city": "Texto36",
            "postal_code": "Texto37",
            "province": "Texto38",
            "mobile_phone": "Texto39",
            "email": "Texto40",
            "legal_rep_name": "Texto41",
            "legal_rep_id": "Texto42",
            "legal_rep_title": "Texto43",
        },
    )

    n = form.notification_address
    _map_notification_block(
        fv,
        n,
        text_fields={
            "name_or_company": "Texto44",
            "id_number": "Texto45",
            "address": "Texto46",
            "address_number": "Texto47",
            "floor_door": "Texto48",
            "city": "Texto49",
            "postal_code": "Texto50",
            "province": "Texto51",
            "mobile_phone": "Texto52",
            "email": "Texto53",
        },
        consent_field="Casilla de verificación72",
    )

    req = form.request_details
    fv["Texto54"] = _s(req.identity_document_change_text)
    fv["Texto55"] = _s(req.cause_specification)

    is_initial = req.category == RequestCategoryEnum.INITIAL
    is_renewed = req.category == RequestCategoryEnum.RENEWED
    is_mod = req.category == RequestCategoryEnum.MODIFICATION
    is_dereg = req.category == RequestCategoryEnum.DEREGISTRATION

    _apply_enum_registry(fv, req.category, {
        "Casilla de verificación73": RequestCategoryEnum.INITIAL,
        "Casilla de verificación76": RequestCategoryEnum.RENEWED,
        "Casilla de verificación79": RequestCategoryEnum.MODIFICATION,
        "Casilla de verificación85": RequestCategoryEnum.DEREGISTRATION,
    })
    _apply_enum_registry(fv, req.work_mode, {
        "Casilla de verificación74": WorkModeEnum.EMPLOYEE,
        "Casilla de verificación75": WorkModeEnum.SELF_EMPLOYED,
    }, enabled=is_initial)
    _apply_enum_registry(fv, req.work_mode, {
        "Casilla de verificación77": WorkModeEnum.EMPLOYEE,
        "Casilla de verificación78": WorkModeEnum.SELF_EMPLOYED,
    }, enabled=is_renewed)

    _apply_enum_registry(fv, req.modification_ground, {
        "Casilla de verificación80": ModificationGroundEnum.PERSONAL_DATA,
        "Casilla de verificación81": ModificationGroundEnum.LABOR_OR_PROFESSIONAL_DATA,
        "Casilla de verificación82": ModificationGroundEnum.ADDRESS_CHANGE,
        "Casilla de verificación83": ModificationGroundEnum.IDENTITY_DOCUMENT_CHANGE,
        "Casilla de verificación84": ModificationGroundEnum.OTHER,
    }, enabled=is_mod)

    fv["Casilla de verificación86"] = bool(req.cause_specification)
    fv["Casilla de verificación87"] = req.truth_statement_accepted

    s = form.signature
    fv["Texto56"] = s.place
    fv["Texto57"] = s.day
    fv["Texto58"] = s.month
    fv["Texto59"] = s.year
    fv["Texto60"] = _s(s.name)

    o = form.office
    fv["Texto61"] = _s(o.target_office)
    fv["Texto62"] = _s(o.dir3_code)
    fv["Texto63"] = o.province

    return fv
