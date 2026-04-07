"""Mapper for EX30 domain model to PDF field values."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any
from mappers.helpers import apply_enum_registry as _apply_enum_registry, map_identity_person_block as _map_identity_person_block, map_notification_block as _map_notification_block, map_optional_object_fields as _map_optional_object_fields, coerce_str as _s

if TYPE_CHECKING:
    from models.ex30 import EX30FormSchema


def to_field_values(form: EX30FormSchema) -> dict[str, Any]:
    from models.ex30 import AuthorizationTypeEnum

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
        consent_field="Casilla de verificación9",
    )

    e = form.employer_details
    fv["Texto50"] = _s(e.name_or_company) if e else ""
    fv["Texto51"] = _s(e.tax_or_id_number) if e else ""
    fv["Texto52"] = _s(e.activity) if e else ""
    fv["Texto53"] = _s(e.cnae) if e else ""
    fv["Texto54"] = _s(e.cno_spe_2011) if e else ""
    fv["Texto55"] = _s(e.registered_address) if e else ""
    fv["Texto56"] = _s(e.address_number) if e else ""
    fv["Texto57"] = _s(e.floor_door) if e else ""
    fv["Texto58"] = _s(e.city) if e else ""
    fv["Texto59"] = _s(e.postal_code) if e else ""
    fv["Texto60"] = _s(e.province) if e else ""
    fv["Texto61"] = _s(e.mobile_phone) if e else ""
    fv["Texto62"] = _s(e.email) if e else ""
    fv["Texto63"] = _s(e.representative_name) if e else ""
    fv["Texto64"] = _s(e.representative_id) if e else ""
    fv["Texto65"] = _s(e.representative_title) if e else ""

    t = form.training_center_details
    fv["Texto66"] = _s(t.provider_name) if t else ""
    fv["Texto67"] = _s(t.training_name) if t else ""
    fv["Texto68"] = _s(t.course_code) if t else ""
    fv["Texto69"] = _s(t.provider_tax_id) if t else ""
    fv["Texto70"] = _s(t.provider_address) if t else ""
    fv["Texto71"] = _s(t.province) if t else ""
    fv["Texto72"] = _s(t.duration_hours) if t else ""
    fv["Texto73"] = _s(t.start_date) if t else ""
    fv["Texto74"] = _s(t.end_date) if t else ""
    fv["Casilla de verificación10"] = bool(t and t.secondary_post_compulsory_education)
    fv["Casilla de verificación11"] = bool(t and t.professional_certificate)
    fv["Casilla de verificación12"] = bool(t and t.adult_mandatory_education_in_person)
    fv["Casilla de verificación13"] = bool(t and t.public_employment_service_training)
    fv["Casilla de verificación14"] = bool(t and t.modality_presential)
    fv["Casilla de verificación15"] = bool(t and t.modality_non_presential)
    fv["Casilla de verificación16"] = bool(t and t.date_range_checkbox)

    req = form.request_details
    fv["Casilla de verificación17"] = True
    _apply_enum_registry(fv, req.authorization_type, {
        "Casilla de verificación18": AuthorizationTypeEnum.SECOND_CHANCE,
        "Casilla de verificación19": AuthorizationTypeEnum.SOCIOLABORAL,
        "Casilla de verificación20": AuthorizationTypeEnum.SOCIAL,
        "Casilla de verificación21": AuthorizationTypeEnum.SOCIOFORMATIVO,
    })

    s = form.signature
    fv["Texto75"] = s.place
    fv["Texto76"] = s.day
    fv["Texto77"] = s.month
    fv["Texto78"] = s.year
    fv["Texto79"] = _s(s.signer_name)

    o = form.office
    fv["Texto80"] = _s(o.target_office)
    fv["Texto81"] = _s(o.dir3_code)
    fv["Texto82"] = o.province

    return fv