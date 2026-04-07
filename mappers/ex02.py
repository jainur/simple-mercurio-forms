"""Mapper for EX02 domain model to PDF field values."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any
from mappers.helpers import assign_checkboxes, coerce_str as _s, split_nie as _split_nie

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
    fv["Texto1"] = _s(app.passport)
    if app.nie:
        n1, n2, n3 = _split_nie(app.nie)
        fv["Texto2"], fv["Texto3"], fv["Texto4"] = n1, n2, n3
    else:
        fv["Texto2"] = fv["Texto3"] = fv["Texto4"] = ""

    fv["Texto5"] = app.first_surname
    fv["Texto6"] = _s(app.second_surname)
    fv["Texto7"] = app.name
    fv["Texto8"] = app.date_of_birth.strftime("%d")
    fv["Texto9"] = app.date_of_birth.strftime("%m")
    fv["Texto10"] = app.date_of_birth.strftime("%Y")
    fv["Texto11"] = app.birth_place
    fv["Texto12"] = app.birth_country
    fv["Texto13"] = app.nationality
    fv["Texto14"] = _s(app.father_name)
    fv["Texto15"] = _s(app.mother_name)
    fv["Texto16"] = app.address
    fv["Texto17"] = _s(app.address_number)
    fv["Texto18"] = _s(app.floor_door)
    fv["Texto19"] = app.city
    fv["Texto20"] = app.postal_code
    fv["Texto21"] = app.province
    fv["Texto22"] = _s(app.mobile_phone)
    fv["Texto23"] = _s(app.email)
    fv["Texto24"] = _s(app.current_authorization)
    fv["Texto25"] = _s(app.current_authorization_document)
    fv["Texto26"] = _s(app.current_authorization_title)
    fv["Texto27"] = _s(app.legal_guardian_name)
    fv["Texto28"] = _s(app.legal_guardian_id)
    fv["Texto29"] = _s(app.legal_guardian_title)

    assign_checkboxes(fv, app.gender.value, {
        "Casilla de verificación82": "X",
        "Casilla de verificación83": "H",
        "Casilla de verificación84": "M",
    })
    assign_checkboxes(fv, app.marital_status.value, {
        "Casilla de verificación85": "S",
        "Casilla de verificación86": "C",
        "Casilla de verificación87": "V",
        "Casilla de verificación88": "D",
        "Casilla de verificación89": "Sp",
    })
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

    assign_checkboxes(fv, sp.gender.value, {
        "Casilla de verificación92": "X",
        "Casilla de verificación93": "H",
        "Casilla de verificación94": "M",
    })
    assign_checkboxes(fv, sp.marital_status.value, {
        "Casilla de verificación95": "S",
        "Casilla de verificación96": "C",
        "Casilla de verificación97": "V",
        "Casilla de verificación98": "D",
        "Casilla de verificación99": "Sp",
    })

    pres = form.presenter_details
    fv["Texto51"] = _s(pres.name_or_company) if pres else ""
    fv["Texto52"] = _s(pres.id_number) if pres else ""
    fv["Texto53"] = _s(pres.address) if pres else ""
    fv["Texto54"] = _s(pres.address_number) if pres else ""
    fv["Texto55"] = _s(pres.floor_door) if pres else ""
    fv["Texto56"] = _s(pres.city) if pres else ""
    fv["Texto57"] = _s(pres.postal_code) if pres else ""
    fv["Texto58"] = _s(pres.province) if pres else ""
    fv["Texto59"] = _s(pres.mobile_phone) if pres else ""
    fv["Texto60"] = _s(pres.email) if pres else ""
    fv["Texto61"] = _s(pres.legal_rep_name) if pres else ""
    fv["Texto62"] = _s(pres.legal_rep_id) if pres else ""
    fv["Texto63"] = _s(pres.legal_rep_title) if pres else ""

    notif = form.notification_address
    fv["Texto64"] = notif.name_or_company
    fv["Texto65"] = notif.id_number
    fv["Texto66"] = notif.address
    fv["Texto67"] = _s(notif.address_number)
    fv["Texto68"] = _s(notif.floor_door)
    fv["Texto69"] = notif.city
    fv["Texto70"] = notif.postal_code
    fv["Texto71"] = notif.province
    fv["Texto72"] = _s(notif.mobile_phone)
    fv["Texto73"] = _s(notif.email)
    fv["Casilla de verificación129"] = notif.consent_electronic_notifications

    req = form.request_details

    fv["Casilla de verificación100"] = req.family_relationship == FamilyRelationshipEnum.SPOUSE
    fv["Casilla de verificación101"] = req.family_relationship == FamilyRelationshipEnum.REGISTERED_PARTNER
    fv["Casilla de verificación102"] = req.family_relationship == FamilyRelationshipEnum.MINOR_LEGALLY_REPRESENTED
    fv["Casilla de verificación103"] = req.family_relationship == FamilyRelationshipEnum.DISABLED_ADULT_LEGALLY_REPRESENTED
    fv["Casilla de verificación104"] = req.family_relationship == FamilyRelationshipEnum.ADULT_CHILD_CAREGIVER
    fv["Casilla de verificación105"] = req.family_relationship == FamilyRelationshipEnum.MINOR_CHILD
    fv["Casilla de verificación106"] = req.family_relationship == FamilyRelationshipEnum.DISABLED_ADULT_CHILD
    fv["Casilla de verificación107"] = req.family_relationship == FamilyRelationshipEnum.UNREGISTERED_PARTNER
    fv["Casilla de verificación108"] = req.family_relationship == FamilyRelationshipEnum.ASCENDANT_OVER_65
    fv["Casilla de verificación109"] = req.family_relationship == FamilyRelationshipEnum.ASCENDANT_UNDER_65
    fv["Casilla de verificación110"] = req.family_relationship == FamilyRelationshipEnum.ADULT_CHILD_RENEWAL_ONLY

    fv["Casilla de verificación111"] = req.authorization_type == AuthorizationTypeEnum.INITIAL_ART_65
    fv["Casilla de verificación112"] = req.authorization_type == AuthorizationTypeEnum.INITIAL_UE_LONG_TERM_FAMILY
    fv["Casilla de verificación113"] = req.authorization_type == AuthorizationTypeEnum.RENEWAL_ART_71
    fv["Casilla de verificación114"] = req.authorization_type == AuthorizationTypeEnum.CHILDREN_CHAPTER_IV_ART_147
    fv["Casilla de verificación115"] = req.authorization_type == AuthorizationTypeEnum.CHILDREN_CHAPTER_V_ART_155

    fv["Casilla de verificación116"] = req.request_independent_residence
    fv["Casilla de verificación117"] = req.independent_residence_reason == IndependentResidenceReasonEnum.INDEPENDENT_MEANS_ART_69_1
    fv["Casilla de verificación118"] = req.independent_residence_reason == IndependentResidenceReasonEnum.BREAKUP_ART_69_2_A
    fv["Casilla de verificación119"] = req.independent_residence_reason == IndependentResidenceReasonEnum.VICTIM_ART_69_2_B
    fv["Casilla de verificación120"] = req.independent_residence_reason == IndependentResidenceReasonEnum.DEATH_ART_69_2_C
    fv["Casilla de verificación121"] = req.independent_residence_reason == IndependentResidenceReasonEnum.MAJORITY_OR_END_OF_REPRESENTATION_ART_69_4
    fv["Casilla de verificación122"] = req.independent_residence_reason == IndependentResidenceReasonEnum.EU_RESIDENCE_BLUE_CARD_CONTEXT_ART_69_5
    fv["Casilla de verificación123"] = req.independent_residence_reason == IndependentResidenceReasonEnum.ASCENDANT_WITH_WORK_AUTH_ART_69_6

    fv["Casilla de verificación124"] = req.request_ascendant_work_authorization
    fv["Casilla de verificación125"] = req.work_mode == WorkModeEnum.CUENTA_AJENA
    fv["Casilla de verificación126"] = req.work_mode == WorkModeEnum.CUENTA_PROPIA

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
