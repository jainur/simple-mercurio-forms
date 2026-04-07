"""Mapper for EX03 domain model to PDF field values."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any
from mappers.helpers import assign_checkboxes, coerce_str as _s, split_nie as _split_nie

if TYPE_CHECKING:
    from models.ex03 import EX03FormSchema


def to_field_values(form: EX03FormSchema) -> dict[str, Any]:
    from models.ex03 import (
        ApplicationPhaseEnum,
        FilingPartyEnum,
        InitialEligibilityEnum,
        RenewalGroundEnum,
        SignaturePartyEnum,
    )

    fv: dict[str, Any] = {}

    # Section 1: Foreigner details
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
    fv["Casilla de verificación35"] = f.children_in_school_age
    fv["Casilla de verificación36"] = not f.children_in_school_age

    # Section 2: Employer
    e = form.employer_details
    fv["Texto37"] = e.name_or_company
    fv["Texto38"] = e.id_number
    fv["Texto39"] = e.activity
    fv["Texto40"] = _s(e.cnae_code)
    fv["Texto41"] = e.address
    fv["Texto42"] = _s(e.address_number)
    fv["Texto43"] = _s(e.floor_door)
    fv["Texto44"] = e.city
    fv["Texto45"] = e.postal_code
    fv["Texto46"] = e.province
    fv["Texto47"] = _s(e.mobile_phone)
    fv["Texto48"] = _s(e.email)
    fv["Texto49"] = _s(e.legal_rep_name)
    fv["Texto50"] = _s(e.legal_rep_id)
    fv["Texto51"] = _s(e.legal_rep_title)

    # Section 3: Job offer
    j = form.job_offer_details
    fv["Texto52"] = j.position_name
    fv["Texto53"] = _s(j.contribution_group)
    fv["Texto54"] = _s(j.cno_sepe_2011)
    fv["Texto55"] = _s(j.convenio_code)
    fv["Texto56"] = _s(j.convenio_name)
    fv["Texto57"] = _s(j.contract_code)
    fv["Texto58"] = _s(j.contract_name)
    fv["Texto59"] = _s(j.social_security_account_code)
    fv["Texto60"] = _s(j.gross_salary_eur)
    fv["Texto61"] = j.work_center_address
    fv["Texto62"] = _s(j.work_center_number)
    fv["Texto63"] = _s(j.work_center_floor_door)
    fv["Texto64"] = j.work_center_city
    fv["Texto65"] = j.work_center_postal_code
    fv["Texto66"] = j.work_center_province

    # Section 4: Filing representative
    r = form.filing_representative
    fv["Texto67"] = _s(r.name_or_company) if r else ""
    fv["Texto68"] = _s(r.id_number) if r else ""
    fv["Texto69"] = _s(r.address) if r else ""
    fv["Texto70"] = _s(r.address_number) if r else ""
    fv["Texto71"] = _s(r.floor_door) if r else ""
    fv["Texto72"] = _s(r.city) if r else ""
    fv["Texto73"] = _s(r.postal_code) if r else ""
    fv["Texto74"] = _s(r.province) if r else ""
    fv["Texto75"] = _s(r.phone) if r else ""
    fv["Texto76"] = _s(r.email) if r else ""
    fv["Texto77"] = _s(r.legal_rep_name) if r else ""
    fv["Texto78"] = _s(r.legal_rep_id) if r else ""
    fv["Texto79"] = _s(r.legal_rep_title) if r else ""

    # Section 5: Notification address
    n = form.notification_address
    fv["Texto80"] = n.name_or_company
    fv["Texto81"] = n.id_number
    fv["Texto82"] = n.address
    fv["Texto83"] = _s(n.address_number)
    fv["Texto84"] = _s(n.floor_door)
    fv["Texto85"] = n.city
    fv["Texto86"] = n.postal_code
    fv["Texto87"] = n.province
    fv["Texto88"] = _s(n.mobile_phone)
    fv["Texto89"] = _s(n.email)
    fv["Casilla de verificación90"] = n.consent_electronic_notifications

    # Section 6: Request + signature + office
    req = form.request_details

    is_initial = req.application_phase == ApplicationPhaseEnum.INITIAL
    is_renewal = req.application_phase == ApplicationPhaseEnum.RENEWAL
    fv["Casilla de verificación91"] = is_initial
    fv["Casilla de verificación105"] = is_renewal

    fv["Casilla de verificación92"] = req.initial_eligibility == InitialEligibilityEnum.INTERNATIONAL_AGREEMENTS_CHILE_PERU_ART_74_2
    fv["Casilla de verificación93"] = req.initial_eligibility == InitialEligibilityEnum.EXEMPTION_ART_40_LO_4_2000
    fv["Casilla de verificación94"] = req.initial_eligibility == InitialEligibilityEnum.HARD_TO_FILL_OCCUPATION_CATALOG
    fv["Casilla de verificación95"] = req.initial_eligibility == InitialEligibilityEnum.PUBLIC_EMPLOYMENT_SERVICE_OFFER
    fv["Casilla de verificación96"] = req.initial_eligibility == InitialEligibilityEnum.COUNCIL_OF_MINISTERS_INSTRUCTIONS_DA2_1
    fv["Casilla de verificación97"] = req.initial_eligibility == InitialEligibilityEnum.PROFESSIONAL_ATHLETES_2005
    fv["Casilla de verificación98"] = req.initial_eligibility == InitialEligibilityEnum.MERCHANT_MARINE_2007
    fv["Casilla de verificación99"] = req.initial_eligibility == InitialEligibilityEnum.FISHING_VESSEL_2019
    fv["Casilla de verificación100"] = req.initial_eligibility == InitialEligibilityEnum.THIRD_GRADE_OR_PAROLE_2005
    fv["Casilla de verificación101"] = req.initial_eligibility == InitialEligibilityEnum.INTERNATIONAL_AGREEMENTS_ANDORRA
    fv["Casilla de verificación102"] = req.initial_eligibility == InitialEligibilityEnum.CROSS_BORDER_WORKER_ART_157
    fv["Casilla de verificación103"] = req.initial_eligibility == InitialEligibilityEnum.EMPLOYER_CHANGE_BREACH_ART_79_2
    fv["Casilla de verificación104"] = req.initial_eligibility == InitialEligibilityEnum.EMPLOYER_CHANGE_OVERRIDING_CIRCUMSTANCES_ART_79_3

    fv["Casilla de verificación106"] = is_renewal
    fv["Casilla de verificación107"] = req.renewal_ground == RenewalGroundEnum.GENERAL_ART_81_1
    fv["Casilla de verificación108"] = req.renewal_ground == RenewalGroundEnum.UNEMPLOYMENT_BENEFIT
    fv["Casilla de verificación109"] = req.renewal_ground == RenewalGroundEnum.CROSS_BORDER_WORKER_ART_158
    fv["Casilla de verificación110"] = req.renewal_ground == RenewalGroundEnum.THIRD_GRADE_OR_PAROLE_2005

    fv["Casilla de verificación111"] = req.filing_party == FilingPartyEnum.FOREIGN_WORKER
    fv["Casilla de verificación112"] = req.filing_party == FilingPartyEnum.EMPLOYER

    sig = form.signature
    fv["Texto113"] = sig.place
    fv["Texto114"] = sig.day
    fv["Texto115"] = sig.month
    fv["Texto116"] = sig.year
    fv["Texto117"] = _s(sig.name)

    off = form.office
    fv["Texto118"] = _s(off.target_office)
    fv["Texto119"] = _s(off.dir3_code)
    fv["Texto120"] = off.province

    fv["Casilla de verificación121"] = req.signature_party == SignaturePartyEnum.LEGAL_REPRESENTATIVE_OR_FOREIGNER
    fv["Casilla de verificación122"] = req.signature_party == SignaturePartyEnum.FOREIGN_WORKER
    fv["Casilla de verificación123"] = req.signature_party == SignaturePartyEnum.EMPLOYER

    return fv
