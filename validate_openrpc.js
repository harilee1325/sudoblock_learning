#!/usr/bin/env node

const fs = require('fs');
const path = require('path');

// Simple OpenRPC validation without external dependencies
// This provides basic structural validation

// Get the file path from command line arguments
const filePath = process.argv[2];

if (!filePath) {
    console.error('Usage: node validate_openrpc.js <openrpc.json>');
    console.error('Example: node validate_openrpc.js openrpc.json');
    process.exit(1);
}

// Check if file exists
if (!fs.existsSync(filePath)) {
    console.error(`Error: File '${filePath}' not found.`);
    process.exit(1);
}

try {
    // Read and parse the OpenRPC document
    const fileContent = fs.readFileSync(filePath, 'utf8');
    const openrpcDoc = JSON.parse(fileContent);
    
    console.log('📄 Validating OpenRPC document:', path.basename(filePath));
    console.log('🔍 OpenRPC version:', openrpcDoc.openrpc || 'Not specified');
    console.log('📝 Title:', openrpcDoc.info?.title || 'Not specified');
    console.log('🔢 Methods count:', openrpcDoc.methods?.length || 0);
    
    // Basic validation checks
    const errors = [];
    
    // Check required fields
    if (!openrpcDoc.openrpc) {
        errors.push('Missing required field: openrpc');
    }
    
    if (!openrpcDoc.info) {
        errors.push('Missing required field: info');
    } else {
        if (!openrpcDoc.info.title) {
            errors.push('Missing required field: info.title');
        }
        if (!openrpcDoc.info.version) {
            errors.push('Missing required field: info.version');
        }
    }
    
    if (!openrpcDoc.methods) {
        errors.push('Missing required field: methods');
    } else if (!Array.isArray(openrpcDoc.methods)) {
        errors.push('Field "methods" must be an array');
    }
    
    // Validate methods
    if (openrpcDoc.methods && Array.isArray(openrpcDoc.methods)) {
        openrpcDoc.methods.forEach((method, index) => {
            if (!method.name) {
                errors.push(`Method ${index}: Missing required field "name"`);
            }
            if (!method.params) {
                errors.push(`Method ${index} (${method.name}): Missing required field "params"`);
            } else if (!Array.isArray(method.params)) {
                errors.push(`Method ${index} (${method.name}): Field "params" must be an array`);
            }
            if (!method.result) {
                errors.push(`Method ${index} (${method.name}): Missing required field "result"`);
            }
        });
    }
    
    if (errors.length === 0) {
        console.log('✅ OpenRPC document is valid!');
        console.log('🎉 All required fields are present and properly formatted.');
    } else {
        console.log('❌ OpenRPC document has validation errors:');
        errors.forEach(error => {
            console.log(`   • ${error}`);
        });
        process.exit(1);
    }
    
} catch (err) {
    if (err instanceof SyntaxError) {
        console.error('❌ Error: Invalid JSON format');
        console.error('   ', err.message);
    } else {
        console.error('❌ Error validating OpenRPC document:');
        console.error('   ', err.message);
    }
    process.exit(1);
}
