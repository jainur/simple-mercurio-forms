"""Mapper for EX29 domain model to PDF field values."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any
from mappers.helpers import map_identity_person_block as _map_identity_person_block, map_notification_block as _map_notification_block, map_optional_object_fields as _map_optional_object_fields, coerce_str as _s

if TYPE_CHECKING:
    from models.ex29 import EX29FormSchema


def to_field_values(form: EX29FormSchema) -> dict[str, Any]:
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
            "legal_representative_name": "Texto24",
            "legal_representative_id": "Texto25",
            "legal_representative_title": "Texto26",
        },
        gender_checkbox_map={
            "Casilla de verificación60": "X",
            "Casilla de verificación61": "H",
            "Casilla de verificación62": "M",
        },
        marital_checkbox_map={
            "Casilla de verificación63": "S",
            "Casilla de verificación64": "C",
            "Casilla de verificación65": "V",
            "Casilla de verificación66": "D",
            "Casilla de verificación67": "Sp",
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
            "legal_representative_name": "Texto37",
            "legal_representative_id": "Texto38",
            "legal_representative_title": "Texto39",
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
        consent_field="Casilla de verificación68",
    )

    e = form.extension_request
    fv["Texto50"] = _s(e.other_description)
    fv["Texto51"] = e.justification_and_extension_period
    fv["Casilla de verificación69"] = e.ordinary_stay_without_visa
    fv["Casilla de verificación70"] = e.short_stay_visa_holder
    fv["Casilla de verificación71"] = e.displaced_minor_medical_treatment
    fv["Casilla de verificación72"] = e.other

    s = form.signature
    fv["Texto52"] = s.place
    fv["Texto53"] = s.day
    fv["Texto54"] = s.month
    fv["Texto55"] = s.year
    fv["Texto56"] = _s(s.signer_name)

    o = form.office
    fv["Texto57"] = _s(o.target_office)
    fv["Texto58"] = _s(o.dir3_code)
    fv["Texto59"] = o.province

    return fv