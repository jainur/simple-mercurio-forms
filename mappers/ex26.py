"""Mapper for EX26 domain model to PDF field values."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any
from mappers.helpers import assign_checkboxes, coerce_str as _s, split_nie as _split_nie

if TYPE_CHECKING:
    from models.ex26 import EX26FormSchema


def to_field_values(form: EX26FormSchema) -> dict[str, Any]:
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
        "Casilla de verificación5": "X",
        "Casilla de verificación6": "H",
        "Casilla de verificación7": "M",
    })
    assign_checkboxes(fv, a.marital_status.value, {
        "Casilla de verificación8": "S",
        "Casilla de verificación9": "C",
        "Casilla de verificación10": "V",
        "Casilla de verificación11": "D",
        "Casilla de verificación12": "Sp",
    })
    fv["Casilla de verificación13"] = a.has_school_age_children_in_spain
    fv["Casilla de verificación14"] = not a.has_school_age_children_in_spain

    e = form.employer_details
    fv["Texto27"] = _s(e.name_or_company) if e else ""
    fv["Texto28"] = _s(e.tax_or_id_number) if e else ""
    fv["Texto29"] = _s(e.activity) if e else ""
    fv["Texto30"] = _s(e.cnae) if e else ""
    fv["Texto31"] = _s(e.registered_address) if e else ""
    fv["Texto32"] = _s(e.address_number) if e else ""
    fv["Texto33"] = _s(e.floor_door) if e else ""
    fv["Texto34"] = _s(e.city) if e else ""
    fv["Texto35"] = _s(e.postal_code) if e else ""
    fv["Texto36"] = _s(e.province) if e else ""
    fv["Texto37"] = _s(e.mobile_phone) if e else ""
    fv["Texto38"] = _s(e.email) if e else ""
    fv["Texto39"] = _s(e.legal_representative_name) if e else ""
    fv["Texto40"] = _s(e.legal_representative_id) if e else ""
    fv["Texto41"] = _s(e.legal_representative_title) if e else ""

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
    fv["Texto52"] = _s(r.legal_representative_name) if r else ""
    fv["Texto53"] = _s(r.legal_representative_id) if r else ""
    fv["Texto54"] = _s(r.legal_representative_title) if r else ""

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
    fv["Casilla de verificación15"] = n.consent_electronic_notifications

    req = form.request_details
    fv["Casilla de verificación16"] = req.from_work_enabled_residence_less_than_one_year_to_employment
    fv["Casilla de verificación17"] = req.from_work_enabled_residence_one_year_to_employment_and_self_employment
    fv["Casilla de verificación18"] = req.from_seasonal_residence_to_employment
    fv["Casilla de verificación19"] = req.from_seasonal_residence_to_self_employment
    fv["Casilla de verificación20"] = req.from_non_work_residence_less_than_one_year_to_employment
    fv["Casilla de verificación21"] = req.from_non_work_residence_one_year_to_employment
    fv["Casilla de verificación22"] = req.from_non_work_residence_one_year_to_self_employment
    fv["Casilla de verificación23"] = req.modify_employment_scope_occupation_or_territory
    fv["Casilla de verificación24"] = req.modify_self_employment_scope_sector_or_territory
    fv["Casilla de verificación25"] = req.from_employment_to_employment_and_self_employment
    fv["Casilla de verificación26"] = req.from_family_member_residence_to_non_lucrative_residence
    fv["Casilla de verificación27"] = req.from_family_member_residence_to_employment
    fv["Casilla de verificación28"] = req.from_family_member_residence_to_self_employment
    fv["Casilla de verificación29"] = req.from_family_member_residence_to_work_exception_residence
    fv["Casilla de verificación30"] = req.from_study_stay_to_employment_article_190_2
    fv["Casilla de verificación31"] = req.from_study_stay_to_self_employment_article_190_3
    fv["Casilla de verificación32"] = req.from_study_stay_to_work_exception_residence_article_190_4
    fv["Casilla de verificación33"] = req.from_study_stay_to_family_reunification_residence
    fv["Casilla de verificación34"] = req.from_study_stay_to_job_search_or_business_project

    s = form.signature
    fv["Texto65"] = s.place
    fv["Texto66"] = s.day
    fv["Texto67"] = s.month
    fv["Texto68"] = s.year
    fv["Texto69"] = _s(s.signer_name)

    o = form.office
    fv["Texto70"] = _s(o.target_office)
    fv["Texto71"] = _s(o.dir3_code)
    fv["Texto72"] = o.province

    return fv