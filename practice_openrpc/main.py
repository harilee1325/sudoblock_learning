import json
import sys
from pathlib import Path
from typing import Dict, Any

from models.info_object import InfoObject
from models.openrpc_object import OpenRPCObject

# Import each namespace module *once*
from methods import eth


def validate_openrpc(spec: Dict[str, Any]) -> bool:
    """Basic OpenRPC validation."""
    required_fields = {
        'openrpc': str,
        'info': dict,
        'methods': list,
    }
    
    # Check required top-level fields
    for field, field_type in required_fields.items():
        if field not in spec:
            print(f"❌ Missing required field: {field}", file=sys.stderr)
            return False
        if not isinstance(spec[field], field_type):
            print(f"❌ Invalid type for {field}: expected {field_type.__name__}, got {type(spec[field]).__name__}", file=sys.stderr)
            return False
    
    # Check required info fields
    required_info = {'title', 'version'}
    if not all(field in spec['info'] for field in required_info):
        print(f"❌ Missing required info fields: {required_info - spec['info'].keys()}", file=sys.stderr)
        return False
    
    # Check methods structure
    for i, method in enumerate(spec['methods']):
        if not isinstance(method, dict):
            print(f"❌ Method at index {i} is not an object", file=sys.stderr)
            return False
        if 'name' not in method:
            print(f"❌ Method at index {i} is missing 'name' field", file=sys.stderr)
            return False
    
    print("✅ OpenRPC specification is valid!")
    return True


def main():
    # ──────────────────────────── collect methods ───────────────────────────
    methods = [
        eth.make_eth_blockNumber(),
        eth.make_eth_getBalance(),
        # Add more here as you create them
    ]

    # ───────────────────────── collect all schemas ─────────────────────────
    schema_registry: Dict[str, dict] = {}
    schema_registry.update(eth.SCHEMAS)  # Pull in everything from eth.py
    # When you add methods/net.py, you'd call:  schema_registry.update(net.SCHEMAS)

    # ─────────────────────── build the OpenRPC root ────────────────────────
    openrpc_doc = OpenRPCObject(
        info=InfoObject(title="My Practice Ethereum API", version="1.0.0"),
        methods=methods,
        components={"schemas": schema_registry}
    )
    
    # Convert to dict and validate
    spec = openrpc_doc.model_dump(by_alias=True, exclude_none=True)
    
    # Validate the specification
    if not validate_openrpc(spec):
        print("❌ Validation failed. Not saving invalid specification.", file=sys.stderr)
        sys.exit(1)
    
    # Pretty-print to console
    print(json.dumps(spec, indent=2))
    
    # Save to file
    output_path = Path("openrpc.json")
    output_path.write_text(json.dumps(spec, indent=2))
    print(f"\n✅ OpenRPC specification saved to {output_path.absolute()}")


if __name__ == "__main__":
    main()
