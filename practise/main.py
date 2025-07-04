#!/usr/bin/env python3
"""
JSON-RPC Learning Project
A simple example script for learning JSON-RPC concepts
"""

import json
import sys

def main():
    print("🚀 JSON-RPC Learning Project Started!")
    print(f"Python version: {sys.version}")
    print("Ready to explore JSON-RPC concepts!")
    
    # Example JSON-RPC request structure
    jsonrpc_request = {
        "jsonrpc": "2.0",
        "method": "eth_getBalance",
        "params": ["0x407d73d8a49eeb85d32cf465507dd71d507100c1", "latest"],
        "id": 1
    }
    
    print("\n📝 Example JSON-RPC Request:")
    print(json.dumps(jsonrpc_request, indent=2))

if __name__ == "__main__":
    main()
