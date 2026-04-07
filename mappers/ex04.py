"""Mapper for EX04 domain model to PDF field values."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any
from mappers.helpers import apply_enum_registry as _apply_enum_registry, coerce_str as _s, map_identity_person_block as _map_identity_person_block, map_notification_block as _map_notification_block, map_optional_object_fields as _map_optional_object_fields

if TYPE_CHECKING:
    from models.ex04 import EX04FormSchema


def to_field_values(form: EX04FormSchema) -> dict[str, Any]:
    from models.ex04 import (
        ApplicationCategoryEnum,
        FamilyAuthorizationPhaseEnum,
        InitialLocationEnum,
        PracticeBasisEnum,
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
            "Casilla de verificación73": "X",
            "Casilla de verificación74": "H",
            "Casilla de verificación75": "M",
        },
        marital_checkbox_map={
            "Casilla de verificación76": "S",
            "Casilla de verificación77": "C",
            "Casilla de verificación78": "V",
            "Casilla de verificación79": "D",
            "Casilla de verificación80": "Sp",
        },
    )

    # Section 2: Host entity
    h = form.host_entity_details
    fv["Texto27"] = h.name_or_company
    fv["Texto28"] = h.id_number
    fv["Texto29"] = h.activity
    fv["Texto30"] = h.occupation
    fv["Texto31"] = h.address
    fv["Texto32"] = _s(h.address_number)
    fv["Texto33"] = _s(h.floor_door)
    fv["Texto34"] = h.city
    fv["Texto35"] = h.postal_code
    fv["Texto36"] = h.province
    fv["Texto37"] = _s(h.mobile_phone)
    fv["Texto38"] = _s(h.email)
    fv["Texto39"] = _s(h.legal_rep_name)
    fv["Texto40"] = _s(h.legal_rep_id)
    fv["Texto41"] = _s(h.legal_rep_title)

    # Section 3: Filing representative
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
            "legal_rep_name": "Texto52",
            "legal_rep_id": "Texto53",
            "legal_rep_title": "Texto54",
        },
    )

    # Section 4: Notification
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
        consent_field="Casilla de verificación81",
    )

    # Section 5: Request + signature + office
    req = form.request_details

    is_initial = req.category == ApplicationCategoryEnum.INITIAL
    is_renewal = req.category == ApplicationCategoryEnum.RENEWAL
    is_family = req.category == ApplicationCategoryEnum.FAMILY

    fv["Casilla de verificación82"] = is_initial
    fv["Casilla de verificación83"] = is_initial and req.initial_location == InitialLocationEnum.OUTSIDE_SPAIN
    fv["Casilla de verificación84"] = is_initial and req.initial_location == InitialLocationEnum.OUTSIDE_SPAIN and req.initial_basis == PracticeBasisEnum.AGREEMENT
    fv["Casilla de verificación85"] = is_initial and req.initial_location == InitialLocationEnum.OUTSIDE_SPAIN and req.initial_basis == PracticeBasisEnum.EMPLOYMENT_CONTRACT
    fv["Casilla de verificación86"] = is_initial and req.initial_location == InitialLocationEnum.IN_SPAIN
    fv["Casilla de verificación87"] = is_initial and req.initial_location == InitialLocationEnum.IN_SPAIN and req.initial_basis == PracticeBasisEnum.AGREEMENT
    fv["Casilla de verificación88"] = is_initial and req.initial_location == InitialLocationEnum.IN_SPAIN and req.initial_basis == PracticeBasisEnum.EMPLOYMENT_CONTRACT

    fv["Casilla de verificación89"] = is_renewal
    fv["Casilla de verificación90"] = is_renewal
    fv["Casilla de verificación91"] = is_renewal and req.renewal_basis == PracticeBasisEnum.AGREEMENT
    fv["Casilla de verificación92"] = is_renewal and req.renewal_basis == PracticeBasisEnum.EMPLOYMENT_CONTRACT

    fv["Casilla de verificación93"] = is_family
    fv["Casilla de verificación94"] = is_family and req.family_phase == FamilyAuthorizationPhaseEnum.INITIAL
    fv["Casilla de verificación95"] = is_family and req.family_phase == FamilyAuthorizationPhaseEnum.RENEWED
    fv["Casilla de verificación96"] = req.is_host_entity_legal_representative_signing

    sig = form.signature
    fv["Texto65"] = sig.place
    fv["Texto66"] = sig.day
    fv["Texto67"] = sig.month
    fv["Texto68"] = sig.year
    fv["Texto69"] = _s(sig.name)

    off = form.office
    fv["Texto70"] = _s(off.target_office)
    fv["Texto71"] = _s(off.dir3_code)
    fv["Texto72"] = off.province

    return fv
