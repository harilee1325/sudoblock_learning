# OpenRPC 1.3.2 Cheat Sheet

## 1. Purpose

Think of OpenRPC as airport signage for developers:

| Real-world | OpenRPC |
|------------|----------|
| Airport signs | JSON-RPC API documentation |
| International standards | OpenRPC specification |
| Clear navigation | Automated SDK generation |

## 2. Key Concepts

### 2.1 RFC 2119 Keywords
- **MUST**: Required (non-compliant if skipped)
- **SHOULD**: Strong recommendation
- **MAY**: Optional

### 2.2 Patterned Fields
- `^x-.*`: Custom fields starting with `x-`
- Example: `x-internal: true`

### 2.3 Format Rules
- **CamelCase** for all keys
- **JSON only** (no YAML/TOML)
- Single format for consistent tooling

## 3. Versioning

OpenRPC follows Semantic Versioning:

| Version | Description |
|---------|-------------|
| Major | Breaking changes |
| Minor | New features |
| Patch | Bug fixes |

## 4. Root Object Structure

```json
{
  "openrpc": "1.3.2",
  "info": {},
  "servers": [],
  "methods": [],
  "components": {}
}
```

## 5. Info Block

```json
{
  "title": "API Name",
  "description": "API description",
  "version": "x.y.z",
  "contact": {},
  "license": {}
}
```

## 6. Server Configuration

```json
{
  "name": "Server Name",
  "url": "http://example.com",
  "summary": "Brief description",
  "description": "Detailed description",
  "variables": {}
}
```

## 7. Method Definition

```json
{
  "name": "method_name",
  "summary": "Brief description",
  "paramStructure": "byPosition",
  "params": [],
  "result": {},
  "errors": [],
  "tags": [],
  "examples": []
}
```

## 8. Content Descriptor

```json
{
  "name": "parameter_name",
  "required": true,
  "schema": {
    "type": "string",
    "pattern": "regex_pattern",
    "description": "Parameter description"
  }
}
```

## 9. Schema Example

```json
{
  "type": "string",
  "pattern": "^0x[0-9a-fA-F]+$",
  "description": "Hex-encoded big-int"
}
```

## 10. Error Definition

```json
{
  "code": 1003,
  "message": "Error description"
}
```

## 11. Components

```json
{
  "schemas": {},
  "contentDescriptors": {},
  "examples": {},
  "errors": {},
  "tags": {}
}
```

## 12. Tags

```json
{
  "name": "tag_name",
  "summary": "Tag description"
}
```

## 13. Reference Object

```json
{
  "$ref": "#path/to/resource"
}
```

## 14. Specification Extensions

```json
{
  "x-custom-field": "value"
}
```

## 15. rpc.discover Method

```json
{
  "name": "rpc.discover",
  "params": [],
  "result": "openrpc.json"
}
```

## 16. Validation

```bash
openrpc-cli validate
```

## 17. Cheat Sheet Structure

```
ROOT
├── openrpc: "1.x.y"
├── info: title • version • description
├── servers[]: name • url • variables
├── methods[]:
│    ├── name (unique)
│    ├── paramStructure (byPosition|byName|either)
│    ├── params[] (ContentDescriptor)
│    ├── result (ContentDescriptor)
│    ├── errors[]
│    ├── examples[]
│    └── tags[]
└── components:
     ├── schemas{}
     ├── contentDescriptors{}
     ├── examples{}
     ├── errors{}
     └── tags{}
```

## 18. Best Practices

1. Draw root structure from memory
2. Write method objects without looking
3. Validate with CLI
4. Generate docs with playground
5. Practice with small specs
6. Repeat until mastery

## 19. Real-world Analogy

| Layer | Real-world | OpenRPC |
|-------|------------|---------|
| Meta-schema | Building code | Validates blueprint |
| openrpc.json | Blueprint | API documentation |
| Method | Arrow sign | API endpoint |
| ContentDescriptor | Sign text/icon | Parameter/return type |
| JSON-Schema | Font/colors | Data validation |

## 20. Final Tips

- Never commit unvalidated specs
- Use consistent naming conventions
- Document all custom fields
- Test with examples
- Keep it simple and maintainable