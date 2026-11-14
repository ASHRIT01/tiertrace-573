"""AL-1 amendment 2: environment record of the machine the extraction runs on (Mac reference or Kaggle). No model call.

  python scripts/al1_env.py OUT.json [--where "M2 Mac" | "Kaggle"]

Records: where, OS, machine, CPU/GPU model and driver (nvidia-smi when present; on macOS the hardware model and chip), power source on macOS,
Python version, installed package versions, Ollama server version and model digest, Ollama server environment variables that are set, and
the repo commit and tag."""
import json
import os
import platform
import subprocess
import sys
import time
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def sh(*a) -> str:
    try:
        return subprocess.run(a, capture_output=True, text=True, timeout=30).stdout.strip()
    except Exception as e:
        return f"unavailable: {type(e).__name__}"


def main(out: str, where: str):
    h = os.environ.get("OLLAMA_HOST", "127.0.0.1:11434")
    h = h if h.startswith("http") else f"http://{h}"
    try:
        ver = json.load(urllib.request.urlopen(f"{h}/api/version", timeout=10))["version"]
        tags = json.load(urllib.request.urlopen(f"{h}/api/tags", timeout=10))["models"]
        digest = next((t["digest"] for t in tags if t["name"] == "qwen3.5:4b-q4_K_M"), None)
    except Exception as e:
        ver, digest = f"unavailable: {e}", None
    from importlib import metadata
    E = {"where": where, "recorded_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
         "os": platform.platform(), "machine": platform.machine(), "python": sys.version.split()[0],
         "packages": sorted(f"{d.metadata['Name']}=={d.version}" for d in metadata.distributions()),
         "ollama_server_version": ver, "model": "qwen3.5:4b-q4_K_M", "model_digest": digest,
         "ollama_env": {k: v for k, v in os.environ.items() if k.startswith("OLLAMA_")},
         "repo_commit": sh("git", "-C", str(ROOT), "rev-parse", "HEAD"),
         "repo_describe": sh("git", "-C", str(ROOT), "describe", "--tags", "--always")}
    if sys.platform == "darwin":
        E["hardware_model"] = sh("sysctl", "-n", "hw.model")
        E["chip"] = sh("sysctl", "-n", "machdep.cpu.brand_string")
        E["memory_bytes"] = sh("sysctl", "-n", "hw.memsize")
        E["power"] = sh("pmset", "-g", "batt").splitlines()[0] if sh("pmset", "-g", "batt") else None
    smi = sh("nvidia-smi", "--query-gpu=index,name,driver_version,memory.total", "--format=csv,noheader")
    E["gpus"] = smi.splitlines() if smi and not smi.startswith("unavailable") else []
    E["cuda_visible_devices"] = os.environ.get("CUDA_VISIBLE_DEVICES")
    Path(out).write_text(json.dumps(E, indent=1) + "\n")
    print(f"env: where={where} os={E['os']} python={E['python']} ollama={ver} digest={(digest or '')[:12]} gpus={E['gpus']} commit={E['repo_commit'][:7]}")


if __name__ == "__main__":
    args = sys.argv[1:]
    where = args[args.index("--where") + 1] if "--where" in args else "unspecified"
    main(args[0], where)
