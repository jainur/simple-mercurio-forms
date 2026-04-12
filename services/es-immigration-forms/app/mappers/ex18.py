"""Mapper for EX18 domain model to PDF field values."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any
from app.mappers.helpers import apply_enum_registry as _apply_enum_registry, coerce_str as _s, map_identity_person_block as _map_identity_person_block, map_notification_block as _map_notification_block, map_optional_object_fields as _map_optional_object_fields

if TYPE_CHECKING:
    from models.ex18 import EX18FormSchema


def to_field_values(form: EX18FormSchema) -> dict[str, Any]:
    from models.ex18 import (
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
    fv["Texto50"] = req.expected_residence_period
    fv["Texto51"] = req.residence_start_day
    fv["Texto52"] = req.residence_start_month
    fv["Texto53"] = req.residence_start_year
    fv["Texto54"] = req.residence_start_location
    fv["Texto55"] = _s(req.eu_citizen_document_id)
    fv["Texto56"] = _s(req.relationship_with_eu_citizen)
    fv["Texto57"] = _s(req.incapacity_with_spanish_spouse_text)
    fv["Texto58"] = _s(req.identity_document_change_text)
    fv["Texto59"] = _s(req.cause_specification)

    is_temp = req.category == MainRequestCategoryEnum.TEMPORARY_RESIDENCE
    is_perm = req.category == MainRequestCategoryEnum.PERMANENT_RESIDENCE
    is_mod = req.category == MainRequestCategoryEnum.MODIFICATION
    is_dereg = req.category == MainRequestCategoryEnum.DEREGISTRATION

    _apply_enum_registry(fv, req.category, {
        "Casilla de verificación10": MainRequestCategoryEnum.TEMPORARY_RESIDENCE,
        "Casilla de verificación16": MainRequestCategoryEnum.PERMANENT_RESIDENCE,
        "Casilla de verificación30": MainRequestCategoryEnum.MODIFICATION,
        "Casilla de verificación35": MainRequestCategoryEnum.DEREGISTRATION,
    })
    _apply_enum_registry(fv, req.temporary_ground, {
        "Casilla de verificación11": TemporaryResidenceGroundEnum.EMPLOYEE,
        "Casilla de verificación12": TemporaryResidenceGroundEnum.SELF_EMPLOYED,
        "Casilla de verificación13": TemporaryResidenceGroundEnum.INACTIVE_WITH_RESOURCES_AND_INSURANCE,
        "Casilla de verificación14": TemporaryResidenceGroundEnum.STUDENT_WITH_RESOURCES_AND_INSURANCE,
        "Casilla de verificación15": TemporaryResidenceGroundEnum.EU_FAMILY_MEMBER,
    }, enabled=is_temp)
    _apply_enum_registry(fv, req.permanent_ground, {
        "Casilla de verificación17": PermanentResidenceGroundEnum.CONTINUOUS_5_YEARS,
        "Casilla de verificación18": PermanentResidenceGroundEnum.RETIREMENT_WITH_12_MONTHS_AND_3_YEARS,
        "Casilla de verificación19": PermanentResidenceGroundEnum.RETIREMENT_WITH_SPANISH_SPOUSE,
        "Casilla de verificación20": PermanentResidenceGroundEnum.RETIREMENT_WITH_SPOUSE_LOST_SPANISH_NATIONALITY,
        "Casilla de verificación21": PermanentResidenceGroundEnum.EARLY_RETIREMENT_WITH_12_MONTHS_AND_3_YEARS,
        "Casilla de verificación22": PermanentResidenceGroundEnum.EARLY_RETIREMENT_WITH_SPANISH_SPOUSE,
        "Casilla de verificación23": PermanentResidenceGroundEnum.EARLY_RETIREMENT_WITH_SPOUSE_LOST_SPANISH_NATIONALITY,
        "Casilla de verificación24": PermanentResidenceGroundEnum.PERMANENT_DISABILITY_AFTER_2_YEARS,
        "Casilla de verificación25": PermanentResidenceGroundEnum.PERMANENT_DISABILITY_WORK_ACCIDENT,
        "Casilla de verificación26": PermanentResidenceGroundEnum.PERMANENT_DISABILITY_WITH_SPANISH_SPOUSE,
        "Casilla de verificación27": PermanentResidenceGroundEnum.PERMANENT_DISABILITY_WITH_SPOUSE_LOST_SPANISH_NATIONALITY,
        "Casilla de verificación28": PermanentResidenceGroundEnum.WORK_IN_OTHER_MEMBER_STATE_KEEPING_RESIDENCE,
        "Casilla de verificación29": PermanentResidenceGroundEnum.OTHER,
    }, enabled=is_perm)
    _apply_enum_registry(fv, req.modification_ground, {
        "Casilla de verificación31": ModificationGroundEnum.PERSONAL_DATA,
        "Casilla de verificación32": ModificationGroundEnum.ADDRESS_CHANGE,
        "Casilla de verificación33": ModificationGroundEnum.IDENTITY_DOCUMENT_CHANGE,
        "Casilla de verificación34": ModificationGroundEnum.OTHER,
    }, enabled=is_mod)

    fv["Casilla de verificación36"] = bool(req.deregistration_cause)
    fv["Casilla de verificación37"] = req.truth_statement_accepted

    sig = form.signature
    fv["Texto60"] = sig.place
    fv["Texto61"] = sig.day
    fv["Texto62"] = sig.month
    fv["Texto63"] = sig.year
    fv["Texto64"] = _s(sig.eu_citizen_signature_name)
    fv["Texto65"] = _s(sig.applicant_signature_name)

    off = form.office
    fv["Texto66"] = _s(off.target_office)
    fv["Texto67"] = _s(off.dir3_code)
    fv["Texto68"] = off.province

    return fv
