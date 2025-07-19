
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from typing import Optional

# Email configuration
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS", "iamthefreakingbot")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD", "vowd xlva emrf tavl")

class EmailService:
    def __init__(self):
        self.smtp_server = SMTP_SERVER
        self.smtp_port = SMTP_PORT
        self.email = EMAIL_ADDRESS
        self.password = EMAIL_PASSWORD
    
    def send_email(self, to_email: str, subject: str, html_content: str):
        """Send HTML email"""
        try:
            msg = MIMEMultipart('alternative')
            msg['From'] = self.email
            msg['To'] = to_email
            msg['Subject'] = subject
            
            html_part = MIMEText(html_content, 'html')
            msg.attach(html_part)
            
            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.starttls()
            server.login(self.email, self.password)
            server.send_message(msg)
            server.quit()
            
            return True
        except Exception as e:
            print(f"Error sending email: {e}")
            return False

email_service = EmailService()

async def send_welcome_email(user_email: str, user_name: str):
    """Send welcome email to new user"""
    subject = "Welcome to Amazon Price Tracker! 🎉"
    
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 0; padding: 20px; background-color: #f5f5f5; }}
            .container {{ max-width: 600px; margin: 0 auto; background-color: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
            .header {{ text-align: center; color: #ff6b35; margin-bottom: 30px; }}
            .content {{ line-height: 1.6; color: #333; }}
            .button {{ display: inline-block; background-color: #ff6b35; color: white; padding: 12px 30px; text-decoration: none; border-radius: 5px; margin: 20px 0; }}
            .footer {{ margin-top: 30px; padding-top: 20px; border-top: 1px solid #eee; color: #666; font-size: 12px; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>Welcome to Amazon Price Tracker!</h1>
            </div>
            <div class="content">
                <h2>Hello {user_name}! 👋</h2>
                <p>Thank you for joining Amazon Price Tracker! We're excited to help you save money on your favorite products.</p>
                
                <h3>What you can do:</h3>
                <ul>
                    <li>🔍 Track prices of any Amazon India product</li>
                    <li>📧 Get instant email alerts when prices drop</li>
                    <li>💰 Set your target price and let us do the monitoring</li>
                    <li>📊 View your savings and tracking history</li>
                </ul>
                
                <p>Start by adding your first product to track!</p>
                
                <a href="http://localhost:5173" class="button">Start Tracking Now</a>
            </div>
            <div class="footer">
                <p>Happy saving!<br>Amazon Price Tracker Team</p>
            </div>
        </div>
    </body>
    </html>
    """
    
    return email_service.send_email(user_email, subject, html_content)

async def send_otp_email(user_email: str, otp: str):
    """Send OTP for password reset"""
    subject = "Password Reset OTP - Amazon Price Tracker"
    
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 0; padding: 20px; background-color: #f5f5f5; }}
            .container {{ max-width: 600px; margin: 0 auto; background-color: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
            .header {{ text-align: center; color: #ff6b35; margin-bottom: 30px; }}
            .otp {{ font-size: 32px; font-weight: bold; color: #ff6b35; text-align: center; background-color: #f9f9f9; padding: 20px; border-radius: 10px; margin: 20px 0; }}
            .content {{ line-height: 1.6; color: #333; }}
            .warning {{ background-color: #fff3cd; border: 1px solid #ffeaa7; color: #856404; padding: 15px; border-radius: 5px; margin: 20px 0; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>Password Reset Request</h1>
            </div>
            <div class="content">
                <p>You requested to reset your password. Use the OTP below to proceed:</p>
                
                <div class="otp">{otp}</div>
                
                <div class="warning">
                    <strong>⚠️ Important:</strong><br>
                    • This OTP is valid for 10 minutes only<br>
                    • Don't share this OTP with anyone<br>
                    • If you didn't request this, please ignore this email
                </div>
            </div>
        </div>
    </body>
    </html>
    """
    
    return email_service.send_email(user_email, subject, html_content)

async def send_price_alert_email(
    user_email: str, 
    user_name: str, 
    product_name: str, 
    current_price: float, 
    target_price: float, 
    lowest_price: float, 
    image_url: str, 
    amazon_url: str
):
    """Send price drop alert email"""
    subject = f"🔥 Price Drop Alert! {product_name[:50]}..."
    
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 0; padding: 20px; background-color: #f5f5f5; }}
            .container {{ max-width: 600px; margin: 0 auto; background-color: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
            .header {{ text-align: center; color: #ff6b35; margin-bottom: 30px; }}
            .product {{ border: 1px solid #ddd; border-radius: 10px; padding: 20px; margin: 20px 0; }}
            .product-image {{ text-align: center; margin-bottom: 15px; }}
            .product-image img {{ max-width: 200px; height: auto; border-radius: 5px; }}
            .price-info {{ background-color: #f9f9f9; padding: 15px; border-radius: 8px; margin: 15px 0; }}
            .current-price {{ font-size: 24px; font-weight: bold; color: #ff6b35; }}
            .target-price {{ color: #28a745; }}
            .lowest-price {{ color: #007bff; }}
            .buy-button {{ display: inline-block; background-color: #ff6b35; color: white; padding: 15px 30px; text-decoration: none; border-radius: 5px; margin: 20px 0; font-weight: bold; font-size: 16px; }}
            .alert {{ background-color: #d4edda; border: 1px solid #c3e6cb; color: #155724; padding: 15px; border-radius: 5px; margin: 20px 0; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🔥 Price Drop Alert!</h1>
            </div>
            
            <p>Hello {user_name}!</p>
            
            <div class="alert">
                <strong>Great news!</strong> The price of your tracked product has dropped to your target range!
            </div>
            
            <div class="product">
                <div class="product-image">
                    <img src="{image_url}" alt="Product Image" />
                </div>
                
                <h2>{product_name}</h2>
                
                <div class="price-info">
                    <div class="current-price">Current Price: ₹{current_price:,.2f}</div>
                    <div class="target-price">Your Target: ₹{target_price:,.2f}</div>
                    <div class="lowest-price">Lowest Price: ₹{lowest_price:,.2f}</div>
                </div>
                
                <div style="text-align: center;">
                    <a href="{amazon_url}" class="buy-button">Buy Now on Amazon</a>
                </div>
            </div>
            
            <p>Don't wait too long - prices can change anytime!</p>
            
            <div style="margin-top: 30px; padding-top: 20px; border-top: 1px solid #eee; color: #666; font-size: 12px;">
                <p>Happy shopping!<br>Amazon Price Tracker Team</p>
            </div>
        </div>
    </body>
    </html>
    """
    
    return email_service.send_email(user_email, subject, html_content)

async def send_thank_you_email(user_email: str, user_name: str, product_name: str):
    """Send thank you email after successful price alert"""
    subject = "Thank you for using Amazon Price Tracker! 🙏"
    
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 0; padding: 20px; background-color: #f5f5f5; }}
            .container {{ max-width: 600px; margin: 0 auto; background-color: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
            .header {{ text-align: center; color: #ff6b35; margin-bottom: 30px; }}
            .content {{ line-height: 1.6; color: #333; }}
            .button {{ display: inline-block; background-color: #ff6b35; color: white; padding: 12px 30px; text-decoration: none; border-radius: 5px; margin: 20px 0; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>Thank You! 🙏</h1>
            </div>
            <div class="content">
                <h2>Hello {user_name}!</h2>
                <p>We hope you were able to grab the deal for <strong>{product_name}</strong>!</p>
                
                <p>We've removed this product from your tracking list since it reached your target price.</p>
                
                <h3>Continue saving with us:</h3>
                <ul>
                    <li>🔍 Add more products to track</li>
                    <li>💰 Discover new deals and savings</li>
                    <li>📱 Share with friends and family</li>
                </ul>
                
                <a href="http://localhost:5173" class="button">Track More Products</a>
                
                <p>Thank you for choosing Amazon Price Tracker!</p>
            </div>
        </div>
    </body>
    </html>
    """
    
    return email_service.send_email(user_email, subject, html_content)

async def send_weekly_reminder_email(user_email: str, user_name: str):
    """Send weekly reminder to visit the site"""
    subject = "Your Weekly Price Update 📊"
    
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 0; padding: 20px; background-color: #f5f5f5; }}
            .container {{ max-width: 600px; margin: 0 auto; background-color: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
            .header {{ text-align: center; color: #ff6b35; margin-bottom: 30px; }}
            .content {{ line-height: 1.6; color: #333; }}
            .button {{ display: inline-block; background-color: #ff6b35; color: white; padding: 12px 30px; text-decoration: none; border-radius: 5px; margin: 20px 0; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>Weekly Price Update 📊</h1>
            </div>
            <div class="content">
                <h2>Hello {user_name}!</h2>
                <p>We've been busy monitoring your tracked products this week!</p>
                
                <p>Check your dashboard to see:</p>
                <ul>
                    <li>📉 Latest price updates</li>
                    <li>💰 Potential savings</li>
                    <li>🎯 Products approaching your target price</li>
                </ul>
                
                <a href="http://localhost:5173/cart" class="button">View My Dashboard</a>
                
                <p>Don't miss out on great deals - check your tracking status!</p>
            </div>
        </div>
    </body>
    </html>
    """
    
    return email_service.send_email(user_email, subject, html_content)

async def send_tracking_started_email(user_email: str, user_name: str, product_name: str, current_price: float, target_price: float, image_url: str, amazon_url: str):
    subject = f"🔔 Now Tracking: {product_name[:50]}..."
    user_name = user_name.title()
    html_content = f"""
    <!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <title>Price Tracker Alert</title>
</head>
<body style="font-family: 'Segoe UI', sans-serif; background-color: #f9fafb; margin: 0; padding: 0;">

  <div style="max-width: 600px; background-color: #ffffff; margin: 30px auto; padding: 25px; border-radius: 16px; box-shadow: 0 6px 18px rgba(0, 0, 0, 0.05);">

    <div style="text-align: center; margin-bottom: 20px;">
      <h2 style="color: #111827; margin: 0;">Hello {user_name},</h2>
      <p style="color: #6b7280; margin-top: 8px;">We’re now tracking your product:</p>
    </div>

    <div style="text-align: center;">
      <img src="{image_url}" alt="Product Image" style="max-width: 100%; border-radius: 10px; margin-bottom: 20px;" />
    </div>

    <div style="background-color: #f3f4f6; padding: 16px; border-radius: 12px; text-align: center; margin-bottom: 20px;">
      <p style="font-size: 16px; margin: 6px 0;"><strong>{product_name}</strong></p>
      <p style="color: #2563eb; font-size: 20px; font-weight: bold; margin: 6px 0;">Current Price: ₹{current_price:,.2f}</p>
      <p style="color: #059669; font-size: 20px; font-weight: bold; margin: 6px 0;">Your Target Price: ₹{target_price:,.2f}</p>
    </div>

    <div style="text-align: center; margin-top: 20px;">
      <a href="{amazon_url}" style="display: inline-block; background-color: #f97316; color: #ffffff; text-decoration: none; padding: 12px 24px; border-radius: 8px; font-weight: 600; font-size: 16px;">View on Amazon</a>
    </div>

    <div style="text-align: center; font-size: 13px; color: #9ca3af; margin-top: 25px;">
      You’ll get an email as soon as the price drops to your target.<br>
      Real-time tracking | 3x Daily Updates
    </div>

  </div>

</body>
</html>

    """
    return email_service.send_email(user_email, subject, html_content)
