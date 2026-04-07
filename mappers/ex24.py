"""Mapper for EX24 domain model to PDF field values."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any
from mappers.helpers import apply_enum_registry as _apply_enum_registry, assign_checkboxes, coerce_str as _s, map_identity_person_block as _map_identity_person_block, map_notification_block as _map_notification_block, map_optional_object_fields as _map_optional_object_fields, split_nie as _split_nie

if TYPE_CHECKING:
    from models.ex24 import EX24FormSchema


def to_field_values(form: EX24FormSchema) -> dict[str, Any]:
    from models.ex24 import (
        InitialRelationshipEnum,
        PreservationGroundEnum,
        RequestCategoryEnum,
    )

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

    s = form.spanish_family_member_details
    fv["Texto35"] = _s(s.passport)
    fv["Texto36"] = _s(s.dni)
    fv["Texto37"] = _s(s.title)
    fv["Texto38"] = s.first_surname
    fv["Texto39"] = _s(s.second_surname)
    fv["Texto40"] = s.name
    fv["Texto41"] = s.date_of_birth.strftime("%d")
    fv["Texto42"] = s.date_of_birth.strftime("%m")
    fv["Texto43"] = s.date_of_birth.strftime("%Y")
    fv["Texto44"] = s.birth_country
    fv["Texto45"] = _s(s.father_name)
    fv["Texto46"] = _s(s.mother_name)
    fv["Texto47"] = s.address
    fv["Texto48"] = _s(s.address_number)
    fv["Texto49"] = _s(s.floor_door)
    fv["Texto50"] = s.city
    fv["Texto51"] = s.postal_code
    fv["Texto52"] = s.province
    fv["Texto53"] = s.relationship_with_applicant

    assign_checkboxes(fv, s.gender.value, {
        "Casilla de verificación54": "X",
        "Casilla de verificación55": "H",
        "Casilla de verificación56": "M",
    })
    assign_checkboxes(fv, s.marital_status.value, {
        "Casilla de verificación57": "S",
        "Casilla de verificación58": "C",
        "Casilla de verificación59": "V",
        "Casilla de verificación60": "D",
        "Casilla de verificación61": "Sp",
    })

    r = form.filing_representative
    _map_optional_object_fields(
        fv,
        r,
        text_fields={
            "name_or_company": "Texto62",
            "id_number": "Texto63",
            "address": "Texto64",
            "address_number": "Texto65",
            "floor_door": "Texto66",
            "city": "Texto67",
            "postal_code": "Texto68",
            "province": "Texto69",
            "mobile_phone": "Texto70",
            "email": "Texto71",
            "legal_rep_name": "Texto72",
            "legal_rep_id": "Texto73",
            "legal_rep_title": "Texto74",
        },
    )

    n = form.notification_address
    _map_notification_block(
        fv,
        n,
        text_fields={
            "name_or_company": "Texto75",
            "id_number": "Texto76",
            "address": "Texto77",
            "address_number": "Texto78",
            "floor_door": "Texto79",
            "city": "Texto80",
            "postal_code": "Texto81",
            "province": "Texto82",
            "mobile_phone": "Texto83",
            "email": "Texto84",
        },
        consent_field="Casilla de verificación85",
    )

    req = form.request_details
    is_initial = req.category == RequestCategoryEnum.INITIAL_RESIDENCE
    is_renewal = req.category == RequestCategoryEnum.RENEWAL
    is_independent = req.category == RequestCategoryEnum.INDEPENDENT_RESIDENCE_BY_PRESERVATION

    _apply_enum_registry(fv, req.category, {
        "Casilla de verificación86": RequestCategoryEnum.INITIAL_RESIDENCE,
        "Casilla de verificación95": RequestCategoryEnum.RENEWAL,
        "Casilla de verificación96": RequestCategoryEnum.INDEPENDENT_RESIDENCE_BY_PRESERVATION,
    })
    _apply_enum_registry(fv, req.initial_relationship, {
        "Casilla de verificación87": InitialRelationshipEnum.SPOUSE_OR_REGISTERED_OR_STABLE_PARTNER,
        "Casilla de verificación88": InitialRelationshipEnum.CHILD_UNDER_26_OR_DISABLED,
        "Casilla de verificación89": InitialRelationshipEnum.CHILD_OVER_26_DEPENDENT,
        "Casilla de verificación90": InitialRelationshipEnum.FIRST_DEGREE_ASCENDANT,
        "Casilla de verificación91": InitialRelationshipEnum.PARENT_OR_GUARDIAN_OF_SPANISH_MINOR,
        "Casilla de verificación92": InitialRelationshipEnum.CAREGIVER_UP_TO_SECOND_DEGREE,
        "Casilla de verificación93": InitialRelationshipEnum.CHILD_OF_SPANISH_PARENT_BY_ORIGIN,
        "Casilla de verificación94": InitialRelationshipEnum.OTHER_DEPENDENT_FAMILY_MEMBER,
    }, enabled=is_initial)
    _apply_enum_registry(fv, req.preservation_ground, {
        "Casilla de verificación97": PreservationGroundEnum.DEATH_OF_SPANISH_NATIONAL,
        "Casilla de verificación98": PreservationGroundEnum.END_OF_EFFECTIVE_RESIDENCE_IN_SPAIN,
        "Casilla de verificación99": PreservationGroundEnum.NULLITY_DIVORCE_OR_CANCELLATION,
        "Casilla de verificación100": PreservationGroundEnum.VICTIM_OF_GENDER_OR_SEXUAL_VIOLENCE_OR_FAMILY_VIOLENCE_OR_TRAFFICKING,
    }, enabled=is_independent)

    sig = form.signature
    fv["Texto101"] = sig.place
    fv["Texto102"] = sig.day
    fv["Texto103"] = sig.month
    fv["Texto104"] = sig.year
    fv["Texto105"] = _s(sig.name)

    off = form.office
    fv["Texto106"] = _s(off.target_office)
    fv["Texto107"] = _s(off.dir3_code)
    fv["Texto108"] = off.province

    return fv
