from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from email.message import EmailMessage
import random
import aiosmtplib

app = FastAPI()

# Allow frontend requests (CORS)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

class FormData(BaseModel):
    name: str
    phone: str
    roll: str
    email: str
    mcq: str

@app.post("/submit")
async def submit_form(data: FormData):
    otp = str(random.randint(100000, 999999))

    subject = "Form Submission Confirmation + OTP"
    body = f"""
    Hello {data.name},

    Thank you for submitting the form. Here are your details:

    - Name: {data.name}
    - Phone: {data.phone}
    - Roll No: {data.roll}
    - Email: {data.email}
    - MCQ Answer: {data.mcq}

    Your OTP is: {otp}

    Regards,
    FastAPI Team
    """

    message = EmailMessage()
    message["From"] = "testmsc1234@gmail.com"
    message["To"] = data.email
    message["Subject"] = subject
    message.set_content(body)

    try:
        await aiosmtplib.send(
            message,
            hostname="smtp.gmail.com",
            port=587,
            start_tls=True,
            username="testmsc1234@gmail.com",
            password="yjhigaknzouuoyof"
        )
        return {"message": "Details submitted and email sent!"}
    except Exception as e:
        return {"error": f"Failed to send email: {e}"}
