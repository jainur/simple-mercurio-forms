"""Mapper for EX20 domain model to PDF field values."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any
from mappers.helpers import apply_enum_registry as _apply_enum_registry, coerce_str as _s, map_identity_person_block as _map_identity_person_block, map_notification_block as _map_notification_block, map_optional_object_fields as _map_optional_object_fields

if TYPE_CHECKING:
    from models.ex20 import EX20FormSchema


def to_field_values(form: EX20FormSchema) -> dict[str, Any]:
    from models.ex20 import (
        MainRequestCategoryEnum,
        ModificationGroundEnum,
        PermanentResidenceGroundEnum,
        TemporaryResidenceGroundEnum,
    )

    fv: dict[str, Any] = {}

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

    r = form.filing_representative
    _map_optional_object_fields(
        fv,
        r,
        text_fields={
            "name_or_company": "Texto35",
            "id_number": "Texto36",
            "address": "Texto37",
            "address_number": "Texto38",
            "floor_door": "Texto39",
            "city": "Texto40",
            "postal_code": "Texto41",
            "province": "Texto42",
            "mobile_phone": "Texto43",
            "email": "Texto44",
            "legal_rep_name": "Texto45",
            "legal_rep_id": "Texto46",
            "legal_rep_title": "Texto47",
        },
    )

    n = form.notification_address
    _map_notification_block(
        fv,
        n,
        text_fields={
            "name_or_company": "Texto48",
            "id_number": "Texto49",
            "address": "Texto50",
            "address_number": "Texto51",
            "floor_door": "Texto52",
            "city": "Texto53",
            "postal_code": "Texto54",
            "province": "Texto55",
            "mobile_phone": "Texto56",
            "email": "Texto57",
        },
        consent_field="Casilla de verificación76",
    )

    req = form.request_details
    fv["Texto58"] = req.residence_start_segment_1
    fv["Texto59"] = req.residence_start_segment_2
    fv["Texto60"] = req.residence_start_segment_3
    fv["Texto61"] = req.residence_start_segment_4
    fv["Texto62"] = _s(req.uk_national_document_id)
    fv["Texto63"] = _s(req.relationship_with_uk_national)
    fv["Texto64"] = _s(req.incapacity_with_spanish_spouse_text)
    fv["Texto65"] = _s(req.identity_document_change_text)
    fv["Texto66"] = _s(req.cause_specification)

    is_temp = req.category == MainRequestCategoryEnum.TEMPORARY_RESIDENCE
    is_perm = req.category == MainRequestCategoryEnum.PERMANENT_RESIDENCE
    is_mod = req.category == MainRequestCategoryEnum.MODIFICATION
    is_dereg = req.category == MainRequestCategoryEnum.DEREGISTRATION

    _apply_enum_registry(fv, req.category, {
        "Casilla de verificación77": MainRequestCategoryEnum.TEMPORARY_RESIDENCE,
        "Casilla de verificación83": MainRequestCategoryEnum.PERMANENT_RESIDENCE,
        "Casilla de verificación97": MainRequestCategoryEnum.MODIFICATION,
        "Casilla de verificación102": MainRequestCategoryEnum.DEREGISTRATION,
    })
    _apply_enum_registry(fv, req.temporary_ground, {
        "Casilla de verificación78": TemporaryResidenceGroundEnum.EMPLOYEE,
        "Casilla de verificación79": TemporaryResidenceGroundEnum.SELF_EMPLOYED,
        "Casilla de verificación80": TemporaryResidenceGroundEnum.INACTIVE_WITH_RESOURCES_AND_INSURANCE,
        "Casilla de verificación81": TemporaryResidenceGroundEnum.STUDENT_WITH_RESOURCES_AND_INSURANCE,
        "Casilla de verificación82": TemporaryResidenceGroundEnum.UK_FAMILY_MEMBER,
    }, enabled=is_temp)
    _apply_enum_registry(fv, req.permanent_ground, {
        "Casilla de verificación84": PermanentResidenceGroundEnum.CONTINUOUS_5_YEARS,
        "Casilla de verificación85": PermanentResidenceGroundEnum.RETIREMENT_WITH_12_MONTHS_AND_3_YEARS,
        "Casilla de verificación86": PermanentResidenceGroundEnum.RETIREMENT_WITH_SPANISH_SPOUSE,
        "Casilla de verificación87": PermanentResidenceGroundEnum.RETIREMENT_WITH_SPOUSE_LOST_SPANISH_NATIONALITY,
        "Casilla de verificación88": PermanentResidenceGroundEnum.EARLY_RETIREMENT_WITH_12_MONTHS_AND_3_YEARS,
        "Casilla de verificación89": PermanentResidenceGroundEnum.EARLY_RETIREMENT_WITH_SPANISH_SPOUSE,
        "Casilla de verificación90": PermanentResidenceGroundEnum.EARLY_RETIREMENT_WITH_SPOUSE_LOST_SPANISH_NATIONALITY,
        "Casilla de verificación91": PermanentResidenceGroundEnum.PERMANENT_DISABILITY_AFTER_2_YEARS,
        "Casilla de verificación92": PermanentResidenceGroundEnum.PERMANENT_DISABILITY_WORK_ACCIDENT,
        "Casilla de verificación93": PermanentResidenceGroundEnum.PERMANENT_DISABILITY_WITH_SPANISH_SPOUSE,
        "Casilla de verificación94": PermanentResidenceGroundEnum.PERMANENT_DISABILITY_WITH_SPOUSE_LOST_SPANISH_NATIONALITY,
        "Casilla de verificación95": PermanentResidenceGroundEnum.WORK_IN_OTHER_MEMBER_STATE_KEEPING_RESIDENCE,
        "Casilla de verificación96": PermanentResidenceGroundEnum.OTHER,
    }, enabled=is_perm)
    _apply_enum_registry(fv, req.modification_ground, {
        "Casilla de verificación98": ModificationGroundEnum.PERSONAL_DATA,
        "Casilla de verificación99": ModificationGroundEnum.ADDRESS_CHANGE,
        "Casilla de verificación100": ModificationGroundEnum.IDENTITY_DOCUMENT_CHANGE,
        "Casilla de verificación101": ModificationGroundEnum.OTHER,
    }, enabled=is_mod)

    fv["Casilla de verificación103"] = bool(req.deregistration_cause)
    fv["Casilla de verificación104"] = req.truth_statement_accepted

    sig = form.signature
    fv["Texto67"] = sig.place
    fv["Texto68"] = sig.day
    fv["Texto69"] = sig.month
    fv["Texto70"] = sig.year
    fv["Texto71"] = _s(sig.uk_national_signature_name)
    fv["Texto72"] = _s(sig.applicant_signature_name)

    off = form.office
    fv["Texto73"] = _s(off.target_office)
    fv["Texto74"] = _s(off.dir3_code)
    fv["Texto75"] = off.province

    return fv
