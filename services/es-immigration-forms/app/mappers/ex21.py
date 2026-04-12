"""Mapper for EX21 domain model to PDF field values."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any
from app.mappers.helpers import apply_enum_registry as _apply_enum_registry, coerce_str as _s, map_identity_person_block as _map_identity_person_block, map_notification_block as _map_notification_block, map_optional_object_fields as _map_optional_object_fields, split_nie as _split_nie

if TYPE_CHECKING:
    from models.ex21 import EX21FormSchema


def to_field_values(form: EX21FormSchema) -> dict[str, Any]:
    from models.ex21 import (
        FamilyRelationshipEnum,
        MainRequestCategoryEnum,
        ModificationGroundEnum,
        PermanentResidenceGroundEnum,
        RenewalSubtypeEnum,
    )

    fv: dict[str, Any] = {}

    a = form.applicant_details
    _map_identity_person_block(
        fv,
        a,
        passport_field="Texto1",
        nie_fields=("Texto2", "Texto3", "Texto4"),
        date_fields=("Texto76", "Texto77", "Texto78"),
        text_fields={
            "first_surname": "Texto5",
            "second_surname": "Texto6",
            "name": "Texto7",
            "birth_place": "Texto8",
            "nationality": "Texto9",
            "birth_country": "Texto10",
            "father_name": "Texto11",
            "mother_name": "Texto12",
            "address": "Texto13",
            "address_number": "Texto14",
            "floor_door": "Texto15",
            "postal_code": "Texto16",
            "city": "Texto17",
            "mobile_phone": "Texto18",
            "email": "Texto19",
            "legal_guardian_name": "Texto20",
            "province": "Texto21",
            "legal_guardian_id": "Texto22",
            "legal_guardian_title": "Texto23",
        },
        gender_checkbox_map={
            "Casilla de verificación79": "X",
            "Casilla de verificación80": "H",
            "Casilla de verificación81": "M",
        },
        marital_checkbox_map={
            "Casilla de verificación82": "S",
            "Casilla de verificación83": "C",
            "Casilla de verificación84": "V",
            "Casilla de verificación85": "D",
            "Casilla de verificación86": "Sp",
        },
    )

    b = form.british_national_details
    fv["Texto24"] = _s(b.passport)
    fv["Texto25"] = b.first_surname
    fv["Texto26"] = _s(b.second_surname)
    fv["Texto27"] = b.name
    fv["Texto28"] = b.address
    fv["Texto29"] = b.city
    if b.nie:
        n1, n2, n3 = _split_nie(b.nie)
        fv["Texto30"], fv["Texto31"], fv["Texto35"] = n1, n2, n3
    else:
        fv["Texto30"] = fv["Texto31"] = fv["Texto35"] = ""
    fv["Texto32"] = b.postal_code
    fv["Texto33"] = b.relationship_with_applicant
    fv["Texto34"] = b.nationality
    fv["Texto36"] = _s(b.address_number)
    fv["Texto37"] = _s(b.floor_door)
    fv["Texto87"] = b.province

    r = form.filing_representative
    _map_optional_object_fields(
        fv,
        r,
        text_fields={
            "name_or_company": "Texto44",
            "address": "Texto46",
            "city": "Texto48",
            "province": "Texto50",
            "email": "Texto52",
            "mobile_phone": "Texto53",
            "legal_rep_name": "Texto54",
            "legal_rep_id": "Texto55",
            "legal_rep_title": "Texto56",
            "id_number": "Texto58",
            "address_number": "Texto38",
            "floor_door": "Texto39",
            "postal_code": "Texto42",
        },
    )

    n = form.notification_address
    _map_notification_block(
        fv,
        n,
        text_fields={
            "name_or_company": "Texto45",
            "id_number": "Texto59",
            "address": "Texto47",
            "address_number": "Texto40",
            "floor_door": "Texto41",
            "city": "Texto49",
            "postal_code": "Texto43",
            "province": "Texto51",
            "email": "Texto60",
            "mobile_phone": "Texto61",
        },
        consent_field="Casilla de verificación88",
    )

    req = form.request_details
    fv["Texto62"] = req.residence_start_day
    fv["Texto63"] = req.residence_start_month
    fv["Texto64"] = req.residence_start_year
    fv["Texto57"] = _s(req.continuous_5_years_text)
    fv["Texto65"] = _s(req.identity_document_change_text)
    fv["Texto66"] = _s(req.cause_specification)

    is_temp = req.category == MainRequestCategoryEnum.TEMPORARY_RESIDENCE
    is_perm = req.category == MainRequestCategoryEnum.PERMANENT_RESIDENCE
    is_mod = req.category == MainRequestCategoryEnum.MODIFICATION
    is_renew = req.category == MainRequestCategoryEnum.CARD_RENEWAL
    is_dereg = req.category == MainRequestCategoryEnum.DEREGISTRATION

    _apply_enum_registry(fv, req.category, {
        "Casilla de verificación89": MainRequestCategoryEnum.TEMPORARY_RESIDENCE,
        "Casilla de verificación97": MainRequestCategoryEnum.PERMANENT_RESIDENCE,
        "Casilla de verificación104": MainRequestCategoryEnum.MODIFICATION,
        "Casilla de verificación111": MainRequestCategoryEnum.CARD_RENEWAL,
        "Casilla de verificación114": MainRequestCategoryEnum.DEREGISTRATION,
    })
    _apply_enum_registry(fv, req.family_relationship, {
        "Casilla de verificación90": FamilyRelationshipEnum.SPOUSE,
        "Casilla de verificación91": FamilyRelationshipEnum.REGISTERED_PARTNER,
        "Casilla de verificación92": FamilyRelationshipEnum.UNREGISTERED_PARTNER,
        "Casilla de verificación93": FamilyRelationshipEnum.DESCENDANT_UNDER_21,
        "Casilla de verificación94": FamilyRelationshipEnum.DESCENDANT_OVER_21_DEPENDENT_OR_DISABLED,
        "Casilla de verificación95": FamilyRelationshipEnum.ASCENDANT_DEPENDENT,
        "Casilla de verificación96": FamilyRelationshipEnum.OTHER_FAMILY_MEMBER,
    }, enabled=is_temp)
    _apply_enum_registry(fv, req.permanent_ground, {
        "Casilla de verificación98": PermanentResidenceGroundEnum.CONTINUOUS_5_YEARS,
        "Casilla de verificación99": PermanentResidenceGroundEnum.FAMILY_OF_BRITISH_WORKER_WITH_PERMANENT_RESIDENCE,
        "Casilla de verificación100": PermanentResidenceGroundEnum.WIDOW_WITH_2_YEARS_RESIDENCE,
        "Casilla de verificación101": PermanentResidenceGroundEnum.WIDOW_WORK_ACCIDENT_OR_PROF_DISEASE,
        "Casilla de verificación102": PermanentResidenceGroundEnum.WIDOW_ORIGINALLY_SPANISH,
    }, enabled=is_perm)
    fv["Casilla de verificación103"] = (
        (is_perm and req.permanent_ground == PermanentResidenceGroundEnum.OTHER)
        or (is_renew and req.renewal_subtype == RenewalSubtypeEnum.PERMANENT_HOLDER)
    )
    _apply_enum_registry(fv, req.modification_ground, {
        "Casilla de verificación105": ModificationGroundEnum.PERSONAL_DATA,
        "Casilla de verificación106": ModificationGroundEnum.ADDRESS,
        "Casilla de verificación107": ModificationGroundEnum.IDENTITY_DOCUMENT,
        "Casilla de verificación108": ModificationGroundEnum.STATUS_WIDOW,
        "Casilla de verificación109": ModificationGroundEnum.STATUS_CHILD_AND_PARENT_UNTIL_END_OF_STUDIES,
        "Casilla de verificación110": ModificationGroundEnum.OTHER,
    }, enabled=is_mod)
    _apply_enum_registry(fv, req.renewal_subtype, {
        "Casilla de verificación112": RenewalSubtypeEnum.TEMPORARY_HOLDER,
    }, enabled=is_renew)
    fv["Casilla de verificación115"] = req.deregistration_cause_present
    fv["Casilla de verificación116"] = req.truth_statement_accepted

    sig = form.signature
    fv["Texto67"] = sig.place
    fv["Texto68"] = sig.day
    fv["Texto69"] = sig.month
    fv["Texto70"] = sig.year
    fv["Texto71"] = _s(sig.british_national_signature_name)
    fv["Texto72"] = _s(sig.applicant_signature_name)

    off = form.office
    fv["Texto73"] = _s(off.target_office)
    fv["Texto74"] = _s(off.dir3_code)
    fv["Texto75"] = off.province

    return fv
