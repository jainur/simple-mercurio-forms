# Phase 2 Capability Algorithms Pseudocode

## 1. Confidence Scoring

```python
def compute_field_confidence(ocr_conf, llm_conf, schema_conf, cross_doc_conf):
    w_ocr = 0.25
    w_llm = 0.35
    w_schema = 0.20
    w_cross = 0.20
    score = (
        w_ocr * ocr_conf
        + w_llm * llm_conf
        + w_schema * schema_conf
        + w_cross * cross_doc_conf
    )
    return clamp(score, 0.0, 1.0)


def compute_requirement_confidence(evidence_conf, reasoning_conf, citation_conf):
    a = 0.45
    b = 0.35
    c = 0.20
    score = a * evidence_conf + b * reasoning_conf + c * citation_conf
    return clamp(score, 0.0, 1.0)


def confidence_band(score):
    if score >= 0.85:
        return "HIGH"
    if score >= 0.65:
        return "MEDIUM"
    return "LOW"


def case_confidence(requirements, importance_weights, penalties):
    # requirements: list of (requirement_id, requirement_confidence)
    weighted_sum = 0.0
    weight_total = 0.0
    for req_id, req_conf in requirements:
        w = importance_weights.get(req_id, 1.0)
        weighted_sum += w * req_conf
        weight_total += w
    base = weighted_sum / max(weight_total, 1e-9)
    score = base - penalties
    return clamp(score, 0.0, 1.0)
```

## 2. Reasoning with GraphRAG (Neo4j)

```python
def run_reasoning(case_context, procedure_ids):
    # 1) retrieve grounded legal context
    retrieval_bundle = retrieve_graphrag_context(case_context, procedure_ids)

    # 2) build requirement frames
    requirement_frames = build_requirement_frames(retrieval_bundle)

    # 3) evaluate each requirement with LLM (structured output)
    evaluations = []
    for frame in requirement_frames:
        eval_result = llm_evaluate_requirement(case_context, frame)
        validated = validate_structured_eval(eval_result)
        evaluations.append(validated)

    # 4) consistency pass
    conflicts = detect_inter_requirement_conflicts(evaluations)
    if conflicts:
        for conflict in conflicts:
            reevaluated = llm_reevaluate_conflict(case_context, conflict)
            merge_reevaluated(evaluations, reevaluated)

    # 5) publish deterministic output
    matrix = build_eligibility_matrix(evaluations)
    ranking = rank_procedures(matrix)
    return {
        "matrix": matrix,
        "ranking": ranking,
    }
```

## 3. Requirement Coverage Evaluation

```python
STATUS_SCORE = {
    "SATISFIED": 1.00,
    "PARTIALLY_SATISFIED": 0.60,
    "NEEDS_REVIEW": 0.40,
    "MISSING": 0.00,
    "CONFLICTING": 0.00,
}


def evaluate_requirement(requirement, artifacts, field_values):
    evidence = gather_candidate_evidence(requirement, artifacts, field_values)
    freshness_ok = check_freshness(requirement, evidence)
    integrity_ok = check_integrity(requirement, evidence)
    consistency_ok = check_consistency(requirement, evidence)
    substitution_ok = check_substitutions(requirement, evidence)

    if evidence and freshness_ok and integrity_ok and consistency_ok:
        status = "SATISFIED"
    elif evidence and (not freshness_ok or not integrity_ok or not substitution_ok):
        status = "PARTIALLY_SATISFIED"
    elif detect_conflicts(evidence):
        status = "CONFLICTING"
    elif not evidence:
        status = "MISSING"
    else:
        status = "NEEDS_REVIEW"

    return {
        "requirement_id": requirement.id,
        "status": status,
        "supporting_evidence": [e.id for e in evidence],
        "missing_evidence": compute_missing_evidence(requirement, evidence),
        "conflicts": compute_conflicts(evidence),
    }


def compute_coverage_score(requirement_results, weights):
    numerator = 0.0
    denominator = 0.0
    for result in requirement_results:
        req_id = result["requirement_id"]
        w = weights.get(req_id, 1.0)
        s = STATUS_SCORE[result["status"]]
        numerator += w * s
        denominator += w
    return numerator / max(denominator, 1e-9)
```

## 4. Guardrails

```python
def enforce_guardrails(requirement_eval):
    # no satisfied outcome without evidence
    if requirement_eval["status"] == "SATISFIED" and not requirement_eval["supporting_evidence"]:
        requirement_eval["status"] = "NEEDS_REVIEW"

    # legal rationale must be grounded
    if not requirement_eval.get("citations"):
        requirement_eval["status"] = "NEEDS_REVIEW"

    # low confidence on mandatory requirement forces review
    if requirement_eval.get("mandatory") and requirement_eval.get("confidence", 0) < 0.65:
        requirement_eval["status"] = "NEEDS_REVIEW"

    return requirement_eval
```
