"""Mapper for EX30 domain model to PDF field values."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any
from mappers.helpers import assign_checkboxes, coerce_str as _s, split_nie as _split_nie

if TYPE_CHECKING:
    from models.ex30 import EX30FormSchema


def to_field_values(form: EX30FormSchema) -> dict[str, Any]:
    from models.ex30 import AuthorizationTypeEnum

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
        "Casilla de verificación1": "X",
        "Casilla de verificación2": "H",
        "Casilla de verificación3": "M",
    })
    assign_checkboxes(fv, a.marital_status.value, {
        "Casilla de verificación4": "S",
        "Casilla de verificación5": "C",
        "Casilla de verificación6": "V",
        "Casilla de verificación7": "D",
        "Casilla de verificación8": "Sp",
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
    fv["Casilla de verificación9"] = n.consent_electronic_notifications

    e = form.employer_details
    fv["Texto50"] = _s(e.name_or_company) if e else ""
    fv["Texto51"] = _s(e.tax_or_id_number) if e else ""
    fv["Texto52"] = _s(e.activity) if e else ""
    fv["Texto53"] = _s(e.cnae) if e else ""
    fv["Texto54"] = _s(e.cno_spe_2011) if e else ""
    fv["Texto55"] = _s(e.registered_address) if e else ""
    fv["Texto56"] = _s(e.address_number) if e else ""
    fv["Texto57"] = _s(e.floor_door) if e else ""
    fv["Texto58"] = _s(e.city) if e else ""
    fv["Texto59"] = _s(e.postal_code) if e else ""
    fv["Texto60"] = _s(e.province) if e else ""
    fv["Texto61"] = _s(e.mobile_phone) if e else ""
    fv["Texto62"] = _s(e.email) if e else ""
    fv["Texto63"] = _s(e.representative_name) if e else ""
    fv["Texto64"] = _s(e.representative_id) if e else ""
    fv["Texto65"] = _s(e.representative_title) if e else ""

    t = form.training_center_details
    fv["Texto66"] = _s(t.provider_name) if t else ""
    fv["Texto67"] = _s(t.training_name) if t else ""
    fv["Texto68"] = _s(t.course_code) if t else ""
    fv["Texto69"] = _s(t.provider_tax_id) if t else ""
    fv["Texto70"] = _s(t.provider_address) if t else ""
    fv["Texto71"] = _s(t.province) if t else ""
    fv["Texto72"] = _s(t.duration_hours) if t else ""
    fv["Texto73"] = _s(t.start_date) if t else ""
    fv["Texto74"] = _s(t.end_date) if t else ""
    fv["Casilla de verificación10"] = bool(t and t.secondary_post_compulsory_education)
    fv["Casilla de verificación11"] = bool(t and t.professional_certificate)
    fv["Casilla de verificación12"] = bool(t and t.adult_mandatory_education_in_person)
    fv["Casilla de verificación13"] = bool(t and t.public_employment_service_training)
    fv["Casilla de verificación14"] = bool(t and t.modality_presential)
    fv["Casilla de verificación15"] = bool(t and t.modality_non_presential)
    fv["Casilla de verificación16"] = bool(t and t.date_range_checkbox)

    req = form.request_details
    fv["Casilla de verificación17"] = True
    fv["Casilla de verificación18"] = req.authorization_type == AuthorizationTypeEnum.SECOND_CHANCE
    fv["Casilla de verificación19"] = req.authorization_type == AuthorizationTypeEnum.SOCIOLABORAL
    fv["Casilla de verificación20"] = req.authorization_type == AuthorizationTypeEnum.SOCIAL
    fv["Casilla de verificación21"] = req.authorization_type == AuthorizationTypeEnum.SOCIOFORMATIVO

    s = form.signature
    fv["Texto75"] = s.place
    fv["Texto76"] = s.day
    fv["Texto77"] = s.month
    fv["Texto78"] = s.year
    fv["Texto79"] = _s(s.signer_name)

    o = form.office
    fv["Texto80"] = _s(o.target_office)
    fv["Texto81"] = _s(o.dir3_code)
    fv["Texto82"] = o.province

    return fv