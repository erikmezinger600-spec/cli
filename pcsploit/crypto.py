"""
PCSploit Encryption Module
AES-256-GCM encryption for all C2 traffic.
GCM mode provides both confidentiality (secrecy) and
authenticity (nobody tampered with the data).
"""

import os       # For generating random numbers (used in encryption)
import base64   # For encoding binary data as text (so it travels safely)

# Try to import the cryptography library
# If it's not installed, we'll use a fallback
try:
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM
    HAS_CRYPTO = True
except ImportError:
    HAS_CRYPTO = False
    import hashlib  # Fallback for basic XOR obfuscation


class PCSploitCrypto:
    """
    Handles encryption and decryption for PCSploit.
    
    Uses AES-256-GCM — the gold standard for symmetric encryption.
    - AES = Advanced Encryption Standard
    - 256 = 256-bit key (brute-forcing this would take billions of years)
    - GCM = Galois/Counter Mode (includes integrity checking)
    """
    
    # AES-256 requires a 32-byte (256-bit) key
    KEY_SIZE = 32
    
    # GCM mode uses a 12-byte nonce (a unique number used once)
    NONCE_SIZE = 12
    
    def __init__(self, key=None):
        """
        Initialize the crypto handler.
        
        Args:
            key: A 32-byte AES-
