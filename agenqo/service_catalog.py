"""Versioned service schemas shared by agent intake, APIs and JSON-Schema forms.

A catalog definition is a contract, not an LLM-generated instruction.
Additional categories must be explicitly activated after compliance review.
"""
from copy import deepcopy
from jsonschema import Draft202012Validator

SERVICE_SCHEMAS = {
    "entruempelung": {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "$id": "https://agenqo.example/schemas/services/entruempelung/1",
        "title": "Entrümpelung / Wohnungsauflösung",
        "type": "object",
        "properties": {
            "object_type": {"type": "string", "title": "Objektart",
                            "enum": ["wohnung", "haus", "keller", "buero", "sonstiges"]},
            "area_m2": {"type": "number", "title": "Fläche in m²", "exclusiveMinimum": 0, "maximum": 100000},
            "volume_m3": {"type": "number", "title": "Geschätztes Volumen in m³",
                          "exclusiveMinimum": 0, "maximum": 100000},
            "floor": {"type": "integer", "title": "Etage", "minimum": -5, "maximum": 100},
            "elevator": {"type": "boolean", "title": "Aufzug vorhanden"},
            "special_waste": {"type": "boolean", "title": "Mögliche Sonderabfälle"},
            "visit_required": {"type": "boolean", "title": "Besichtigung notwendig"},
        },
        "additionalProperties": False,
        "minProperties": 1,
    }
}

FORM_SCHEMA = {
    "title": "Verbindliches Dienstleistungsangebot (Pilot)",
    "type": "object",
    "properties": {
        "description": {"title": "Vollständiger Leistungsumfang", "type": "string", "minLength": 8},
        "conditions": {"title": "Vorbehalte / Bedingungen", "type": "string", "default": ""},
        "price_net_eur": {"title": "Angebot netto in EUR", "type": "string",
                          "pattern": r"^\d{1,7}(\.\d{1,2})?$"},
        "vat_percent": {"title": "Umsatzsteuersatz in Prozent", "type": "string",
                        "enum": ["0", "7", "19"], "default": "19"},
        "valid_days": {"title": "Gültigkeit in Tagen", "type": "integer",
                       "minimum": 1, "maximum": 30, "default": 7},
        "binding_declared_by_provider": {
            "title": "Ich erkläre ein verbindliches Angebot zu diesen Bedingungen",
            "type": "boolean", "const": True
        },
    },
    "required": ["description", "price_net_eur", "vat_percent",
                 "valid_days", "binding_declared_by_provider"],
    "additionalProperties": False,
}

def public_schema(category: str) -> dict:
    if category not in SERVICE_SCHEMAS:
        raise ValueError("service_category_not_activated")
    return deepcopy(SERVICE_SCHEMAS[category])

def quote_form_schema() -> dict:
    return deepcopy(FORM_SCHEMA)

def validate_attributes(category: str, attributes: dict | None) -> dict:
    if attributes is None:
        return {}
    if not isinstance(attributes, dict):
        raise ValueError("service_attributes_must_be_object")
    schema = SERVICE_SCHEMAS.get(category)
    if schema is None:
        if attributes:
            raise ValueError("service_category_not_activated")
        return {}
    errors = sorted(Draft202012Validator(schema).iter_errors(attributes), key=lambda e: list(map(str,e.path)))
    if errors:
        raise ValueError("invalid_service_attributes: " + errors[0].message)
    return dict(attributes)
