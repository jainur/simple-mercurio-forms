"""Mapper for EX17 domain model to PDF field values."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any
from mappers.helpers import apply_enum_registry as _apply_enum_registry, coerce_str as _s, map_identity_person_block as _map_identity_person_block, map_notification_block as _map_notification_block, map_optional_object_fields as _map_optional_object_fields

if TYPE_CHECKING:
    from models.ex17 import EX17FormSchema


def to_field_values(form: EX17FormSchema) -> dict[str, Any]:
    from models.ex17 import CardRequestTypeEnum

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
            "legal_guardian_name": "Texto24",
            "legal_guardian_id": "Texto25",
            "legal_guardian_title": "Texto26",
        },
        gender_checkbox_map={
            "Casilla de verificación1": "X",
            "Casilla de verificación2": "H",
            "Casilla de verificación3": "M",
        },
        marital_checkbox_map={
            "Casilla de verificación4": "S",
            "Casilla de verificación5": "C",
            "Casilla de verificación6": "V",
            "Casilla de verificación7": "D",
            "Casilla de verificación8": "Sp",
        },
    )

    # Section 2: Filing representative
    r = form.filing_representative
    _map_optional_object_fields(
        fv,
        r,
        text_fields={
            "name_or_company": "Texto27",
            "id_number": "Texto28",
            "address": "Texto29",
            "address_number": "Texto30",
            "floor_door": "Texto31",
            "city": "Texto32",
            "postal_code": "Texto33",
            "province": "Texto34",
            "mobile_phone": "Texto35",
            "email": "Texto36",
            "legal_rep_name": "Texto37",
            "legal_rep_id": "Texto38",
            "legal_rep_title": "Texto39",
        },
    )

    # Section 3: Notification
    n = form.notification_address
    _map_notification_block(
        fv,
        n,
        text_fields={
            "name_or_company": "Texto40",
            "id_number": "Texto41",
            "address": "Texto42",
            "address_number": "Texto43",
            "floor_door": "Texto44",
            "city": "Texto45",
            "postal_code": "Texto46",
            "province": "Texto47",
            "mobile_phone": "Texto48",
            "email": "Texto49",
        },
        consent_field="Casilla de verificación9",
    )

    # Section 4: Request + signature + office
    req = form.request_details
    _apply_enum_registry(fv, req.card_request_type, {
        "Casilla de verificación10": CardRequestTypeEnum.INITIAL_CARD,
        "Casilla de verificación11": CardRequestTypeEnum.CARD_RENEWAL,
        "Casilla de verificación12": CardRequestTypeEnum.DUPLICATE_LOSS_THEFT_DAMAGE_OR_DATA_CHANGE,
    })

    s = form.signature
    fv["Texto50"] = s.place
    fv["Texto51"] = s.day
    fv["Texto52"] = s.month
    fv["Texto53"] = s.year
    fv["Texto54"] = _s(s.name)

    o = form.office
    fv["Texto55"] = _s(o.target_office)
    fv["Texto56"] = _s(o.dir3_code)
    fv["Texto57"] = o.province

    return fv
