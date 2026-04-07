"""Mapper for EX04 domain model to PDF field values."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any
from mappers.helpers import assign_checkboxes, coerce_str as _s, split_nie as _split_nie

if TYPE_CHECKING:
    from models.ex04 import EX04FormSchema


def to_field_values(form: EX04FormSchema) -> dict[str, Any]:
    from models.ex04 import (
        ApplicationCategoryEnum,
        FamilyAuthorizationPhaseEnum,
        InitialLocationEnum,
        PracticeBasisEnum,
    )

    fv: dict[str, Any] = {}

    # Section 1: Foreigner
    f = form.foreigner_details
    fv["Texto1"] = _s(f.passport)
    if f.nie:
        n1, n2, n3 = _split_nie(f.nie)
        fv["Texto2"], fv["Texto3"], fv["Texto4"] = n1, n2, n3
    else:
        fv["Texto2"] = fv["Texto3"] = fv["Texto4"] = ""

    fv["Texto5"] = f.first_surname
    fv["Texto6"] = _s(f.second_surname)
    fv["Texto7"] = f.name
    fv["Texto8"] = f.date_of_birth.strftime("%d")
    fv["Texto9"] = f.date_of_birth.strftime("%m")
    fv["Texto10"] = f.date_of_birth.strftime("%Y")
    fv["Texto11"] = f.birth_place
    fv["Texto12"] = f.birth_country
    fv["Texto13"] = f.nationality
    fv["Texto14"] = _s(f.father_name)
    fv["Texto15"] = _s(f.mother_name)
    fv["Texto16"] = f.address
    fv["Texto17"] = _s(f.address_number)
    fv["Texto18"] = _s(f.floor_door)
    fv["Texto19"] = f.city
    fv["Texto20"] = f.postal_code
    fv["Texto21"] = f.province
    fv["Texto22"] = _s(f.mobile_phone)
    fv["Texto23"] = _s(f.email)
    fv["Texto24"] = _s(f.legal_guardian_name)
    fv["Texto25"] = _s(f.legal_guardian_id)
    fv["Texto26"] = _s(f.legal_guardian_title)

    assign_checkboxes(fv, f.gender.value, {
        "Casilla de verificación73": "X",
        "Casilla de verificación74": "H",
        "Casilla de verificación75": "M",
    })
    assign_checkboxes(fv, f.marital_status.value, {
        "Casilla de verificación76": "S",
        "Casilla de verificación77": "C",
        "Casilla de verificación78": "V",
        "Casilla de verificación79": "D",
        "Casilla de verificación80": "Sp",
    })

    # Section 2: Host entity
    h = form.host_entity_details
    fv["Texto27"] = h.name_or_company
    fv["Texto28"] = h.id_number
    fv["Texto29"] = h.activity
    fv["Texto30"] = h.occupation
    fv["Texto31"] = h.address
    fv["Texto32"] = _s(h.address_number)
    fv["Texto33"] = _s(h.floor_door)
    fv["Texto34"] = h.city
    fv["Texto35"] = h.postal_code
    fv["Texto36"] = h.province
    fv["Texto37"] = _s(h.mobile_phone)
    fv["Texto38"] = _s(h.email)
    fv["Texto39"] = _s(h.legal_rep_name)
    fv["Texto40"] = _s(h.legal_rep_id)
    fv["Texto41"] = _s(h.legal_rep_title)

    # Section 3: Filing representative
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

    # Section 4: Notification
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
    fv["Casilla de verificación81"] = n.consent_electronic_notifications

    # Section 5: Request + signature + office
    req = form.request_details

    is_initial = req.category == ApplicationCategoryEnum.INITIAL
    is_renewal = req.category == ApplicationCategoryEnum.RENEWAL
    is_family = req.category == ApplicationCategoryEnum.FAMILY

    fv["Casilla de verificación82"] = is_initial
    fv["Casilla de verificación83"] = is_initial and req.initial_location == InitialLocationEnum.OUTSIDE_SPAIN
    fv["Casilla de verificación84"] = is_initial and req.initial_location == InitialLocationEnum.OUTSIDE_SPAIN and req.initial_basis == PracticeBasisEnum.AGREEMENT
    fv["Casilla de verificación85"] = is_initial and req.initial_location == InitialLocationEnum.OUTSIDE_SPAIN and req.initial_basis == PracticeBasisEnum.EMPLOYMENT_CONTRACT
    fv["Casilla de verificación86"] = is_initial and req.initial_location == InitialLocationEnum.IN_SPAIN
    fv["Casilla de verificación87"] = is_initial and req.initial_location == InitialLocationEnum.IN_SPAIN and req.initial_basis == PracticeBasisEnum.AGREEMENT
    fv["Casilla de verificación88"] = is_initial and req.initial_location == InitialLocationEnum.IN_SPAIN and req.initial_basis == PracticeBasisEnum.EMPLOYMENT_CONTRACT

    fv["Casilla de verificación89"] = is_renewal
    fv["Casilla de verificación90"] = is_renewal
    fv["Casilla de verificación91"] = is_renewal and req.renewal_basis == PracticeBasisEnum.AGREEMENT
    fv["Casilla de verificación92"] = is_renewal and req.renewal_basis == PracticeBasisEnum.EMPLOYMENT_CONTRACT

    fv["Casilla de verificación93"] = is_family
    fv["Casilla de verificación94"] = is_family and req.family_phase == FamilyAuthorizationPhaseEnum.INITIAL
    fv["Casilla de verificación95"] = is_family and req.family_phase == FamilyAuthorizationPhaseEnum.RENEWED
    fv["Casilla de verificación96"] = req.is_host_entity_legal_representative_signing

    sig = form.signature
    fv["Texto65"] = sig.place
    fv["Texto66"] = sig.day
    fv["Texto67"] = sig.month
    fv["Texto68"] = sig.year
    fv["Texto69"] = _s(sig.name)

    off = form.office
    fv["Texto70"] = _s(off.target_office)
    fv["Texto71"] = _s(off.dir3_code)
    fv["Texto72"] = off.province

    return fv
