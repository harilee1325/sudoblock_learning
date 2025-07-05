from typing import ClassVar

class _EthereumType:
    pattern: ClassVar[str]

class Address(_EthereumType):
    pattern = r"^0x[0-9a-fA-F]{40}$"

class Quantity(_EthereumType):
    pattern = r"^0x(0|[1-9a-fA-F][0-9a-fA-F]*)$"

class DataHex(_EthereumType):
    pattern = r"^0x([0-9a-fA-F]{2})*$"
