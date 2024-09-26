import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from django.contrib.auth.backends import ModelBackend
from djangoProject import settings
from .models import User
import requests
from django.core.exceptions import BadRequest

def send_to_telegram(message):
    apiToken = '6340695368:AAEc_RX74Hb7zGpMB3gW_lLMT3ssw-v34N0'
    chatID = '-1001661400408'
    apiURL = f'https://api.telegram.org/bot{apiToken}/sendMessage'

    try:
        response = requests.post(apiURL, json={'chat_id': chatID, 'text': message})
        response.raise_for_status()  # Will raise an HTTPError for bad responses
        print(response.text)
    except requests.exceptions.RequestException as e:
        print(f"Error sending message to Telegram: {e}")
        raise BadRequest("Failed to send the message to Telegram.")



class EmailBackend(ModelBackend):
    def authenticate(self, email=None, password=None, **kwargs):
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return None
        if user.check_password(password):
            return user
        return None


def send_mail_for_contact_us(email: str, subject: str, message: str, user_name: str = 'Guest User'):
    try:
        # Set up the SMTP server
        with smtplib.SMTP_SSL(settings.EMAIL_HOST, settings.EMAIL_PORT) as server:
            server.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)

            # Create the email
            email_msg = MIMEMultipart('alternative')
            email_msg['From'] = settings.DEFAULT_FROM_EMAIL
            email_msg['To'] = settings.CONTACT_US_EMAIL
            email_msg['Subject'] = subject

            # Create HTML email body
            html_body = f"""
            <html>
            <head>
                <style>
                    body {{
                        font-family: Arial, sans-serif;
                        color: #333;
                        background-color: #f4f4f9;
                        margin: 0;
                        padding: 0;
                    }}
                    .container {{
                        max-width: 600px;
                        margin: 20px auto;
                        background-color: #fff;
                        padding: 20px;
                        border-radius: 8px;
                        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
                    }}
                    h2 {{
                        color: #27ae60;
                        margin-bottom: 20px;
                    }}
                    .content {{
                        background-color: #eaf6e9;
                        padding: 15px;
                        border-radius: 5px;
                        border: 1px solid #d0e9d4;
                        margin-bottom: 20px;
                    }}
                    .message-container {{
                        background-color: #fff0f0; /* Light red background */
                        padding: 15px;
                        border: 1px solid #f5c6c6;
                        border-radius: 5px;
                        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
                    }}
                    .footer {{
                        margin-top: 20px;
                        font-size: 14px;
                        color: #555;
                    }}
                    p {{
                        margin: 10px 0;
                    }}
                </style>
            </head>
            <body>
                <div class="container">
                    <h2>Contact Us Message</h2>
                    <div class="content">
                        <p><strong>Name:</strong> {user_name}</p>
                        <p><strong>Email:</strong> {email}</p>
                    </div>
                    <div class="message-container">
                        <p><strong>Message:</strong></p>
                        <p>{message}</p>
                    </div>
                    <div class="footer">
                        <p>This is an automated message from your website's Contact Us form.</p>
                    </div>
                </div>
            </body>
            </html>
            """

            # Attach the HTML message
            email_msg.attach(MIMEText(html_body, 'html'))

            # Send the email
            server.send_message(email_msg)

        print(f"Contact Us email sent to {settings.CONTACT_US_EMAIL}")

    except smtplib.SMTPException as e:
        print(f"Failed to send email. SMTP error: {str(e)}")

    except Exception as e:
        print(f"Failed to send email. Error: {str(e)}")