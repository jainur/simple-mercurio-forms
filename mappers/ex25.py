"""Mapper for EX25 domain model to PDF field values."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any
from mappers.helpers import map_identity_person_block as _map_identity_person_block, map_notification_block as _map_notification_block, map_optional_object_fields as _map_optional_object_fields, coerce_str as _s

if TYPE_CHECKING:
    from models.ex25 import EX25FormSchema


def to_field_values(form: EX25FormSchema) -> dict[str, Any]:
    fv: dict[str, Any] = {}

    m = form.minor_details
    _map_identity_person_block(
        fv,
        m,
        passport_field="Texto157",
        nie_fields=("Texto158", "Texto159", "Texto160"),
        date_fields=("Texto164", "Texto165", "Texto166"),
        text_fields={
            "first_surname": "Texto161",
            "second_surname": "Texto162",
            "name": "Texto163",
            "birth_place": "Texto167",
            "birth_country": "Texto168",
            "nationality": "Texto169",
            "father_name": "Texto170",
            "mother_name": "Texto171",
            "address": "Texto172",
            "address_number": "Texto173",
            "floor_door": "Texto174",
            "city": "Texto175",
            "mobile_phone": "Texto176",
            "postal_code": "Texto177",
            "province": "Texto178",
            "email": "Texto179",
            "legal_guardian_name": "Texto180",
            "legal_guardian_id": "Texto181",
            "legal_guardian_title": "Texto182",
            "representative_nature": "Texto183",
            "relationship_with_minor": "Texto184",
        },
        gender_checkbox_map={
            "Casilla de verificación235": "X",
            "Casilla de verificación236": "H",
            "Casilla de verificación237": "M",
        },
        marital_checkbox_map={},
    )

    g = form.guardian_or_entity_details
    _map_optional_object_fields(
        fv,
        g,
        text_fields={
            "name_or_company": "Texto185",
            "id_number": "Texto186",
            "address": "Texto187",
            "address_number": "Texto188",
            "floor_door": "Texto189",
            "city": "Texto190",
            "postal_code": "Texto191",
            "province": "Texto192",
            "mobile_phone": "Texto193",
            "email": "Texto194",
            "legal_rep_name": "Texto195",
            "legal_rep_id": "Texto196",
            "legal_rep_title": "Texto197",
        },
    )

    r = form.filing_representative
    _map_optional_object_fields(
        fv,
        r,
        text_fields={
            "name_or_company": "Texto198",
            "id_number": "Texto199",
            "address": "Texto200",
            "address_number": "Texto201",
            "floor_door": "Texto202",
            "city": "Texto203",
            "postal_code": "Texto204",
            "province": "Texto205",
            "mobile_phone": "Texto206",
            "email": "Texto207",
            "legal_rep_name": "Texto208",
            "legal_rep_id": "Texto209",
            "legal_rep_title": "Texto210",
        },
    )

    n = form.notification_address
    _map_notification_block(
        fv,
        n,
        text_fields={
            "name_or_company": "Texto211",
            "id_number": "Texto212",
            "address": "Texto213",
            "address_number": "Texto214",
            "floor_door": "Texto215",
            "city": "Texto216",
            "postal_code": "Texto217",
            "province": "Texto218",
            "mobile_phone": "Texto219",
            "email": "Texto220",
        },
        consent_field="Casilla de verificación260",
    )

    req = form.request_details
    fv["Casilla de verificación238"] = req.temporary_residence_minor_born_in_spain
    fv["Casilla de verificación239"] = req.temporary_residence_accompanied_disabled_minor_not_born_in_spain
    fv["Casilla de verificación240"] = req.temporary_residence_dana_2024_minor_with_guardian
    fv["Casilla de verificación241"] = req.temporary_initial_unaccompanied_minor
    fv["Casilla de verificación242"] = req.temporary_initial_former_ward_without_residence_at_majority
    fv["Casilla de verificación243"] = req.temporary_initial_displaced_minor_medical_treatment_extension_exhausted
    fv["Casilla de verificación244"] = req.temporary_initial_parent_or_guardian_medical_treatment_extension_exhausted
    fv["Casilla de verificación245"] = req.renewal_unaccompanied_minor_with_residence
    fv["Casilla de verificación246"] = req.renewal_former_ward_with_residence_at_majority
    fv["Casilla de verificación247"] = req.renewal_former_ward_without_residence_at_majority
    fv["Casilla de verificación248"] = req.renewal_displaced_minor_medical_treatment_exceptional
    fv["Casilla de verificación249"] = req.renewal_parent_or_guardian_medical_treatment_exceptional
    fv["Casilla de verificación250"] = req.humanitarian_program_minor_medical_treatment_stay
    fv["Casilla de verificación251"] = req.humanitarian_program_parent_or_guardian_medical_treatment_stay
    fv["Casilla de verificación252"] = req.humanitarian_program_minor_holiday_stay
    fv["Casilla de verificación253"] = req.humanitarian_program_monitor_holiday_stay
    fv["Casilla de verificación254"] = req.humanitarian_program_schooling_stay
    fv["Casilla de verificación255"] = req.humanitarian_extension_medical_treatment
    fv["Casilla de verificación256"] = req.humanitarian_extension_parent_or_guardian_medical_treatment
    fv["Casilla de verificación257"] = req.humanitarian_extension_schooling_exceptional_return_impediment
    fv["Casilla de verificación258"] = req.other_international_adoption
    fv["Casilla de verificación259"] = req.other_vacations_in_peace_program

    s = form.signature
    fv["Texto221"] = s.day
    fv["Texto222"] = _s(s.signer_1_id)
    fv["Texto223"] = _s(s.signer_1_title)
    fv["Texto224"] = s.place
    fv["Texto225"] = _s(s.signer_2_id)
    fv["Texto226"] = _s(s.signer_2_title)
    fv["Texto227"] = s.month
    fv["Texto228"] = s.year
    fv["Texto229"] = _s(s.signer_1_name)
    fv["Texto230"] = ""
    fv["Texto231"] = _s(s.signer_2_name)

    o = form.office
    fv["Texto232"] = _s(o.target_office)
    fv["Texto233"] = _s(o.dir3_code)
    fv["Texto234"] = o.province

    return fv
