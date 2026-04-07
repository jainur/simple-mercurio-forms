"""Mapper for EX13 domain model to PDF field values."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any
from mappers.helpers import assign_checkboxes, coerce_str as _s, split_nie as _split_nie

if TYPE_CHECKING:
    from models.ex13 import EX13FormSchema


def to_field_values(form: EX13FormSchema) -> dict[str, Any]:
    from models.ex13 import ReturnAuthorizationGroundEnum

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

    # Section 2: Filing representative
    r = form.filing_representative
    fv["Texto42"] = _s(r.name_or_company) if r else ""
    fv["Texto43"] = _s(r.id_number) if r else ""
    fv["Texto44"] = _s(r.address) if r else ""
    fv["Texto45"] = _s(r.address_number) if r else ""
    fv["Texto46"] = _s(r.floor_door) if r else ""
    fv["Texto47"] = _s(r.city) if r else ""
    fv["Texto48"] = _s(r.postal_code) if r else ""
    fv["Texto49"] = _s(r.province) if r else ""
    fv["Texto50"] = _s(r.mobile_phone) if r else ""
    fv["Texto51"] = _s(r.email) if r else ""
    fv["Texto52"] = _s(r.legal_rep_name) if r else ""
    fv["Texto53"] = _s(r.legal_rep_id) if r else ""
    fv["Texto54"] = _s(r.legal_rep_title) if r else ""

    # Section 3: Notification
    n = form.notification_address
    fv["Texto55"] = n.name_or_company
    fv["Texto56"] = n.id_number
    fv["Texto57"] = n.address
    fv["Texto58"] = _s(n.address_number)
    fv["Texto59"] = _s(n.floor_door)
    fv["Texto60"] = n.city
    fv["Texto61"] = n.postal_code
    fv["Texto62"] = n.province
    fv["Texto63"] = _s(n.mobile_phone)
    fv["Texto64"] = _s(n.email)
    fv["Casilla de verificación35"] = n.consent_electronic_notifications

    # Section 4: Grounds + signature + office
    req = form.request_details
    fv["Casilla de verificación36"] = req.ground == ReturnAuthorizationGroundEnum.RESIDENCE_RENEWAL_OR_EXTENSION_ART_5
    fv["Casilla de verificación37"] = req.ground == ReturnAuthorizationGroundEnum.STAY_EXTENSION_ART_5
    fv["Casilla de verificación38"] = req.ground == ReturnAuthorizationGroundEnum.TIE_DUPLICATE_THEFT_LOSS_DAMAGE_ART_5
    fv["Casilla de verificación39"] = req.ground == ReturnAuthorizationGroundEnum.INITIAL_RESIDENCE_TIE_ISSUANCE_EXCEPTIONAL_REASONS_ART_5
    fv["Casilla de verificación40"] = req.ground == ReturnAuthorizationGroundEnum.INITIAL_STAY_TIE_ISSUANCE_EXCEPTIONAL_REASONS_ART_5
    fv["Casilla de verificación41"] = req.ground == ReturnAuthorizationGroundEnum.OTHER

    # The form has 3 separate 'Otros' text boxes in extracted widgets.
    fv["Texto74"] = _s(req.other_reason_text_1)
    fv["Texto75"] = _s(req.other_reason_text_2)
    fv["Texto27"] = _s(req.other_reason_text_3)

    sig = form.signature
    fv["Texto66"] = sig.place
    fv["Texto67"] = sig.day
    fv["Texto68"] = sig.month
    fv["Texto69"] = sig.year
    fv["Texto70"] = _s(sig.name)

    off = form.office
    fv["Texto71"] = _s(off.target_office)
    fv["Texto72"] = _s(off.dir3_code)
    fv["Texto73"] = off.province

    return fv
