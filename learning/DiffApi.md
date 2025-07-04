# Understanding API Differences in Ethereum Clients

This document explains the differences between Ethereum client APIs, focusing on standard and non-standard namespaces, and provides guidance for schema validation.

## Core Principle: Shared Standard

### Common Standard API
All major Execution Clients (Geth, Reth, Nethermind, Besu) comply with the official Ethereum JSON-RPC API specification:

| Namespace | Common Methods |
|-----------|----------------|
| `eth` | eth_getBalance, eth_call, eth_sendRawTransaction, etc. |
| `net` | net_version, net_listening, etc. |
| `web3` | web3_clientVersion, etc. |
| `engine` | Strict standard for Consensus Client communication |

### Core API Interoperability
- Standard methods work across all clients
- Ethers.js can switch between clients without code changes
- Shared standards enable client diversity

## Non-Standard API Differences

### 1. Debug Namespace

#### Purpose
- Node state inspection
- Transaction replay
- Debugging tools

#### Client-Specific Implementations

| Client | Key Features |
|--------|--------------|
| Geth | debug_traceTransaction (de-facto standard) |
| Reth | Geth-compatible debug methods |
| Nethermind | Extensive debugging tools |

### 2. Trace Namespace

#### Purpose
- Detailed transaction execution traces
- Transaction filtering
- Contract interaction analysis

#### Client-Specific Features

| Client | Key Features |
|--------|--------------|
| Geth/Erigon | trace_filter (transaction criteria) |
| Parity/Old Clients | Parity-style trace format |
| Reth | Compatibility with established standards |

### 3. TxPool Namespace

#### Purpose
- Transaction pool inspection
- Pending transaction management
- Queue management

#### Client-Specific Methods

| Client | Key Methods |
|--------|-------------|
| Geth | txpool_content, txpool_inspect |
| Reth/Nethermind | Similar functionality with minor differences |

### 4. Custom Administrative Namespaces

| Client | Custom Namespaces | Key Features |
|--------|-------------------|--------------|
| Nethermind | nethermind | Administrative tasks |
| Geth | admin, personal | Node management |

#### Security Note
- admin namespace: Manual peer connections, node info
- personal namespace: Account management (insecure on public endpoints)

## Schema Validation Checklist

### 1. Standard Namespaces
- eth, net, web3, engine
- Follow official public specification
- Client-agnostic schema

### 2. Non-Standard Namespaces
- debug, trace, txpool
- Client-specific implementations
- Detailed documentation required

### 3. Output Structure Focus
- JSON object nesting
- Field names
- Data formats
- 0x-prefixed hex vs decimal numbers

## Schema Organization

### Recommended Structure

```
openrpc.json          # Core standard methods
geth_debug.json       # Geth-specific debug methods
reth_debug.json       # Reth-specific debug methods
nethermind_admin.json # Nethermind-specific admin methods
```

## Key Takeaways for Schema Developers

1. **Core API Consistency**
   - Standard namespaces are consistent across clients
   - No need for client-specific handling

2. **Custom API Variability**
   - Debug, trace, and admin namespaces vary
   - Client-specific documentation essential

3. **Validation Focus**
   - Output structure differences
   - Parameter compatibility
   - Data format consistency

4. **Security Considerations**
   - Personal namespace handling
   - Public endpoint restrictions
   - Client-specific security features