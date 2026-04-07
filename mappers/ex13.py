"""Mapper for EX13 domain model to PDF field values."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any
from mappers.helpers import apply_enum_registry as _apply_enum_registry, coerce_str as _s, map_identity_person_block as _map_identity_person_block, map_notification_block as _map_notification_block, map_optional_object_fields as _map_optional_object_fields

if TYPE_CHECKING:
    from models.ex13 import EX13FormSchema


def to_field_values(form: EX13FormSchema) -> dict[str, Any]:
    from models.ex13 import ReturnAuthorizationGroundEnum

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
            "Casilla de verificación27": "X",
            "Casilla de verificación28": "H",
            "Casilla de verificación29": "M",
        },
        marital_checkbox_map={
            "Casilla de verificación30": "S",
            "Casilla de verificación31": "C",
            "Casilla de verificación32": "V",
            "Casilla de verificación33": "D",
            "Casilla de verificación34": "Sp",
        },
    )

    # Section 2: Filing representative
    r = form.filing_representative
    _map_optional_object_fields(
        fv,
        r,
        text_fields={
            "name_or_company": "Texto42",
            "id_number": "Texto43",
            "address": "Texto44",
            "address_number": "Texto45",
            "floor_door": "Texto46",
            "city": "Texto47",
            "postal_code": "Texto48",
            "province": "Texto49",
            "mobile_phone": "Texto50",
            "email": "Texto51",
            "legal_rep_name": "Texto52",
            "legal_rep_id": "Texto53",
            "legal_rep_title": "Texto54",
        },
    )

    # Section 3: Notification
    n = form.notification_address
    _map_notification_block(
        fv,
        n,
        text_fields={
            "name_or_company": "Texto55",
            "id_number": "Texto56",
            "address": "Texto57",
            "address_number": "Texto58",
            "floor_door": "Texto59",
            "city": "Texto60",
            "postal_code": "Texto61",
            "province": "Texto62",
            "mobile_phone": "Texto63",
            "email": "Texto64",
        },
        consent_field="Casilla de verificación35",
    )

    # Section 4: Grounds + signature + office
    req = form.request_details
    _apply_enum_registry(fv, req.ground, {
        "Casilla de verificación36": ReturnAuthorizationGroundEnum.RESIDENCE_RENEWAL_OR_EXTENSION_ART_5,
        "Casilla de verificación37": ReturnAuthorizationGroundEnum.STAY_EXTENSION_ART_5,
        "Casilla de verificación38": ReturnAuthorizationGroundEnum.TIE_DUPLICATE_THEFT_LOSS_DAMAGE_ART_5,
        "Casilla de verificación39": ReturnAuthorizationGroundEnum.INITIAL_RESIDENCE_TIE_ISSUANCE_EXCEPTIONAL_REASONS_ART_5,
        "Casilla de verificación40": ReturnAuthorizationGroundEnum.INITIAL_STAY_TIE_ISSUANCE_EXCEPTIONAL_REASONS_ART_5,
        "Casilla de verificación41": ReturnAuthorizationGroundEnum.OTHER,
    })

    # The form has 3 separate 'Otros' text boxes in extracted widgets.
    fv["Texto74"] = _s(req.other_reason_text_1)
    fv["Texto75"] = _s(req.other_reason_text_2)
    fv["Texto27"] = _s(req.other_reason_text_3)

    sig = form.signature
    fv["Texto66"] = sig.place
    fv["Texto67"] = sig.day
    fv["Texto68"] = sig.month
    fv["Texto69"] = sig.year
    fv["Texto70"] = _s(sig.name)

    off = form.office
    fv["Texto71"] = _s(off.target_office)
    fv["Texto72"] = _s(off.dir3_code)
    fv["Texto73"] = off.province

    return fv
