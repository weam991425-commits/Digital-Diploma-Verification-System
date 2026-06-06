import ecdsa
import json
# استيراد دوال التقييس والهاش لضمان تطابق العمليات الرياضية
from hashing_module import generate_sha256_hash

def verify_signature(public_key_hex, signature_hex, diploma_data):
    """
    المهمة الرابعة: دالة التحقق من التوقيع الرقمي للشهادة (Verification).
    تستقبل: المفتاح العام، التوقيع الرقمي، وبيانات الشهادة المقروءة.
    """
    try:
        # 1. إعادة التشفير (إعادة حساب الـ Hash لبيانات الشهادة المستلمة)
        computed_hash_hex = generate_sha256_hash(diploma_data)
        hash_bytes = bytes.fromhex(computed_hash_hex)
        
        # 2. تحويل المفتاح العام والتوقيع من صيغة الـ Hex إلى بايتات
        public_key_bytes = bytes.fromhex(public_key_hex)
        signature_bytes = bytes.fromhex(signature_hex)
        
        # استعادة كائن التحقق للمفتاح العام بناءً على المنحنى المتفق عليه NIST256p
        public_key = ecdsa.VerifyingKey.from_string(public_key_bytes, curve=ecdsa.NIST256p)
        
        # 3. المطابقة: التحقق مما إذا كان التوقيع يتطابق مع الـ Hash الجديد باستخدام المفتاح العام
        is_valid = public_key.verify_digest(signature_bytes, hash_bytes)
        return is_valid
        
    except ecdsa.BadSignatureError:
        # في حال حدوث أي تلاعب بالبيانات أو التوقيع، ستفشل المطابقة الرياضية
        return False
    except Exception as e:
        print(f"[-] Verification Error: {e}")
        return False

def run_testing_scenarios(qr_output_data):
    """
    إجراء سيناريوهات الاختبار المطلوبة (السيناريو السليم وسيناريو التلاعب).
    """
    print("\n==================================================")
    # استخراج البيانات المقروءة من كائن الـ QR المولد
    pub_key_hex = qr_output_data["university_public_key"]
    signature_hex = qr_output_data["signature"]
    authentic_data = qr_output_data["diploma_data"]

    # ------------------------------------------------------------------
    # 1. السيناريو السليم (Valid Scenario)
    # ------------------------------------------------------------------
    print("[+] Running Scenario 1: Valid Scenario (Authentic Diploma)")
    print(f"    - Verifying Diploma for Student: {authentic_data['student_name']}")
    print(f"    - Checked GPA: {authentic_data['gpa']}")
    
    # استدعاء دالة التحقق
    is_authentic_valid = verify_signature(pub_key_hex, signature_hex, authentic_data)
    
    if is_authentic_valid:
        print("    [RESULT] Verification SUCCESSFUL: Diploma is Authentic! ✓")
    else:
        print("    [RESULT] Verification FAILED: Valid document rejected! ✗")

    # ------------------------------------------------------------------
    # 2. سيناريو التلاعب (Tampered Scenario)
    # ------------------------------------------------------------------
    print("\n[+] Running Scenario 2: Tampered Scenario (Forgery Attempt)")
    
    # محاكاة شخص يحاول التلاعب بالبيانات النصية (تغيير الدرجة أو حرف في الاسم)
    tampered_data = authentic_data.copy()
    
    # التلاعب 1: تغيير المعدل GPA من 4.75 إلى 4.90 لغرض التزوير
    tampered_data["gpa"] = "4.90" 
    
    # التلاعب 2 (اختياري): تعديل بسيط جداً في الاسم
    # tampered_data["student_name"] = "Bayan Al-Zahrany"

    print(f"    - Attacker altered GPA to: {tampered_data['gpa']} (Original was 4.75)")
    print(f"    - Presenting same original signature: {signature_hex[:30]}...")
    
    # استدعاء دالة التحقق على البيانات المتلاعب بها
    is_tampered_valid = verify_signature(pub_key_hex, signature_hex, tampered_data)
    
    if is_tampered_valid:
        print("    [RESULT] Verification SUCCESSFUL: Forgery went undetected! ✗")
    else:
        print("    [RESULT] CRITICAL ALERT - Verification FAILED: Document has been tampered with! ✗")
        print("            Mathematical Proof: Recalculated Hash does not match the ECDSA signature.")
    print("==================================================")