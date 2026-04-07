"""Mapper for EX28 domain model to PDF field values."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any
from mappers.helpers import map_identity_person_block as _map_identity_person_block, map_notification_block as _map_notification_block, map_optional_object_fields as _map_optional_object_fields, coerce_str as _s

if TYPE_CHECKING:
    from models.ex28 import EX28FormSchema


def to_field_values(form: EX28FormSchema) -> dict[str, Any]:
    fv: dict[str, Any] = {}

    a = form.applicant_details
    _map_identity_person_block(
        fv,
        a,
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
            "current_authorization_type": "Texto24",
            "current_authorization_id": "Texto25",
            "legal_representative_name": "Texto26",
            "legal_representative_id": "Texto27",
            "legal_representative_title": "Texto28",
        },
        gender_checkbox_map={
            "Casilla de verificación29": "X",
            "Casilla de verificación30": "H",
            "Casilla de verificación31": "M",
        },
        marital_checkbox_map={
            "Casilla de verificación32": "S",
            "Casilla de verificación33": "C",
            "Casilla de verificación34": "V",
            "Casilla de verificación35": "D",
            "Casilla de verificación36": "Sp",
        },
    )
    fv["Casilla de verificación37"] = a.has_school_age_children_in_spain
    fv["Casilla de verificación38"] = not a.has_school_age_children_in_spain

    p = form.pending_application
    fv["Texto54"] = p.case_number
    fv["Texto55"] = p.filing_date

    r = form.filing_representative
    _map_optional_object_fields(
        fv,
        r,
        text_fields={
            "name_or_company": "Texto56",
            "id_number": "Texto57",
            "address": "Texto58",
            "address_number": "Texto59",
            "floor_door": "Texto60",
            "city": "Texto61",
            "postal_code": "Texto62",
            "province": "Texto63",
            "mobile_phone": "Texto64",
            "email": "Texto65",
            "legal_representative_name": "Texto66",
            "legal_representative_id": "Texto67",
            "legal_representative_title": "Texto68",
        },
    )

    n = form.notification_address
    _map_notification_block(
        fv,
        n,
        text_fields={
            "name_or_company": "Texto69",
            "id_number": "Texto70",
            "address": "Texto71",
            "address_number": "Texto72",
            "floor_door": "Texto73",
            "city": "Texto74",
            "postal_code": "Texto75",
            "province": "Texto76",
            "mobile_phone": "Texto77",
            "email": "Texto78",
        },
        consent_field="Casilla de verificación39",
    )

    req = form.request_details
    fv["Casilla de verificación40"] = req.long_term_stay_from_study_or_mobility_or_volunteering
    fv["Casilla de verificación41"] = req.exceptional_circumstances_family_roots_to_parent_guardian_of_eu_minor
    fv["Casilla de verificación42"] = req.exceptional_circumstances_training_roots_to_sociotraining_roots
    fv["Casilla de verificación43"] = req.exceptional_circumstances_social_roots_employment_to_sociolabor_roots
    fv["Casilla de verificación44"] = req.exceptional_circumstances_social_roots_self_employment_to_social_roots
    fv["Casilla de verificación45"] = req.exceptional_circumstances_other_to_equivalent_title_vii
    fv["Casilla de verificación46"] = req.temporary_residence_title_iv_to_equivalent_title_iv
    fv["Casilla de verificación47"] = req.temporary_residence_minor_child_or_ward_to_equivalent
    fv["Casilla de verificación48"] = req.long_term_residence_to_long_term_national
    fv["Casilla de verificación49"] = req.long_term_residence_to_long_term_eu
    fv["Casilla de verificación50"] = req.modification_of_situations_to_title_xi_equivalent
    fv["Casilla de verificación51"] = req.simultaneous_family_reunification_requests
    fv["Casilla de verificación52"] = not req.simultaneous_family_reunification_requests
    fv["Casilla de verificación53"] = req.family_members_of_spanish_nationals_transition

    s = form.signature
    fv["Texto79"] = s.place
    fv["Texto80"] = s.day
    fv["Texto81"] = s.month
    fv["Texto82"] = s.year
    fv["Texto83"] = _s(s.signer_name)

    o = form.office
    fv["Texto84"] = _s(o.target_office)
    fv["Texto85"] = _s(o.dir3_code)
    fv["Texto86"] = o.province

    return fv