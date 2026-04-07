"""Mapper for EX19 domain model to PDF field values."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any
from mappers.helpers import apply_enum_registry as _apply_enum_registry, coerce_str as _s, map_identity_person_block as _map_identity_person_block, map_notification_block as _map_notification_block, map_optional_object_fields as _map_optional_object_fields, split_nie as _split_nie

if TYPE_CHECKING:
    from models.ex19 import EX19FormSchema


def to_field_values(form: EX19FormSchema) -> dict[str, Any]:
    from models.ex19 import (
        FamilyRelationshipEnum,
        MaintainRightGroundEnum,
        ResidenceRequestTypeEnum,
    )

    fv: dict[str, Any] = {}

    a = form.applicant_details
    _map_identity_person_block(
        fv,
        a,
        passport_field="Texto2",
        nie_fields=("Texto3", "Texto4", "Texto5"),
        date_fields=("Texto9", "Texto10", "Texto11"),
        text_fields={
            "first_surname": "Texto6",
            "second_surname": "Texto7",
            "name": "Texto8",
            "birth_place": "Texto12",
            "birth_country": "Texto13",
            "nationality": "Texto14",
            "father_name": "Texto15",
            "mother_name": "Texto16",
            "address": "Texto17",
            "address_number": "Texto18",
            "floor_door": "Texto19",
            "city": "Texto20",
            "postal_code": "Texto21",
            "province": "Texto22",
            "mobile_phone": "Texto23",
            "email": "Texto24",
            "legal_guardian_name": "Texto25",
            "legal_guardian_id": "Texto26",
            "legal_guardian_title": "Texto27",
        },
        gender_checkbox_map={
            "Casilla de verificación3": "X",
            "Casilla de verificación4": "H",
            "Casilla de verificación5": "M",
        },
        marital_checkbox_map={
            "Casilla de verificación6": "S",
            "Casilla de verificación7": "C",
            "Casilla de verificación8": "V",
            "Casilla de verificación9": "D",
            "Casilla de verificación10": "Sp",
        },
    )

    eu = form.eu_citizen_details
    fv["Texto28"] = _s(eu.passport)
    if eu.nie:
        n1, n2, n3 = _split_nie(eu.nie)
        fv["Texto29"], fv["Texto30"], fv["Texto31"] = n1, n2, n3
    else:
        fv["Texto29"] = fv["Texto30"] = fv["Texto31"] = ""
    fv["Texto32"] = eu.first_surname
    fv["Texto33"] = _s(eu.second_surname)
    fv["Texto34"] = eu.name
    fv["Texto35"] = eu.nationality
    fv["Texto36"] = eu.address
    fv["Texto37"] = _s(eu.address_number)
    fv["Texto38"] = _s(eu.floor_door)
    fv["Texto39"] = eu.city
    fv["Texto40"] = eu.postal_code
    fv["Texto41"] = eu.province

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
        consent_field="Casilla de verificación12",
    )

    req = form.request_details
    is_temp = req.request_type == ResidenceRequestTypeEnum.TEMPORARY_INITIAL
    is_perm = req.request_type == ResidenceRequestTypeEnum.PERMANENT
    is_renew = req.request_type == ResidenceRequestTypeEnum.CARD_RENEWAL
    is_keep = req.request_type == ResidenceRequestTypeEnum.MAINTAIN_PERSONAL_RIGHT

    _apply_enum_registry(fv, req.request_type, {
        "Casilla de verificación13": ResidenceRequestTypeEnum.TEMPORARY_INITIAL,
        "Casilla de verificación22": ResidenceRequestTypeEnum.PERMANENT,
        "Casilla de verificación23": ResidenceRequestTypeEnum.CARD_RENEWAL,
        "Casilla de verificación24": ResidenceRequestTypeEnum.MAINTAIN_PERSONAL_RIGHT,
    })
    _apply_enum_registry(fv, req.family_relationship, {
        "Casilla de verificación14": FamilyRelationshipEnum.SPOUSE,
        "Casilla de verificación15": FamilyRelationshipEnum.REGISTERED_PARTNER,
        "Casilla de verificación16": FamilyRelationshipEnum.STABLE_PARTNER,
        "Casilla de verificación17": FamilyRelationshipEnum.DESCENDANT_UNDER_21,
        "Casilla de verificación18": FamilyRelationshipEnum.DESCENDANT_OVER_21_DEPENDENT,
        "Casilla de verificación19": FamilyRelationshipEnum.ASCENDANT_DEPENDENT,
        "Casilla de verificación20": FamilyRelationshipEnum.PARENT_OF_MINOR_EU_CITIZEN,
        "Casilla de verificación21": FamilyRelationshipEnum.OTHER_FAMILY_MEMBER,
    }, enabled=is_temp)
    _apply_enum_registry(fv, req.maintain_right_ground, {
        "Casilla de verificación25": {
            MaintainRightGroundEnum.DEATH_OF_EU_CITIZEN,
            MaintainRightGroundEnum.MARITAL_NULLITY_DIVORCE_OR_CANCELLED_PARTNERSHIP,
        },
        "Casilla de verificación26": MaintainRightGroundEnum.VICTIM_OF_GENDER_OR_SEXUAL_VIOLENCE_OR_TRAFFICKING,
        "Casilla de verificación27": MaintainRightGroundEnum.OTHER_CHILD_CUSTODY_OR_VISITATION,
    }, enabled=is_keep)
    fv["Casilla de verificación28"] = req.truth_statement_accepted

    sig = form.signature
    fv["Texto65"] = sig.place
    fv["Texto66"] = sig.day
    fv["Texto67"] = sig.month
    fv["Texto68"] = sig.year
    fv["Texto69"] = _s(sig.eu_citizen_signature_name)
    fv["Texto70"] = _s(sig.applicant_signature_name)

    off = form.office
    fv["Texto71"] = _s(off.target_office)
    fv["Texto72"] = _s(off.dir3_code)
    fv["Texto73"] = off.province

    return fv
