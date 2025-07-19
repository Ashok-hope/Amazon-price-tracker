# Endpoint to send welcome email on login
from fastapi import Body
from fastapi import APIRouter, HTTPException, status, Depends, Body
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from models import UserCreate, UserLogin, User, PasswordReset, PasswordResetConfirm
from firebase_config import firebase_service
from email_service import send_welcome_email, send_otp_email
import secrets
from datetime import datetime, timedelta
from firebase_admin import auth as firebase_auth

# Ensure router is defined before any route decorators
router = APIRouter()
security = HTTPBearer()

# In-memory OTP storage (use Redis in production)
otp_storage = {}


# No signup/login endpoints: handled by Firebase Auth client SDK
@router.post("/send-login-email")
async def send_login_email(email: str = Body(...), name: str = Body("")):
    try:
        await send_welcome_email(email, name)
        return {"message": "Welcome email sent"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )



# @router.post("/forgot-password")
# async def forgot_password(reset_data: PasswordReset):
#     try:
#         # Use Firebase Auth to send password reset email
#         firebase_auth.send_password_reset_email(reset_data.email)
#         return {"message": "Password reset email sent"}
    
#     except Exception as e:
#         raise HTTPException(
#             status_code=status.HTTP_400_BAD_REQUEST,
#             detail=str(e)
#         )


# No reset-password endpoint needed: handled by Firebase Auth password reset link


async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    try:
        id_token = credentials.credentials
        decoded_token = firebase_auth.verify_id_token(id_token)
        uid = decoded_token["uid"]
        email = decoded_token.get("email")
        name = decoded_token.get("name", "")
        return {"uid": uid, "email": email, "name": name}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired Firebase ID token"
        )


@router.post("/send-tracking-email")
async def send_tracking_email(
    email: str = Body(...),
    name: str = Body(...),
    product_name: str = Body(...),
    current_price: float = Body(...),
    target_price: float = Body(...),
    image_url: str = Body(...),
    amazon_url: str = Body(...)
):
    from email_service import send_tracking_started_email
    try:
        await send_tracking_started_email(
            email, name, product_name, current_price, target_price, image_url, amazon_url
        )
        return {"message": "Tracking started email sent"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

