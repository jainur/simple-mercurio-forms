"""Mapper for EX16 domain model to PDF field values."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any
from mappers.helpers import apply_enum_registry as _apply_enum_registry, coerce_str as _s, map_identity_person_block as _map_identity_person_block, map_notification_block as _map_notification_block, map_optional_object_fields as _map_optional_object_fields

if TYPE_CHECKING:
    from models.ex16 import EX16FormSchema


def to_field_values(form: EX16FormSchema) -> dict[str, Any]:
    from models.ex16 import AuthorizationStageEnum, ReturnModeEnum, TravelDocumentTypeEnum

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
    fv["Texto50"] = req.destination

    fv["Casilla de verificación10"] = req.reason_humanitarian
    fv["Casilla de verificación11"] = req.reason_public_interest
    fv["Casilla de verificación12"] = req.reason_spain_commitments
    fv["Casilla de verificación13"] = req.reason_exceptional_circumstances

    _apply_enum_registry(fv, req.stage, {
        "Casilla de verificación14": AuthorizationStageEnum.RENEWAL,
        "Casilla de verificación15": AuthorizationStageEnum.INITIAL,
    })
    _apply_enum_registry(fv, req.document_type, {
        "Casilla de verificación16": TravelDocumentTypeEnum.TRAVEL_TITLE,
    })
    _apply_enum_registry(fv, req.return_mode, {
        "Casilla de verificación17": ReturnModeEnum.WITH_RETURN,
        "Casilla de verificación18": ReturnModeEnum.WITHOUT_RETURN,
    })

    fv["Casilla de verificación19"] = req.title_motivos_checkbox
    fv["Casilla de verificación20"] = req.title_reason_humanitarian
    fv["Casilla de verificación21"] = req.title_reason_public_interest

    sig = form.signature
    fv["Texto51"] = sig.place
    fv["Texto52"] = sig.day
    fv["Texto53"] = sig.month
    fv["Texto54"] = sig.year
    fv["Texto55"] = _s(sig.name)

    off = form.office
    fv["Texto56"] = _s(off.target_office)
    fv["Texto57"] = _s(off.dir3_code)
    fv["Texto58"] = off.province

    return fv
