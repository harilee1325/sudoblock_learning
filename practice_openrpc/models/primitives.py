from pydantic import constr

# Re-usable regex-validated scalars
Address = constr(pattern=r'^0x[0-9a-fA-F]{40}$')
Quantity = constr(pattern=r'^0x(0|[1-9a-fA-F][0-9a-fA-F]*)$')
DataHex  = constr(pattern=r'^0x([0-9a-fA-F]{2})*$')
    