"""Mapper for EX25 domain model to PDF field values."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any
from mappers.helpers import assign_checkboxes, coerce_str as _s, split_nie as _split_nie

if TYPE_CHECKING:
    from models.ex25 import EX25FormSchema


def to_field_values(form: EX25FormSchema) -> dict[str, Any]:
    fv: dict[str, Any] = {}

    m = form.minor_details
    fv["Texto157"] = _s(m.passport)
    if m.nie:
        n1, n2, n3 = _split_nie(m.nie)
        fv["Texto158"], fv["Texto159"], fv["Texto160"] = n1, n2, n3
    else:
        fv["Texto158"] = fv["Texto159"] = fv["Texto160"] = ""
    fv["Texto161"] = m.first_surname
    fv["Texto162"] = _s(m.second_surname)
    fv["Texto163"] = m.name
    fv["Texto164"] = m.date_of_birth.strftime("%d")
    fv["Texto165"] = m.date_of_birth.strftime("%m")
    fv["Texto166"] = m.date_of_birth.strftime("%Y")
    fv["Texto167"] = m.birth_place
    fv["Texto168"] = m.birth_country
    fv["Texto169"] = m.nationality
    fv["Texto170"] = _s(m.father_name)
    fv["Texto171"] = _s(m.mother_name)
    fv["Texto172"] = m.address
    fv["Texto173"] = _s(m.address_number)
    fv["Texto174"] = _s(m.floor_door)
    fv["Texto175"] = m.city
    fv["Texto176"] = _s(m.mobile_phone)
    fv["Texto177"] = m.postal_code
    fv["Texto178"] = m.province
    fv["Texto179"] = _s(m.email)
    fv["Texto180"] = _s(m.legal_guardian_name)
    fv["Texto181"] = _s(m.legal_guardian_id)
    fv["Texto182"] = _s(m.legal_guardian_title)
    fv["Texto183"] = _s(m.representative_nature)
    fv["Texto184"] = _s(m.relationship_with_minor)

    assign_checkboxes(fv, m.gender.value, {
        "Casilla de verificación235": "X",
        "Casilla de verificación236": "H",
        "Casilla de verificación237": "M",
    })

    g = form.guardian_or_entity_details
    fv["Texto185"] = g.name_or_company
    fv["Texto186"] = g.id_number
    fv["Texto187"] = g.address
    fv["Texto188"] = _s(g.address_number)
    fv["Texto189"] = _s(g.floor_door)
    fv["Texto190"] = g.city
    fv["Texto191"] = g.postal_code
    fv["Texto192"] = g.province
    fv["Texto193"] = _s(g.mobile_phone)
    fv["Texto194"] = _s(g.email)
    fv["Texto195"] = _s(g.legal_rep_name)
    fv["Texto196"] = _s(g.legal_rep_id)
    fv["Texto197"] = _s(g.legal_rep_title)

    r = form.filing_representative
    fv["Texto198"] = r.name_or_company
    fv["Texto199"] = r.id_number
    fv["Texto200"] = r.address
    fv["Texto201"] = _s(r.address_number)
    fv["Texto202"] = _s(r.floor_door)
    fv["Texto203"] = r.city
    fv["Texto204"] = r.postal_code
    fv["Texto205"] = r.province
    fv["Texto206"] = _s(r.mobile_phone)
    fv["Texto207"] = _s(r.email)
    fv["Texto208"] = _s(r.legal_rep_name)
    fv["Texto209"] = _s(r.legal_rep_id)
    fv["Texto210"] = _s(r.legal_rep_title)

    n = form.notification_address
    fv["Texto211"] = n.name_or_company
    fv["Texto212"] = n.id_number
    fv["Texto213"] = n.address
    fv["Texto214"] = _s(n.address_number)
    fv["Texto215"] = _s(n.floor_door)
    fv["Texto216"] = n.city
    fv["Texto217"] = n.postal_code
    fv["Texto218"] = n.province
    fv["Texto219"] = _s(n.mobile_phone)
    fv["Texto220"] = _s(n.email)
    fv["Casilla de verificación260"] = n.consent_electronic_notifications

    req = form.request_details
    fv["Casilla de verificación238"] = req.temporary_residence_minor_born_in_spain
    fv["Casilla de verificación239"] = req.temporary_residence_accompanied_disabled_minor_not_born_in_spain
    fv["Casilla de verificación240"] = req.temporary_residence_dana_2024_minor_with_guardian
    fv["Casilla de verificación241"] = req.temporary_initial_unaccompanied_minor
    fv["Casilla de verificación242"] = req.temporary_initial_former_ward_without_residence_at_majority
    fv["Casilla de verificación243"] = req.temporary_initial_displaced_minor_medical_treatment_extension_exhausted
    fv["Casilla de verificación244"] = req.temporary_initial_parent_or_guardian_medical_treatment_extension_exhausted
    fv["Casilla de verificación245"] = req.renewal_unaccompanied_minor_with_residence
    fv["Casilla de verificación246"] = req.renewal_former_ward_with_residence_at_majority
    fv["Casilla de verificación247"] = req.renewal_former_ward_without_residence_at_majority
    fv["Casilla de verificación248"] = req.renewal_displaced_minor_medical_treatment_exceptional
    fv["Casilla de verificación249"] = req.renewal_parent_or_guardian_medical_treatment_exceptional
    fv["Casilla de verificación250"] = req.humanitarian_program_minor_medical_treatment_stay
    fv["Casilla de verificación251"] = req.humanitarian_program_parent_or_guardian_medical_treatment_stay
    fv["Casilla de verificación252"] = req.humanitarian_program_minor_holiday_stay
    fv["Casilla de verificación253"] = req.humanitarian_program_monitor_holiday_stay
    fv["Casilla de verificación254"] = req.humanitarian_program_schooling_stay
    fv["Casilla de verificación255"] = req.humanitarian_extension_medical_treatment
    fv["Casilla de verificación256"] = req.humanitarian_extension_parent_or_guardian_medical_treatment
    fv["Casilla de verificación257"] = req.humanitarian_extension_schooling_exceptional_return_impediment
    fv["Casilla de verificación258"] = req.other_international_adoption
    fv["Casilla de verificación259"] = req.other_vacations_in_peace_program

    s = form.signature
    fv["Texto221"] = s.day
    fv["Texto222"] = _s(s.signer_1_id)
    fv["Texto223"] = _s(s.signer_1_title)
    fv["Texto224"] = s.place
    fv["Texto225"] = _s(s.signer_2_id)
    fv["Texto226"] = _s(s.signer_2_title)
    fv["Texto227"] = s.month
    fv["Texto228"] = s.year
    fv["Texto229"] = _s(s.signer_1_name)
    fv["Texto230"] = ""
    fv["Texto231"] = _s(s.signer_2_name)

    o = form.office
    fv["Texto232"] = _s(o.target_office)
    fv["Texto233"] = _s(o.dir3_code)
    fv["Texto234"] = o.province

    return fv
