import json
from models.info_object import InfoObject
from models.openrpc_object import OpenRPCObject

# import each namespace module *once*
from methods import eth

# ───────────────────────────── collect methods ───────────────────────────
methods = [
    eth.make_eth_blockNumber(),
    eth.make_eth_getBalance(),
    # add more here as you create them
]

# ─────────────────────────── collect all schemas ─────────────────────────
schema_registry: dict[str, dict] = {}
schema_registry.update(eth.SCHEMAS)     # pull in everything from eth.py
# when you add methods/net.py, you’d call:  schema_registry.update(net.SCHEMAS)

# ───────────────────────── build the OpenRPC root ────────────────────────
openrpc_doc = OpenRPCObject(
    info=InfoObject(title="My Practice Ethereum API", version="1.0.0"),
    methods=methods,
    components={"schemas": schema_registry}
)

# ────────────────────────── pretty-print / save  ─────────────────────────
print(json.dumps(
    openrpc_doc.model_dump(by_alias=True, exclude_none=True),
    indent=2
))
# If you want a file:  Path("openrpc.json").write_text(…)
