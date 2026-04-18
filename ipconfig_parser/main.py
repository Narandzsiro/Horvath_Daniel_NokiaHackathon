import json
import re
from pathlib import Path

def sanitize_key(raw_key):
    clean = raw_key.replace(".", "").strip().lower()
    mapping = {
        "description": "description", "leírás": "description",
        "physical address": "physical_address", "fizikai cím": "physical_address",
        "dhcp enabled": "dhcp_enabled", "dhcp-engedélyezve": "dhcp_enabled",
        "ipv4 address": "ipv4_address", "ipv4-cím": "ipv4_address",
        "autoconfiguration ipv4 address": "ipv4_address",
        "subnet mask": "subnet_mask", "almask": "subnet_mask",
        "default gateway": "default_gateway", "alapértelmezett átjáró": "default_gateway",
        "dns servers": "dns_servers", "névkiszolgálók": "dns_servers"
    }
    for k, v in mapping.items():
        if k in clean: return v
    return None

def clean_value(key, value):
    if "address" in key or "gateway" in key or "mask" in key:
        return re.sub(r"\(.*?\)", "", value).strip()
    return value.strip()

def parse_network_config(file_path):
    CLEAN_RE = re.compile(r"\s*\(.*?\)\s*")
    file_report = {"file_name": file_path.name, "adapters": []}
    
    content = ""
    for encoding in ['utf-16', 'utf-8', 'latin-1']:
        try:
            content = file_path.read_text(encoding=encoding)
            if '\u0000' not in content:
                break
        except:
            continue

    current_adapter = None
    last_key = None
    required_keys = ["description", "physical_address", "dhcp_enabled", "ipv4_address", "subnet_mask", "default_gateway", "dns_servers"]

    for line in content.splitlines():
        clean_line = line.rstrip()
        stripped = clean_line.strip()
        
        if not stripped or "Windows IP Configuration" in stripped:
            continue

        if not line.startswith(" ") and "adapter" in stripped.lower():
            if current_adapter:
                file_report["adapters"].append(current_adapter)
            
            current_adapter = {k: ("" if k != "dns_servers" else []) for k in required_keys}
            current_adapter["adapter_name"] = stripped.split(":")[0].strip()
            last_key = None
            continue

        if current_adapter and ":" in stripped:
            parts = stripped.split(":", 1)
            key = sanitize_key(parts[0])
            value = CLEAN_RE.sub("", parts[1]).strip()

            if key:
                if key == "dns_servers":
                    if value: current_adapter[key].append(value)
                else:
                    current_adapter[key] = value
                last_key = key
            else:
                last_key = None
        
        elif current_adapter and last_key and line.startswith(" "):
            val = stripped
            if last_key == "dns_servers":
                current_adapter[last_key].append(val)
            elif last_key == "default_gateway":
                if current_adapter[last_key]: current_adapter[last_key] += ", "
                current_adapter[last_key] += val

    if current_adapter:
        file_report["adapters"].append(current_adapter)

    return file_report

def main():
    final_output = []
    for file_path in Path(".").glob("*.txt"):
        if file_path.name == "adapters_config.json": continue
        final_output.append(parse_network_config(file_path))

    with open("adapters_config.json", "w", encoding="utf-8") as f:
        json.dump(final_output, f, indent=2, ensure_ascii=False)

    print(json.dumps(final_output, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()