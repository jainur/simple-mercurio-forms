"""Mapper for EX06 domain model to PDF field values."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any
from mappers.helpers import assign_checkboxes, coerce_str as _s, split_nie as _split_nie

if TYPE_CHECKING:
    from models.ex06 import EX06FormSchema


def to_field_values(form: EX06FormSchema) -> dict[str, Any]:
    from models.ex06 import ApplicationTypeEnum

    fv: dict[str, Any] = {}

    # Section 1: Foreigner
    f = form.foreigner_details
    fv["Texto1"] = _s(f.passport)
    if f.nie:
        n1, n2, n3 = _split_nie(f.nie)
        fv["Texto3"], fv["Texto4"], fv["Texto5"] = n1, n2, n3
    else:
        fv["Texto3"] = fv["Texto4"] = fv["Texto5"] = ""

    fv["Texto6"] = f.first_surname
    fv["Texto7"] = _s(f.second_surname)
    fv["Texto8"] = f.name
    assign_checkboxes(fv, f.gender.value, {
        "Casilla de verificación9": "X",
        "Casilla de verificación10": "H",
        "Casilla de verificación11": "M",
    })

    fv["Texto12"] = f.date_of_birth.strftime("%d")
    fv["Texto13"] = f.date_of_birth.strftime("%m")
    fv["Texto14"] = f.date_of_birth.strftime("%Y")
    fv["Texto15"] = f.birth_place
    fv["Texto16"] = f.birth_country
    fv["Texto17"] = f.nationality

    assign_checkboxes(fv, f.marital_status.value, {
        "Casilla de verificación18": "S",
        "Casilla de verificación19": "C",
        "Casilla de verificación20": "V",
        "Casilla de verificación21": "D",
        "Casilla de verificación22": "Sp",
    })

    fv["Texto23"] = _s(f.father_name)
    fv["Texto24"] = _s(f.mother_name)
    fv["Texto25"] = f.address
    fv["Texto26"] = _s(f.address_number)
    fv["Texto27"] = _s(f.floor_door)
    fv["Texto28"] = f.city
    fv["Texto29"] = f.postal_code
    fv["Texto30"] = f.province
    fv["Texto31"] = _s(f.mobile_phone)
    fv["Texto32"] = _s(f.email)
    fv["Texto33"] = _s(f.legal_guardian_name)
    fv["Texto34"] = _s(f.legal_guardian_id)
    fv["Texto35"] = _s(f.legal_guardian_title)

    # Section 2: Employer
    e = form.employer_details
    fv["Texto36"] = e.name_or_company
    fv["Texto37"] = e.id_number
    fv["Texto38"] = e.activity
    fv["Texto39"] = e.occupation
    fv["Texto40"] = e.address
    fv["Texto41"] = _s(e.address_number)
    fv["Texto42"] = _s(e.floor_door)
    fv["Texto43"] = e.city
    fv["Texto44"] = e.postal_code
    fv["Texto45"] = e.province
    fv["Texto46"] = _s(e.mobile_phone)
    fv["Texto47"] = _s(e.email)
    fv["Texto48"] = _s(e.legal_rep_name)
    fv["Texto49"] = _s(e.legal_rep_id)

    # Section 3: Filing representative
    r = form.filing_representative
    fv["Texto50"] = _s(r.name_or_company) if r else ""
    fv["Texto51"] = _s(r.id_number) if r else ""
    fv["Texto52"] = _s(r.address) if r else ""
    fv["Texto53"] = _s(r.address_number) if r else ""
    fv["Texto54"] = _s(r.floor_door) if r else ""
    fv["Texto55"] = _s(r.city) if r else ""
    fv["Texto56"] = _s(r.postal_code) if r else ""
    fv["Texto57"] = _s(r.province) if r else ""
    fv["Texto58"] = _s(r.mobile_phone) if r else ""
    fv["Texto59"] = _s(r.email) if r else ""
    fv["Texto60"] = _s(r.legal_rep_name) if r else ""
    fv["Texto61"] = _s(r.legal_rep_id) if r else ""
    fv["Texto62"] = _s(r.legal_rep_title) if r else ""

    # Section 4: Notification
    n = form.notification_address
    fv["Texto63"] = n.name_or_company
    fv["Texto64"] = n.id_number
    fv["Texto65"] = n.address
    fv["Texto66"] = _s(n.address_number)
    fv["Texto67"] = _s(n.floor_door)
    fv["Texto68"] = n.city
    fv["Texto69"] = n.postal_code
    fv["Texto70"] = n.province
    fv["Texto71"] = _s(n.mobile_phone)
    fv["Texto72"] = _s(n.email)
    fv["Casilla de verificación73"] = n.consent_electronic_notifications

    # Section 5: Request + signature + office
    req = form.request_details
    fv["Casilla de verificación74"] = req.application_type == ApplicationTypeEnum.RESIDENCIA_INICIAL
    fv["Casilla de verificación75"] = req.application_type == ApplicationTypeEnum.PRIMER_LLAMAMIENTO
    fv["Casilla de verificación76"] = req.application_type == ApplicationTypeEnum.SEGUNDO_LLAMAMIENTO
    fv["Casilla de verificación77"] = req.application_type == ApplicationTypeEnum.TERCER_LLAMAMIENTO
    fv["Casilla de verificación78"] = req.application_type == ApplicationTypeEnum.CAMBIO_EMPLEADOR
    fv["Casilla de verificación79"] = req.application_type == ApplicationTypeEnum.PRORROGA_O_CONCATENACION
    fv["Casilla de verificación80"] = req.application_type == ApplicationTypeEnum.RENOVACION_PLURIANUAL
    fv["Casilla de verificación81"] = req.accepts_truth_responsibility

    s = form.signature
    fv["Texto82"] = s.place
    fv["Texto83"] = s.day
    fv["Texto84"] = s.month
    fv["Texto85"] = s.year
    fv["Texto86"] = _s(s.name)

    o = form.office
    fv["Texto87"] = _s(o.target_office)
    fv["Texto88"] = _s(o.dir3_code)
    fv["Texto89"] = o.province

    return fv
