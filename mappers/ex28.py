"""Mapper for EX28 domain model to PDF field values."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any
from mappers.helpers import assign_checkboxes, coerce_str as _s, split_nie as _split_nie

if TYPE_CHECKING:
    from models.ex28 import EX28FormSchema


def to_field_values(form: EX28FormSchema) -> dict[str, Any]:
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
    fv["Texto24"] = _s(a.current_authorization_type)
    fv["Texto25"] = _s(a.current_authorization_id)
    fv["Texto26"] = _s(a.legal_representative_name)
    fv["Texto27"] = _s(a.legal_representative_id)
    fv["Texto28"] = _s(a.legal_representative_title)

    assign_checkboxes(fv, a.gender.value, {
        "Casilla de verificación29": "X",
        "Casilla de verificación30": "H",
        "Casilla de verificación31": "M",
    })
    assign_checkboxes(fv, a.marital_status.value, {
        "Casilla de verificación32": "S",
        "Casilla de verificación33": "C",
        "Casilla de verificación34": "V",
        "Casilla de verificación35": "D",
        "Casilla de verificación36": "Sp",
    })
    fv["Casilla de verificación37"] = a.has_school_age_children_in_spain
    fv["Casilla de verificación38"] = not a.has_school_age_children_in_spain

    p = form.pending_application
    fv["Texto54"] = p.case_number
    fv["Texto55"] = p.filing_date

    r = form.filing_representative
    fv["Texto56"] = _s(r.name_or_company) if r else ""
    fv["Texto57"] = _s(r.id_number) if r else ""
    fv["Texto58"] = _s(r.address) if r else ""
    fv["Texto59"] = _s(r.address_number) if r else ""
    fv["Texto60"] = _s(r.floor_door) if r else ""
    fv["Texto61"] = _s(r.city) if r else ""
    fv["Texto62"] = _s(r.postal_code) if r else ""
    fv["Texto63"] = _s(r.province) if r else ""
    fv["Texto64"] = _s(r.mobile_phone) if r else ""
    fv["Texto65"] = _s(r.email) if r else ""
    fv["Texto66"] = _s(r.legal_representative_name) if r else ""
    fv["Texto67"] = _s(r.legal_representative_id) if r else ""
    fv["Texto68"] = _s(r.legal_representative_title) if r else ""

    n = form.notification_address
    fv["Casilla de verificación39"] = n.consent_electronic_notifications
    fv["Texto69"] = n.name_or_company
    fv["Texto70"] = n.id_number
    fv["Texto71"] = n.address
    fv["Texto72"] = _s(n.address_number)
    fv["Texto73"] = _s(n.floor_door)
    fv["Texto74"] = n.city
    fv["Texto75"] = n.postal_code
    fv["Texto76"] = n.province
    fv["Texto77"] = _s(n.mobile_phone)
    fv["Texto78"] = _s(n.email)

    req = form.request_details
    fv["Casilla de verificación40"] = req.long_term_stay_from_study_or_mobility_or_volunteering
    fv["Casilla de verificación41"] = req.exceptional_circumstances_family_roots_to_parent_guardian_of_eu_minor
    fv["Casilla de verificación42"] = req.exceptional_circumstances_training_roots_to_sociotraining_roots
    fv["Casilla de verificación43"] = req.exceptional_circumstances_social_roots_employment_to_sociolabor_roots
    fv["Casilla de verificación44"] = req.exceptional_circumstances_social_roots_self_employment_to_social_roots
    fv["Casilla de verificación45"] = req.exceptional_circumstances_other_to_equivalent_title_vii
    fv["Casilla de verificación46"] = req.temporary_residence_title_iv_to_equivalent_title_iv
    fv["Casilla de verificación47"] = req.temporary_residence_minor_child_or_ward_to_equivalent
    fv["Casilla de verificación48"] = req.long_term_residence_to_long_term_national
    fv["Casilla de verificación49"] = req.long_term_residence_to_long_term_eu
    fv["Casilla de verificación50"] = req.modification_of_situations_to_title_xi_equivalent
    fv["Casilla de verificación51"] = req.simultaneous_family_reunification_requests
    fv["Casilla de verificación52"] = not req.simultaneous_family_reunification_requests
    fv["Casilla de verificación53"] = req.family_members_of_spanish_nationals_transition

    s = form.signature
    fv["Texto79"] = s.place
    fv["Texto80"] = s.day
    fv["Texto81"] = s.month
    fv["Texto82"] = s.year
    fv["Texto83"] = _s(s.signer_name)

    o = form.office
    fv["Texto84"] = _s(o.target_office)
    fv["Texto85"] = _s(o.dir3_code)
    fv["Texto86"] = o.province

    return fv