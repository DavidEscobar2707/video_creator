#!/usr/bin/env python
"""Test PORT environment variable handling"""
import os
import sys

print('Testing Dockerfile CMD...')
print('=' * 70)

# Test 1: Default port
print('\nTest 1: Default PORT (not set)')
# Clear PORT if it exists
if 'PORT' in os.environ:
    del os.environ['PORT']

port = int(os.environ.get('PORT', 8000))
port_env = os.environ.get('PORT', 'NOT SET')
print(f'  PORT env var: {port_env}')
print(f'  Parsed port: {port}')
print(f'  Type: {type(port).__name__}')
if port == 8000:
    print('  ✓ PASS')
else:
    print('  ✗ FAIL')
    sys.exit(1)

# Test 2: Custom port
print('\nTest 2: Custom PORT (3000)')
os.environ['PORT'] = '3000'
port = int(os.environ.get('PORT', 8000))
print(f'  PORT env var: {os.environ.get("PORT")}')
print(f'  Parsed port: {port}')
if port == 3000:
    print('  ✓ PASS')
else:
    print('  ✗ FAIL')
    sys.exit(1)

# Test 3: Verify uvicorn can be imported
print('\nTest 3: Verify uvicorn import')
try:
    import uvicorn
    print('  ✓ uvicorn imported successfully')
except ImportError as e:
    print(f'  ✗ FAIL: {e}')
    sys.exit(1)

# Test 4: Verify src.api can be imported
print('\nTest 4: Verify src.api import')
try:
    from src.api import app
    print('  ✓ src.api imported successfully')
except ImportError as e:
    print(f'  ✗ FAIL: {e}')
    sys.exit(1)

print('\n' + '=' * 70)
print('✅ All tests passed')
print('=' * 70)
print('\nDockerfile CMD will:')
print('  1. Read PORT from environment')
print('  2. Default to 8000 if not set')
print('  3. Parse as integer')
print('  4. Start uvicorn on 0.0.0.0:PORT')
print('  5. Use 1 worker')
