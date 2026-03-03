from flask import Flask, request, jsonify
import smtplib
from email.message import EmailMessage
import base64
import os
import re
app = Flask(__name__)


SENDER_EMAIL = os.getenv("SENDER_EMAIL") # Get sender email from environment variable
APP_PASSWORD = os.getenv("EMAIL_PASS")   # Get app password from environment variable

if not SENDER_EMAIL or not APP_PASSWORD:
    raise ValueError("Environment variables not set")

@app.route("/send-mail", methods=["POST"])
def send_mail():

    data = request.json                           # Get JSON data from the request
    
    receiver_email = data.get("receiver_email")   # Get receiver email from the data
    message = data.get("otp")                     # Get message from the data
    

    if not receiver_email or not message:
        return jsonify({"error": "Missing data"}), 400
    # Create Email
    msg = EmailMessage()
    msg["Subject"] = "Verificaton OTP for JSRN Bank"
    msg["From"] = SENDER_EMAIL
    msg["To"] = receiver_email
    # msg.set_content(message)                      # Plain text content (optional)
   
    msg.add_alternative(f"""
<!DOCTYPE html>
<html>
  <body style="margin:0;padding:0;font-family:Arial,Helvetica,sans-serif;background-color:#f4f6f9;">
    
    <table width="100%" cellpadding="0" cellspacing="0" style="background-color:#f4f6f9;padding:30px 0;">
      <tr>
        <td align="center">
          
          <table width="500" cellpadding="0" cellspacing="0" 
                 style="background-color:#ffffff;border-radius:8px;padding:30px;
                        box-shadow:0 4px 12px rgba(0,0,0,0.08);">
            
            <!-- Logo -->
            <tr>
              <td align="center" style="padding-bottom:20px;">
                <img src="https://res.cloudinary.com/dvevvrpvk/image/upload/v1772506894/jsr_muijfd.png" 
                     alt="JSRN Bank Logo"
                     width="140"
                     style="display:block;"><h1>JSRN Bank</h1>
              </td>
            </tr>

            <!-- Greeting -->
            <tr>
              <td style="font-size:15px;color:#333333;padding-bottom:15px;">
                Dear Customer,
              </td>
            </tr>

            <!-- Message -->
            <tr>
              <td style="font-size:15px;color:#333333;padding-bottom:20px;">
                Your One-Time Password (OTP) for verification is:
              </td>
            </tr>

            <!-- OTP Box -->
            <tr>
              <td align="center" style="padding:20px 0;">
                <div style="
                    display:inline-block;
                    padding:15px 25px;
                    font-size:28px;
                    letter-spacing:6px;
                    font-weight:bold;
                    color:#e63946;
                    background-color:#f1f5ff;
                    border-radius:6px;">
                  {message}
                </div>
              </td>
            </tr>

            <!-- Validity -->
            <tr>
              <td style="font-size:14px;color:#555555;padding-bottom:15px;">
                This OTP is valid for <strong>5 minutes</strong>. 
                Please do not share this code with anyone.
              </td>
            </tr>

            <!-- Footer -->
            <tr>
              <td style="font-size:12px;color:#888888;padding-top:20px;border-top:1px solid #eeeeee;">
                © 2026 JSRN Bank. All rights reserved.<br>
                This is an automated email. Please do not reply.
              </td>
            </tr>

          </table>
          
        </td>
      </tr>
    </table>

  </body>
</html>
""", subtype="html")                             # HTML email content with OTP
    # Send Email
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(SENDER_EMAIL, APP_PASSWORD)
        smtp.send_message(msg)

    return jsonify({
    "status_code": "200",
    "message": f"OTP sent successfully to {receiver_email}"
}), 200


if __name__ == "__main__":

    # app.run(host="0.0.0.0", port=5000)    # Run the Flask app on port 5000
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
