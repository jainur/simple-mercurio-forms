"""Mapper for EX09 domain model to PDF field values."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any
from mappers.helpers import apply_enum_registry as _apply_enum_registry, coerce_str as _s, map_identity_person_block as _map_identity_person_block, map_notification_block as _map_notification_block, map_optional_object_fields as _map_optional_object_fields

if TYPE_CHECKING:
    from models.ex09 import EX09FormSchema


def to_field_values(form: EX09FormSchema) -> dict[str, Any]:
    from models.ex09 import ApplicationCategoryEnum, InitialExceptionSubtypeEnum

    fv: dict[str, Any] = {}

    # Section 1: Foreigner
    f = form.foreigner_details
    _map_identity_person_block(
        fv,
        f,
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
        },
        gender_checkbox_map={
            "Casilla de verificación79": "X",
            "Casilla de verificación80": "H",
            "Casilla de verificación81": "M",
        },
        marital_checkbox_map={
            "Casilla de verificación71": "S",
            "Casilla de verificación72": "C",
            "Casilla de verificación73": "V",
            "Casilla de verificación74": "D",
            "Casilla de verificación75": "Sp",
        },
    )
    fv["Casilla de verificación76"] = f.children_in_school_age
    fv["Casilla de verificación77"] = not f.children_in_school_age

    # Section 2: Activity entity
    a = form.activity_entity_details
    fv["Texto24"] = a.name_or_company
    fv["Texto25"] = a.id_number
    fv["Texto26"] = a.activity
    fv["Texto27"] = a.occupation
    fv["Texto28"] = a.address
    fv["Texto29"] = _s(a.address_number)
    fv["Texto30"] = _s(a.floor_door)
    fv["Texto31"] = a.city
    fv["Texto32"] = a.postal_code
    fv["Texto33"] = a.province
    fv["Texto34"] = _s(a.mobile_phone)
    fv["Texto35"] = _s(a.email)
    fv["Texto36"] = _s(a.legal_rep_name)
    fv["Texto37"] = _s(a.legal_rep_id)
    fv["Texto38"] = _s(a.legal_rep_title)

    # Section 3: Filing representative
    r = form.filing_representative
    _map_optional_object_fields(
        fv,
        r,
        text_fields={
            "name_or_company": "Texto39",
            "id_number": "Texto40",
            "address": "Texto41",
            "address_number": "Texto42",
            "floor_door": "Texto43",
            "city": "Texto44",
            "postal_code": "Texto45",
            "province": "Texto46",
            "mobile_phone": "Texto47",
            "email": "Texto48",
            "legal_rep_name": "Texto49",
            "legal_rep_id": "Texto50",
            "legal_rep_title": "Texto51",
        },
    )

    # Section 4: Notification
    n = form.notification_address
    _map_notification_block(
        fv,
        n,
        text_fields={
            "name_or_company": "Texto52",
            "id_number": "Texto53",
            "address": "Texto54",
            "address_number": "Texto55",
            "floor_door": "Texto56",
            "city": "Texto57",
            "postal_code": "Texto58",
            "province": "Texto59",
            "mobile_phone": "Texto60",
            "email": "Texto61",
        },
        consent_field="Casilla de verificación78",
    )

    # Section 5: Request + signature + office
    req = form.request_details
    is_initial = req.category == ApplicationCategoryEnum.INITIAL_EXCEPTION
    is_extension = req.category == ApplicationCategoryEnum.EXTENSION

    fv["Casilla de verificación82"] = is_initial
    fv["Casilla de verificación83"] = is_initial and req.initial_subtype == InitialExceptionSubtypeEnum.RELIGIOUS_MEMBER
    fv["Casilla de verificación84"] = is_initial and req.initial_subtype == InitialExceptionSubtypeEnum.OTHER
    fv["Texto62"] = _s(req.other_initial_exception_details)

    fv["Casilla de verificación85"] = is_extension
    fv["Casilla de verificación86"] = is_extension

    s = form.signature
    fv["Texto63"] = s.place
    fv["Texto67"] = s.day
    fv["Texto64"] = s.month
    fv["Texto65"] = s.year
    fv["Texto66"] = _s(s.name)

    o = form.office
    fv["Texto68"] = _s(o.target_office)
    fv["Texto69"] = _s(o.dir3_code)
    fv["Texto70"] = o.province

    return fv
