"""Mapper for EX19 domain model to PDF field values."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any
from mappers.helpers import assign_checkboxes, coerce_str as _s, split_nie as _split_nie

if TYPE_CHECKING:
    from models.ex19 import EX19FormSchema


def to_field_values(form: EX19FormSchema) -> dict[str, Any]:
    from models.ex19 import (
        FamilyRelationshipEnum,
        MaintainRightGroundEnum,
        ResidenceRequestTypeEnum,
    )

    fv: dict[str, Any] = {}

    a = form.applicant_details
    fv["Texto2"] = _s(a.passport)
    if a.nie:
        n1, n2, n3 = _split_nie(a.nie)
        fv["Texto3"], fv["Texto4"], fv["Texto5"] = n1, n2, n3
    else:
        fv["Texto3"] = fv["Texto4"] = fv["Texto5"] = ""
    fv["Texto6"] = a.first_surname
    fv["Texto7"] = _s(a.second_surname)
    fv["Texto8"] = a.name
    fv["Texto9"] = a.date_of_birth.strftime("%d")
    fv["Texto10"] = a.date_of_birth.strftime("%m")
    fv["Texto11"] = a.date_of_birth.strftime("%Y")
    fv["Texto12"] = a.birth_place
    fv["Texto13"] = a.birth_country
    fv["Texto14"] = a.nationality
    fv["Texto15"] = _s(a.father_name)
    fv["Texto16"] = _s(a.mother_name)
    fv["Texto17"] = a.address
    fv["Texto18"] = _s(a.address_number)
    fv["Texto19"] = _s(a.floor_door)
    fv["Texto20"] = a.city
    fv["Texto21"] = a.postal_code
    fv["Texto22"] = a.province
    fv["Texto23"] = _s(a.mobile_phone)
    fv["Texto24"] = _s(a.email)
    fv["Texto25"] = _s(a.legal_guardian_name)
    fv["Texto26"] = _s(a.legal_guardian_id)
    fv["Texto27"] = _s(a.legal_guardian_title)

    assign_checkboxes(fv, a.gender.value, {
        "Casilla de verificación3": "X",
        "Casilla de verificación4": "H",
        "Casilla de verificación5": "M",
    })
    assign_checkboxes(fv, a.marital_status.value, {
        "Casilla de verificación6": "S",
        "Casilla de verificación7": "C",
        "Casilla de verificación8": "V",
        "Casilla de verificación9": "D",
        "Casilla de verificación10": "Sp",
    })

    eu = form.eu_citizen_details
    fv["Texto28"] = _s(eu.passport)
    if eu.nie:
        n1, n2, n3 = _split_nie(eu.nie)
        fv["Texto29"], fv["Texto30"], fv["Texto31"] = n1, n2, n3
    else:
        fv["Texto29"] = fv["Texto30"] = fv["Texto31"] = ""
    fv["Texto32"] = eu.first_surname
    fv["Texto33"] = _s(eu.second_surname)
    fv["Texto34"] = eu.name
    fv["Texto35"] = eu.nationality
    fv["Texto36"] = eu.address
    fv["Texto37"] = _s(eu.address_number)
    fv["Texto38"] = _s(eu.floor_door)
    fv["Texto39"] = eu.city
    fv["Texto40"] = eu.postal_code
    fv["Texto41"] = eu.province

    r = form.filing_representative
    fv["Texto42"] = _s(r.name_or_company) if r else ""
    fv["Texto43"] = _s(r.id_number) if r else ""
    fv["Texto44"] = _s(r.address) if r else ""
    fv["Texto45"] = _s(r.address_number) if r else ""
    fv["Texto46"] = _s(r.floor_door) if r else ""
    fv["Texto47"] = _s(r.city) if r else ""
    fv["Texto48"] = _s(r.postal_code) if r else ""
    fv["Texto49"] = _s(r.province) if r else ""
    fv["Texto50"] = _s(r.mobile_phone) if r else ""
    fv["Texto51"] = _s(r.email) if r else ""
    fv["Texto52"] = _s(r.legal_rep_name) if r else ""
    fv["Texto53"] = _s(r.legal_rep_id) if r else ""
    fv["Texto54"] = _s(r.legal_rep_title) if r else ""

    n = form.notification_address
    fv["Texto55"] = n.name_or_company
    fv["Texto56"] = n.id_number
    fv["Texto57"] = n.address
    fv["Texto58"] = _s(n.address_number)
    fv["Texto59"] = _s(n.floor_door)
    fv["Texto60"] = n.city
    fv["Texto61"] = n.postal_code
    fv["Texto62"] = n.province
    fv["Texto63"] = _s(n.mobile_phone)
    fv["Texto64"] = _s(n.email)
    fv["Casilla de verificación12"] = n.consent_electronic_notifications

    req = form.request_details
    is_temp = req.request_type == ResidenceRequestTypeEnum.TEMPORARY_INITIAL
    is_perm = req.request_type == ResidenceRequestTypeEnum.PERMANENT
    is_renew = req.request_type == ResidenceRequestTypeEnum.CARD_RENEWAL
    is_keep = req.request_type == ResidenceRequestTypeEnum.MAINTAIN_PERSONAL_RIGHT

    fv["Casilla de verificación13"] = is_temp
    fv["Casilla de verificación14"] = is_temp and req.family_relationship == FamilyRelationshipEnum.SPOUSE
    fv["Casilla de verificación15"] = is_temp and req.family_relationship == FamilyRelationshipEnum.REGISTERED_PARTNER
    fv["Casilla de verificación16"] = is_temp and req.family_relationship == FamilyRelationshipEnum.STABLE_PARTNER
    fv["Casilla de verificación17"] = is_temp and req.family_relationship == FamilyRelationshipEnum.DESCENDANT_UNDER_21
    fv["Casilla de verificación18"] = is_temp and req.family_relationship == FamilyRelationshipEnum.DESCENDANT_OVER_21_DEPENDENT
    fv["Casilla de verificación19"] = is_temp and req.family_relationship == FamilyRelationshipEnum.ASCENDANT_DEPENDENT
    fv["Casilla de verificación20"] = is_temp and req.family_relationship == FamilyRelationshipEnum.PARENT_OF_MINOR_EU_CITIZEN
    fv["Casilla de verificación21"] = is_temp and req.family_relationship == FamilyRelationshipEnum.OTHER_FAMILY_MEMBER

    fv["Casilla de verificación22"] = is_perm
    fv["Casilla de verificación23"] = is_renew
    fv["Casilla de verificación24"] = is_keep
    fv["Casilla de verificación25"] = is_keep and req.maintain_right_ground in {
        MaintainRightGroundEnum.DEATH_OF_EU_CITIZEN,
        MaintainRightGroundEnum.MARITAL_NULLITY_DIVORCE_OR_CANCELLED_PARTNERSHIP,
    }
    fv["Casilla de verificación26"] = is_keep and req.maintain_right_ground == MaintainRightGroundEnum.VICTIM_OF_GENDER_OR_SEXUAL_VIOLENCE_OR_TRAFFICKING
    fv["Casilla de verificación27"] = is_keep and req.maintain_right_ground == MaintainRightGroundEnum.OTHER_CHILD_CUSTODY_OR_VISITATION
    fv["Casilla de verificación28"] = req.truth_statement_accepted

    sig = form.signature
    fv["Texto65"] = sig.place
    fv["Texto66"] = sig.day
    fv["Texto67"] = sig.month
    fv["Texto68"] = sig.year
    fv["Texto69"] = _s(sig.eu_citizen_signature_name)
    fv["Texto70"] = _s(sig.applicant_signature_name)

    off = form.office
    fv["Texto71"] = _s(off.target_office)
    fv["Texto72"] = _s(off.dir3_code)
    fv["Texto73"] = off.province

    return fv
