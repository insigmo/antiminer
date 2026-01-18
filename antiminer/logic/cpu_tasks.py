import hashlib
import time

def heavy_computation(data: str) -> str:
    """Example CPU-bound task: stateless, pickle-safe, top-level."""
    # Simulate heavy work
    result = data
    for _ in range(100000):
        result = hashlib.sha256(result.encode()).hexdigest()
    return result

def analyze_file_content(content: str) -> bool:
    """Simulate file analysis for threats."""
    time.sleep(0.1) # Simulate processing
    return "miner" in content.lower() or "malware" in content.lower()
