import hashlib
import json

def normalize_diploma_data(diploma_data):
    """
    Converts diploma fields into a consistent JSON format.
    This ensures that the same diploma data always produces the same hash.
    """
    return json.dumps(
        diploma_data,
        sort_keys=True,
        ensure_ascii=False,
        separators=(",", ":")
    )

def generate_sha256_hash(diploma_data):
    """
    Generates a SHA-256 hash from the normalized diploma data.
    """
    normalized_data = normalize_diploma_data(diploma_data)
    encoded_data = normalized_data.encode("utf-8")
    return hashlib.sha256(encoded_data).hexdigest()

def compare_hashes(original_hash, new_hash):
    """
    Compares the original hash with the new hash.
    If they are different, this means the diploma data was changed.
    """
    return original_hash == new_hash

if __name__ == "__main__":

    original_diploma = {
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

    original_hash = generate_sha256_hash(original_diploma)

    print("===== ORIGINAL DIPLOMA =====")
    print(normalize_diploma_data(original_diploma))
    print("\nOriginal SHA-256 Hash:")
    print(original_hash)

    tampered_diploma = original_diploma.copy()
    tampered_diploma["gpa"] = "4.70"

    tampered_hash = generate_sha256_hash(tampered_diploma)

    print("\n===== TAMPERED DIPLOMA =====")
    print(normalize_diploma_data(tampered_diploma))
    print("\nTampered SHA-256 Hash:")
    print(tampered_hash)

    print("\n===== VERIFICATION RESULT =====")
    if compare_hashes(original_hash, tampered_hash):
        print("Valid: No tampering detected.")
    else:
        print("Invalid: Tampering detected. The diploma data was modified.")