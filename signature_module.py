import ecdsa
# التعديل هنا: حذفنا استدعاء original_diploma لمنع خطأ الـ ImportError
from hashing_module import generate_sha256_hash 

def generate_ecc_keys():
    # Generate ECC private and public keys using NIST256p curve
    private_key = ecdsa.SigningKey.generate(curve=ecdsa.NIST256p)
    public_key = private_key.get_verifying_key()
    return private_key, public_key

def sign_document_hash(private_key, hash_hex):
    # Convert hex hash string to bytes
    hash_bytes = bytes.fromhex(hash_hex)
    
    # Sign the document hash
    signature = private_key.sign_digest(hash_bytes)
    
    # Return signature as hex
    return signature.hex()

def export_keys(private_key, public_key):
    # Convert keys to hex strings for easier storage/transfer
    priv_hex = private_key.to_string().hex()
    pub_hex = public_key.to_string().hex()
    return priv_hex, pub_hex

if __name__ == "__main__":
    print("--- 1. Key Management ---")
    priv_key, pub_key = generate_ecc_keys()
    priv_hex, pub_hex = export_keys(priv_key, pub_key)
    
    print(f"Private Key: {priv_hex[:40]}...") 
    print(f"Public Key: {pub_hex[:40]}...")
    
    print("\n--- 2. Digital Signature ---")
    
    # التعديل هنا لتجربة الملف بشكل مستقل دون الاعتماد على الملف الآخر:
    # قمنا بإنشاء قاموس محلي داخل الـ main الخاص بهذا الملف فقط للتجربة والتأكد من عمله
    test_diploma = {
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
    
    diploma_hash = generate_sha256_hash(test_diploma)
    print(f"Document Hash: {diploma_hash}")
    
    # Generate signature
    signature_hex = sign_document_hash(priv_key, diploma_hash)
    print(f"Signature: {signature_hex}")