"""Mapper for EX22 domain model to PDF field values."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any
from mappers.helpers import assign_checkboxes, coerce_str as _s, split_nie as _split_nie

if TYPE_CHECKING:
    from models.ex22 import EX22FormSchema


def to_field_values(form: EX22FormSchema) -> dict[str, Any]:
    from models.ex22 import ModificationGroundEnum, RequestCategoryEnum, WorkModeEnum

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
    fv["Texto16"] = _s(a.mobile_phone)
    fv["Texto17"] = _s(a.email)
    fv["Texto18"] = _s(a.legal_guardian_name)
    fv["Texto19"] = _s(a.legal_guardian_id)
    fv["Texto20"] = _s(a.legal_guardian_title)

    assign_checkboxes(fv, a.gender.value, {
        "Casilla de verificación64": "X",
        "Casilla de verificación65": "H",
        "Casilla de verificación66": "M",
    })
    assign_checkboxes(fv, a.marital_status.value, {
        "Casilla de verificación67": "S",
        "Casilla de verificación68": "C",
        "Casilla de verificación69": "V",
        "Casilla de verificación70": "D",
        "Casilla de verificación71": "Sp",
    })

    e = form.employer_details
    fv["Texto21"] = e.name_or_company
    fv["Texto22"] = e.id_number
    fv["Texto23"] = e.activity
    fv["Texto24"] = e.occupation
    fv["Texto25"] = e.address
    fv["Texto26"] = _s(e.address_number)
    fv["Texto27"] = _s(e.floor_door)
    fv["Texto28"] = e.city
    fv["Texto29"] = e.postal_code
    fv["Texto30"] = e.province

    r = form.filing_representative
    fv["Texto31"] = _s(r.name_or_company) if r else ""
    fv["Texto32"] = _s(r.id_number) if r else ""
    fv["Texto33"] = _s(r.address) if r else ""
    fv["Texto34"] = _s(r.address_number) if r else ""
    fv["Texto35"] = _s(r.floor_door) if r else ""
    fv["Texto36"] = _s(r.city) if r else ""
    fv["Texto37"] = _s(r.postal_code) if r else ""
    fv["Texto38"] = _s(r.province) if r else ""
    fv["Texto39"] = _s(r.mobile_phone) if r else ""
    fv["Texto40"] = _s(r.email) if r else ""
    fv["Texto41"] = _s(r.legal_rep_name) if r else ""
    fv["Texto42"] = _s(r.legal_rep_id) if r else ""
    fv["Texto43"] = _s(r.legal_rep_title) if r else ""

    n = form.notification_address
    fv["Texto44"] = n.name_or_company
    fv["Texto45"] = n.id_number
    fv["Texto46"] = n.address
    fv["Texto47"] = _s(n.address_number)
    fv["Texto48"] = _s(n.floor_door)
    fv["Texto49"] = n.city
    fv["Texto50"] = n.postal_code
    fv["Texto51"] = n.province
    fv["Texto52"] = _s(n.mobile_phone)
    fv["Texto53"] = _s(n.email)
    fv["Casilla de verificación72"] = n.consent_electronic_notifications

    req = form.request_details
    fv["Texto54"] = _s(req.identity_document_change_text)
    fv["Texto55"] = _s(req.cause_specification)

    is_initial = req.category == RequestCategoryEnum.INITIAL
    is_renewed = req.category == RequestCategoryEnum.RENEWED
    is_mod = req.category == RequestCategoryEnum.MODIFICATION
    is_dereg = req.category == RequestCategoryEnum.DEREGISTRATION

    fv["Casilla de verificación73"] = is_initial
    fv["Casilla de verificación74"] = is_initial and req.work_mode == WorkModeEnum.EMPLOYEE
    fv["Casilla de verificación75"] = is_initial and req.work_mode == WorkModeEnum.SELF_EMPLOYED
    fv["Casilla de verificación76"] = is_renewed
    fv["Casilla de verificación77"] = is_renewed and req.work_mode == WorkModeEnum.EMPLOYEE
    fv["Casilla de verificación78"] = is_renewed and req.work_mode == WorkModeEnum.SELF_EMPLOYED

    fv["Casilla de verificación79"] = is_mod
    fv["Casilla de verificación80"] = is_mod and req.modification_ground == ModificationGroundEnum.PERSONAL_DATA
    fv["Casilla de verificación81"] = is_mod and req.modification_ground == ModificationGroundEnum.LABOR_OR_PROFESSIONAL_DATA
    fv["Casilla de verificación82"] = is_mod and req.modification_ground == ModificationGroundEnum.ADDRESS_CHANGE
    fv["Casilla de verificación83"] = is_mod and req.modification_ground == ModificationGroundEnum.IDENTITY_DOCUMENT_CHANGE
    fv["Casilla de verificación84"] = is_mod and req.modification_ground == ModificationGroundEnum.OTHER

    fv["Casilla de verificación85"] = is_dereg
    fv["Casilla de verificación86"] = bool(req.cause_specification)
    fv["Casilla de verificación87"] = req.truth_statement_accepted

    s = form.signature
    fv["Texto56"] = s.place
    fv["Texto57"] = s.day
    fv["Texto58"] = s.month
    fv["Texto59"] = s.year
    fv["Texto60"] = _s(s.name)

    o = form.office
    fv["Texto61"] = _s(o.target_office)
    fv["Texto62"] = _s(o.dir3_code)
    fv["Texto63"] = o.province

    return fv
