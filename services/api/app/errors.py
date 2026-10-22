from fastapi import Request

MESSAGES = {
    "auth_required": ("Please sign in to continue.", "يرجى تسجيل الدخول للمتابعة."),
    "credentials": ("The email or password is incorrect.", "البريد الإلكتروني أو كلمة المرور غير صحيحة."),
    "email_exists": (
        "An account already uses this email. Try signing in.",
        "يوجد حساب بهذا البريد. جرّب تسجيل الدخول.",
    ),
    "validation": ("Please check the highlighted information.", "يرجى مراجعة المعلومات المحددة."),
    "consent_required": (
        "Please accept the service privacy notice.",
        "يرجى الموافقة على إشعار خصوصية الخدمة.",
    ),
    "csrf": (
        "Your session needs refreshing. Please reload and try again.",
        "يرجى تحديث الصفحة وإعادة المحاولة.",
    ),
    "origin": ("This request could not be verified.", "تعذّر التحقق من هذا الطلب."),
    "rate_limit": (
        "Too many attempts. Please try again in 15 minutes.",
        "محاولات كثيرة. يرجى المحاولة بعد ١٥ دقيقة.",
    ),
    "not_found": ("We couldn't find that item.", "لم نتمكن من العثور على هذا العنصر."),
    "food_unavailable": (
        "This food version is unavailable. Choose another source-backed item.",
        "هذا الإصدار الغذائي غير متاح. اختر عنصراً موثّق المصدر.",
    ),
    "idempotency_conflict": (
        "This save key belongs to another meal. Please start a new entry.",
        "مفتاح الحفظ مستخدم لوجبة أخرى. يرجى بدء تسجيل جديد.",
    ),
    "profile_conflict": (
        "Your profile changed in another window. Reload and try again.",
        "تم تعديل ملفك في نافذة أخرى. حدّث الصفحة وحاول مجدداً.",
    ),
    "allergy_status": (
        "Choose recorded allergies when adding an allergy.",
        "اختر «حساسية مسجّلة» عند إضافة مادة مسببة للحساسية.",
    ),
    "session_expired": (
        "Your session has expired. Please sign in again.",
        "انتهت جلستك. يرجى تسجيل الدخول مجدداً.",
    ),
    "service_unavailable": (
        "The service is temporarily unavailable. Please try again shortly.",
        "الخدمة غير متاحة مؤقتاً. يرجى المحاولة بعد قليل.",
    ),
    "internal": (
        "Something went wrong. Please retry using the reference shown.",
        "حدث خطأ. يرجى إعادة المحاولة باستخدام الرقم المرجعي الظاهر.",
    ),
}


def language(request: Request) -> str:
    return "ar" if request.headers.get("accept-language", "en").lower().startswith("ar") else "en"


class AppError(Exception):
    def __init__(self, code: str, status: int = 400):
        self.code = code
        self.status = status


def error_body(request: Request, code: str, fields: list | None = None):
    messages = MESSAGES.get(code, MESSAGES["internal"])
    result = {
        "code": code,
        "message": messages[language(request) == "ar"],
        "request_id": getattr(request.state, "request_id", ""),
    }
    if fields:
        result["fields"] = fields
    return {"error": result}
