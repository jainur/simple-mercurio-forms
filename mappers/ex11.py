"""Mapper for EX11 domain model to PDF field values."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any
from mappers.helpers import assign_checkboxes, coerce_str as _s, split_nie as _split_nie

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

    # Section 2: Filing representative (fields start at Texto54)
    r = form.filing_representative
    fv["Texto54"] = _s(r.name_or_company) if r else ""
    fv["Texto55"] = _s(r.id_number) if r else ""
    fv["Texto56"] = _s(r.address) if r else ""
    fv["Texto57"] = _s(r.address_number) if r else ""
    fv["Texto58"] = _s(r.floor_door) if r else ""
    fv["Texto59"] = _s(r.city) if r else ""
    fv["Texto60"] = _s(r.postal_code) if r else ""
    fv["Texto61"] = _s(r.province) if r else ""
    fv["Texto62"] = _s(r.mobile_phone) if r else ""
    fv["Texto63"] = _s(r.email) if r else ""
    fv["Texto64"] = _s(r.legal_rep_name) if r else ""
    fv["Texto65"] = _s(r.legal_rep_id) if r else ""
    fv["Texto66"] = _s(r.legal_rep_title) if r else ""

    # Section 3: Notification
    n = form.notification_address
    fv["Texto67"] = n.name_or_company
    fv["Texto68"] = n.id_number
    fv["Texto69"] = n.address
    fv["Texto70"] = _s(n.address_number)
    fv["Texto71"] = _s(n.floor_door)
    fv["Texto72"] = n.city
    fv["Texto73"] = n.postal_code
    fv["Texto74"] = n.province
    fv["Texto75"] = _s(n.mobile_phone)
    fv["Texto76"] = _s(n.email)
    fv["Casilla de verificación37"] = n.consent_electronic_notifications

    # Section 4: Request + signature + office
    req = form.request_details
    is_ld = req.authorization_family == AuthorizationFamilyEnum.RESIDENCIA_LARGA_DURACION
    is_ld_ue = req.authorization_family == AuthorizationFamilyEnum.RESIDENCIA_LARGA_DURACION_UE

    fv["Casilla de verificación38"] = is_ld
    fv["Casilla de verificación39"] = is_ld and req.ld_subtype == LdSubtypeEnum.GENERAL_5_YEARS_ART_183_1
    fv["Casilla de verificación40"] = is_ld and req.ld_subtype == LdSubtypeEnum.PENSION_OR_PERMANENT_DISABILITY_ART_183_3
    fv["Casilla de verificación41"] = is_ld and req.ld_subtype == LdSubtypeEnum.BORN_IN_SPAIN_AND_3_YEARS_RESIDENCE_ART_183_3_C
    fv["Casilla de verificación42"] = is_ld and req.ld_subtype == LdSubtypeEnum.FORMER_SPANISH_NATIONAL_ART_183_3_D
    fv["Casilla de verificación43"] = is_ld and req.ld_subtype == LdSubtypeEnum.FORMER_PUBLIC_GUARDIANSHIP_ART_183_3_E
    fv["Casilla de verificación44"] = is_ld and req.ld_subtype == LdSubtypeEnum.STATELESS_OR_REFUGEE_ART_183_3_F
    fv["Casilla de verificación45"] = is_ld and req.ld_subtype == LdSubtypeEnum.FAMILY_REUNIFICATION_WITH_LTR_SPONSOR
    fv["Casilla de verificación46"] = is_ld and req.ld_subtype == LdSubtypeEnum.EU_LTR_HOLDER_IN_OTHER_MEMBER_STATE_ART_179
    fv["Casilla de verificación47"] = is_ld and req.ld_subtype == LdSubtypeEnum.RECOVERY_AFTER_LOSS_ART_188

    fv["Casilla de verificación48"] = is_ld_ue
    fv["Casilla de verificación49"] = is_ld_ue and req.ld_ue_subtype == LdUeSubtypeEnum.GENERAL_5_YEARS_WITH_RESOURCES_AND_INSURANCE_ART_176_1_A
    fv["Casilla de verificación50"] = is_ld_ue and req.ld_ue_subtype == LdUeSubtypeEnum.STUDIES_EXCHANGE_PRACTICES_COMPUTED_50_ART_176_A
    fv["Casilla de verificación51"] = is_ld_ue and req.ld_ue_subtype == LdUeSubtypeEnum.TWO_YEARS_SPAIN_PLUS_THREE_YEARS_BLUE_CARD_EU_ART_176_A
    fv["Casilla de verificación52"] = is_ld_ue and req.ld_ue_subtype == LdUeSubtypeEnum.OTHER_MEMBER_STATE_EU_LTR_RENUNCIATION_ART_181
    fv["Casilla de verificación53"] = is_ld_ue and req.ld_ue_subtype == LdUeSubtypeEnum.RECOVERY_AFTER_LOSS_ART_186

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
