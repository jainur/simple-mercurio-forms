"""Mapper for EX24 domain model to PDF field values."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any
from mappers.helpers import assign_checkboxes, coerce_str as _s, split_nie as _split_nie

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
    fv["Texto1"] = _s(a.passport)
    if a.nie:
        n1, n2, n3 = _split_nie(a.nie)
        fv["Texto2"], fv["Texto3"], fv["Texto4"] = n1, n2, n3
    else:
        fv["Texto2"] = fv["Texto3"] = fv["Texto4"] = ""
    fv["Texto5"] = a.first_surname
    fv["Texto6"] = _s(a.second_surname)
    fv["Texto7"] = a.name
    fv["Texto8"] = a.date_of_birth.strftime("%d")
    fv["Texto9"] = a.date_of_birth.strftime("%m")
    fv["Texto10"] = a.date_of_birth.strftime("%Y")
    fv["Texto11"] = a.birth_place
    fv["Texto12"] = a.birth_country
    fv["Texto13"] = a.nationality
    fv["Texto14"] = _s(a.father_name)
    fv["Texto15"] = _s(a.mother_name)
    fv["Texto16"] = a.address
    fv["Texto17"] = _s(a.address_number)
    fv["Texto18"] = _s(a.floor_door)
    fv["Texto19"] = a.city
    fv["Texto20"] = a.postal_code
    fv["Texto21"] = a.province
    fv["Texto22"] = _s(a.mobile_phone)
    fv["Texto23"] = _s(a.email)
    fv["Texto24"] = _s(a.legal_guardian_name)
    fv["Texto25"] = _s(a.legal_guardian_id)
    fv["Texto26"] = _s(a.legal_guardian_title)

    assign_checkboxes(fv, a.gender.value, {
        "Casilla de verificación27": "X",
        "Casilla de verificación28": "H",
        "Casilla de verificación29": "M",
    })
    assign_checkboxes(fv, a.marital_status.value, {
        "Casilla de verificación30": "S",
        "Casilla de verificación31": "C",
        "Casilla de verificación32": "V",
        "Casilla de verificación33": "D",
        "Casilla de verificación34": "Sp",
    })

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
    fv["Texto62"] = _s(r.name_or_company) if r else ""
    fv["Texto63"] = _s(r.id_number) if r else ""
    fv["Texto64"] = _s(r.address) if r else ""
    fv["Texto65"] = _s(r.address_number) if r else ""
    fv["Texto66"] = _s(r.floor_door) if r else ""
    fv["Texto67"] = _s(r.city) if r else ""
    fv["Texto68"] = _s(r.postal_code) if r else ""
    fv["Texto69"] = _s(r.province) if r else ""
    fv["Texto70"] = _s(r.mobile_phone) if r else ""
    fv["Texto71"] = _s(r.email) if r else ""
    fv["Texto72"] = _s(r.legal_rep_name) if r else ""
    fv["Texto73"] = _s(r.legal_rep_id) if r else ""
    fv["Texto74"] = _s(r.legal_rep_title) if r else ""

    n = form.notification_address
    fv["Texto75"] = n.name_or_company
    fv["Texto76"] = n.id_number
    fv["Texto77"] = n.address
    fv["Texto78"] = _s(n.address_number)
    fv["Texto79"] = _s(n.floor_door)
    fv["Texto80"] = n.city
    fv["Texto81"] = n.postal_code
    fv["Texto82"] = n.province
    fv["Texto83"] = _s(n.mobile_phone)
    fv["Texto84"] = _s(n.email)
    fv["Casilla de verificación85"] = n.consent_electronic_notifications

    req = form.request_details
    is_initial = req.category == RequestCategoryEnum.INITIAL_RESIDENCE
    is_renewal = req.category == RequestCategoryEnum.RENEWAL
    is_independent = req.category == RequestCategoryEnum.INDEPENDENT_RESIDENCE_BY_PRESERVATION

    fv["Casilla de verificación86"] = is_initial
    fv["Casilla de verificación87"] = is_initial and req.initial_relationship == InitialRelationshipEnum.SPOUSE_OR_REGISTERED_OR_STABLE_PARTNER
    fv["Casilla de verificación88"] = is_initial and req.initial_relationship == InitialRelationshipEnum.CHILD_UNDER_26_OR_DISABLED
    fv["Casilla de verificación89"] = is_initial and req.initial_relationship == InitialRelationshipEnum.CHILD_OVER_26_DEPENDENT
    fv["Casilla de verificación90"] = is_initial and req.initial_relationship == InitialRelationshipEnum.FIRST_DEGREE_ASCENDANT
    fv["Casilla de verificación91"] = is_initial and req.initial_relationship == InitialRelationshipEnum.PARENT_OR_GUARDIAN_OF_SPANISH_MINOR
    fv["Casilla de verificación92"] = is_initial and req.initial_relationship == InitialRelationshipEnum.CAREGIVER_UP_TO_SECOND_DEGREE
    fv["Casilla de verificación93"] = is_initial and req.initial_relationship == InitialRelationshipEnum.CHILD_OF_SPANISH_PARENT_BY_ORIGIN
    fv["Casilla de verificación94"] = is_initial and req.initial_relationship == InitialRelationshipEnum.OTHER_DEPENDENT_FAMILY_MEMBER

    fv["Casilla de verificación95"] = is_renewal
    fv["Casilla de verificación96"] = is_independent
    fv["Casilla de verificación97"] = is_independent and req.preservation_ground == PreservationGroundEnum.DEATH_OF_SPANISH_NATIONAL
    fv["Casilla de verificación98"] = is_independent and req.preservation_ground == PreservationGroundEnum.END_OF_EFFECTIVE_RESIDENCE_IN_SPAIN
    fv["Casilla de verificación99"] = is_independent and req.preservation_ground == PreservationGroundEnum.NULLITY_DIVORCE_OR_CANCELLATION
    fv["Casilla de verificación100"] = is_independent and req.preservation_ground == PreservationGroundEnum.VICTIM_OF_GENDER_OR_SEXUAL_VIOLENCE_OR_FAMILY_VIOLENCE_OR_TRAFFICKING

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
