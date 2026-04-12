"""Mapper for EX02 domain model to PDF field values."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any
from app.mappers.helpers import apply_enum_registry as _apply_enum_registry, coerce_str as _s, map_identity_person_block as _map_identity_person_block, map_notification_block as _map_notification_block, map_optional_object_fields as _map_optional_object_fields, split_nie as _split_nie

if TYPE_CHECKING:
    from models.ex02 import EX02FormSchema


def to_field_values(form: EX02FormSchema) -> dict[str, Any]:
    from models.ex02 import (
        AuthorizationTypeEnum,
        FamilyRelationshipEnum,
        IndependentResidenceReasonEnum,
        WorkModeEnum,
    )

    fv: dict[str, Any] = {}

    app = form.applicant_details
    _map_identity_person_block(
        fv,
        app,
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
            "current_authorization": "Texto24",
            "current_authorization_document": "Texto25",
            "current_authorization_title": "Texto26",
            "legal_guardian_name": "Texto27",
            "legal_guardian_id": "Texto28",
            "legal_guardian_title": "Texto29",
        },
        gender_checkbox_map={
            "Casilla de verificación82": "X",
            "Casilla de verificación83": "H",
            "Casilla de verificación84": "M",
        },
        marital_checkbox_map={
            "Casilla de verificación85": "S",
            "Casilla de verificación86": "C",
            "Casilla de verificación87": "V",
            "Casilla de verificación88": "D",
            "Casilla de verificación89": "Sp",
        },
    )
    fv["Casilla de verificación90"] = app.children_in_school_age
    fv["Casilla de verificación91"] = not app.children_in_school_age

    sp = form.sponsor_details
    fv["Texto30"] = _s(sp.passport)
    if sp.nie:
        n1, n2, n3 = _split_nie(sp.nie)
        fv["Texto31"], fv["Texto32"], fv["Texto33"] = n1, n2, n3
    else:
        fv["Texto31"] = fv["Texto32"] = fv["Texto33"] = ""

    fv["Texto34"] = sp.first_surname
    fv["Texto35"] = _s(sp.second_surname)
    fv["Texto36"] = sp.name
    fv["Texto37"] = sp.date_of_birth.strftime("%d")
    fv["Texto38"] = sp.date_of_birth.strftime("%m")
    fv["Texto39"] = sp.date_of_birth.strftime("%Y")
    fv["Texto40"] = sp.birth_place
    fv["Texto41"] = sp.birth_country
    fv["Texto42"] = sp.nationality
    fv["Texto43"] = _s(sp.father_name)
    fv["Texto44"] = _s(sp.mother_name)
    fv["Texto45"] = sp.address
    fv["Texto46"] = _s(sp.address_number)
    fv["Texto47"] = _s(sp.floor_door)
    fv["Texto48"] = sp.city
    fv["Texto49"] = sp.postal_code
    fv["Texto50"] = sp.province

    _apply_enum_registry(fv, sp.gender, {
        "Casilla de verificación92": "X",
        "Casilla de verificación93": "H",
        "Casilla de verificación94": "M",
    })
    _apply_enum_registry(fv, sp.marital_status, {
        "Casilla de verificación95": "S",
        "Casilla de verificación96": "C",
        "Casilla de verificación97": "V",
        "Casilla de verificación98": "D",
        "Casilla de verificación99": "Sp",
    })

    pres = form.presenter_details
    _map_optional_object_fields(
        fv,
        pres,
        text_fields={
            "name_or_company": "Texto51",
            "id_number": "Texto52",
            "address": "Texto53",
            "address_number": "Texto54",
            "floor_door": "Texto55",
            "city": "Texto56",
            "postal_code": "Texto57",
            "province": "Texto58",
            "mobile_phone": "Texto59",
            "email": "Texto60",
            "legal_rep_name": "Texto61",
            "legal_rep_id": "Texto62",
            "legal_rep_title": "Texto63",
        },
    )

    notif = form.notification_address
    _map_notification_block(
        fv,
        notif,
        text_fields={
            "name_or_company": "Texto64",
            "id_number": "Texto65",
            "address": "Texto66",
            "address_number": "Texto67",
            "floor_door": "Texto68",
            "city": "Texto69",
            "postal_code": "Texto70",
            "province": "Texto71",
            "mobile_phone": "Texto72",
            "email": "Texto73",
        },
        consent_field="Casilla de verificación129",
    )

    req = form.request_details

    _apply_enum_registry(fv, req.family_relationship, {
        "Casilla de verificación100": FamilyRelationshipEnum.SPOUSE,
        "Casilla de verificación101": FamilyRelationshipEnum.REGISTERED_PARTNER,
        "Casilla de verificación102": FamilyRelationshipEnum.MINOR_LEGALLY_REPRESENTED,
        "Casilla de verificación103": FamilyRelationshipEnum.DISABLED_ADULT_LEGALLY_REPRESENTED,
        "Casilla de verificación104": FamilyRelationshipEnum.ADULT_CHILD_CAREGIVER,
        "Casilla de verificación105": FamilyRelationshipEnum.MINOR_CHILD,
        "Casilla de verificación106": FamilyRelationshipEnum.DISABLED_ADULT_CHILD,
        "Casilla de verificación107": FamilyRelationshipEnum.UNREGISTERED_PARTNER,
        "Casilla de verificación108": FamilyRelationshipEnum.ASCENDANT_OVER_65,
        "Casilla de verificación109": FamilyRelationshipEnum.ASCENDANT_UNDER_65,
        "Casilla de verificación110": FamilyRelationshipEnum.ADULT_CHILD_RENEWAL_ONLY,
    })
    _apply_enum_registry(fv, req.authorization_type, {
        "Casilla de verificación111": AuthorizationTypeEnum.INITIAL_ART_65,
        "Casilla de verificación112": AuthorizationTypeEnum.INITIAL_UE_LONG_TERM_FAMILY,
        "Casilla de verificación113": AuthorizationTypeEnum.RENEWAL_ART_71,
        "Casilla de verificación114": AuthorizationTypeEnum.CHILDREN_CHAPTER_IV_ART_147,
        "Casilla de verificación115": AuthorizationTypeEnum.CHILDREN_CHAPTER_V_ART_155,
    })
    _apply_enum_registry(fv, req.independent_residence_reason, {
        "Casilla de verificación117": IndependentResidenceReasonEnum.INDEPENDENT_MEANS_ART_69_1,
        "Casilla de verificación118": IndependentResidenceReasonEnum.BREAKUP_ART_69_2_A,
        "Casilla de verificación119": IndependentResidenceReasonEnum.VICTIM_ART_69_2_B,
        "Casilla de verificación120": IndependentResidenceReasonEnum.DEATH_ART_69_2_C,
        "Casilla de verificación121": IndependentResidenceReasonEnum.MAJORITY_OR_END_OF_REPRESENTATION_ART_69_4,
        "Casilla de verificación122": IndependentResidenceReasonEnum.EU_RESIDENCE_BLUE_CARD_CONTEXT_ART_69_5,
        "Casilla de verificación123": IndependentResidenceReasonEnum.ASCENDANT_WITH_WORK_AUTH_ART_69_6,
    })
    fv["Casilla de verificación116"] = req.request_independent_residence
    _apply_enum_registry(fv, req.work_mode, {
        "Casilla de verificación125": WorkModeEnum.CUENTA_AJENA,
        "Casilla de verificación126": WorkModeEnum.CUENTA_PROPIA,
    })
    fv["Casilla de verificación124"] = req.request_ascendant_work_authorization
    fv["Casilla de verificación127"] = req.simultaneous_other_family_reunification_requests
    fv["Casilla de verificación128"] = not req.simultaneous_other_family_reunification_requests

    sig = form.signature
    fv["Texto74"] = sig.place
    fv["Texto75"] = sig.day
    fv["Texto76"] = sig.month
    fv["Texto77"] = sig.year
    fv["Texto78"] = _s(sig.name)

    off = form.office
    fv["Texto79"] = _s(off.target_office)
    fv["Texto80"] = _s(off.dir3_code)
    fv["Texto81"] = off.province

    return fv
