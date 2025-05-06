import os
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from dotenv import load_dotenv
import logging

logger = logging.getLogger(__name__)


load_dotenv()

conf = ConnectionConfig(
    MAIL_USERNAME=os.getenv("MAIL_USERNAME"),
    MAIL_PASSWORD=os.getenv("MAIL_PASSWORD"),
    MAIL_FROM=os.getenv("MAIL_FROM"),
    MAIL_PORT=int(os.getenv("MAIL_PORT", "587")),
    MAIL_SERVER=os.getenv("MAIL_SERVER"),
    MAIL_STARTTLS = True,
    MAIL_SSL_TLS = False,
    USE_CREDENTIALS = True,
    VALIDATE_CERTS = True
)

async def send_verification_email(email: str, token: str):
    try:
        verification_url = f"{os.getenv('FRONTEND_URL', 'http://localhost:8000')}/api/v1/users/verify-email?token={token}"

        message = MessageSchema(
            subject="Verify your email for SoloForge",
            recipients=[email],
            body=f"""
            <html>
                <body>
                    <h1>Welcome to SoloForge!</h1>
                    <p>Please verify your email address by clicking the link below:</p>
                    <p>
                        <a href="{verification_url}">Verify Email</a>
                    </p>
                    <p>If you didn't request this verification, please ignore this email.</p>
                    <p>This link will expire in 24 hours.</p>
                </body>
            </html>
            """,
            subtype="html"
        )

        fm = FastMail(conf)
        await fm.send_message(message)

    except Exception as e:
        logger.error(f"Failed to send verification email: {e}")
        raise e 