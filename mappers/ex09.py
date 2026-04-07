"""Mapper for EX09 domain model to PDF field values."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any
from mappers.helpers import assign_checkboxes, coerce_str as _s, split_nie as _split_nie

if TYPE_CHECKING:
    from models.ex09 import EX09FormSchema


def to_field_values(form: EX09FormSchema) -> dict[str, Any]:
    from models.ex09 import ApplicationCategoryEnum, InitialExceptionSubtypeEnum

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

    assign_checkboxes(fv, f.gender.value, {
        "Casilla de verificación79": "X",
        "Casilla de verificación80": "H",
        "Casilla de verificación81": "M",
    })
    assign_checkboxes(fv, f.marital_status.value, {
        "Casilla de verificación71": "S",
        "Casilla de verificación72": "C",
        "Casilla de verificación73": "V",
        "Casilla de verificación74": "D",
        "Casilla de verificación75": "Sp",
    })
    fv["Casilla de verificación76"] = f.children_in_school_age
    fv["Casilla de verificación77"] = not f.children_in_school_age

    # Section 2: Activity entity
    a = form.activity_entity_details
    fv["Texto24"] = a.name_or_company
    fv["Texto25"] = a.id_number
    fv["Texto26"] = a.activity
    fv["Texto27"] = a.occupation
    fv["Texto28"] = a.address
    fv["Texto29"] = _s(a.address_number)
    fv["Texto30"] = _s(a.floor_door)
    fv["Texto31"] = a.city
    fv["Texto32"] = a.postal_code
    fv["Texto33"] = a.province
    fv["Texto34"] = _s(a.mobile_phone)
    fv["Texto35"] = _s(a.email)
    fv["Texto36"] = _s(a.legal_rep_name)
    fv["Texto37"] = _s(a.legal_rep_id)
    fv["Texto38"] = _s(a.legal_rep_title)

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
    fv["Casilla de verificación78"] = n.consent_electronic_notifications

    # Section 5: Request + signature + office
    req = form.request_details
    is_initial = req.category == ApplicationCategoryEnum.INITIAL_EXCEPTION
    is_extension = req.category == ApplicationCategoryEnum.EXTENSION

    fv["Casilla de verificación82"] = is_initial
    fv["Casilla de verificación83"] = is_initial and req.initial_subtype == InitialExceptionSubtypeEnum.RELIGIOUS_MEMBER
    fv["Casilla de verificación84"] = is_initial and req.initial_subtype == InitialExceptionSubtypeEnum.OTHER
    fv["Texto62"] = _s(req.other_initial_exception_details)

    fv["Casilla de verificación85"] = is_extension
    fv["Casilla de verificación86"] = is_extension

    s = form.signature
    fv["Texto63"] = s.place
    fv["Texto67"] = s.day
    fv["Texto64"] = s.month
    fv["Texto65"] = s.year
    fv["Texto66"] = _s(s.name)

    o = form.office
    fv["Texto68"] = _s(o.target_office)
    fv["Texto69"] = _s(o.dir3_code)
    fv["Texto70"] = o.province

    return fv
