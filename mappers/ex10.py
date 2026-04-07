"""Mapper for EX10 domain model to PDF field values."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any
from mappers.helpers import assign_checkboxes, coerce_str as _s, split_nie as _split_nie

if TYPE_CHECKING:
    from models.ex10 import EX10FormSchema


def to_field_values(form: EX10FormSchema) -> dict[str, Any]:
    from models.ex10 import (
        ApplicationRequestTypeEnum,
        AuthorizationTypeEnum,
        TrainingModeEnum,
    )

    fv: dict[str, Any] = {}

    # Section 1: Foreigner + optional EU family block + filing representative + notification
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
        "Casilla de verificación96": "X",
        "Casilla de verificación97": "H",
        "Casilla de verificación98": "M",
    })
    assign_checkboxes(fv, f.marital_status.value, {
        "Casilla de verificación99": "S",
        "Casilla de verificación100": "C",
        "Casilla de verificación101": "V",
        "Casilla de verificación102": "D",
        "Casilla de verificación103": "Sp",
    })

    eu = form.eu_family_details
    fv["Texto27"] = _s(eu.passport) if eu else ""
    if eu and eu.nie:
        n1, n2, n3 = _split_nie(eu.nie)
        fv["Texto28"], fv["Texto29"], fv["Texto30"] = n1, n2, n3
    else:
        fv["Texto28"] = fv["Texto29"] = fv["Texto30"] = ""

    fv["Texto31"] = eu.first_surname if eu else ""
    fv["Texto32"] = _s(eu.second_surname) if eu else ""
    fv["Texto33"] = eu.name if eu else ""
    fv["Texto34"] = eu.date_of_birth.strftime("%d") if eu else ""
    fv["Texto35"] = eu.date_of_birth.strftime("%m") if eu else ""
    fv["Texto36"] = eu.date_of_birth.strftime("%Y") if eu else ""
    fv["Texto37"] = _s(eu.birth_country) if eu else ""
    fv["Texto38"] = _s(eu.relationship_or_type) if eu else ""
    fv["Texto39"] = _s(eu.father_name) if eu else ""
    fv["Texto40"] = _s(eu.mother_name) if eu else ""
    fv["Texto41"] = _s(eu.address) if eu else ""
    fv["Texto42"] = _s(eu.address_number) if eu else ""
    fv["Texto43"] = _s(eu.floor_door) if eu else ""
    fv["Texto44"] = _s(eu.city) if eu else ""
    fv["Texto45"] = _s(eu.postal_code) if eu else ""
    fv["Texto46"] = _s(eu.province) if eu else ""
    fv["Texto47"] = _s(eu.relationship_with_applicant) if eu else ""

    assign_checkboxes(fv, eu.gender.value if eu else None, {
        "Casilla de verificación104": "X",
        "Casilla de verificación105": "H",
        "Casilla de verificación106": "M",
    })
    assign_checkboxes(fv, eu.marital_status.value if eu else None, {
        "Casilla de verificación107": "S",
        "Casilla de verificación108": "C",
        "Casilla de verificación109": "V",
        "Casilla de verificación110": "D",
        "Casilla de verificación111": "Sp",
    })

    r = form.filing_representative
    fv["Texto48"] = _s(r.name_or_company) if r else ""
    fv["Texto49"] = _s(r.id_number) if r else ""
    fv["Texto50"] = _s(r.address) if r else ""
    fv["Texto51"] = _s(r.address_number) if r else ""
    fv["Texto52"] = _s(r.floor_door) if r else ""
    fv["Texto53"] = _s(r.city) if r else ""
    fv["Texto54"] = _s(r.postal_code) if r else ""
    fv["Texto55"] = _s(r.province) if r else ""
    fv["Texto56"] = _s(r.mobile_phone) if r else ""
    fv["Texto57"] = _s(r.email) if r else ""
    fv["Texto58"] = _s(r.legal_rep_name) if r else ""
    fv["Texto59"] = _s(r.legal_rep_id) if r else ""
    fv["Texto60"] = _s(r.legal_rep_title) if r else ""

    n = form.notification_address
    fv["Texto61"] = n.name_or_company
    fv["Texto62"] = n.id_number
    fv["Texto63"] = n.address
    fv["Texto64"] = _s(n.address_number)
    fv["Texto65"] = _s(n.floor_door)
    fv["Texto66"] = n.city
    fv["Texto67"] = n.postal_code
    fv["Texto68"] = n.province
    fv["Texto69"] = _s(n.mobile_phone)
    fv["Texto70"] = _s(n.email)

    # Section 5: Employer details
    e = form.employer_details
    fv["Texto71"] = e.name_or_company
    fv["Texto72"] = e.id_number
    fv["Texto73"] = e.activity
    fv["Texto74"] = _s(e.cnae_code)
    fv["Texto75"] = _s(e.cno_spe_2011)
    fv["Texto76"] = e.address
    fv["Texto77"] = _s(e.address_number)
    fv["Texto78"] = _s(e.floor_door)
    fv["Texto79"] = e.city
    fv["Texto80"] = e.postal_code
    fv["Texto81"] = e.province
    fv["Texto82"] = _s(e.mobile_phone)
    fv["Texto83"] = _s(e.email)
    fv["Texto84"] = _s(e.legal_rep_name)
    fv["Texto85"] = _s(e.legal_rep_id)
    fv["Texto86"] = _s(e.legal_rep_title)

    # Section 6: Training details
    t = form.training_details
    fv["Texto87"] = _s(t.training_name)
    fv["Texto88"] = _s(t.course_code_1)
    fv["Texto89"] = _s(t.course_code_2)
    fv["Texto90"] = _s(t.course_code_3)
    fv["Texto91"] = _s(t.end_date)
    fv["Texto92"] = _s(t.province)
    fv["Texto93"] = _s(t.duration_hours)
    fv["Texto94"] = _s(t.start_date)
    fv["Texto95"] = _s(t.end_date)

    fv["Casilla de verificación112"] = t.training_mode is not None
    fv["Casilla de verificación113"] = t.training_mode == TrainingModeEnum.SECONDARY_POSTOBLIGATORY
    fv["Casilla de verificación114"] = t.training_mode == TrainingModeEnum.PROFESSIONAL_CERTIFICATE_LEVEL_1
    fv["Casilla de verificación115"] = t.training_mode == TrainingModeEnum.PROFESSIONAL_CERTIFICATE_LEVEL_2
    fv["Casilla de verificación116"] = t.training_mode == TrainingModeEnum.MIXED
    fv["Casilla de verificación117"] = t.training_mode == TrainingModeEnum.MIXED
    fv["Casilla de verificación118"] = t.training_mode == TrainingModeEnum.IN_PERSON_OR_DISTANCE

    # Section 7: Request, signatures and office
    req = form.request_details
    fv["Casilla de verificación119"] = req.request_type == ApplicationRequestTypeEnum.INITIAL
    fv["Casilla de verificación120"] = req.request_type == ApplicationRequestTypeEnum.INITIAL
    fv["Casilla de verificación121"] = req.request_type == ApplicationRequestTypeEnum.INITIAL
    fv["Casilla de verificación122"] = req.request_type == ApplicationRequestTypeEnum.EXTENSION

    fv["Casilla de verificación123"] = req.authorization_type == AuthorizationTypeEnum.SECOND_OPPORTUNITY_ART_127_A
    fv["Casilla de verificación124"] = req.authorization_type == AuthorizationTypeEnum.SECOND_OPPORTUNITY_ART_127_A
    fv["Casilla de verificación125"] = req.authorization_type == AuthorizationTypeEnum.SECOND_OPPORTUNITY_ART_127_A
    fv["Casilla de verificación126"] = req.authorization_type == AuthorizationTypeEnum.SOCIOLABORAL_ART_127_B
    fv["Casilla de verificación127"] = req.authorization_type == AuthorizationTypeEnum.SOCIAL_ART_127_C
    fv["Casilla de verificación128"] = req.authorization_type == AuthorizationTypeEnum.SOCIOFORMATIVO_ART_127_D
    fv["Casilla de verificación129"] = req.authorization_type == AuthorizationTypeEnum.FAMILY_ART_127_E

    fv["Casilla de verificación130"] = req.humanitarian_option_1
    fv["Casilla de verificación131"] = req.humanitarian_option_2
    fv["Casilla de verificación132"] = req.humanitarian_option_3
    fv["Casilla de verificación133"] = req.humanitarian_option_4
    fv["Casilla de verificación134"] = req.humanitarian_option_5

    fv["Casilla de verificación135"] = req.public_interest_option_1
    fv["Casilla de verificación136"] = req.public_interest_option_2

    fv["Casilla de verificación137"] = req.gender_violence_woman_option_1
    fv["Casilla de verificación138"] = req.gender_violence_woman_option_2
    fv["Casilla de verificación139"] = req.parent_of_gender_violence_victim

    fv["Casilla de verificación140"] = req.sexual_violence_option_1
    fv["Casilla de verificación141"] = req.sexual_violence_option_2

    fv["Casilla de verificación142"] = req.parent_of_sexual_violence_option_1
    fv["Casilla de verificación143"] = req.parent_of_sexual_violence_option_2
    fv["Casilla de verificación144"] = req.parent_of_sexual_violence_option_3
    fv["Casilla de verificación145"] = req.parent_of_sexual_violence_option_4
    fv["Casilla de verificación146"] = req.parent_of_sexual_violence_option_5
    fv["Casilla de verificación147"] = req.parent_of_sexual_violence_option_6
    fv["Casilla de verificación148"] = req.unknown_option_148

    fv["Casilla de verificación261"] = req.has_valid_electronic_certificate_or_clave

    sig = form.signature
    fv["Texto149"] = _s(sig.signer_1)
    fv["Texto150"] = _s(sig.signer_2)
    fv["Texto151"] = _s(sig.signer_3)
    fv["Texto152"] = _s(sig.signer_4)
    fv["Texto153"] = _s(sig.signer_5)

    o = form.office
    fv["Texto154"] = _s(o.target_office)
    fv["Texto155"] = _s(o.dir3_code)
    fv["Texto156"] = o.province

    return fv
