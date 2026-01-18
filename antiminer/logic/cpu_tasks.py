import hashlib

import json
import os
import re
def heavy_computation(data: str) -> str:
    """Example CPU-bound task: stateless, pickle-safe, top-level."""
    # Simulate heavy work
    result = data
    for _ in range(100000):
        result = hashlib.sha256(result.encode()).hexdigest()
    return result


def analyze_file_content(file_path: str, mode: str = "Full Scan") -> dict:
    """Analyze file content for threats using THREAT_DB and advanced techniques."""
    # Load threat database
    db_path = os.path.join(os.path.dirname(__file__), "..", "threat_db.json")
    with open(db_path, "r", encoding="utf-8") as f:
        db = json.load(f)
    
    threat_db = db.get("THREAT_DB", {})
    found_threats = []

    try:
        with open(file_path, "rb") as f:
            content_bytes = f.read()
            content = content_bytes.decode('utf-8', errors='ignore')
    except Exception:
        return None

    # 1. Pattern Matching
    for threat_id, info in threat_db.items():
        patterns = info.get("patterns", [])
        for pattern in patterns:
            if re.search(pattern, content, re.IGNORECASE):
                found_threats.append({
                    "id": threat_id,
                    "name": info.get("name"),
                    "mechanism": info.get("mechanism"),
                    "mitigation": info.get("mitigation"),
                    "level": info.get("threat_level")
                })
                break

    # 2. Deep Analysis / Evasive Techniques
    if mode == "Deep Analysis":
        # Check for evasive techniques (simplified from scratch_7.py)
        evasive = []
        if b"UPX" in content_bytes: evasive.append("UPX Packer")
        if b"IsDebuggerPresent" in content_bytes: evasive.append("Anti-Debug")
        
        if evasive:
            found_threats.append({
                "id": "evasive_tech",
                "name": "Evasive Techniques Detected",
                "mechanism": f"Detected: {', '.join(evasive)}",
                "mitigation": "Perform manual memory analysis",
                "level": 6
            })

        # Check for chat patterns
        chat_patterns = db.get("CHAT_PATTERNS", [])
        for pattern in chat_patterns:
            if re.search(pattern, content, re.IGNORECASE):
                found_threats.append({
                    "id": "chat_integration",
                    "name": "Внедренный чат/API",
                    "mechanism": "Обнаружены паттерны интеграции с внешними мессенджерами",
                    "mitigation": "Проверить легитимность сетевой активности",
                    "level": 5
                })
                break

    if found_threats:
        return max(found_threats, key=lambda x: x["level"])
    
    return None
