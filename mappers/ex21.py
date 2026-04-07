"""Mapper for EX21 domain model to PDF field values."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any
from mappers.helpers import assign_checkboxes, coerce_str as _s, split_nie as _split_nie

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
    fv["Texto1"] = _s(a.passport)
    if a.nie:
        n1, n2, n3 = _split_nie(a.nie)
        fv["Texto2"], fv["Texto3"], fv["Texto4"] = n1, n2, n3
    else:
        fv["Texto2"] = fv["Texto3"] = fv["Texto4"] = ""
    fv["Texto5"] = a.first_surname
    fv["Texto6"] = _s(a.second_surname)
    fv["Texto7"] = a.name
    fv["Texto8"] = a.birth_place
    fv["Texto9"] = a.nationality
    fv["Texto10"] = a.birth_country
    fv["Texto11"] = _s(a.father_name)
    fv["Texto12"] = _s(a.mother_name)
    fv["Texto13"] = a.address
    fv["Texto14"] = _s(a.address_number)
    fv["Texto15"] = _s(a.floor_door)
    fv["Texto16"] = a.postal_code
    fv["Texto17"] = a.city
    fv["Texto18"] = _s(a.mobile_phone)
    fv["Texto19"] = _s(a.email)
    fv["Texto20"] = _s(a.legal_guardian_name)
    fv["Texto21"] = a.province
    fv["Texto22"] = _s(a.legal_guardian_id)
    fv["Texto23"] = _s(a.legal_guardian_title)
    fv["Texto76"] = a.date_of_birth.strftime("%d")
    fv["Texto77"] = a.date_of_birth.strftime("%m")
    fv["Texto78"] = a.date_of_birth.strftime("%Y")

    assign_checkboxes(fv, a.gender.value, {
        "Casilla de verificación79": "X",
        "Casilla de verificación80": "H",
        "Casilla de verificación81": "M",
    })
    assign_checkboxes(fv, a.marital_status.value, {
        "Casilla de verificación82": "S",
        "Casilla de verificación83": "C",
        "Casilla de verificación84": "V",
        "Casilla de verificación85": "D",
        "Casilla de verificación86": "Sp",
    })

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
    fv["Texto44"] = _s(r.name_or_company) if r else ""
    fv["Texto46"] = _s(r.address) if r else ""
    fv["Texto48"] = _s(r.city) if r else ""
    fv["Texto50"] = _s(r.province) if r else ""
    fv["Texto52"] = _s(r.email) if r else ""
    fv["Texto53"] = _s(r.mobile_phone) if r else ""
    fv["Texto54"] = _s(r.legal_rep_name) if r else ""
    fv["Texto55"] = _s(r.legal_rep_id) if r else ""
    fv["Texto56"] = _s(r.legal_rep_title) if r else ""
    fv["Texto58"] = _s(r.id_number) if r else ""
    fv["Texto38"] = _s(r.address_number) if r else ""
    fv["Texto39"] = _s(r.floor_door) if r else ""
    fv["Texto42"] = _s(r.postal_code) if r else ""

    n = form.notification_address
    fv["Texto45"] = n.name_or_company
    fv["Texto59"] = n.id_number
    fv["Texto47"] = n.address
    fv["Texto40"] = _s(n.address_number)
    fv["Texto41"] = _s(n.floor_door)
    fv["Texto49"] = n.city
    fv["Texto43"] = n.postal_code
    fv["Texto51"] = n.province
    fv["Texto60"] = _s(n.email)
    fv["Texto61"] = _s(n.mobile_phone)
    fv["Casilla de verificación88"] = n.consent_electronic_notifications

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

    fv["Casilla de verificación89"] = is_temp
    fv["Casilla de verificación90"] = is_temp and req.family_relationship == FamilyRelationshipEnum.SPOUSE
    fv["Casilla de verificación91"] = is_temp and req.family_relationship == FamilyRelationshipEnum.REGISTERED_PARTNER
    fv["Casilla de verificación92"] = is_temp and req.family_relationship == FamilyRelationshipEnum.UNREGISTERED_PARTNER
    fv["Casilla de verificación93"] = is_temp and req.family_relationship == FamilyRelationshipEnum.DESCENDANT_UNDER_21
    fv["Casilla de verificación94"] = is_temp and req.family_relationship == FamilyRelationshipEnum.DESCENDANT_OVER_21_DEPENDENT_OR_DISABLED
    fv["Casilla de verificación95"] = is_temp and req.family_relationship == FamilyRelationshipEnum.ASCENDANT_DEPENDENT
    fv["Casilla de verificación96"] = is_temp and req.family_relationship == FamilyRelationshipEnum.OTHER_FAMILY_MEMBER

    fv["Casilla de verificación97"] = is_perm
    fv["Casilla de verificación98"] = is_perm and req.permanent_ground == PermanentResidenceGroundEnum.CONTINUOUS_5_YEARS
    fv["Casilla de verificación99"] = is_perm and req.permanent_ground == PermanentResidenceGroundEnum.FAMILY_OF_BRITISH_WORKER_WITH_PERMANENT_RESIDENCE
    fv["Casilla de verificación100"] = is_perm and req.permanent_ground == PermanentResidenceGroundEnum.WIDOW_WITH_2_YEARS_RESIDENCE
    fv["Casilla de verificación101"] = is_perm and req.permanent_ground == PermanentResidenceGroundEnum.WIDOW_WORK_ACCIDENT_OR_PROF_DISEASE
    fv["Casilla de verificación102"] = is_perm and req.permanent_ground == PermanentResidenceGroundEnum.WIDOW_ORIGINALLY_SPANISH
    fv["Casilla de verificación103"] = (
        (is_perm and req.permanent_ground == PermanentResidenceGroundEnum.OTHER)
        or (is_renew and req.renewal_subtype == RenewalSubtypeEnum.PERMANENT_HOLDER)
    )

    fv["Casilla de verificación104"] = is_mod
    fv["Casilla de verificación105"] = is_mod and req.modification_ground == ModificationGroundEnum.PERSONAL_DATA
    fv["Casilla de verificación106"] = is_mod and req.modification_ground == ModificationGroundEnum.ADDRESS
    fv["Casilla de verificación107"] = is_mod and req.modification_ground == ModificationGroundEnum.IDENTITY_DOCUMENT
    fv["Casilla de verificación108"] = is_mod and req.modification_ground == ModificationGroundEnum.STATUS_WIDOW
    fv["Casilla de verificación109"] = is_mod and req.modification_ground == ModificationGroundEnum.STATUS_CHILD_AND_PARENT_UNTIL_END_OF_STUDIES
    fv["Casilla de verificación110"] = is_mod and req.modification_ground == ModificationGroundEnum.OTHER

    fv["Casilla de verificación111"] = is_renew
    fv["Casilla de verificación112"] = is_renew and req.renewal_subtype == RenewalSubtypeEnum.TEMPORARY_HOLDER
    fv["Casilla de verificación114"] = is_dereg
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
