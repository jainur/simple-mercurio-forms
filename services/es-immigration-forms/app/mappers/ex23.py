"""Mapper for EX23 domain model to PDF field values."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any
from app.mappers.helpers import apply_enum_registry as _apply_enum_registry, coerce_str as _s, map_identity_person_block as _map_identity_person_block, map_notification_block as _map_notification_block, map_optional_object_fields as _map_optional_object_fields

if TYPE_CHECKING:
    from models.ex23 import EX23FormSchema


def to_field_values(form: EX23FormSchema) -> dict[str, Any]:
    from models.ex23 import AdditionalEuRegistrationOptionEnum, ResidenceStatusEnum

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

    req = form.request_details
    _apply_enum_registry(fv, req.residence_status, {
        "Casilla de verificación10": ResidenceStatusEnum.INITIAL_WITHOUT_PREVIOUS_REGISTRATION,
        "Casilla de verificación11": ResidenceStatusEnum.WITH_EU_REGISTRATION_CERTIFICATE,
        "Casilla de verificación12": ResidenceStatusEnum.TEMPORARY_WITH_UK_FAMILY_CARD,
        "Casilla de verificación13": ResidenceStatusEnum.PERMANENT_WITH_UK_FAMILY_CARD,
        "Casilla de verificación14": ResidenceStatusEnum.OTHER,
    })
    _apply_enum_registry(fv, req.additional_eu_registration_option, {
        "Casilla de verificación15": AdditionalEuRegistrationOptionEnum.OPTION_15,
        "Casilla de verificación16": AdditionalEuRegistrationOptionEnum.OPTION_16,
        "Casilla de verificación17": AdditionalEuRegistrationOptionEnum.OPTION_17,
    })
    fv["Texto58"] = _s(req.other_status_text)

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
