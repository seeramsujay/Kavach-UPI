import os
import re
import xml.etree.ElementTree as ET
import pytest

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

def test_upi_target_registry_packages():
    upi_path = os.path.join(
        REPO_ROOT,
        "app/src/main/kotlin/com/kavach/upi/detection/UpiTargetRegistry.kt"
    )
    assert os.path.isfile(upi_path), "UpiTargetRegistry.kt not found"
    with open(upi_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Verify major Indian UPI targets are explicitly present
    assert "com.google.android.apps.nbu.paisa.user" in content  # Google Pay
    assert "com.phonepe.app" in content                        # PhonePe
    assert "net.one97.paytm" in content                        # Paytm
    assert "in.org.npci.upiapp" in content                     # BHIM
    assert "com.dreamplug.androidapp" in content               # CRED

def test_threat_signature_store_packages():
    threat_path = os.path.join(
        REPO_ROOT,
        "app/src/main/kotlin/com/kavach/upi/detection/ThreatSignatureStore.kt"
    )
    assert os.path.isfile(threat_path), "ThreatSignatureStore.kt not found"
    with open(threat_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Verify prominent remote screen-sharing tools are flagged
    assert "com.anydesk.anydeskandroid" in content
    assert "com.teamviewer.host.market" in content
    assert "com.splashtop.personal" in content
    assert "com.logmein.joinme" in content

def test_accessibility_service_config_xml():
    xml_path = os.path.join(
        REPO_ROOT,
        "app/src/main/res/xml/accessibility_service_config.xml"
    )
    assert os.path.isfile(xml_path), "accessibility_service_config.xml missing"
    tree = ET.parse(xml_path)
    root = tree.getroot()
    
    attribs = {k.split("}")[-1]: v for k, v in root.attrib.items()}
    assert attribs.get("canRetrieveWindowContent") == "true"
    assert "flagRetrieveInteractiveWindows" in attribs.get("accessibilityFlags", "")

def test_android_manifest_accessibility_permission():
    manifest_path = os.path.join(
        REPO_ROOT,
        "app/src/main/AndroidManifest.xml"
    )
    assert os.path.isfile(manifest_path), "AndroidManifest.xml missing"
    with open(manifest_path, "r", encoding="utf-8") as f:
        content = f.read()

    assert "android.permission.BIND_ACCESSIBILITY_SERVICE" in content
    assert "android.permission.SYSTEM_ALERT_WINDOW" in content
    assert ".service.KavachAccessibilityService" in content
