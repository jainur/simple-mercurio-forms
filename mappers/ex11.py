"""Mapper for EX11 domain model to PDF field values."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any
from mappers.helpers import apply_enum_registry as _apply_enum_registry, coerce_str as _s, map_identity_person_block as _map_identity_person_block, map_notification_block as _map_notification_block, map_optional_object_fields as _map_optional_object_fields

if TYPE_CHECKING:
    from models.ex11 import EX11FormSchema


def to_field_values(form: EX11FormSchema) -> dict[str, Any]:
    from models.ex11 import (
        AuthorizationFamilyEnum,
        LdSubtypeEnum,
        LdUeSubtypeEnum,
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

    # Section 2: Filing representative (fields start at Texto54)
    r = form.filing_representative
    _map_optional_object_fields(
        fv,
        r,
        text_fields={
            "name_or_company": "Texto54",
            "id_number": "Texto55",
            "address": "Texto56",
            "address_number": "Texto57",
            "floor_door": "Texto58",
            "city": "Texto59",
            "postal_code": "Texto60",
            "province": "Texto61",
            "mobile_phone": "Texto62",
            "email": "Texto63",
            "legal_rep_name": "Texto64",
            "legal_rep_id": "Texto65",
            "legal_rep_title": "Texto66",
        },
    )

    # Section 3: Notification
    n = form.notification_address
    _map_notification_block(
        fv,
        n,
        text_fields={
            "name_or_company": "Texto67",
            "id_number": "Texto68",
            "address": "Texto69",
            "address_number": "Texto70",
            "floor_door": "Texto71",
            "city": "Texto72",
            "postal_code": "Texto73",
            "province": "Texto74",
            "mobile_phone": "Texto75",
            "email": "Texto76",
        },
        consent_field="Casilla de verificación37",
    )

    # Section 4: Request + signature + office
    req = form.request_details
    is_ld = req.authorization_family == AuthorizationFamilyEnum.RESIDENCIA_LARGA_DURACION
    is_ld_ue = req.authorization_family == AuthorizationFamilyEnum.RESIDENCIA_LARGA_DURACION_UE

    _apply_enum_registry(fv, req.authorization_family, {
        "Casilla de verificación38": AuthorizationFamilyEnum.RESIDENCIA_LARGA_DURACION,
        "Casilla de verificación48": AuthorizationFamilyEnum.RESIDENCIA_LARGA_DURACION_UE,
    })
    _apply_enum_registry(fv, req.ld_subtype, {
        "Casilla de verificación39": LdSubtypeEnum.GENERAL_5_YEARS_ART_183_1,
        "Casilla de verificación40": LdSubtypeEnum.PENSION_OR_PERMANENT_DISABILITY_ART_183_3,
        "Casilla de verificación41": LdSubtypeEnum.BORN_IN_SPAIN_AND_3_YEARS_RESIDENCE_ART_183_3_C,
        "Casilla de verificación42": LdSubtypeEnum.FORMER_SPANISH_NATIONAL_ART_183_3_D,
        "Casilla de verificación43": LdSubtypeEnum.FORMER_PUBLIC_GUARDIANSHIP_ART_183_3_E,
        "Casilla de verificación44": LdSubtypeEnum.STATELESS_OR_REFUGEE_ART_183_3_F,
        "Casilla de verificación45": LdSubtypeEnum.FAMILY_REUNIFICATION_WITH_LTR_SPONSOR,
        "Casilla de verificación46": LdSubtypeEnum.EU_LTR_HOLDER_IN_OTHER_MEMBER_STATE_ART_179,
        "Casilla de verificación47": LdSubtypeEnum.RECOVERY_AFTER_LOSS_ART_188,
    }, enabled=is_ld)
    _apply_enum_registry(fv, req.ld_ue_subtype, {
        "Casilla de verificación49": LdUeSubtypeEnum.GENERAL_5_YEARS_WITH_RESOURCES_AND_INSURANCE_ART_176_1_A,
        "Casilla de verificación50": LdUeSubtypeEnum.STUDIES_EXCHANGE_PRACTICES_COMPUTED_50_ART_176_A,
        "Casilla de verificación51": LdUeSubtypeEnum.TWO_YEARS_SPAIN_PLUS_THREE_YEARS_BLUE_CARD_EU_ART_176_A,
        "Casilla de verificación52": LdUeSubtypeEnum.OTHER_MEMBER_STATE_EU_LTR_RENUNCIATION_ART_181,
        "Casilla de verificación53": LdUeSubtypeEnum.RECOVERY_AFTER_LOSS_ART_186,
    }, enabled=is_ld_ue)

    sig = form.signature
    fv["Texto77"] = sig.place
    fv["Texto78"] = sig.day
    fv["Texto79"] = sig.month
    fv["Texto80"] = sig.year
    fv["Texto81"] = _s(sig.name)

    off = form.office
    fv["Texto82"] = _s(off.target_office)
    fv["Texto83"] = _s(off.dir3_code)
    fv["Texto84"] = off.province

    return fv
