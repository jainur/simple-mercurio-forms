# Phase 2 API Field-by-Field Contracts

## Purpose
This document provides JSON Schema-like contracts for all frontend-consumed endpoints defined in the API contract specification.

## Conventions
- type: string, integer, number, boolean, object, array
- format: uuid, date-time, date, uri, email
- enum: constrained values
- required: required fields only
- nullable: true means field may be null

## Shared Envelope Schemas

### Request Headers (Common)
{
  "Authorization": {"type": "string", "required": true, "description": "Bearer JWT token"},
  "Idempotency-Key": {"type": "string", "required": false, "description": "Required for mutating endpoints"},
  "X-Request-ID": {"type": "string", "required": false}
}

### Response Envelope
{
  "type": "object",
  "required": ["request_id", "api_version", "data", "error"],
  "properties": {
    "request_id": {"type": "string"},
    "api_version": {"type": "string", "enum": ["v1"]},
    "data": {"type": ["object", "array", "null"]},
    "error": {
      "type": ["object", "null"],
      "properties": {
        "code": {"type": "string"},
        "message": {"type": "string"},
        "details": {"type": ["object", "null"]}
      }
    }
  }
}

## A01 Cases and Overview

### GET /v1/cases
Query Schema
{
  "type": "object",
  "properties": {
    "q": {"type": "string"},
    "state": {"type": "string"},
    "assignee": {"type": "string"},
    "procedure_id": {"type": "string"},
    "page": {"type": "integer", "minimum": 1, "default": 1},
    "page_size": {"type": "integer", "minimum": 1, "maximum": 100, "default": 25},
    "sort_by": {"type": "string"},
    "sort_dir": {"type": "string", "enum": ["asc", "desc"], "default": "desc"},
    "from": {"type": "string", "format": "date-time"},
    "to": {"type": "string", "format": "date-time"}
  }
}

Response data Schema
{
  "type": "object",
  "required": ["items", "total", "page", "page_size", "has_next"],
  "properties": {
    "items": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["case_id", "external_matter_id", "state", "priority", "opened_at"],
        "properties": {
          "case_id": {"type": "string"},
          "external_matter_id": {"type": "string"},
          "procedure_id": {"type": ["string", "null"]},
          "state": {"type": "string"},
          "priority": {"type": "string", "enum": ["normal", "high", "urgent"]},
          "assignee": {"type": ["string", "null"]},
          "sync_health": {"type": ["string", "null"], "enum": ["healthy", "degraded", "disconnected", null]},
          "opened_at": {"type": "string", "format": "date-time"}
        }
      }
    },
    "total": {"type": "integer"},
    "page": {"type": "integer"},
    "page_size": {"type": "integer"},
    "has_next": {"type": "boolean"}
  }
}

### POST /v1/cases
Request Schema
{
  "type": "object",
  "required": ["external_matter_id", "priority"],
  "properties": {
    "external_matter_id": {"type": "string", "minLength": 1},
    "procedure_id": {"type": ["string", "null"]},
    "priority": {"type": "string", "enum": ["normal", "high", "urgent"]}
  }
}

Response data Schema
{
  "type": "object",
  "required": ["case_id", "external_matter_id", "state", "priority", "opened_at"],
  "properties": {
    "case_id": {"type": "string"},
    "external_matter_id": {"type": "string"},
    "procedure_id": {"type": ["string", "null"]},
    "state": {"type": "string"},
    "priority": {"type": "string"},
    "opened_at": {"type": "string", "format": "date-time"}
  }
}

### GET /v1/cases/{case_id}/overview
Path Params Schema
{
  "type": "object",
  "required": ["case_id"],
  "properties": {
    "case_id": {"type": "string"}
  }
}

Response data Schema
{
  "type": "object",
  "required": ["stage", "next_action", "blockers", "risk_flags", "deadlines"],
  "properties": {
    "stage": {"type": "string"},
    "next_action": {"type": "string"},
    "blockers": {
      "type": "array",
      "items": {"type": "object", "properties": {"code": {"type": "string"}, "message": {"type": "string"}, "severity": {"type": "string"}}}
    },
    "risk_flags": {
      "type": "array",
      "items": {"type": "object", "properties": {"code": {"type": "string"}, "label": {"type": "string"}, "severity": {"type": "string"}}}
    },
    "deadlines": {
      "type": "array",
      "items": {"type": "object", "properties": {"code": {"type": "string"}, "due_at": {"type": "string", "format": "date-time"}, "status": {"type": "string"}}}
    }
  }
}

## A02 Intake and Documents

### POST /v1/cases/{case_id}/intake/submissions
Request Schema
{
  "type": "object",
  "required": ["intake_version", "answers", "declarations"],
  "properties": {
    "intake_version": {"type": "string"},
    "answers": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["question_id", "value"],
        "properties": {
          "question_id": {"type": "string"},
          "value": {}
        }
      }
    },
    "declarations": {
      "type": "object",
      "required": ["data_accuracy_confirmed", "consent_to_processing"],
      "properties": {
        "data_accuracy_confirmed": {"type": "boolean"},
        "consent_to_processing": {"type": "boolean"}
      }
    }
  }
}

Response data Schema
{
  "type": "object",
  "required": ["case_id", "intake_status", "completeness_score", "missing_sections", "next_action"],
  "properties": {
    "case_id": {"type": "string"},
    "intake_status": {"type": "string", "enum": ["draft", "submitted", "needs_clarification"]},
    "completeness_score": {"type": "number", "minimum": 0, "maximum": 1},
    "missing_sections": {"type": "array", "items": {"type": "string"}},
    "next_action": {"type": "string"}
  }
}

### POST /v1/cases/{case_id}/documents
Request Schema
{
  "type": "object",
  "required": ["document_type", "source_channel"],
  "properties": {
    "document_type": {"type": "string"},
    "source_channel": {"type": "string", "enum": ["client_portal", "assistant_upload", "integration", "email"]},
    "upload_token": {"type": ["string", "null"]},
    "file_name": {"type": ["string", "null"]},
    "mime_type": {"type": ["string", "null"]},
    "metadata": {"type": ["object", "null"]}
  }
}

Response data Schema
{
  "type": "object",
  "required": ["artifact_id", "processing_status"],
  "properties": {
    "artifact_id": {"type": "string"},
    "processing_status": {"type": "string", "enum": ["queued", "processing", "completed", "failed"]}
  }
}

### GET /v1/cases/{case_id}/documents
Response data Schema
{
  "type": "object",
  "required": ["checklist", "artifacts", "unresolved_requirements"],
  "properties": {
    "checklist": {
      "type": "array",
      "items": {"type": "object", "properties": {"requirement_code": {"type": "string"}, "status": {"type": "string"}, "mandatory": {"type": "boolean"}}}
    },
    "artifacts": {
      "type": "array",
      "items": {"type": "object", "properties": {"artifact_id": {"type": "string"}, "document_type": {"type": "string"}, "uploaded_at": {"type": "string", "format": "date-time"}, "extraction_status": {"type": "string"}}}
    },
    "unresolved_requirements": {"type": "array", "items": {"type": "string"}}
  }
}

### POST /v1/cases/{case_id}/document-requests
Request Schema
{
  "type": "object",
  "required": ["missing_items", "due_date", "message_template_id"],
  "properties": {
    "missing_items": {"type": "array", "items": {"type": "string"}},
    "due_date": {"type": "string", "format": "date"},
    "message_template_id": {"type": "string"},
    "custom_message": {"type": ["string", "null"]}
  }
}

Response data Schema
{
  "type": "object",
  "required": ["request_id", "status"],
  "properties": {
    "request_id": {"type": "string"},
    "status": {"type": "string", "enum": ["queued", "sent", "failed"]}
  }
}

## A03 Data Review and Extractions

### GET /v1/cases/{case_id}/extractions
Response data Schema
{
  "type": "object",
  "required": ["items"],
  "properties": {
    "items": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["artifact_id", "document_type", "status", "fields"],
        "properties": {
          "artifact_id": {"type": "string"},
          "document_type": {"type": "string"},
          "status": {"type": "string", "enum": ["pending", "partially_corrected", "approved"]},
          "fields": {
            "type": "array",
            "items": {
              "type": "object",
              "required": ["field_key", "value", "source", "confidence", "corrected"],
              "properties": {
                "field_key": {"type": "string"},
                "value": {},
                "source": {"type": "string", "enum": ["ocr", "intake", "manual", "pms"]},
                "confidence": {"type": "number", "minimum": 0, "maximum": 1},
                "corrected": {"type": "boolean"}
              }
            }
          }
        }
      }
    }
  }
}

### PATCH /v1/cases/{case_id}/extractions/{artifact_id}
Request Schema
{
  "type": "object",
  "required": ["field_updates"],
  "properties": {
    "field_updates": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["field_key", "new_value"],
        "properties": {
          "field_key": {"type": "string"},
          "new_value": {},
          "reason": {"type": ["string", "null"]}
        }
      }
    },
    "comment": {"type": ["string", "null"]}
  }
}

Response data Schema
{
  "type": "object",
  "required": ["artifact_id", "status", "updated_fields"],
  "properties": {
    "artifact_id": {"type": "string"},
    "status": {"type": "string"},
    "updated_fields": {"type": "array", "items": {"type": "string"}}
  }
}

### POST /v1/cases/{case_id}/extractions/approve
Request Schema
{
  "type": "object",
  "required": ["approval_note"],
  "properties": {
    "approval_note": {"type": "string", "minLength": 1}
  }
}

Response data Schema
{
  "type": "object",
  "required": ["gate_status", "next_state"],
  "properties": {
    "gate_status": {"type": "string", "enum": ["approved"]},
    "next_state": {"type": "string"}
  }
}

## A04 Eligibility and Requirements

### GET /v1/cases/{case_id}/procedure/requirements
Response data Schema
{
  "type": "object",
  "required": ["procedure_id", "required_documents", "prerequisites", "fees", "deadlines", "channels"],
  "properties": {
    "procedure_id": {"type": "string"},
    "required_documents": {
      "type": "array",
      "items": {"type": "object", "properties": {"code": {"type": "string"}, "name": {"type": "string"}, "mandatory": {"type": "boolean"}}}
    },
    "prerequisites": {
      "type": "array",
      "items": {"type": "object", "properties": {"code": {"type": "string"}, "description": {"type": "string"}}}
    },
    "fees": {
      "type": "array",
      "items": {"type": "object", "properties": {"code": {"type": "string"}, "amount": {"type": "number"}, "currency": {"type": "string"}}}
    },
    "deadlines": {
      "type": "array",
      "items": {"type": "object", "properties": {"code": {"type": "string"}, "days_from_start": {"type": "integer"}}}
    },
    "channels": {"type": "array", "items": {"type": "string"}}
  }
}

### POST /v1/cases/{case_id}/eligibility/runs
Request Schema
{
  "type": "object",
  "required": ["procedure_ids"],
  "properties": {
    "procedure_ids": {"type": "array", "items": {"type": "string"}, "minItems": 1}
  }
}

Response data Schema
{
  "type": "object",
  "required": ["assessment_id", "ranked_options"],
  "properties": {
    "assessment_id": {"type": "string"},
    "ranked_options": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "procedure_id": {"type": "string"},
          "score": {"type": "number"},
          "readiness": {"type": "string"}
        }
      }
    }
  }
}

### GET /v1/cases/{case_id}/eligibility/{assessment_id}
Response data Schema
{
  "type": "object",
  "required": ["assessment_id", "matrix"],
  "properties": {
    "assessment_id": {"type": "string"},
    "matrix": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["requirement_id", "status", "confidence", "citations"],
        "properties": {
          "requirement_id": {"type": "string"},
          "status": {"type": "string", "enum": ["SATISFIED", "PARTIALLY_SATISFIED", "MISSING", "CONFLICTING", "NEEDS_REVIEW"]},
          "confidence": {"type": "number", "minimum": 0, "maximum": 1},
          "citations": {"type": "array", "items": {"type": "string"}},
          "gaps": {"type": "array", "items": {"type": "string"}}
        }
      }
    }
  }
}

## A05 Forms and Review

### POST /v1/cases/{case_id}/forms/generate
Request Schema
{
  "type": "object",
  "required": ["submission_mode"],
  "properties": {
    "submission_mode": {"type": "string", "enum": ["offline", "online"]}
  }
}

Response data Schema
{
  "type": "object",
  "required": ["form_id", "status", "unresolved_fields", "next_state"],
  "properties": {
    "form_id": {"type": "string"},
    "status": {"type": "string", "enum": ["generating", "ready", "approved", "submitted"]},
    "unresolved_fields": {"type": "integer", "minimum": 0},
    "next_state": {"type": "string"}
  }
}

### GET /v1/cases/{case_id}/forms
Response data Schema
{
  "type": "object",
  "required": ["items"],
  "properties": {
    "items": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["form_id", "procedure_id", "submission_mode", "status"],
        "properties": {
          "form_id": {"type": "string"},
          "procedure_id": {"type": "string"},
          "submission_mode": {"type": "string", "enum": ["offline", "online"]},
          "status": {"type": "string"},
          "unresolved_fields": {"type": "integer"}
        }
      }
    }
  }
}

### GET /v1/cases/{case_id}/forms/{form_id}
Response data Schema
{
  "type": "object",
  "required": ["form_id", "status"],
  "properties": {
    "form_id": {"type": "string"},
    "status": {"type": "string"},
    "html_uri": {"type": ["string", "null"], "format": "uri"},
    "pdf_uri": {"type": ["string", "null"], "format": "uri"},
    "filled_fields": {"type": ["object", "null"]}
  }
}

### PATCH /v1/cases/{case_id}/forms/{form_id}
Request Schema
{
  "type": "object",
  "required": ["field_updates"],
  "properties": {
    "field_updates": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["field_key", "new_value"],
        "properties": {
          "field_key": {"type": "string"},
          "new_value": {},
          "reason": {"type": ["string", "null"]}
        }
      }
    },
    "rationale": {"type": ["string", "null"]}
  }
}

Response data Schema
{
  "type": "object",
  "required": ["form_id", "status", "unresolved_fields"],
  "properties": {
    "form_id": {"type": "string"},
    "status": {"type": "string"},
    "unresolved_fields": {"type": "integer", "minimum": 0}
  }
}

### POST /v1/cases/{case_id}/forms/{form_id}/approve
Request Schema
{
  "type": "object",
  "required": ["rationale"],
  "properties": {
    "rationale": {"type": "string", "minLength": 1}
  }
}

Response data Schema
{
  "type": "object",
  "required": ["decision", "next_state"],
  "properties": {
    "decision": {"type": "string", "enum": ["approved"]},
    "next_state": {"type": "string"}
  }
}

### POST /v1/cases/{case_id}/forms/{form_id}/submit-decision
Request Schema
{
  "type": "object",
  "required": ["decision", "rationale"],
  "properties": {
    "decision": {"type": "string", "enum": ["submit", "decline"]},
    "rationale": {"type": "string", "minLength": 1}
  }
}

Response data Schema
{
  "type": "object",
  "required": ["case_id", "form_id", "decision", "next_state"],
  "properties": {
    "case_id": {"type": "string"},
    "form_id": {"type": "string"},
    "decision": {"type": "string"},
    "next_state": {"type": "string"}
  }
}

## A06 Filing and Monitoring

### POST /v1/cases/{case_id}/certificate
Request Schema (metadata)
{
  "type": "object",
  "required": ["file_name", "mime_type"],
  "properties": {
    "file_name": {"type": "string"},
    "mime_type": {"type": "string", "enum": ["application/x-pkcs12"]},
    "passphrase": {"type": ["string", "null"]}
  }
}

Response data Schema
{
  "type": "object",
  "required": ["certificate_status"],
  "properties": {
    "certificate_status": {"type": "string", "enum": ["provided", "in_use", "purged"]}
  }
}

### GET /v1/cases/{case_id}/filing/status
Response data Schema
{
  "type": "object",
  "required": ["readiness", "submission_state", "receipt_refs"],
  "properties": {
    "readiness": {"type": "string", "enum": ["not_ready", "ready", "blocked"]},
    "submission_state": {"type": "string"},
    "certificate_status": {"type": ["string", "null"]},
    "receipt_refs": {
      "type": "array",
      "items": {"type": "object", "properties": {"receipt_id": {"type": "string"}, "captured_at": {"type": "string", "format": "date-time"}}}
    }
  }
}

### GET /v1/cases/{case_id}/timeline
Query Schema
{
  "type": "object",
  "properties": {
    "event_type": {"type": "string"},
    "actor": {"type": "string"},
    "from": {"type": "string", "format": "date-time"},
    "to": {"type": "string", "format": "date-time"},
    "page": {"type": "integer", "minimum": 1},
    "page_size": {"type": "integer", "minimum": 1, "maximum": 100}
  }
}

Response data Schema
{
  "type": "object",
  "required": ["items", "total", "page", "page_size", "has_next"],
  "properties": {
    "items": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["event_id", "event_type", "occurred_at"],
        "properties": {
          "event_id": {"type": "string"},
          "event_type": {"type": "string"},
          "actor": {"type": ["string", "null"]},
          "summary": {"type": ["string", "null"]},
          "occurred_at": {"type": "string", "format": "date-time"},
          "artifact_ref": {"type": ["string", "null"]}
        }
      }
    },
    "total": {"type": "integer"},
    "page": {"type": "integer"},
    "page_size": {"type": "integer"},
    "has_next": {"type": "boolean"}
  }
}

## A07 Sync and Integrations

### GET /v1/cases/{case_id}/external-record
Response data Schema
{
  "type": "object",
  "required": ["system_name", "external_matter_id", "last_sync_at", "conflict_count", "fields"],
  "properties": {
    "system_name": {"type": "string"},
    "external_matter_id": {"type": "string"},
    "last_sync_at": {"type": ["string", "null"], "format": "date-time"},
    "conflict_count": {"type": "integer", "minimum": 0},
    "fields": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "field_key": {"type": "string"},
          "local_value": {},
          "external_value": {},
          "source": {"type": "string", "enum": ["pms", "intake", "ocr", "manual"]},
          "status": {"type": "string", "enum": ["in_sync", "conflicted", "pending_publish"]}
        }
      }
    }
  }
}

### GET /v1/cases/{case_id}/sync-log
Query Schema
{
  "type": "object",
  "properties": {
    "direction": {"type": "string", "enum": ["inbound", "outbound"]},
    "status": {"type": "string"},
    "from": {"type": "string", "format": "date-time"},
    "to": {"type": "string", "format": "date-time"},
    "page": {"type": "integer", "minimum": 1},
    "page_size": {"type": "integer", "minimum": 1, "maximum": 100}
  }
}

Response data Schema
{
  "type": "object",
  "required": ["items", "total", "page", "page_size", "has_next"],
  "properties": {
    "items": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "sync_event_id": {"type": "string"},
          "direction": {"type": "string"},
          "operation": {"type": "string"},
          "status": {"type": "string"},
          "attempt_count": {"type": "integer"},
          "occurred_at": {"type": "string", "format": "date-time"}
        }
      }
    },
    "total": {"type": "integer"},
    "page": {"type": "integer"},
    "page_size": {"type": "integer"},
    "has_next": {"type": "boolean"}
  }
}

### POST /v1/cases/{case_id}/sync/retry
Request Schema
{
  "type": "object",
  "required": ["sync_event_id"],
  "properties": {
    "sync_event_id": {"type": "string"},
    "reason": {"type": ["string", "null"]}
  }
}

Response data Schema
{
  "type": "object",
  "required": ["sync_event_id", "retry_status"],
  "properties": {
    "sync_event_id": {"type": "string"},
    "retry_status": {"type": "string", "enum": ["queued", "rejected"]}
  }
}

### POST /v1/cases/{case_id}/sync/conflicts/{conflict_id}/resolve
Request Schema
{
  "type": "object",
  "required": ["strategy"],
  "properties": {
    "strategy": {"type": "string", "enum": ["use_local", "use_external", "merge"]},
    "merged_value": {},
    "rationale": {"type": ["string", "null"]}
  }
}

Response data Schema
{
  "type": "object",
  "required": ["conflict_id", "status", "resolution", "publish_back_queued"],
  "properties": {
    "conflict_id": {"type": "string"},
    "status": {"type": "string", "enum": ["resolved"]},
    "resolution": {"type": "string"},
    "publish_back_queued": {"type": "boolean"}
  }
}

## A08 Admin and Governance

### GET /v1/admin/connectors
Response data Schema
{
  "type": "object",
  "required": ["items"],
  "properties": {
    "items": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "connector_id": {"type": "string"},
          "type": {"type": "string"},
          "status": {"type": "string", "enum": ["connected", "degraded", "disconnected"]},
          "last_health_check": {"type": ["string", "null"], "format": "date-time"}
        }
      }
    }
  }
}

### PATCH /v1/admin/connectors/{connector_id}
Request Schema
{
  "type": "object",
  "properties": {
    "enabled": {"type": "boolean"},
    "config": {"type": ["object", "null"]}
  }
}

Response data Schema
{
  "type": "object",
  "required": ["connector_id", "status"],
  "properties": {
    "connector_id": {"type": "string"},
    "status": {"type": "string"}
  }
}

### GET /v1/admin/templates
Response data Schema
{
  "type": "object",
  "required": ["items"],
  "properties": {
    "items": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "template_id": {"type": "string"},
          "name": {"type": "string"},
          "category": {"type": "string"},
          "version": {"type": "string"},
          "status": {"type": "string"}
        }
      }
    }
  }
}

### POST /v1/admin/templates
Request Schema
{
  "type": "object",
  "required": ["name", "category", "definition"],
  "properties": {
    "name": {"type": "string"},
    "category": {"type": "string", "enum": ["intake", "documents", "forms", "review", "sync"]},
    "definition": {"type": "object"}
  }
}

Response data Schema
{
  "type": "object",
  "required": ["template_id", "version", "status"],
  "properties": {
    "template_id": {"type": "string"},
    "version": {"type": "string"},
    "status": {"type": "string", "enum": ["draft", "active"]}
  }
}

### GET /v1/admin/security/roles
Response data Schema
{
  "type": "object",
  "required": ["items"],
  "properties": {
    "items": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "role_id": {"type": "string"},
          "name": {"type": "string"},
          "permissions": {"type": "array", "items": {"type": "string"}}
        }
      }
    }
  }
}

### PATCH /v1/admin/security/users/{user_id}/roles
Request Schema
{
  "type": "object",
  "required": ["role_ids"],
  "properties": {
    "role_ids": {"type": "array", "items": {"type": "string"}, "minItems": 1},
    "workspace_scope": {"type": ["array", "null"], "items": {"type": "string"}}
  }
}

Response data Schema
{
  "type": "object",
  "required": ["user_id", "role_ids", "updated_at"],
  "properties": {
    "user_id": {"type": "string"},
    "role_ids": {"type": "array", "items": {"type": "string"}},
    "updated_at": {"type": "string", "format": "date-time"}
  }
}
