"""Mapper for EX20 domain model to PDF field values."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any
from mappers.helpers import assign_checkboxes, coerce_str as _s, split_nie as _split_nie

if TYPE_CHECKING:
    from models.ex20 import EX20FormSchema


def to_field_values(form: EX20FormSchema) -> dict[str, Any]:
    from models.ex20 import (
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
        "Casilla de verificación27": "X",
        "Casilla de verificación28": "H",
        "Casilla de verificación29": "M",
    })
    assign_checkboxes(fv, f.marital_status.value, {
        "Casilla de verificación30": "S",
        "Casilla de verificación31": "C",
        "Casilla de verificación32": "V",
        "Casilla de verificación33": "D",
        "Casilla de verificación34": "Sp",
    })

    r = form.filing_representative
    fv["Texto35"] = _s(r.name_or_company) if r else ""
    fv["Texto36"] = _s(r.id_number) if r else ""
    fv["Texto37"] = _s(r.address) if r else ""
    fv["Texto38"] = _s(r.address_number) if r else ""
    fv["Texto39"] = _s(r.floor_door) if r else ""
    fv["Texto40"] = _s(r.city) if r else ""
    fv["Texto41"] = _s(r.postal_code) if r else ""
    fv["Texto42"] = _s(r.province) if r else ""
    fv["Texto43"] = _s(r.mobile_phone) if r else ""
    fv["Texto44"] = _s(r.email) if r else ""
    fv["Texto45"] = _s(r.legal_rep_name) if r else ""
    fv["Texto46"] = _s(r.legal_rep_id) if r else ""
    fv["Texto47"] = _s(r.legal_rep_title) if r else ""

    n = form.notification_address
    fv["Texto48"] = n.name_or_company
    fv["Texto49"] = n.id_number
    fv["Texto50"] = n.address
    fv["Texto51"] = _s(n.address_number)
    fv["Texto52"] = _s(n.floor_door)
    fv["Texto53"] = n.city
    fv["Texto54"] = n.postal_code
    fv["Texto55"] = n.province
    fv["Texto56"] = _s(n.mobile_phone)
    fv["Texto57"] = _s(n.email)
    fv["Casilla de verificación76"] = n.consent_electronic_notifications

    req = form.request_details
    fv["Texto58"] = req.residence_start_segment_1
    fv["Texto59"] = req.residence_start_segment_2
    fv["Texto60"] = req.residence_start_segment_3
    fv["Texto61"] = req.residence_start_segment_4
    fv["Texto62"] = _s(req.uk_national_document_id)
    fv["Texto63"] = _s(req.relationship_with_uk_national)
    fv["Texto64"] = _s(req.incapacity_with_spanish_spouse_text)
    fv["Texto65"] = _s(req.identity_document_change_text)
    fv["Texto66"] = _s(req.cause_specification)

    is_temp = req.category == MainRequestCategoryEnum.TEMPORARY_RESIDENCE
    is_perm = req.category == MainRequestCategoryEnum.PERMANENT_RESIDENCE
    is_mod = req.category == MainRequestCategoryEnum.MODIFICATION
    is_dereg = req.category == MainRequestCategoryEnum.DEREGISTRATION

    fv["Casilla de verificación77"] = is_temp
    fv["Casilla de verificación78"] = is_temp and req.temporary_ground == TemporaryResidenceGroundEnum.EMPLOYEE
    fv["Casilla de verificación79"] = is_temp and req.temporary_ground == TemporaryResidenceGroundEnum.SELF_EMPLOYED
    fv["Casilla de verificación80"] = is_temp and req.temporary_ground == TemporaryResidenceGroundEnum.INACTIVE_WITH_RESOURCES_AND_INSURANCE
    fv["Casilla de verificación81"] = is_temp and req.temporary_ground == TemporaryResidenceGroundEnum.STUDENT_WITH_RESOURCES_AND_INSURANCE
    fv["Casilla de verificación82"] = is_temp and req.temporary_ground == TemporaryResidenceGroundEnum.UK_FAMILY_MEMBER

    fv["Casilla de verificación83"] = is_perm
    fv["Casilla de verificación84"] = is_perm and req.permanent_ground == PermanentResidenceGroundEnum.CONTINUOUS_5_YEARS
    fv["Casilla de verificación85"] = is_perm and req.permanent_ground == PermanentResidenceGroundEnum.RETIREMENT_WITH_12_MONTHS_AND_3_YEARS
    fv["Casilla de verificación86"] = is_perm and req.permanent_ground == PermanentResidenceGroundEnum.RETIREMENT_WITH_SPANISH_SPOUSE
    fv["Casilla de verificación87"] = is_perm and req.permanent_ground == PermanentResidenceGroundEnum.RETIREMENT_WITH_SPOUSE_LOST_SPANISH_NATIONALITY
    fv["Casilla de verificación88"] = is_perm and req.permanent_ground == PermanentResidenceGroundEnum.EARLY_RETIREMENT_WITH_12_MONTHS_AND_3_YEARS
    fv["Casilla de verificación89"] = is_perm and req.permanent_ground == PermanentResidenceGroundEnum.EARLY_RETIREMENT_WITH_SPANISH_SPOUSE
    fv["Casilla de verificación90"] = is_perm and req.permanent_ground == PermanentResidenceGroundEnum.EARLY_RETIREMENT_WITH_SPOUSE_LOST_SPANISH_NATIONALITY
    fv["Casilla de verificación91"] = is_perm and req.permanent_ground == PermanentResidenceGroundEnum.PERMANENT_DISABILITY_AFTER_2_YEARS
    fv["Casilla de verificación92"] = is_perm and req.permanent_ground == PermanentResidenceGroundEnum.PERMANENT_DISABILITY_WORK_ACCIDENT
    fv["Casilla de verificación93"] = is_perm and req.permanent_ground == PermanentResidenceGroundEnum.PERMANENT_DISABILITY_WITH_SPANISH_SPOUSE
    fv["Casilla de verificación94"] = is_perm and req.permanent_ground == PermanentResidenceGroundEnum.PERMANENT_DISABILITY_WITH_SPOUSE_LOST_SPANISH_NATIONALITY
    fv["Casilla de verificación95"] = is_perm and req.permanent_ground == PermanentResidenceGroundEnum.WORK_IN_OTHER_MEMBER_STATE_KEEPING_RESIDENCE
    fv["Casilla de verificación96"] = is_perm and req.permanent_ground == PermanentResidenceGroundEnum.OTHER

    fv["Casilla de verificación97"] = is_mod
    fv["Casilla de verificación98"] = is_mod and req.modification_ground == ModificationGroundEnum.PERSONAL_DATA
    fv["Casilla de verificación99"] = is_mod and req.modification_ground == ModificationGroundEnum.ADDRESS_CHANGE
    fv["Casilla de verificación100"] = is_mod and req.modification_ground == ModificationGroundEnum.IDENTITY_DOCUMENT_CHANGE
    fv["Casilla de verificación101"] = is_mod and req.modification_ground == ModificationGroundEnum.OTHER

    fv["Casilla de verificación102"] = is_dereg
    fv["Casilla de verificación103"] = bool(req.deregistration_cause)
    fv["Casilla de verificación104"] = req.truth_statement_accepted

    sig = form.signature
    fv["Texto67"] = sig.place
    fv["Texto68"] = sig.day
    fv["Texto69"] = sig.month
    fv["Texto70"] = sig.year
    fv["Texto71"] = _s(sig.uk_national_signature_name)
    fv["Texto72"] = _s(sig.applicant_signature_name)

    off = form.office
    fv["Texto73"] = _s(off.target_office)
    fv["Texto74"] = _s(off.dir3_code)
    fv["Texto75"] = off.province

    return fv
