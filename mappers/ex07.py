"""Mapper for EX07 domain model to PDF field values."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any
from mappers.helpers import assign_checkboxes, coerce_str as _s, split_nie as _split_nie

if TYPE_CHECKING:
    from models.ex07 import EX07FormSchema


def to_field_values(form: EX07FormSchema) -> dict[str, Any]:
    from models.ex07 import (
        ApplicationCategoryEnum,
        InitialGroundEnum,
        RenewalGroundEnum,
        SignerRoleEnum,
        TerritorialScopeGroundEnum,
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
        "Casilla de verificación62": "X",
        "Casilla de verificación63": "H",
        "Casilla de verificación64": "M",
    })
    assign_checkboxes(fv, f.marital_status.value, {
        "Casilla de verificación65": "S",
        "Casilla de verificación66": "C",
        "Casilla de verificación67": "V",
        "Casilla de verificación68": "D",
        "Casilla de verificación69": "Sp",
    })
    fv["Casilla de verificación70"] = f.children_in_school_age
    fv["Casilla de verificación71"] = not f.children_in_school_age

    # Section 2: Self-employment details
    se = form.self_employment_details
    fv["Texto27"] = se.name_or_company
    fv["Texto28"] = se.id_number
    fv["Texto29"] = se.activity
    fv["Texto30"] = _s(se.cnae_code)
    fv["Texto31"] = se.address
    fv["Texto32"] = _s(se.address_number)
    fv["Texto33"] = _s(se.floor_door)
    fv["Texto34"] = se.city
    fv["Texto35"] = se.postal_code
    fv["Texto36"] = se.province
    fv["Texto37"] = _s(se.mobile_phone)
    fv["Texto38"] = _s(se.email)

    # Section 3: Filing representative
    r = form.filing_representative
    fv["Texto39"] = _s(r.name_or_company) if r else ""
    fv["Texto40"] = _s(r.id_number) if r else ""
    fv["Texto41"] = _s(r.address) if r else ""
    fv["Texto42"] = _s(r.address_number) if r else ""
    fv["Texto43"] = _s(r.floor_door) if r else ""
    fv["Texto44"] = _s(r.city) if r else ""
    fv["Texto45"] = _s(r.postal_code) if r else ""
    fv["Texto46"] = _s(r.province) if r else ""
    fv["Texto47"] = _s(r.mobile_phone) if r else ""
    fv["Texto48"] = _s(r.email) if r else ""
    fv["Texto49"] = _s(r.legal_rep_name) if r else ""
    fv["Texto50"] = _s(r.legal_rep_id) if r else ""
    fv["Texto51"] = _s(r.legal_rep_title) if r else ""

    # Section 4: Notification
    n = form.notification_address
    fv["Texto52"] = n.name_or_company
    fv["Texto53"] = n.id_number
    fv["Texto54"] = n.address
    fv["Texto55"] = _s(n.address_number)
    fv["Texto56"] = _s(n.floor_door)
    fv["Texto57"] = n.city
    fv["Texto58"] = n.postal_code
    fv["Texto59"] = n.province
    fv["Texto60"] = _s(n.mobile_phone)
    fv["Texto61"] = _s(n.email)
    fv["Casilla de verificación72"] = n.consent_electronic_notifications

    # Section 5: Request + signature + office
    req = form.request_details
    is_initial = req.category == ApplicationCategoryEnum.INITIAL
    is_renewal = req.category == ApplicationCategoryEnum.RENEWAL
    is_scope = req.category == ApplicationCategoryEnum.TERRITORIAL_SCOPE_EXTENSION

    fv["Casilla de verificación73"] = is_initial
    fv["Casilla de verificación74"] = is_initial and req.initial_ground == InitialGroundEnum.GENERAL_RESIDENT_OUTSIDE_SPAIN_ART_85
    fv["Casilla de verificación76"] = is_initial and req.initial_ground == InitialGroundEnum.INTERNATIONAL_AGREEMENTS_ANDORRA
    fv["Casilla de verificación77"] = is_initial and req.initial_ground == InitialGroundEnum.CROSS_BORDER_SELF_EMPLOYED_ART_157

    fv["Casilla de verificación78"] = is_renewal
    fv["Casilla de verificación79"] = is_renewal and req.renewal_ground == RenewalGroundEnum.CONTINUITY_ART_86
    fv["Casilla de verificación80"] = is_renewal and req.renewal_ground == RenewalGroundEnum.OTHER_CASES_ART_86
    fv["Casilla de verificación81"] = is_renewal and req.renewal_ground == RenewalGroundEnum.CROSS_BORDER_SELF_EMPLOYED_ART_158

    fv["Casilla de verificación82"] = is_scope
    fv["Casilla de verificación83"] = is_scope and req.territorial_scope_ground == TerritorialScopeGroundEnum.SAME_ACTIVITY_MULTIPLE_AUTONOMOUS_COMMUNITIES_ART_85_6

    fv["Casilla de verificación84"] = req.signer_role == SignerRoleEnum.FOREIGNER
    fv["Casilla de verificación85"] = req.signer_role == SignerRoleEnum.REPRESENTATIVE

    s = form.signature
    fv["Texto86"] = s.place
    fv["Texto87"] = s.day
    fv["Texto88"] = s.month
    fv["Texto89"] = s.year
    fv["Texto90"] = _s(s.name)

    o = form.office
    fv["Texto91"] = _s(o.target_office)
    fv["Texto92"] = _s(o.dir3_code)
    fv["Texto93"] = o.province

    return fv
