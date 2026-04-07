"""Mapper for EX10 domain model to PDF field values."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any
from mappers.helpers import apply_enum_registry as _apply_enum_registry, coerce_str as _s, map_identity_person_block as _map_identity_person_block, map_notification_block as _map_notification_block, map_optional_object_fields as _map_optional_object_fields, split_nie as _split_nie

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
            "Casilla de verificación96": "X",
            "Casilla de verificación97": "H",
            "Casilla de verificación98": "M",
        },
        marital_checkbox_map={
            "Casilla de verificación99": "S",
            "Casilla de verificación100": "C",
            "Casilla de verificación101": "V",
            "Casilla de verificación102": "D",
            "Casilla de verificación103": "Sp",
        },
    )

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

    _apply_enum_registry(fv, eu.gender if eu else None, {
        "Casilla de verificación104": "X",
        "Casilla de verificación105": "H",
        "Casilla de verificación106": "M",
    })
    _apply_enum_registry(fv, eu.marital_status if eu else None, {
        "Casilla de verificación107": "S",
        "Casilla de verificación108": "C",
        "Casilla de verificación109": "V",
        "Casilla de verificación110": "D",
        "Casilla de verificación111": "Sp",
    })

    r = form.filing_representative
    _map_optional_object_fields(
        fv,
        r,
        text_fields={
            "name_or_company": "Texto48",
            "id_number": "Texto49",
            "address": "Texto50",
            "address_number": "Texto51",
            "floor_door": "Texto52",
            "city": "Texto53",
            "postal_code": "Texto54",
            "province": "Texto55",
            "mobile_phone": "Texto56",
            "email": "Texto57",
            "legal_rep_name": "Texto58",
            "legal_rep_id": "Texto59",
            "legal_rep_title": "Texto60",
        },
    )

    n = form.notification_address
    _map_notification_block(
        fv,
        n,
        text_fields={
            "name_or_company": "Texto61",
            "id_number": "Texto62",
            "address": "Texto63",
            "address_number": "Texto64",
            "floor_door": "Texto65",
            "city": "Texto66",
            "postal_code": "Texto67",
            "province": "Texto68",
            "mobile_phone": "Texto69",
            "email": "Texto70",
        },
        consent_field="",
    )

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
