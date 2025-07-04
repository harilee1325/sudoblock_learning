# JSON-RPC Fundamentals

## Phase 1: The Foundation - Mastering JSON Schema Data Types

Before you can describe an API, you must be a master of describing data itself. OpenRPC uses JSON Schema for this. Here are the core types you'll use constantly, with a blockchain-specific focus.

### 1. string
This is your most versatile tool. But a simple `"type": "string"` is not enough. You must add constraints.

- `description`: ALWAYS include a clear, human-readable description. Example: "The keccak-256 hash of the transaction."
- `pattern`: A regular expression to enforce a format. This is CRITICAL for blockchains.
  - For a 32-byte hash (transaction hash, block hash): `"pattern": "^0x[a-fA-F0-9]{64}$"`
  - For an address: `"pattern": "^0x[a-fA-F0-9]{40}$"`
- `format`: Pre-defined formats for common types.
  - `"format": "uri"` for URLs
  - `"format": "email"` for email addresses
- `enum`: A fixed list of allowed string values.
  - Example: For a transaction status: `"enum": ["pending", "confirmed", "failed"]`

### 2. integer and number
Used for numerical values.

**CRITICAL CAVEAT**: JavaScript cannot safely handle integers larger than 2^53 - 1. Blockchain values like token balances or block numbers are often much larger.

**BEST PRACTICE**: For any large numerical value, represent it as a hexadecimal string in your schema. This is the Ethereum standard.

```json
{
  "type": "string",
  "pattern": "^0x[a-fA-F0-9]+$"
}
```

### 3. boolean
Simple true/false values.

Example: For the `net_listening` method, the result schema is just `"type": "boolean"`.

### 4. object
Used for complex, structured data. This is how you describe things like a full block or a transaction receipt.

```json
{
  "type": "object",
  "properties": {
    "hash": { "type": "string", "pattern": "^0x[a-fA-F0-9]{64}$" },
    "from": { "type": "string", "pattern": "^0x[a-fA-F0-9]{40}$" },
    "to": { "type": "string", "pattern": "^0x[a-fA-F0-9]{40}$" },
    "value": { "type": "string", "pattern": "^0x[a-fA-F0-9]+$" }
  },
  "required": ["hash", "from", "to"]
}
```

### 5. array
Used for lists of items.

```json
{
  "type": "object",
  "properties": {
    "blockNumber": { "type": "string", "pattern": "^0x[a-fA-F0-9]+$" },
    "transactions": {
      "type": "array",
      "items": {
        "type": "string",
        "pattern": "^0x[a-fA-F0-9]{64}$"
      }
    }
  }
}
```

## Phase 2: The Building Blocks - The Reusable OpenRPC Objects

Now we use the JSON Schema types to build the specific "LEGO bricks" of our OpenRPC document. Your job is to create these bricks and store them in the components section for reuse.

### ContentDescriptorObject
This describes a single piece of content, whether it's an input parameter or an output result.
- Fields: `name`, `summary`, `description`, `required`, `deprecated`, and most importantly, `schema` (which contains the JSON Schema from Phase 1).

### ErrorObject
A good API describes its failures as well as its successes.
- Fields: `code` (an integer), `message` (a string), and an optional `data` (any type, but you should define its schema!).
- Example: You might define a standard InvalidParameter error that your methods can return.

### ExampleObject & ExamplePairingObject
These are not for machines; they are for the humans who will use your API. They are your most powerful tool for making an API easy to learn.
- An ExampleObject contains a value that is a concrete example of a parameter or result.
- An ExamplePairingObject bundles example params with their expected result.

## Phase 3: The Assembly - A Practical Walkthrough

Let's imagine a new blockchain, "AquaChain," needs a schema. They have a custom method they need you to document: `aqua_getAssetDetails`.

### Your Process as a Schema Author

#### Step 1: Be a Detective (The Interview)
You can't write a schema without information. You must ask the developers of AquaChain the right questions:

- You: "What is the exact name of the method?"
  - Devs: "aqua_getAssetDetails"
- You: "What does it do?"
  - Devs: "It retrieves details for a specific asset on our chain."
- You: "What information do you need to find the asset?"
  - Devs: "We need the assetId, which is a 64-character hex string, and an optional boolean flag includeHistory to say if they want the transaction history."
- You: "What happens if includeHistory isn't provided?"
  - Devs: "It defaults to false."
- You: "What information do you return?"
  - Devs: "We return an object with the asset's ownerAddress, its name (string), and its creationBlock (hex number). If includeHistory was true, we also include a history field, which is an array of transaction hashes."
- You: "What can go wrong?"
  - Devs: "If the assetId doesn't exist, we return a specific error with code 4040 and message 'Asset not found'."

#### Step 2: Draft the Building Blocks (in components)

```json
{
  "components": {
    "schemas": {
      "AssetID": {
        "type": "string",
        "pattern": "^0x[a-fA-F0-9]{64}$",
        "description": "The unique 64-character hexadecimal identifier for an asset."
      },
      "Address": {
        "type": "string",
        "pattern": "^0x[a-fA-F0-9]{40}$",
        "description": "A standard 20-byte AquaChain address."
      },
      "TxHash": {
        "type": "string",
        "pattern": "^0x[a-fA-F0-9]{64}$"
      },
      "BlockNumber": {
        "type": "string",
        "pattern": "^0x[a-fA-F0-9]+$"
      },
      "AssetDetails": {
        "type": "object",
        "properties": {
          "ownerAddress": { "$ref": "#/components/schemas/Address" },
          "name": { "type": "string" },
          "creationBlock": { "$ref": "#/components/schemas/BlockNumber" },
          "history": {
            "type": "array",
            "items": { "$ref": "#/components/schemas/TxHash" }
          }
        },
        "required": ["ownerAddress", "name", "creationBlock"]
      }
    },
    "errors": {
      "AssetNotFound": {
        "code": 4040,
        "message": "Asset not found.",
        "data": { "type": "null" }
      }
    }
  }
}
```

#### Step 3: Assemble the MethodObject

```json
{
  "methods": [
    {
      "name": "aqua_getAssetDetails",
      "summary": "Retrieves detailed information about a specific AquaChain asset.",
      "paramStructure": "by-position",
      "params": [
        {
          "name": "assetId",
          "description": "The ID of the asset to query.",
          "required": true,
          "schema": { "$ref": "#/components/schemas/AssetID" }
        },
        {
          "name": "includeHistory",
          "description": "If true, the full transaction history of the asset is included.",
          "required": false,
          "schema": { "type": "boolean", "default": false }
        }
      ],
      "result": {
        "name": "assetDetails",
        "description": "An object containing the details of the requested asset.",
        "schema": { "$ref": "#/components/schemas/AssetDetails" }
      },
      "errors": [
        { "$ref": "#/components/errors/AssetNotFound" }
      ]
    }
  ]
}
```

#### Step 4: Add an ExamplePairingObject

```json
{
  "examples": [
    {
      "name": "SimpleAssetLookup",
      "summary": "A basic lookup without history.",
      "params": [
        {
          "name": "assetId",
          "value": "0x123...abc"
        },
        {
          "name": "includeHistory",
          "value": false
        }
      ],
      "result": {
        "name": "simpleAssetResult",
        "value": {
          "ownerAddress": "0xdef...456",
          "name": "My Cool Aqua Asset",
          "creationBlock": "0x123"
        }
      }
    }
  ]
}
```
