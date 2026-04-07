"""Mapper for EX16 domain model to PDF field values."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any
from mappers.helpers import assign_checkboxes, coerce_str as _s, split_nie as _split_nie

if TYPE_CHECKING:
    from models.ex16 import EX16FormSchema


def to_field_values(form: EX16FormSchema) -> dict[str, Any]:
    from models.ex16 import AuthorizationStageEnum, ReturnModeEnum, TravelDocumentTypeEnum

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
        "Casilla de verificación1": "X",
        "Casilla de verificación2": "H",
        "Casilla de verificación3": "M",
    })
    assign_checkboxes(fv, f.marital_status.value, {
        "Casilla de verificación4": "S",
        "Casilla de verificación5": "C",
        "Casilla de verificación6": "V",
        "Casilla de verificación7": "D",
        "Casilla de verificación8": "Sp",
    })

    # Section 2: Filing representative
    r = form.filing_representative
    fv["Texto27"] = _s(r.name_or_company) if r else ""
    fv["Texto28"] = _s(r.id_number) if r else ""
    fv["Texto29"] = _s(r.address) if r else ""
    fv["Texto30"] = _s(r.address_number) if r else ""
    fv["Texto31"] = _s(r.floor_door) if r else ""
    fv["Texto32"] = _s(r.city) if r else ""
    fv["Texto33"] = _s(r.postal_code) if r else ""
    fv["Texto34"] = _s(r.province) if r else ""
    fv["Texto35"] = _s(r.mobile_phone) if r else ""
    fv["Texto36"] = _s(r.email) if r else ""
    fv["Texto37"] = _s(r.legal_rep_name) if r else ""
    fv["Texto38"] = _s(r.legal_rep_id) if r else ""
    fv["Texto39"] = _s(r.legal_rep_title) if r else ""

    # Section 3: Notification
    n = form.notification_address
    fv["Texto40"] = n.name_or_company
    fv["Texto41"] = n.id_number
    fv["Texto42"] = n.address
    fv["Texto43"] = _s(n.address_number)
    fv["Texto44"] = _s(n.floor_door)
    fv["Texto45"] = n.city
    fv["Texto46"] = n.postal_code
    fv["Texto47"] = n.province
    fv["Texto48"] = _s(n.mobile_phone)
    fv["Texto49"] = _s(n.email)
    fv["Casilla de verificación9"] = n.consent_electronic_notifications

    # Section 4: Request + signature + office
    req = form.request_details
    fv["Texto50"] = req.destination

    fv["Casilla de verificación10"] = req.reason_humanitarian
    fv["Casilla de verificación11"] = req.reason_public_interest
    fv["Casilla de verificación12"] = req.reason_spain_commitments
    fv["Casilla de verificación13"] = req.reason_exceptional_circumstances

    fv["Casilla de verificación14"] = req.stage == AuthorizationStageEnum.RENEWAL
    fv["Casilla de verificación15"] = req.stage == AuthorizationStageEnum.INITIAL

    fv["Casilla de verificación16"] = req.document_type == TravelDocumentTypeEnum.TRAVEL_TITLE
    fv["Casilla de verificación17"] = req.return_mode == ReturnModeEnum.WITH_RETURN
    fv["Casilla de verificación18"] = req.return_mode == ReturnModeEnum.WITHOUT_RETURN

    fv["Casilla de verificación19"] = req.title_motivos_checkbox
    fv["Casilla de verificación20"] = req.title_reason_humanitarian
    fv["Casilla de verificación21"] = req.title_reason_public_interest

    sig = form.signature
    fv["Texto51"] = sig.place
    fv["Texto52"] = sig.day
    fv["Texto53"] = sig.month
    fv["Texto54"] = sig.year
    fv["Texto55"] = _s(sig.name)

    off = form.office
    fv["Texto56"] = _s(off.target_office)
    fv["Texto57"] = _s(off.dir3_code)
    fv["Texto58"] = off.province

    return fv
