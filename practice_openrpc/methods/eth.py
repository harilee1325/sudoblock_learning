"""
Factory functions that create MethodObject instances for the eth_* namespace.
"""

from models.method_object import MethodObject
from models.content_descriptor import ContentDescriptorObject, ReferenceObject
from models.schema_objects import SchemaObject
from models.example_objects import ExamplePairingObject, ExampleObject

# ─────────────────────────── reusable schemas ────────────────────────────
block_number_schema = SchemaObject(
    title="BlockNumber",
    type="string",
    description="Block number in hex quantity format.",
    pattern=r"^0x[0-9a-fA-F]+$"
)

address_schema = SchemaObject(
    title="Address",
    type="string",
    description="20-byte address (0x-prefixed)",
    pattern=r"^0x[0-9a-fA-F]{40}$"
)

wei_balance_schema = SchemaObject(
    title="WeiBalance",
    type="string",
    description="Balance in wei (hex quantity).",
    pattern=r"^0x[0-9a-fA-F]+$"
)

# collect them once so the builder can import a single dict
SCHEMAS: dict[str, dict] = {
    "BlockNumber": block_number_schema.model_dump(by_alias=True, exclude_none=True),
    "Address":     address_schema.model_dump(by_alias=True, exclude_none=True),
    "WeiBalance":  wei_balance_schema.model_dump(by_alias=True, exclude_none=True),
}

# ───────────────────────────── method builders ───────────────────────────
def make_eth_blockNumber() -> MethodObject:
    return MethodObject(
        name="eth_blockNumber",
        summary="Get the current block number",
        description="Returns the number of the most recent block.",
        params=[],
        result=ContentDescriptorObject(
            name="blockNumber",
            description="Most recent block number.",
            schema_=ReferenceObject(**{"$ref": "#/components/schemas/BlockNumber"})
        ),
        examples=[
            ExamplePairingObject(
                name="ethBlockNumberExample",
                params=[],
                result=ExampleObject(
                    name="exampleBlockNumber",
                    value="0x4b7"
                )
            )
        ]
    )


def make_eth_getBalance() -> MethodObject:
    return MethodObject(
        name="eth_getBalance",
        summary="Get the balance of an account",
        description="Returns the balance of the account of given address.",
        params=[
            ContentDescriptorObject(
                name="address",
                description="Address to check.",
                schema_=ReferenceObject(**{"$ref": "#/components/schemas/Address"})
            ),
            ContentDescriptorObject(
                name="blockTag",
                description="Block number or tag.",
                schema_=ReferenceObject(**{"$ref": "#/components/schemas/BlockNumber"})
            )
        ],
        result=ContentDescriptorObject(
            name="balance",
            description="Balance in wei.",
            schema_=ReferenceObject(**{"$ref": "#/components/schemas/WeiBalance"})
        ),
        examples=[
            ExamplePairingObject(
                name="ethGetBalanceExample",
                params=[
                    ExampleObject(name="address",
                                  value="0x407d73d8a49eeb85d32cf465507dd71d507100c1"),
                    ExampleObject(name="blockTag", value="latest")
                ],
                result=ExampleObject(
                    name="exampleBalance",
                    value="0x0234c8a3397aab58"
                )
            )
        ]
    )


__all__ = [
    "make_eth_blockNumber",
    "make_eth_getBalance",
    "SCHEMAS",
]
