"""Mapper for EX18 domain model to PDF field values."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any
from mappers.helpers import assign_checkboxes, coerce_str as _s, split_nie as _split_nie

if TYPE_CHECKING:
    from models.ex18 import EX18FormSchema


def to_field_values(form: EX18FormSchema) -> dict[str, Any]:
    from models.ex18 import (
        MainRequestCategoryEnum,
        ModificationGroundEnum,
        PermanentResidenceGroundEnum,
        TemporaryResidenceGroundEnum,
    )

    fv: dict[str, Any] = {}

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
        "Casilla de verificación1": "X",
        "Casilla de verificación2": "H",
        "Casilla de verificación3": "M",
    })
    assign_checkboxes(fv, f.marital_status.value, {
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
    fv["Texto37"] = _s(r.legal_rep_name) if r else ""
    fv["Texto38"] = _s(r.legal_rep_id) if r else ""
    fv["Texto39"] = _s(r.legal_rep_title) if r else ""

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

    req = form.request_details
    fv["Texto50"] = req.expected_residence_period
    fv["Texto51"] = req.residence_start_day
    fv["Texto52"] = req.residence_start_month
    fv["Texto53"] = req.residence_start_year
    fv["Texto54"] = req.residence_start_location
    fv["Texto55"] = _s(req.eu_citizen_document_id)
    fv["Texto56"] = _s(req.relationship_with_eu_citizen)
    fv["Texto57"] = _s(req.incapacity_with_spanish_spouse_text)
    fv["Texto58"] = _s(req.identity_document_change_text)
    fv["Texto59"] = _s(req.cause_specification)

    is_temp = req.category == MainRequestCategoryEnum.TEMPORARY_RESIDENCE
    is_perm = req.category == MainRequestCategoryEnum.PERMANENT_RESIDENCE
    is_mod = req.category == MainRequestCategoryEnum.MODIFICATION
    is_dereg = req.category == MainRequestCategoryEnum.DEREGISTRATION

    fv["Casilla de verificación10"] = is_temp
    fv["Casilla de verificación11"] = is_temp and req.temporary_ground == TemporaryResidenceGroundEnum.EMPLOYEE
    fv["Casilla de verificación12"] = is_temp and req.temporary_ground == TemporaryResidenceGroundEnum.SELF_EMPLOYED
    fv["Casilla de verificación13"] = is_temp and req.temporary_ground == TemporaryResidenceGroundEnum.INACTIVE_WITH_RESOURCES_AND_INSURANCE
    fv["Casilla de verificación14"] = is_temp and req.temporary_ground == TemporaryResidenceGroundEnum.STUDENT_WITH_RESOURCES_AND_INSURANCE
    fv["Casilla de verificación15"] = is_temp and req.temporary_ground == TemporaryResidenceGroundEnum.EU_FAMILY_MEMBER

    fv["Casilla de verificación16"] = is_perm
    fv["Casilla de verificación17"] = is_perm and req.permanent_ground == PermanentResidenceGroundEnum.CONTINUOUS_5_YEARS
    fv["Casilla de verificación18"] = is_perm and req.permanent_ground == PermanentResidenceGroundEnum.RETIREMENT_WITH_12_MONTHS_AND_3_YEARS
    fv["Casilla de verificación19"] = is_perm and req.permanent_ground == PermanentResidenceGroundEnum.RETIREMENT_WITH_SPANISH_SPOUSE
    fv["Casilla de verificación20"] = is_perm and req.permanent_ground == PermanentResidenceGroundEnum.RETIREMENT_WITH_SPOUSE_LOST_SPANISH_NATIONALITY
    fv["Casilla de verificación21"] = is_perm and req.permanent_ground == PermanentResidenceGroundEnum.EARLY_RETIREMENT_WITH_12_MONTHS_AND_3_YEARS
    fv["Casilla de verificación22"] = is_perm and req.permanent_ground == PermanentResidenceGroundEnum.EARLY_RETIREMENT_WITH_SPANISH_SPOUSE
    fv["Casilla de verificación23"] = is_perm and req.permanent_ground == PermanentResidenceGroundEnum.EARLY_RETIREMENT_WITH_SPOUSE_LOST_SPANISH_NATIONALITY
    fv["Casilla de verificación24"] = is_perm and req.permanent_ground == PermanentResidenceGroundEnum.PERMANENT_DISABILITY_AFTER_2_YEARS
    fv["Casilla de verificación25"] = is_perm and req.permanent_ground == PermanentResidenceGroundEnum.PERMANENT_DISABILITY_WORK_ACCIDENT
    fv["Casilla de verificación26"] = is_perm and req.permanent_ground == PermanentResidenceGroundEnum.PERMANENT_DISABILITY_WITH_SPANISH_SPOUSE
    fv["Casilla de verificación27"] = is_perm and req.permanent_ground == PermanentResidenceGroundEnum.PERMANENT_DISABILITY_WITH_SPOUSE_LOST_SPANISH_NATIONALITY
    fv["Casilla de verificación28"] = is_perm and req.permanent_ground == PermanentResidenceGroundEnum.WORK_IN_OTHER_MEMBER_STATE_KEEPING_RESIDENCE
    fv["Casilla de verificación29"] = is_perm and req.permanent_ground == PermanentResidenceGroundEnum.OTHER

    fv["Casilla de verificación30"] = is_mod
    fv["Casilla de verificación31"] = is_mod and req.modification_ground == ModificationGroundEnum.PERSONAL_DATA
    fv["Casilla de verificación32"] = is_mod and req.modification_ground == ModificationGroundEnum.ADDRESS_CHANGE
    fv["Casilla de verificación33"] = is_mod and req.modification_ground == ModificationGroundEnum.IDENTITY_DOCUMENT_CHANGE
    fv["Casilla de verificación34"] = is_mod and req.modification_ground == ModificationGroundEnum.OTHER

    fv["Casilla de verificación35"] = is_dereg
    fv["Casilla de verificación36"] = bool(req.deregistration_cause)
    fv["Casilla de verificación37"] = req.truth_statement_accepted

    sig = form.signature
    fv["Texto60"] = sig.place
    fv["Texto61"] = sig.day
    fv["Texto62"] = sig.month
    fv["Texto63"] = sig.year
    fv["Texto64"] = _s(sig.eu_citizen_signature_name)
    fv["Texto65"] = _s(sig.applicant_signature_name)

    off = form.office
    fv["Texto66"] = _s(off.target_office)
    fv["Texto67"] = _s(off.dir3_code)
    fv["Texto68"] = off.province

    return fv
