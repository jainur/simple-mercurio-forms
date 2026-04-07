"""Mapper for EX07 domain model to PDF field values."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any
from mappers.helpers import apply_enum_registry as _apply_enum_registry, coerce_str as _s, map_identity_person_block as _map_identity_person_block, map_notification_block as _map_notification_block, map_optional_object_fields as _map_optional_object_fields

if TYPE_CHECKING:
    from models.ex07 import EX07FormSchema


def to_field_values(form: EX07FormSchema) -> dict[str, Any]:
    from models.ex07 import (
        ApplicationCategoryEnum,
        InitialGroundEnum,
        RenewalGroundEnum,
        SignerRoleEnum,
        TerritorialScopeGroundEnum,
    )

    fv: dict[str, Any] = {}

    # Section 1: Foreigner
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
            "Casilla de verificación62": "X",
            "Casilla de verificación63": "H",
            "Casilla de verificación64": "M",
        },
        marital_checkbox_map={
            "Casilla de verificación65": "S",
            "Casilla de verificación66": "C",
            "Casilla de verificación67": "V",
            "Casilla de verificación68": "D",
            "Casilla de verificación69": "Sp",
        },
    )
    fv["Casilla de verificación70"] = f.children_in_school_age
    fv["Casilla de verificación71"] = not f.children_in_school_age

    # Section 2: Self-employment details
    se = form.self_employment_details
    fv["Texto27"] = se.name_or_company
    fv["Texto28"] = se.id_number
    fv["Texto29"] = se.activity
    fv["Texto30"] = _s(se.cnae_code)
    fv["Texto31"] = se.address
    fv["Texto32"] = _s(se.address_number)
    fv["Texto33"] = _s(se.floor_door)
    fv["Texto34"] = se.city
    fv["Texto35"] = se.postal_code
    fv["Texto36"] = se.province
    fv["Texto37"] = _s(se.mobile_phone)
    fv["Texto38"] = _s(se.email)

    # Section 3: Filing representative
    r = form.filing_representative
    _map_optional_object_fields(
        fv,
        r,
        text_fields={
            "name_or_company": "Texto39",
            "id_number": "Texto40",
            "address": "Texto41",
            "address_number": "Texto42",
            "floor_door": "Texto43",
            "city": "Texto44",
            "postal_code": "Texto45",
            "province": "Texto46",
            "mobile_phone": "Texto47",
            "email": "Texto48",
            "legal_rep_name": "Texto49",
            "legal_rep_id": "Texto50",
            "legal_rep_title": "Texto51",
        },
    )

    # Section 4: Notification
    n = form.notification_address
    _map_notification_block(
        fv,
        n,
        text_fields={
            "name_or_company": "Texto52",
            "id_number": "Texto53",
            "address": "Texto54",
            "address_number": "Texto55",
            "floor_door": "Texto56",
            "city": "Texto57",
            "postal_code": "Texto58",
            "province": "Texto59",
            "mobile_phone": "Texto60",
            "email": "Texto61",
        },
        consent_field="Casilla de verificación72",
    )

    # Section 5: Request + signature + office
    req = form.request_details
    is_initial = req.category == ApplicationCategoryEnum.INITIAL
    is_renewal = req.category == ApplicationCategoryEnum.RENEWAL
    is_scope = req.category == ApplicationCategoryEnum.TERRITORIAL_SCOPE_EXTENSION

    fv["Casilla de verificación73"] = is_initial
    fv["Casilla de verificación74"] = is_initial and req.initial_ground == InitialGroundEnum.GENERAL_RESIDENT_OUTSIDE_SPAIN_ART_85
    fv["Casilla de verificación76"] = is_initial and req.initial_ground == InitialGroundEnum.INTERNATIONAL_AGREEMENTS_ANDORRA
    fv["Casilla de verificación77"] = is_initial and req.initial_ground == InitialGroundEnum.CROSS_BORDER_SELF_EMPLOYED_ART_157

    fv["Casilla de verificación78"] = is_renewal
    fv["Casilla de verificación79"] = is_renewal and req.renewal_ground == RenewalGroundEnum.CONTINUITY_ART_86
    fv["Casilla de verificación80"] = is_renewal and req.renewal_ground == RenewalGroundEnum.OTHER_CASES_ART_86
    fv["Casilla de verificación81"] = is_renewal and req.renewal_ground == RenewalGroundEnum.CROSS_BORDER_SELF_EMPLOYED_ART_158

    fv["Casilla de verificación82"] = is_scope
    fv["Casilla de verificación83"] = is_scope and req.territorial_scope_ground == TerritorialScopeGroundEnum.SAME_ACTIVITY_MULTIPLE_AUTONOMOUS_COMMUNITIES_ART_85_6

    fv["Casilla de verificación84"] = req.signer_role == SignerRoleEnum.FOREIGNER
    fv["Casilla de verificación85"] = req.signer_role == SignerRoleEnum.REPRESENTATIVE

    s = form.signature
    fv["Texto86"] = s.place
    fv["Texto87"] = s.day
    fv["Texto88"] = s.month
    fv["Texto89"] = s.year
    fv["Texto90"] = _s(s.name)

    o = form.office
    fv["Texto91"] = _s(o.target_office)
    fv["Texto92"] = _s(o.dir3_code)
    fv["Texto93"] = o.province

    return fv
