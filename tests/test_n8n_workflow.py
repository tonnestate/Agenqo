"""Static safety contract for the importable n8n workflow.

This does not replace testing on the user's own n8n version.
"""
import json
from pathlib import Path

def test_n8n_workflow_has_safe_internal_only_handoff():
    p=Path(__file__).resolve().parents[1]/"n8n/workflows/agenqo_internal_review_outbox.json"
    workflow=json.loads(p.read_text(encoding="utf-8"))
    assert workflow["active"] is False
    nodes=workflow["nodes"]
    kinds={node["type"] for node in nodes}
    assert kinds=={
        "n8n-nodes-base.scheduleTrigger",
        "n8n-nodes-base.httpRequest",
        "n8n-nodes-base.if",
    }
    names={node["name"] for node in nodes}
    assert len(names)==len(nodes)
    assert len(nodes)==4
    assert len([node for node in nodes if node["type"]=="n8n-nodes-base.httpRequest"])==2
    for node in nodes:
        if node["type"]=="n8n-nodes-base.httpRequest":
            assert node["parameters"]["method"]=="POST"
            assert node["parameters"]["authentication"]=="genericCredentialType"
            assert node["parameters"]["genericAuthType"]=="httpHeaderAuth"
            assert node["parameters"]["url"].startswith("https://REPLACE-WITH-AGENQO-HOST")
            assert node["retryOnFail"] is True
    raw=json.dumps(workflow).lower()
    assert "smtp" not in raw
    assert "gmail" not in raw
    assert "sendemail" not in raw
    assert "customer_email" not in raw
    assert "authorization" not in raw
    assert "sk_test" not in raw
    assert not workflow["settings"]["saveManualExecutions"]
    assert workflow["settings"]["saveDataSuccessExecution"]=="none"
    assert workflow["settings"]["saveDataErrorExecution"]=="none"
    assert workflow["connections"]["Event available?"]["main"][0][0]["node"] == "Create internal review task and ACK"
