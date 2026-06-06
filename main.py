import json
from hashing_module import generate_sha256_hash
from signature_module import generate_ecc_keys, sign_document_hash, export_keys
from qr_module import generate_qr_code
from verification_module import run_testing_scenarios

def main():
    # Student data
    diploma_data = {
        "student_name": "Bayan Al-Zahrani",
        "student_id": "443005277",
        "university": "Umm Al-Qura University",
        "college": "College of Computing",
        "department": "Cybersecurity",
        "degree": "Bachelor of Cybersecurity",
        "gpa": "4.75",
        "graduation_year": "2026",
        "issue_date": "2026-06-09"
    }
    
    print("=== Step 1: Key Management ===")
    private_key, public_key = generate_ecc_keys()
    priv_hex, pub_hex = export_keys(private_key, public_key)
    print("University ECC keys generated successfully.")
    
    print("\n=== Step 2: Hashing and Digital Signature ===")
    diploma_hash = generate_sha256_hash(diploma_data)
    signature_hex = sign_document_hash(private_key, diploma_hash)
    print(f"Generated Hash: {diploma_hash}")
    print(f"Generated Signature: {signature_hex[:50]}...")
    
    print("\n=== Step 3: Packaging and QR Code Generation ===")
    payload = {
        "diploma_data": diploma_data,
        "signature": signature_hex,
        "university_public_key": pub_hex,
        "algorithm": "ECDSA-NIST256-SHA256"
    }
    
    qr_output = generate_qr_code(payload)
    
    print("\n=== Step 4: Verification and System Evaluation ===")
    run_testing_scenarios(qr_output)

if __name__ == "__main__":
    main()
