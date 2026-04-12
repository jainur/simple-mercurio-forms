"""Mapper for EX26 domain model to PDF field values."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any
from app.mappers.helpers import map_identity_person_block as _map_identity_person_block, map_notification_block as _map_notification_block, map_optional_object_fields as _map_optional_object_fields, coerce_str as _s

if TYPE_CHECKING:
    from models.ex26 import EX26FormSchema


def to_field_values(form: EX26FormSchema) -> dict[str, Any]:
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
            "legal_representative_name": "Texto24",
            "legal_representative_id": "Texto25",
            "legal_representative_title": "Texto26",
        },
        gender_checkbox_map={
            "Casilla de verificación5": "X",
            "Casilla de verificación6": "H",
            "Casilla de verificación7": "M",
        },
        marital_checkbox_map={
            "Casilla de verificación8": "S",
            "Casilla de verificación9": "C",
            "Casilla de verificación10": "V",
            "Casilla de verificación11": "D",
            "Casilla de verificación12": "Sp",
        },
    )
    fv["Casilla de verificación13"] = a.has_school_age_children_in_spain
    fv["Casilla de verificación14"] = not a.has_school_age_children_in_spain

    e = form.employer_details
    _map_optional_object_fields(
        fv,
        e,
        text_fields={
            "name_or_company": "Texto27",
            "tax_or_id_number": "Texto28",
            "activity": "Texto29",
            "cnae": "Texto30",
            "registered_address": "Texto31",
            "address_number": "Texto32",
            "floor_door": "Texto33",
            "city": "Texto34",
            "postal_code": "Texto35",
            "province": "Texto36",
            "mobile_phone": "Texto37",
            "email": "Texto38",
            "legal_representative_name": "Texto39",
            "legal_representative_id": "Texto40",
            "legal_representative_title": "Texto41",
        },
    )

    r = form.filing_representative
    _map_optional_object_fields(
        fv,
        r,
        text_fields={
            "name_or_company": "Texto42",
            "id_number": "Texto43",
            "address": "Texto44",
            "address_number": "Texto45",
            "floor_door": "Texto46",
            "city": "Texto47",
            "postal_code": "Texto48",
            "province": "Texto49",
            "mobile_phone": "Texto50",
            "email": "Texto51",
            "legal_representative_name": "Texto52",
            "legal_representative_id": "Texto53",
            "legal_representative_title": "Texto54",
        },
    )

    n = form.notification_address
    _map_notification_block(
        fv,
        n,
        text_fields={
            "name_or_company": "Texto55",
            "id_number": "Texto56",
            "address": "Texto57",
            "address_number": "Texto58",
            "floor_door": "Texto59",
            "city": "Texto60",
            "postal_code": "Texto61",
            "province": "Texto62",
            "mobile_phone": "Texto63",
            "email": "Texto64",
        },
        consent_field="Casilla de verificación15",
    )

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