"""Mapper for EX29 domain model to PDF field values."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any
from mappers.helpers import assign_checkboxes, coerce_str as _s, split_nie as _split_nie

if TYPE_CHECKING:
    from models.ex29 import EX29FormSchema


def to_field_values(form: EX29FormSchema) -> dict[str, Any]:
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
    fv["Texto24"] = _s(a.legal_representative_name)
    fv["Texto25"] = _s(a.legal_representative_id)
    fv["Texto26"] = _s(a.legal_representative_title)

    assign_checkboxes(fv, a.gender.value, {
        "Casilla de verificación60": "X",
        "Casilla de verificación61": "H",
        "Casilla de verificación62": "M",
    })
    assign_checkboxes(fv, a.marital_status.value, {
        "Casilla de verificación63": "S",
        "Casilla de verificación64": "C",
        "Casilla de verificación65": "V",
        "Casilla de verificación66": "D",
        "Casilla de verificación67": "Sp",
    })

    r = form.filing_representative
    fv["Texto27"] = _s(r.name_or_company) if r else ""
    fv["Texto28"] = _s(r.id_number) if r else ""
    fv["Texto29"] = _s(r.address) if r else ""
    fv["Texto30"] = _s(r.address_number) if r else ""
    fv["Texto31"] = _s(r.floor_door) if r else ""
    fv["Texto32"] = _s(r.city) if r else ""
    fv["Texto33"] = _s(r.postal_code) if r else ""
    fv["Texto34"] = _s(r.province) if r else ""
    fv["Texto35"] = _s(r.mobile_phone) if r else ""
    fv["Texto36"] = _s(r.email) if r else ""
    fv["Texto37"] = _s(r.legal_representative_name) if r else ""
    fv["Texto38"] = _s(r.legal_representative_id) if r else ""
    fv["Texto39"] = _s(r.legal_representative_title) if r else ""

    n = form.notification_address
    fv["Texto40"] = n.name_or_company
    fv["Texto41"] = n.id_number
    fv["Texto42"] = n.address
    fv["Texto43"] = _s(n.address_number)
    fv["Texto44"] = _s(n.floor_door)
    fv["Texto45"] = n.city
    fv["Texto46"] = n.postal_code
    fv["Texto47"] = n.province
    fv["Texto48"] = _s(n.mobile_phone)
    fv["Texto49"] = _s(n.email)
    fv["Casilla de verificación68"] = n.consent_electronic_notifications

    e = form.extension_request
    fv["Texto50"] = _s(e.other_description)
    fv["Texto51"] = e.justification_and_extension_period
    fv["Casilla de verificación69"] = e.ordinary_stay_without_visa
    fv["Casilla de verificación70"] = e.short_stay_visa_holder
    fv["Casilla de verificación71"] = e.displaced_minor_medical_treatment
    fv["Casilla de verificación72"] = e.other

    s = form.signature
    fv["Texto52"] = s.place
    fv["Texto53"] = s.day
    fv["Texto54"] = s.month
    fv["Texto55"] = s.year
    fv["Texto56"] = _s(s.signer_name)

    o = form.office
    fv["Texto57"] = _s(o.target_office)
    fv["Texto58"] = _s(o.dir3_code)
    fv["Texto59"] = o.province

    return fv