"""
Factories for eth_* namespace — Pydantic v2 style
"""
from typing import Dict
from pydantic import Field
from models.method_object import MethodObject
from models.content_descriptor import ContentDescriptorObject, ReferenceObject
from models.schema_objects import SchemaObject
from models.example_objects import ExamplePairingObject, ExampleObject
from models.primitives import Address, Quantity

# ─── reusable schemas ────────────────────────────────────────────────────
block_number_schema = SchemaObject(
    title="BlockNumber",
    type="string",
    description="Hex block number",
    pattern=Quantity.pattern,
)
address_schema = SchemaObject(
    title="Address",
    type="string",
    description="20-byte address (hex)",
    pattern=Address.pattern,
)
wei_balance_schema = SchemaObject(
    title="WeiBalance",
    type="string",
    description="Wei (hex quantity)",
    pattern=Quantity.pattern,  # Same pattern as Quantity
)

SCHEMAS: Dict[str, dict] = {
    "BlockNumber": block_number_schema.model_dump(),
    "Address": address_schema.model_dump(),
    "WeiBalance": wei_balance_schema.model_dump(),
}

# ─── method builders ─────────────────────────────────────────────────────
def make_eth_blockNumber() -> MethodObject:
    return MethodObject(
        name="eth_blockNumber",
        summary="Current block number",
        description="Returns the most recent block number.",
        params=[],
        result=ContentDescriptorObject(
            name="blockNumber",
            description="Most recent block number.",
            schema_=ReferenceObject(ref="#/components/schemas/BlockNumber"),
        ),
        examples=[
            ExamplePairingObject(
                name="ethBlockNumberExample",
                params=[],
                result=ExampleObject(name="exampleBlockNumber", value="0x4b7"),
            )
        ],
    )


def make_eth_getBalance() -> MethodObject:
    return MethodObject(
        name="eth_getBalance",
        summary="Balance of an address",
        description="Returns the balance of the account of given address.",
        params=[
            ContentDescriptorObject(
                name="address",
                description="Address to check.",
                schema_=ReferenceObject(ref="#/components/schemas/Address"),
            ),
            ContentDescriptorObject(
                name="blockTag",
                description="Block number or tag.",
                schema_=ReferenceObject(ref="#/components/schemas/BlockNumber"),
            ),
        ],
        result=ContentDescriptorObject(
            name="balance",
            description="Balance in wei.",
            schema_=ReferenceObject(ref="#/components/schemas/WeiBalance"),
        ),
        examples=[
            ExamplePairingObject(
                name="ethGetBalanceExample",
                params=[
                    ExampleObject(
                        name="address",
                        value="0x407d73d8a49eeb85d32cf465507dd71d507100c1",
                    ),
                    ExampleObject(name="blockTag", value="latest"),
                ],
                result=ExampleObject(name="exampleBalance", value="0x0234c8a3397aab58"),
            )
        ],
    )


__all__ = [
    "make_eth_blockNumber",
    "make_eth_getBalance",
    "SCHEMAS",
]
