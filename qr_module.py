import json
import qrcode
from datetime import datetime

def generate_qr_code(payload):

    qr_data = {
        "document_id": "UQU-2026-001",
        "issue_timestamp": datetime.now().isoformat(),

        "diploma_data": payload["diploma_data"],

        "signature": payload["signature"],

        "university_public_key": payload["university_public_key"],

        "algorithm": payload["algorithm"]
    }

    json_data = json.dumps(
        qr_data,
        ensure_ascii=False,
        indent=2
    )

    qr = qrcode.make(json_data)

    qr.save("diploma_qr.png")

    print("\n==================================================")
    print(" QR CODE MODULE EXECUTED SUCCESSFULLY ")
    print("==================================================")
    print("QR image saved as diploma_qr.png")

    return qr_data 