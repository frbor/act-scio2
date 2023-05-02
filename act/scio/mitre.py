from typing import Dict, Any, List, cast


def navigator_layer(mitre_map: Dict[str, Any], metadata_name: str) -> Dict[str, Any]:
    """Function for writing MITRE ATT&CK navigator JSON data to file"""

    # MITRE ATT&CK navigator configuration
    data = {
        "name": "Argus MITRE ATT&CK Coverage",
        "versions": {"navigator": "4.0", "layer": "4.0"},
        "domain": "enterprise-attack",
        "description": "description",
        "filters": {"platforms": ["Windows", "Azure", "Azure AD", "Office 365"]},
        "sorting": 0,
        "layout": {
            "layout": "flat",
            "showName": True,
            "showID": False,
        },
        "hideDisable": False,
        "selectSubtechniquesWithParent": False,
        "techniques": [],
        "showTacticRowBackground": False,
        "tacticRowBackground": "#dddddd",
        "selectTechniquesAcrossTactics": True,
        "legendItems": [
            {"label": "Detection score 0: Forensics/Context", "color": "#9C27B0"},
            {"label": "Detection score 1: Basic", "color": "#DCEDC8"},
            {"label": "Detection score 2: Fair", "color": "#AED581"},
            {"label": "Detection score 3: Good", "color": "#8BC34A"},
            {"label": "Detection score 4: Very good", "color": "#689F38"},
            {"label": "Detection score 5: Excellent", "color": "#33691E"},
        ],
    }

    # Iterate over each technique
    for mitre_id in mitre_map:
        # Skip tactics
        if mitre_id.startswith("TA"):
            continue

        # Format technique to navigator format
        technique = {
            "techniqueID": mitre_id,
            "color": "#DCEDC8",
            "comment": "",
            "enabled": True,
            "metadata": [],
            "score": 1,
        }

        for value in mitre_map[mitre_id]:
            cast(List[Dict[str, str]], technique["metadata"]).append(
                {
                    "name": metadata_name,
                    "value": value,
                }
            )

        data["techniques"].append(technique)  # type: ignore

    return data
