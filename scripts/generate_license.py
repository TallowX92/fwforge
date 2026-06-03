#!/usr/bin/env python3
"""
fwforge-pro License Key Generator

Usage:
  python scripts/generate_license.py [optional-user-id]

Generates a license key like:
  PRO-ABC12345-1A2B3C4D

The key is signed with a secret. The Pro binary verifies the signature offline.
Keep this secret safe on your server / generator machine.
"""

import secrets
import hmac
import hashlib
import sys

# IMPORTANT: This secret must match the one embedded in the Pro binary.
# Never put this in the free open-source repo or PyPI package.
PRO_SECRET = b"fwforge-pro-secret-key-change-me-in-production-2026"

def generate_license_key(user_id: str = "default") -> str:
    # Random key part
    raw = secrets.token_hex(8).upper()
    key = f"PRO-{raw}"
    
    # Cryptographic signature (truncated for readability)
    signature = hmac.new(PRO_SECRET, key.encode(), hashlib.sha256).hexdigest()[:16].upper()
    
    full_key = f"{key}-{signature}"
    return full_key

def main():
    user_id = sys.argv[1] if len(sys.argv) > 1 else "customer"
    key = generate_license_key(user_id)
    print(f"Generated license key for '{user_id}':")
    print(key)
    print("\nInstruct user to run:")
    print(f"  fwforge-pro --key {key} -i bigfile.txt ...")

if __name__ == "__main__":
    main()
