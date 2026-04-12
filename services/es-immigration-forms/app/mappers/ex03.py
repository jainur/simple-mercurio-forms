"""Mapper for EX03 domain model to PDF field values."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any
from app.mappers.helpers import apply_enum_registry as _apply_enum_registry, coerce_str as _s, map_identity_person_block as _map_identity_person_block, map_notification_block as _map_notification_block, map_optional_object_fields as _map_optional_object_fields

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
    _map_identity_person_block(
        fv,
        f,
        passport_field="Texto1",
        nie_fields=("Texto2", "Texto3", "Texto4"),
        date_fields=("Texto8", "Texto9", "Texto10"),
        text_fields={
            "first_surname": "Texto5",
            "second_surname": "Texto6",
            "name": "Texto7",
            "birth_place": "Texto11",
            "birth_country": "Texto12",
            "nationality": "Texto13",
            "father_name": "Texto14",
            "mother_name": "Texto15",
            "address": "Texto16",
            "address_number": "Texto17",
            "floor_door": "Texto18",
            "city": "Texto19",
            "postal_code": "Texto20",
            "province": "Texto21",
            "mobile_phone": "Texto22",
            "email": "Texto23",
            "legal_guardian_name": "Texto24",
            "legal_guardian_id": "Texto25",
            "legal_guardian_title": "Texto26",
        },
        gender_checkbox_map={
            "Casilla de verificación27": "X",
            "Casilla de verificación28": "H",
            "Casilla de verificación29": "M",
        },
        marital_checkbox_map={
            "Casilla de verificación30": "S",
            "Casilla de verificación31": "C",
            "Casilla de verificación32": "V",
            "Casilla de verificación33": "D",
            "Casilla de verificación34": "Sp",
        },
    )
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
    _map_optional_object_fields(
        fv,
        r,
        text_fields={
            "name_or_company": "Texto67",
            "id_number": "Texto68",
            "address": "Texto69",
            "address_number": "Texto70",
            "floor_door": "Texto71",
            "city": "Texto72",
            "postal_code": "Texto73",
            "province": "Texto74",
            "phone": "Texto75",
            "email": "Texto76",
            "legal_rep_name": "Texto77",
            "legal_rep_id": "Texto78",
            "legal_rep_title": "Texto79",
        },
    )

    # Section 5: Notification address
    n = form.notification_address
    _map_notification_block(
        fv,
        n,
        text_fields={
            "name_or_company": "Texto80",
            "id_number": "Texto81",
            "address": "Texto82",
            "address_number": "Texto83",
            "floor_door": "Texto84",
            "city": "Texto85",
            "postal_code": "Texto86",
            "province": "Texto87",
            "mobile_phone": "Texto88",
            "email": "Texto89",
        },
        consent_field="Casilla de verificación90",
    )

    # Section 6: Request + signature + office
    req = form.request_details

    is_initial = req.application_phase == ApplicationPhaseEnum.INITIAL
    is_renewal = req.application_phase == ApplicationPhaseEnum.RENEWAL
    _apply_enum_registry(fv, req.application_phase, {
        "Casilla de verificación91": ApplicationPhaseEnum.INITIAL,
        "Casilla de verificación105": ApplicationPhaseEnum.RENEWAL,
    })
    _apply_enum_registry(fv, req.initial_eligibility, {
        "Casilla de verificación92": InitialEligibilityEnum.INTERNATIONAL_AGREEMENTS_CHILE_PERU_ART_74_2,
        "Casilla de verificación93": InitialEligibilityEnum.EXEMPTION_ART_40_LO_4_2000,
        "Casilla de verificación94": InitialEligibilityEnum.HARD_TO_FILL_OCCUPATION_CATALOG,
        "Casilla de verificación95": InitialEligibilityEnum.PUBLIC_EMPLOYMENT_SERVICE_OFFER,
        "Casilla de verificación96": InitialEligibilityEnum.COUNCIL_OF_MINISTERS_INSTRUCTIONS_DA2_1,
        "Casilla de verificación97": InitialEligibilityEnum.PROFESSIONAL_ATHLETES_2005,
        "Casilla de verificación98": InitialEligibilityEnum.MERCHANT_MARINE_2007,
        "Casilla de verificación99": InitialEligibilityEnum.FISHING_VESSEL_2019,
        "Casilla de verificación100": InitialEligibilityEnum.THIRD_GRADE_OR_PAROLE_2005,
        "Casilla de verificación101": InitialEligibilityEnum.INTERNATIONAL_AGREEMENTS_ANDORRA,
        "Casilla de verificación102": InitialEligibilityEnum.CROSS_BORDER_WORKER_ART_157,
        "Casilla de verificación103": InitialEligibilityEnum.EMPLOYER_CHANGE_BREACH_ART_79_2,
        "Casilla de verificación104": InitialEligibilityEnum.EMPLOYER_CHANGE_OVERRIDING_CIRCUMSTANCES_ART_79_3,
    }, enabled=is_initial)
    fv["Casilla de verificación106"] = is_renewal
    _apply_enum_registry(fv, req.renewal_ground, {
        "Casilla de verificación107": RenewalGroundEnum.GENERAL_ART_81_1,
        "Casilla de verificación108": RenewalGroundEnum.UNEMPLOYMENT_BENEFIT,
        "Casilla de verificación109": RenewalGroundEnum.CROSS_BORDER_WORKER_ART_158,
        "Casilla de verificación110": RenewalGroundEnum.THIRD_GRADE_OR_PAROLE_2005,
    }, enabled=is_renewal)
    _apply_enum_registry(fv, req.filing_party, {
        "Casilla de verificación111": FilingPartyEnum.FOREIGN_WORKER,
        "Casilla de verificación112": FilingPartyEnum.EMPLOYER,
    })

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
