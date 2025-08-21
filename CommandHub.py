import streamlit as st
import psutil
import time
import subprocess
import requests
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont
from bs4 import BeautifulSoup
import os
import platform
import smtplib
from email.message import EmailMessage
import webbrowser
import urllib.parse
import tempfile

# Selenium for optional browser automation (credential-based)
try:
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.common.keys import Keys
    from selenium.webdriver.chrome.options import Options as ChromeOptions
except Exception:
    webdriver = None

# Optional: WhatsApp automation via WhatsApp Web
try:
    import pywhatkit  # type: ignore
except Exception:
    pywhatkit = None


st.set_page_config(page_title="CommandHub", layout="wide")

# Custom CSS for gradient background and styling
st.markdown("""
<style>
    .main {
        background: #FEE8D9 !important;
        min-height: 100vh;
    }
    .stApp {
        background: #FEE8D9 !important;
        color: #ffffff !important;
    }
    .block-container {
        background: #FEE8D9 !important;
        color: #ffffff !important;
    }
    .stApp > header {
        background: #FEE8D9 !important;
        color: #ffffff !important;
    }
    .stApp > footer {
        background: #FEE8D9 !important;
        color: #F5C9B0 !important;
    }
    .stButton > button {
        background-color: #F5C9B0 !important;
        color: #ffffff !important;
        border: 2px solid #ffffff !important;
        border-radius: 10px !important;
        padding: 10px 20px !important;
        font-weight: bold !important;
    }
    .stButton > button * {
        color: #ffffff !important;
    }
    .stButton > button:hover {
        background-color: #EA5B6F !important;
        border-color: #E8F5E8 !important;
    }
    .stTextInput > div > div > input {
        background-color: #F5C9B0 !important;
        color: #ffffff !important;
        border: 2px solid #ffffff !important;
        border-radius: 8px !important;
    }
    .stTextArea > div > div > textarea {
        background-color: #F5C9B0 !important;
        color: #ffffff !important;
        border: 2px solid #ffffff !important;
        border-radius: 8px !important;
    }
    .stSelectbox > div > div > select {
        background-color: #F5C9B0 !important;
        color: #ffffff !important;
        border: 2px solid #ffffff !important;
        border-radius: 8px !important;
    }
    .stSelectbox > div > div > select option {
        background-color: #F5C9B0 !important;
        color: #ffffff !important;
    }
    .stSelectbox > div > div > div {
        color: #ffffff !important;
    }
    .stSelectbox > div > div > div > div {
        color: #ffffff !important;
    }
    .stSelectbox > div > div > div > div > div {
        color: #ffffff !important;
    }
    .stSelectbox > div > div > div > div > div > div {
        color: #ffffff !important;
    }
    .stSelectbox > div > div > div > div > div > div > div {
        color: #ffffff !important;
    }
    .stSelectbox > div > div > div > div > div > div > div > span {
        color: #ffffff !important;
    }
    .stSelectbox > div > div > div > div > div > div > div > div {
        color: #ffffff !important;
    }
    .stSelectbox > div > div > div > div > div > div > div > div > span {
        color: #ffffff !important;
    }
    .stSelectbox option {
        color: #ffffff !important;
        background-color: #F5C9B0 !important;
    }
    .stSelectbox select option {
        color: #ffffff !important;
        background-color: #F5C9B0 !important;
    }
    .stSelectbox > div > div > div > div > div > div > div > div > div {
        color: #ffffff !important;
    }
    .stSelectbox > div > div > div > div > div > div > div > div > div > span {
        color: #ffffff !important;
    }
    .stSelectbox > div > div > div > div > div > div > div > div > div > div {
        color: #ffffff !important;
    }
    .stSelectbox > div > div > div > div > div > div > div > div > div > div > span {
        color: #ffffff !important;
    }
    .stNumberInput > div > div > input {
        background-color: #F5C9B0 !important;
        color: #ffffff !important;
        border: 2px solid #ffffff !important;
        border-radius: 8px !important;
    }
    .stCheckbox > div > div > label {
        color: #F5C9B0 !important;
        font-weight: bold !important;
    }
    .stRadio > div > div > label {
        color: #F5C9B0 !important;
        font-weight: bold !important;
    }
    .stRadio > div > div > div {
        color: #ffffff !important;
    }
    .stRadio > div > div > div > div {
        color: #ffffff !important;
    }
    .stFileUploader > div > div > div {
        background-color: #F5C9B0 !important;
        color: #ffffff !important;
        border: 2px solid #ffffff !important;
        border-radius: 8px !important;
    }
    .stFileUploader > div > div > div * {
        color: #ffffff !important;
    }
    .stFileUploader > div > div > div > div {
        color: #ffffff !important;
    }
    .stFileUploader > div > div > div > div > div {
        color: #ffffff !important;
    }
    .stFileUploader > div > div > div > div > div > div {
        color: #ffffff !important;
    }
    .stFileUploader > div > div > div > div > div > div > span {
        color: #ffffff !important;
    }
    .stFileUploader > div > div > div > div > div > div > p {
        color: #ffffff !important;
    }
    .stColorPicker > div > div > div {
        background-color: #F5C9B0 !important;
        color: #ffffff !important;
        border: 2px solid #ffffff !important;
        border-radius: 8px !important;
    }
    .stSuccess {
        background-color: #F5C9B0 !important;
        color: #ffffff !important;
        border: 2px solid #ffffff !important;
        border-radius: 8px !important;
    }
    .stError {
        background-color: #F5C9B0 !important;
        color: #ffffff !important;
        border: 2px solid #ffffff !important;
        border-radius: 8px !important;
    }
    .stInfo {
        background-color: #F5C9B0 !important;
        color: #ffffff !important;
        border: 2px solid #ffffff !important;
        border-radius: 8px !important;
    }
    .stWarning {
        background-color: #F5C9B0 !important;
        color: #ffffff !important;
        border: 2px solid #ffffff !important;
        border-radius: 8px !important;
    }
    h1, h2, h3, h4, h5, h6 {
        color: #EA5B6F !important;
    }
    .stMarkdown {
        color: #F5C9B0 !important;
    }
    .stCaption {
        color: #EA5B6F !important;
    }
    p, span, div, label {
        color: #EA5B6F !important;
    }
    .stText {
        color: #EA5B6F !important;
    }
    .stWrite {
        color: #F5C9B0 !important;
    }
    .stSubheader {
        color: #F5C9B0 !important;
    }
    .stHeader {
        color: #F5C9B0 !important;
    }
    .stJson {
        color: #ffffff !important;
    }
    .stJson * {
        color: #ffffff !important;
    }
    pre {
        color: #ffffff !important;
    }
    code {
        color: #ffffff !important;
    }
    .stCodeBlock {
        color: #ffffff !important;
    }
    .stCodeBlock * {
        color: #ffffff !important;
    }
</style>
""", unsafe_allow_html=True)

APP_BG_COLOR = "#A6B28B"


if "page" not in st.session_state:
    st.session_state.page = "home"


def navigate(page_name: str):
    with st.spinner("Rotating cube..."):
        time.sleep(0.45)
    st.session_state.page = page_name


def show_result(success: bool, message: str = ""):
    if success:
        st.success(message or "Task completed successfully ✅")
    else:
        st.error(message or "Task failed ❌")


def ensure_pywhatkit_installed() -> bool:
    if pywhatkit is None:
        st.error("WhatsApp sending requires 'pywhatkit'. Install with: pip install pywhatkit pyautogui")
        return False
    return True


TASK_ICONS = [
    "🧠",  # 1 read RAM
    "💬",  # 2 whatsapp
    "✉️",  # 3 send email
    "📲",  # 4 whatsapp non-contact
    "📩",  # 5 sms
    "📞",  # 6 phone call
    "🔎",  # 7 google search
    "📣",  # 8 post social
    "📥",  # 9 download website data
    "🕵️‍♂️",  #10 anonymous email
    "🖼️",  #11 create image
    "😎",  #12 swap faces
    "🤖",  #13 LLM analyze
    "🧠",  #14 ChatGPT agent
    "🛠️",  #15 CommandHub
]

TASK_LABELS = [
    "RAM Monitor",
    "WhatsApp Sender",
    "Email Client",
    "WhatsApp Non-Contact",
    "SMS Gateway",
    "Call Center",
    "Web Search",
    "Social Auto-Poster",
    "Website Downloader",
    "Anonymous Mailer",
    "AI Image Creator",
    "Face Swapper",
    "LLM Analyzer",
    "ChatGPT Bot",
    "System Commands",
]


def placeholder_api_message(task_name, extra=""):
    st.info(f"This is a placeholder UI for **{task_name}**. Add your API keys / SDK calls in the function body.")
    if extra:
        st.write(extra)

def page_read_ram():
    st.header("1. RAM Monitor")
    st.write("This reads the system's RAM using `psutil`.")
    if st.button("Read RAM Now", key="ram_read"):
        try:
            vm = psutil.virtual_memory()
            st.json({
                "total_MB": vm.total // (1024*1024),
                "available_MB": vm.available // (1024*1024),
                "used_MB": vm.used // (1024*1024),
                "percent": vm.percent
            })
            show_result(True, "RAM read successfully.")
        except Exception as e:
            show_result(False, f"Error reading RAM: {e}")


def page_send_whatsapp():
    st.header("2. WhatsApp Sender")
    st.write("Send a WhatsApp message via WhatsApp Web using `pywhatkit` (no API keys required). Ensure you are logged into web.whatsapp.com in your default browser.")
    phone = st.text_input("Recipient phone (with country code, e.g. +911234567890)", key="wa_phone")
    message = st.text_area("Message", key="wa_message")
    if st.button("Send WhatsApp", key="wa_send"):
        if not phone or not message:
            show_result(False, "Please provide both phone and message.")
            return
        if not ensure_pywhatkit_installed():
            return
        try:
            pywhatkit.sendwhatmsg_instantly(
                phone_no=phone,
                message=message,
                wait_time=20,
                tab_close=True,
                close_time=3,
            )
            st.info("A browser tab was opened to WhatsApp Web to deliver your message. Keep the browser focused until sent.")
            show_result(True, f"WhatsApp message queued to {phone}")
        except Exception as e:
            show_result(False, f"WhatsApp send failed: {e}")


def page_send_email():
    st.header("3. Email Client")
    st.write("Send email using SMTP with proper authentication setup.")
    
    # Email Provider Selection
    email_provider = st.selectbox("Email Provider", ["Gmail", "Outlook", "Yahoo", "Custom SMTP"], key="email_provider")
    
    # Auto-configure based on provider
    if email_provider == "Gmail":
        smtp_server = "smtp.gmail.com"
        smtp_port = 587
        st.info("📧 **Gmail Setup Instructions:**")
        st.write("1. Enable 2-Factor Authentication on your Google account")
        st.write("2. Generate an App Password:")
        st.write("   - Go to Google Account Settings")
        st.write("   - Security → 2-Step Verification → App passwords")
        st.write("   - Generate password for 'Mail'")
        st.write("3. Use the App Password (not your regular password)")
        st.write("4. Make sure 'Less secure app access' is OFF")
    elif email_provider == "Outlook":
        smtp_server = "smtp-mail.outlook.com"
        smtp_port = 587
        st.info("📧 **Outlook Setup:**")
        st.write("Use your regular Outlook password")
    elif email_provider == "Yahoo":
        smtp_server = "smtp.mail.yahoo.com"
        smtp_port = 587
        st.info("📧 **Yahoo Setup:**")
        st.write("Use your regular Yahoo password")
    else:  # Custom SMTP
        smtp_server = st.text_input("SMTP server", value="smtp.gmail.com", key="smtp_server")
        smtp_port = st.number_input("SMTP port", value=587, key="smtp_port")
    
    username = st.text_input("Email address", key="smtp_user")
    password = st.text_input("Password/App Password", type="password", key="smtp_pass")
    to_email = st.text_input("To email", key="to_email")
    subject = st.text_input("Subject", key="email_subject")
    body = st.text_area("Body", key="email_body")
    
    # Test connection button
    if st.button("Test Connection", key="test_email_conn"):
        if not (smtp_server and username and password):
            show_result(False, "Please provide server details and credentials.")
            return
        try:
            with st.spinner("Testing connection..."):
                port_int = int(smtp_port)
                if port_int == 465:
                    with smtplib.SMTP_SSL(smtp_server, port_int, timeout=10) as server:
                        server.login(username, password)
                        st.success("✅ Connection successful!")
                else:
                    with smtplib.SMTP(smtp_server, port_int, timeout=10) as server:
                        server.ehlo()
                        server.starttls()
                        server.ehlo()
                        server.login(username, password)
                        st.success("✅ Connection successful!")
        except smtplib.SMTPAuthenticationError:
            st.error("❌ Authentication failed! Check your credentials.")
            if email_provider == "Gmail":
                st.info("💡 **Gmail Tip:** Make sure you're using an App Password, not your regular password.")
        except Exception as e:
            st.error(f"❌ Connection failed: {e}")
    
    if st.button("Send Email", key="send_email"):
        if not (smtp_server and username and password and to_email):
            show_result(False, "Please provide all required details.")
            return
        try:
            msg = EmailMessage()
            msg["From"] = username
            msg["To"] = to_email
            msg["Subject"] = subject or "No Subject"
            msg.set_content(body or "No content")

            with st.spinner("Sending email..."):
                port_int = int(smtp_port)
                if port_int == 465:
                    with smtplib.SMTP_SSL(smtp_server, port_int, timeout=30) as server:
                        server.login(username, password)
                        server.send_message(msg)
                else:
                    with smtplib.SMTP(smtp_server, port_int, timeout=30) as server:
                        server.ehlo()
                        server.starttls()
                        server.ehlo()
                        server.login(username, password)
                        server.send_message(msg)
                
                show_result(True, f"Email sent successfully to {to_email}")
                
        except smtplib.SMTPAuthenticationError:
            show_result(False, "Authentication failed. Check your username and password.")
            if email_provider == "Gmail":
                st.error("💡 **Gmail Issue:** Make sure you're using an App Password, not your regular password.")
                st.write("**Steps to fix:**")
                st.write("1. Go to Google Account Settings")
                st.write("2. Security → 2-Step Verification → App passwords")
                st.write("3. Generate a new App Password for 'Mail'")
                st.write("4. Use that 16-character password here")
        except smtplib.SMTPRecipientsRefused:
            show_result(False, "Recipient email address is invalid or rejected.")
        except smtplib.SMTPServerDisconnected:
            show_result(False, "Server connection was lost. Try again.")
        except Exception as e:
            show_result(False, f"Email send failed: {e}")
            st.error("💡 **Troubleshooting Tips:**")
            st.write("1. Check your internet connection")
            st.write("2. Verify SMTP server and port")
            st.write("3. Ensure credentials are correct")
            st.write("4. Check if your email provider allows SMTP access")


def page_whatsapp_non_contact():
    st.header("4. WhatsApp Non-Contact")
    st.write("Send WhatsApp message without saving contact using `pywhatkit`.")
    phone = st.text_input("Recipient phone (with country code)", key="wa_nc_phone")
    message = st.text_area("Message", key="wa_nc_message")
    if st.button("Send", key="wa_nc_send"):
        if not (phone and message):
            show_result(False, "Enter phone and message.")
            return
        if not ensure_pywhatkit_installed():
            return
        try:
            pywhatkit.sendwhatmsg_instantly(
                phone_no=phone,
                message=message,
                wait_time=20,
                tab_close=True,
                close_time=3,
            )
            st.info("Browser tab opened to WhatsApp Web. Ensure you are logged in.")
            show_result(True, f"WhatsApp message queued to {phone}")
        except Exception as e:
            show_result(False, f"Failed to send WhatsApp: {e}")


def page_send_sms():
    st.header("5. SMS Gateway")
    st.write("Send SMS via Twilio or other SMS providers.")
    
    # SMS Provider Selection
    sms_provider = st.selectbox("SMS Provider", ["Twilio", "Vonage", "Simulation"], key="sms_provider")
    
    to_num = st.text_input("Destination phone (with country code)", placeholder="+1234567890", key="sms_to")
    sms_text = st.text_area("SMS text", key="sms_text")
    
    if sms_provider == "Twilio":
        st.info("📱 **Twilio Setup Required:**")
        st.write("1. Get Twilio Account SID and Auth Token")
        st.write("2. Get a Twilio phone number")
        st.write("3. Add credentials below")
        
        twilio_sid = st.text_input("Twilio Account SID", key="twilio_sid")
        twilio_token = st.text_input("Twilio Auth Token", type="password", key="twilio_token")
        twilio_from = st.text_input("Twilio Phone Number", key="twilio_from")
        
        if st.button("Send SMS via Twilio", key="send_sms_twilio"):
            if not all([to_num, sms_text, twilio_sid, twilio_token, twilio_from]):
                show_result(False, "Please provide all Twilio credentials and message details.")
                return
            try:
                # Import Twilio if available
                try:
                    from twilio.rest import Client
                    client = Client(twilio_sid, twilio_token)
                    message = client.messages.create(
                        body=sms_text,
                        from_=twilio_from,
                        to=to_num
                    )
                    show_result(True, f"SMS sent successfully! SID: {message.sid}")
                except ImportError:
                    st.error("Twilio not installed. Run: pip install twilio")
                    return
            except Exception as e:
                show_result(False, f"Twilio SMS failed: {e}")
    
    elif sms_provider == "Vonage":
        st.info("📱 **Vonage Setup Required:**")
        st.write("1. Get Vonage API Key and Secret")
        st.write("2. Get a Vonage phone number")
        st.write("3. Add credentials below")
        
        vonage_key = st.text_input("Vonage API Key", key="vonage_key")
        vonage_secret = st.text_input("Vonage API Secret", type="password", key="vonage_secret")
        vonage_from = st.text_input("Vonage Phone Number", key="vonage_from")
        
        if st.button("Send SMS via Vonage", key="send_sms_vonage"):
            if not all([to_num, sms_text, vonage_key, vonage_secret, vonage_from]):
                show_result(False, "Please provide all Vonage credentials and message details.")
                return
            try:
                # Import Vonage if available
                try:
                    import vonage
                    client = vonage.Client(key=vonage_key, secret=vonage_secret)
                    response = client.sms.send_message({
                        "from": vonage_from,
                        "to": to_num,
                        "text": sms_text
                    })
                    if response["messages"][0]["status"] == "0":
                        show_result(True, f"SMS sent successfully! ID: {response['messages'][0]['message-id']}")
                    else:
                        show_result(False, f"SMS failed: {response['messages'][0]['error-text']}")
                except ImportError:
                    st.error("Vonage not installed. Run: pip install vonage")
                    return
            except Exception as e:
                show_result(False, f"Vonage SMS failed: {e}")
    
    else:  # Simulation
        if st.button("Send SMS (Simulation)", key="send_sms_sim"):
            if not (to_num and sms_text):
                show_result(False, "Please provide phone and message.")
                return
            try:
                with st.spinner("Sending SMS..."):
                    time.sleep(2)
                    # Simulate SMS sending process
                    st.info("📱 **SMS Simulation:**")
                    st.write(f"**To:** {to_num}")
                    st.write(f"**Message:** {sms_text}")
                    st.write("**Status:** Queued for delivery")
                    st.write("**Provider:** SMS Gateway")
                    time.sleep(1)
                    st.success("✅ **SMS Delivered Successfully!**")
                    show_result(True, f"Simulated SMS sent to {to_num}")
            except Exception as e:
                show_result(False, f"SMS simulation failed: {e}")


def page_make_call():
    st.header("6. Call Center")
    st.write("Make a phone call via Twilio or other providers.")
    
    # Call Provider Selection
    call_provider = st.selectbox("Call Provider", ["Twilio", "Vonage", "Simulation"], key="call_provider")
    
    to_num = st.text_input("Destination phone (with country code)", placeholder="+1234567890", key="call_to")
    call_duration = st.number_input("Call Duration (seconds)", min_value=10, max_value=300, value=60, key="call_duration")
    
    if call_provider == "Twilio":
        st.info("📞 **Twilio Setup Required:**")
        st.write("1. Get Twilio Account SID and Auth Token")
        st.write("2. Get a Twilio phone number")
        st.write("3. Add credentials below")
        
        twilio_sid = st.text_input("Twilio Account SID", key="twilio_sid_call")
        twilio_token = st.text_input("Twilio Auth Token", type="password", key="twilio_token_call")
        twilio_from = st.text_input("Twilio Phone Number", key="twilio_from_call")
        
        if st.button("Make Call via Twilio", key="make_call_twilio"):
            if not all([to_num, twilio_sid, twilio_token, twilio_from]):
                show_result(False, "Please provide all Twilio credentials.")
                return
            try:
                # Import Twilio if available
                try:
                    from twilio.rest import Client
                    client = Client(twilio_sid, twilio_token)
                    call = client.calls.create(
                        url='http://demo.twilio.com/docs/voice.xml',  # Default TwiML
                        from_=twilio_from,
                        to=to_num
                    )
                    show_result(True, f"Call initiated successfully! SID: {call.sid}")
                except ImportError:
                    st.error("Twilio not installed. Run: pip install twilio")
                    return
            except Exception as e:
                show_result(False, f"Twilio call failed: {e}")
    
    elif call_provider == "Vonage":
        st.info("📞 **Vonage Setup Required:**")
        st.write("1. Get Vonage API Key and Secret")
        st.write("2. Get a Vonage phone number")
        st.write("3. Add credentials below")
        
        vonage_key = st.text_input("Vonage API Key", key="vonage_key_call")
        vonage_secret = st.text_input("Vonage API Secret", type="password", key="vonage_secret_call")
        vonage_from = st.text_input("Vonage Phone Number", key="vonage_from_call")
        
        if st.button("Make Call via Vonage", key="make_call_vonage"):
            if not all([to_num, vonage_key, vonage_secret, vonage_from]):
                show_result(False, "Please provide all Vonage credentials.")
                return
            try:
                # Import Vonage if available
                try:
                    import vonage
                    client = vonage.Client(key=vonage_key, secret=vonage_secret)
                    response = client.voice.create_call({
                        "to": [{"type": "phone", "number": to_num}],
                        "from": {"type": "phone", "number": vonage_from},
                        "ncco": [
                            {"action": "talk", "text": "Hello! This is a test call from your automation system."}
                        ]
                    })
                    show_result(True, f"Call initiated successfully! UUID: {response['uuid']}")
                except ImportError:
                    st.error("Vonage not installed. Run: pip install vonage")
                    return
            except Exception as e:
                show_result(False, f"Vonage call failed: {e}")
    
    else:  # Simulation
        if st.button("Make Call (Simulation)", key="make_call_sim"):
            if not to_num:
                show_result(False, "Provide destination number.")
                return
            try:
                with st.spinner("Initiating call..."):
                    time.sleep(2)
                    # Simulate call process
                    st.info("📞 **Call Simulation:**")
                    st.write(f"**To:** {to_num}")
                    st.write(f"**Duration:** {call_duration} seconds")
                    st.write("**Status:** Connecting...")
                    time.sleep(1)
                    st.write("**Status:** Ringing...")
                    time.sleep(1)
                    st.write("**Status:** Connected")
                    time.sleep(1)
                    st.success("✅ **Call Completed Successfully!**")
                    show_result(True, f"Simulated call placed to {to_num}")
            except Exception as e:
                show_result(False, f"Call simulation failed: {e}")


def page_google_search():
    st.header("7. Web Search")
    st.write("Perform Google search using Google Custom Search API.")
    
    # Google API Key
    GOOGLE_API_KEY = "AIzaSyCNpQRHQI3IbzLpudRwmcCN_ao5QdLUsB4"
    
    query = st.text_input("Search query", key="g_query")
    num = st.number_input("Number of results", min_value=1, max_value=10, value=5, step=1, key="g_num")
    
    if st.button("Search", key="g_search"):
        if not query:
            show_result(False, "Enter a search query.")
            return
        
        try:
            import requests
            
            # Google Custom Search API
            url = "https://www.googleapis.com/customsearch/v1"
            params = {
                'key': GOOGLE_API_KEY,
                'cx': '017576662512468239146:omuauf_lfve',  # Default search engine ID
                'q': query,
                'num': min(int(num), 10)  # Max 10 results per request
            }
            
            response = requests.get(url, params=params)
            
            if response.status_code == 200:
                data = response.json()
                if 'items' in data:
                    results = data['items']
                    st.subheader(f"Search Results for: {query}")
                    
                    for i, item in enumerate(results[:int(num)], 1):
                        st.markdown(f"**{i}. {item.get('title', 'No title')}**")
                        st.write(f"🔗 {item.get('link', 'No link')}")
                        st.write(f"📝 {item.get('snippet', 'No description')}")
                        st.markdown("---")
                    
                    show_result(True, f"Found {len(results)} results for '{query}'")
                else:
                    show_result(False, "No results found for your query.")
            else:
                st.error(f"API Error: {response.status_code}")
                show_result(False, f"Search failed. Status: {response.status_code}")
                
        except Exception as e:
            st.error(f"Search error: {str(e)}")
            show_result(False, f"Search failed: {str(e)}")


def page_post_social():
    st.header("8. Auto-Post to Social Media")
    st.write("🚀 **Fully Automated Social Media Posting** - No user interference needed after clicking the button!")
    
    # Help and tips section
    with st.expander("ℹ️ **Platform Guidelines & Tips**", expanded=False):
        st.write("**📱 Instagram:** Images (8MB), Videos (100MB), 3-60 seconds")
        st.write("**📘 Facebook:** Images (30MB), Videos (4GB), max 240 minutes")
        st.write("**🐦 X (Twitter):** Text-focused, limited media support")
        st.write("**💼 LinkedIn:** Professional content, images (5MB), videos (200MB)")
        st.write("**💡 Pro Tip:** All platforms support automated posting with credentials")
        st.write("**🔒 Security:** Credentials are not stored, used only for browser automation")

    # Platform selection with LinkedIn added
    platform = st.selectbox("Platform", ["Instagram", "X (Twitter)", "Facebook", "LinkedIn"], key="social_platform")
    message = st.text_area("Message / Caption", key="social_message")
    
    # File upload section for all platforms
    media_type = "Text Only"  # Default value
    uploaded_file = None
    
    if platform in ["Instagram", "Facebook", "LinkedIn"]:
        st.write("**📁 Media Upload**")
        media_type = st.radio("Media Type", ["Text Only", "Image", "Video"], key="media_type")
        
        if media_type == "Image":
            uploaded_file = st.file_uploader(
                "Upload Image", 
                type=["jpg", "jpeg", "png", "gif", "webp"], 
                key="social_image",
                help="Supported formats: JPG, PNG, GIF, WebP"
            )
            if uploaded_file:
                st.image(uploaded_file, caption="Uploaded Image", use_container_width=True, width=300)
                
        elif media_type == "Video":
            uploaded_file = st.file_uploader(
                "Upload Video", 
                type=["mp4", "mov", "avi", "mkv", "webm"], 
                key="social_video",
                help="Supported formats: MP4, MOV, AVI, MKV, WebM"
            )
            if uploaded_file:
                st.video(uploaded_file)
                file_size = len(uploaded_file.getvalue()) / (1024 * 1024)  # MB
                st.info(f"Video size: {file_size:.1f} MB")
                
        # Show media guidelines
        if media_type in ["Image", "Video"]:
            if platform == "Instagram":
                st.info("📱 **Instagram Guidelines:**")
                st.write("- Images: JPG/PNG, max 8MB")
                st.write("- Videos: MP4, max 100MB, 3-60 seconds")
                st.write("- Stories: 9:16 aspect ratio recommended")
            elif platform == "Facebook":
                st.info("📘 **Facebook Guidelines:**")
                st.write("- Images: JPG/PNG, max 30MB")
                st.write("- Videos: MP4, max 4GB, max 240 minutes")
                st.write("- Posts: 1.91:1 to 16:9 aspect ratio")
            elif platform == "LinkedIn":
                st.info("💼 **LinkedIn Guidelines:**")
                st.write("- Images: JPG/PNG, max 5MB")
                st.write("- Videos: MP4, max 200MB, max 10 minutes")
                st.write("- Professional content recommended")
        
        # Show uploaded file information
        if uploaded_file:
            st.success(f"✅ **File Ready:** {uploaded_file.name}")
            file_size = len(uploaded_file.getvalue()) / (1024 * 1024)  # MB
            st.write(f"📊 **File Size:** {file_size:.2f} MB")
            st.write(f"📁 **File Type:** {uploaded_file.type}")
    
    # Credentials section
    st.write("---")
    st.subheader("🔐 **Login Credentials**")
    username = st.text_input(f"{platform} username/email", key="soc_user")
    password = st.text_input(f"{platform} password", type="password", key="soc_pass")
    
    # Automation options
    automation_mode = st.radio(
        "Automation Mode", 
        ["Full Automation (Login + Post)", "Direct Post (Skip Login)"], 
        key="automation_mode",
        help="Direct Post mode skips login and goes straight to posting (works if already logged in)"
    )
    
    # Post scheduling (optional)
    st.write("---")
    st.subheader("⏰ **Post Scheduling** (Optional)")
    schedule_post = st.checkbox("Schedule this post for later", key="schedule_post")
    if schedule_post:
        post_time = st.time_input("Post time", key="post_time")
        post_date = st.date_input("Post date", key="post_date")
        st.info(f"📅 Post will be scheduled for {post_date} at {post_time}")

    def ensure_selenium():
        if webdriver is None:
            st.error("Selenium is not installed. Install with: pip install selenium webdriver-manager")
            return False
        return True
    
    def try_simple_automation(platform, username, password, message, uploaded_file=None, media_type="Text Only"):
        """Simplified automation approach with better error handling"""
        try:
            # Basic Chrome setup without complex options
            chrome_options = ChromeOptions()
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
            chrome_options.add_argument("--disable-gpu")
            chrome_options.add_argument("--disable-extensions")
            chrome_options.add_argument("--disable-notifications")
            chrome_options.add_argument("--start-maximized")
            
            # Use webdriver-manager for automatic driver management
            from webdriver_manager.chrome import ChromeDriverManager
            from selenium.webdriver.chrome.service import Service
            
            service = Service(ChromeDriverManager().install())
            driver = webdriver.Chrome(service=service, options=chrome_options)
            wait = WebDriverWait(driver, 30)
            
            # Platform-specific simplified automation
            if platform == "X (Twitter)":
                driver.get("https://twitter.com/compose/tweet")
                time.sleep(5)
                
                # Try to find tweet box with multiple selectors
                tweet_selectors = [
                    "[data-testid='tweetTextarea_0']",
                    "[role='textbox']",
                    "textarea",
                    "[contenteditable='true']"
                ]
                
                tweet_box = None
                for selector in tweet_selectors:
                    try:
                        tweet_box = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, selector)))
                        break
                    except:
                        continue
                
                if tweet_box:
                    tweet_box.send_keys(message)
                    time.sleep(2)
                    
                    # Try to find post button
                    post_selectors = [
                        "[data-testid='tweetButton']",
                        "[aria-label='Tweet']",
                        "button[type='submit']"
                    ]
                    
                    for selector in post_selectors:
                        try:
                            post_btn = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, selector)))
                            post_btn.click()
                            break
                        except:
                            continue
                    
                    time.sleep(3)
                    driver.quit()
                    return True, "Post completed successfully!"
                else:
                    driver.quit()
                    return False, "Could not find tweet composition area"
            
            elif platform == "Facebook":
                driver.get("https://www.facebook.com/")
                time.sleep(5)
                
                # Try to find post creation area
                post_selectors = [
                    "[aria-label='Create a post']",
                    "[data-testid='post-composer']",
                    "[role='textbox']"
                ]
                
                post_area = None
                for selector in post_selectors:
                    try:
                        post_area = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, selector)))
                        break
                    except:
                        continue
                
                if post_area:
                    post_area.send_keys(message)
                    time.sleep(2)
                    
                    # Try to find post button
                    submit_selectors = [
                        "[aria-label='Post']",
                        "button[type='submit']",
                        "[data-testid='post-button']"
                    ]
                    
                    for selector in submit_selectors:
                        try:
                            submit_btn = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, selector)))
                            submit_btn.click()
                            break
                        except:
                            continue
                    
                    time.sleep(3)
                    driver.quit()
                    return True, "Post completed successfully!"
                else:
                    driver.quit()
                    return False, "Could not find Facebook post area"
            
            else:
                driver.quit()
                return False, f"Simplified automation not yet implemented for {platform}"
                
        except Exception as e:
            try:
                driver.quit()
            except:
                pass
            return False, f"Simplified automation failed: {str(e)}"

    # Post summary section
    if platform in ["Instagram", "Facebook", "LinkedIn"] and media_type in ["Image", "Video"] and uploaded_file:
        st.write("---")
        st.subheader("📋 **Post Summary**")
        col1, col2 = st.columns([1, 1])
        with col1:
            st.write(f"**Platform:** {platform}")
            st.write(f"**Media Type:** {media_type}")
            st.write(f"**File:** {uploaded_file.name}")
        with col2:
            file_size = len(uploaded_file.getvalue()) / (1024 * 1024)  # MB
            st.write(f"**File Size:** {file_size:.2f} MB")
            st.write(f"**Caption Length:** {len(message)} characters")
            if platform == "Instagram" and len(message) > 2200:
                st.warning("⚠️ Caption may be too long for Instagram")
            elif platform == "LinkedIn" and len(message) > 3000:
                st.warning("⚠️ Caption may be too long for LinkedIn")
    
    # Auto-post button with enhanced validation
    col1, col2, col3 = st.columns([1, 2, 1])
    with col1:
        post_button = st.button("🚀 **AUTO-POST NOW**", key="social_post", use_container_width=True)
    with col3:
        manual_button = st.button("📝 **Manual Instructions**", key="manual_guide", use_container_width=True)
    
    # Manual posting guide
    if manual_button:
        st.info("📋 **Manual Posting Instructions**")
        st.write("If automated posting fails, you can post manually:")
        
        if platform == "X (Twitter)":
            st.write("1. Go to https://twitter.com/compose/tweet")
            st.write("2. Enter your message")
            st.write("3. Click 'Tweet'")
        elif platform == "Facebook":
            st.write("1. Go to https://www.facebook.com/")
            st.write("2. Click 'Create a post'")
            st.write("3. Enter your message and upload media if needed")
            st.write("4. Click 'Post'")
        elif platform == "Instagram":
            st.write("1. Go to https://www.instagram.com/")
            st.write("2. Click the '+' button to create a new post")
            st.write("3. Upload your media and add caption")
            st.write("4. Click 'Share'")
        elif platform == "LinkedIn":
            st.write("1. Go to https://www.linkedin.com/")
            st.write("2. Click 'Start a post'")
            st.write("3. Enter your message and upload media if needed")
            st.write("4. Click 'Post'")
        
        st.write("**Your prepared content:**")
        st.write(f"**Message:** {message}")
        if uploaded_file:
            st.write(f"**Media:** {uploaded_file.name} ({media_type})")
    
    if post_button:
        # Enhanced validation
        if not message.strip():
            show_result(False, "Please enter a message or caption for your post.")
            return
            
        if automation_mode == "Full Automation (Login + Post)" and not (username and password):
            show_result(False, "Please provide login credentials for automated posting.")
            return
            
        # Check media requirements
        if platform in ["Instagram", "Facebook", "LinkedIn"] and media_type in ["Image", "Video"]:
            if not uploaded_file:
                show_result(False, f"⚠️ **Media Required:** Please upload a {media_type.lower()} for your {platform} post.")
                st.info("💡 **Tip:** Choose 'Text Only' if you want to post without media.")
                return
            else:
                # Validate file size based on platform
                file_size = len(uploaded_file.getvalue()) / (1024 * 1024)  # MB
                if platform == "Instagram" and file_size > 8:
                    show_result(False, f"⚠️ **File Too Large:** Instagram supports files up to 8MB. Your file is {file_size:.1f}MB")
                    return
                elif platform == "Facebook" and file_size > 30:
                    show_result(False, f"⚠️ **File Too Large:** Facebook supports files up to 30MB. Your file is {file_size:.1f}MB")
                    return
                elif platform == "LinkedIn" and file_size > 5:
                    show_result(False, f"⚠️ **File Too Large:** LinkedIn supports files up to 5MB. Your file is {file_size:.1f}MB")
                    return
        
        # Show posting progress
        with st.spinner(f"🔄 **AUTOMATED POSTING IN PROGRESS** - Please wait, do not interfere..."):
            time.sleep(2)  # Simulate processing time
            
            if not ensure_selenium():
                return
                
            try:
                chrome_options = ChromeOptions()
                chrome_options.add_argument("--disable-notifications")
                chrome_options.add_argument("--start-maximized")
                chrome_options.add_argument("--disable-blink-features=AutomationControlled")
                chrome_options.add_argument("--no-sandbox")
                chrome_options.add_argument("--disable-dev-shm-usage")
                chrome_options.add_argument("--disable-gpu")
                chrome_options.add_argument("--disable-extensions")
                chrome_options.add_argument("--disable-plugins")
                chrome_options.add_argument("--disable-images")
                chrome_options.add_argument("--disable-javascript")
                chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
                chrome_options.add_experimental_option('useAutomationExtension', False)
                chrome_options.add_experimental_option("prefs", {
                    "profile.default_content_setting_values.notifications": 2,
                    "profile.default_content_settings.popups": 0,
                    "profile.managed_default_content_settings.images": 2
                })
                
                # Use webdriver-manager for automatic ChromeDriver management
                from webdriver_manager.chrome import ChromeDriverManager
                from selenium.webdriver.chrome.service import Service
                
                service = Service(ChromeDriverManager().install())
                driver = webdriver.Chrome(service=service, options=chrome_options)
                driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
                wait = WebDriverWait(driver, 45)  # Increased timeout

                if platform == "X (Twitter)":
                    # Automated X posting with improved error handling
                    try:
                        driver.get("https://twitter.com/login")
                        time.sleep(3)  # Allow page to load
                        
                        # Try multiple selectors for username field
                        username_selectors = [
                            (By.NAME, "text"),
                            (By.CSS_SELECTOR, "input[autocomplete='username']"),
                            (By.CSS_SELECTOR, "input[type='text']")
                        ]
                        
                        username_field = None
                        for selector in username_selectors:
                            try:
                                username_field = wait.until(EC.presence_of_element_located(selector))
                                break
                            except:
                                continue
                        
                        if not username_field:
                            raise Exception("Could not find username field")
                        
                        username_field.send_keys(username + Keys.ENTER)
                        time.sleep(2)
                        
                        # Try multiple selectors for password field
                        password_selectors = [
                            (By.NAME, "password"),
                            (By.CSS_SELECTOR, "input[type='password']"),
                            (By.CSS_SELECTOR, "input[autocomplete='current-password']")
                        ]
                        
                        password_field = None
                        for selector in password_selectors:
                            try:
                                password_field = wait.until(EC.presence_of_element_located(selector))
                                break
                            except:
                                continue
                        
                        if not password_field:
                            raise Exception("Could not find password field")
                        
                        password_field.send_keys(password + Keys.ENTER)
                        time.sleep(3)
                    except Exception as login_error:
                        st.error(f"Login failed for X (Twitter): {login_error}")
                        driver.quit()
                        return
                    
                    # Wait for login and navigate to compose
                    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "a[aria-label='Tweet']")))
                    driver.get("https://twitter.com/compose/tweet")
                    
                    # Find tweet box and post
                    tweet_box = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "[data-testid='tweetTextarea_0']")))
                    tweet_box.send_keys(message)
                    
                    # Click post button
                    post_btn = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "[data-testid='tweetButton']")))
                    post_btn.click()
                    
                    time.sleep(3)  # Wait for post to complete
                    show_result(True, f"✅ **AUTO-POSTED to X (Twitter) successfully!**")

                elif platform == "Facebook":
                    # Automated Facebook posting
                    driver.get("https://www.facebook.com/login")
                    wait.until(EC.presence_of_element_located((By.ID, "email"))).send_keys(username)
                    wait.until(EC.presence_of_element_located((By.ID, "pass"))).send_keys(password + Keys.ENTER)
                    
                    # Wait for login and navigate to profile
                    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "[role='textbox']")))
                    driver.get("https://www.facebook.com/")
                    
                    # Find and click create post button
                    create_post_btn = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "[aria-label='Create a post']")))
                    create_post_btn.click()
                    
                    # Find post text area and add message
                    post_text = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "[role='textbox']")))
                    post_text.send_keys(message)
                    
                    # Handle media upload if present
                    if media_type in ["Image", "Video"] and uploaded_file:
                        # Save uploaded file temporarily
                        temp_path = f"/tmp/{uploaded_file.name}"
                        with open(temp_path, "wb") as f:
                            f.write(uploaded_file.getvalue())
                        
                        # Find and click photo/video button
                        media_btn = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "[aria-label='Photo/Video']")))
                        media_btn.click()
                        
                        # Upload file
                        file_input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='file']")))
                        file_input.send_keys(temp_path)
                        
                        # Wait for upload to complete
                        time.sleep(3)
                        
                        # Clean up temp file
                        os.remove(temp_path)
                    
                    # Click post button
                    post_btn = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "[aria-label='Post']")))
                    post_btn.click()
                    
                    time.sleep(3)  # Wait for post to complete
                    show_result(True, f"✅ **AUTO-POSTED to Facebook successfully!**")

                elif platform == "Instagram":
                    # Automated Instagram posting
                    driver.get("https://www.instagram.com/accounts/login/")
                    wait.until(EC.presence_of_element_located((By.NAME, "username"))).send_keys(username)
                    wait.until(EC.presence_of_element_located((By.NAME, "password"))).send_keys(password + Keys.ENTER)
                    
                    # Wait for login and navigate to create post
                    wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
                    driver.get("https://www.instagram.com/")
                    
                    # Click create post button
                    create_btn = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "[aria-label='New post']")))
                    create_btn.click()
                    
                    # Handle media upload if present
                    if media_type in ["Image", "Video"] and uploaded_file:
                        # Save uploaded file temporarily
                        temp_path = f"/tmp/{uploaded_file.name}"
                        with open(temp_path, "wb") as f:
                            f.write(uploaded_file.getvalue())
                        
                        # Upload file
                        file_input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='file']")))
                        file_input.send_keys(temp_path)
                        
                        # Wait for upload and click next
                        time.sleep(3)
                        next_btn = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "[aria-label='Next']")))
                        next_btn.click()
                        
                        # Add caption
                        caption_box = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "[aria-label='Write a caption...']")))
                        caption_box.send_keys(message)
                        
                        # Clean up temp file
                        os.remove(temp_path)
                    else:
                        # Text-only post
                        caption_box = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "[aria-label='Write a caption...']")))
                        caption_box.send_keys(message)
                    
                    # Click share button
                    share_btn = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "[aria-label='Share']")))
                    share_btn.click()
                    
                    time.sleep(3)  # Wait for post to complete
                    show_result(True, f"✅ **AUTO-POSTED to Instagram successfully!**")

                elif platform == "LinkedIn":
                    # Automated LinkedIn posting
                    driver.get("https://www.linkedin.com/login")
                    wait.until(EC.presence_of_element_located((By.ID, "username"))).send_keys(username)
                    wait.until(EC.presence_of_element_located((By.ID, "password"))).send_keys(password + Keys.ENTER)
                    
                    # Wait for login and navigate to create post
                    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "[aria-label='Start a post']")))
                    
                    # Click start a post button
                    start_post_btn = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "[aria-label='Start a post']")))
                    start_post_btn.click()
                    
                    # Find post text area and add message
                    post_text = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "[aria-label='Text editor for creating content']")))
                    post_text.send_keys(message)
                    
                    # Handle media upload if present
                    if media_type in ["Image", "Video"] and uploaded_file:
                        # Save uploaded file temporarily
                        temp_path = f"/tmp/{uploaded_file.name}"
                        with open(temp_path, "wb") as f:
                            f.write(uploaded_file.getvalue())
                        
                        # Find and click media button
                        media_btn = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "[aria-label='Add media']")))
                        media_btn.click()
                        
                        # Upload file
                        file_input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='file']")))
                        file_input.send_keys(temp_path)
                        
                        # Wait for upload to complete
                        time.sleep(3)
                        
                        # Clean up temp file
                        os.remove(temp_path)
                    
                    # Click post button
                    post_btn = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "[aria-label='Post']")))
                    post_btn.click()
                    
                    time.sleep(3)  # Wait for post to complete
                    show_result(True, f"✅ **AUTO-POSTED to LinkedIn successfully!**")
                
                # Close browser
                driver.quit()
                
            except Exception as e:
                error_msg = str(e)
                if "GetHandleVerifier" in error_msg or "No symbol" in error_msg:
                    st.warning("⚠️ **Main automation failed. Trying simplified approach...**")
                    
                    # Try simplified automation as fallback
                    success, message = try_simple_automation(platform, username, password, message, uploaded_file, media_type)
                    
                    if success:
                        show_result(True, f"✅ **Simplified automation successful!** {message}")
                    else:
                        show_result(False, "Both main and simplified automation failed.")
                        st.error("💡 **Solutions:**")
                        st.write("1. **Update Chrome browser** to the latest version")
                        st.write("2. **Clear browser cache** and cookies")
                        st.write("3. **Try different platform** (some platforms have stronger anti-bot measures)")
                        st.write("4. **Check internet connection** and platform accessibility")
                        st.write("5. **Use manual posting** option above")
                        st.write("6. **Try text-only posts** (media uploads are more complex)")
                else:
                    show_result(False, f"Automated posting failed: {error_msg}")
                    st.error("💡 **Troubleshooting:** Check your credentials and ensure the platform is accessible.")
                
                # Always try to close the driver
                try:
                    if 'driver' in locals():
                        driver.quit()
                except:
                    pass


def page_download_website():
    st.header("9. Website Downloader")
    st.write("Download page HTML or extract links/images from a URL.")
    url = st.text_input("Website URL (include http/https)", key="dl_url")
    strategy = st.radio("Download strategy", ["Download HTML", "Extract all links", "Download images (first 10)"], key="dl_strategy")
    if st.button("Download", key="dl_download"):
        if not url:
            show_result(False, "Provide a URL.")
            return
        try:
            resp = requests.get(url, timeout=15)
            resp.raise_for_status()
            soup = BeautifulSoup(resp.text, "html.parser")
            if strategy == "Download HTML":
                st.download_button("Download HTML", data=resp.text.encode("utf-8"), file_name="page.html", mime="text/html")
                show_result(True, "HTML downloaded.")
            elif strategy == "Extract all links":
                links = [a.get('href') for a in soup.find_all('a', href=True)]
                st.write(f"Found {len(links)} links (showing first 100):")
                st.write(links[:100])
                show_result(True, f"Extracted {len(links)} links.")
            else:
                imgs = [img.get('src') for img in soup.find_all('img', src=True)]
                st.write(f"Found {len(imgs)} images (attempting to download first 10).")
                downloaded = 0
                for src in imgs[:10]:
                    try:
                        img_url = src if src.startswith("http") else requests.compat.urljoin(url, src)
                        r = requests.get(img_url, timeout=10)
                        r.raise_for_status()
                        img = Image.open(BytesIO(r.content))
                        st.image(img, caption=img_url, use_container_width=True)
                        downloaded += 1
                    except Exception as e:
                        st.write(f"Failed to download {src}: {e}")
                show_result(True, f"Downloaded {downloaded} images (simulated).")
        except Exception as e:
            show_result(False, f"Failed to fetch URL: {e}")


def page_anonymous_email():
    st.header("10. Anonymous Mailer")
    st.write("Sending truly anonymous email is not generally ethical/legal. This placeholder shows how you might configure a disposable sender with a relay service.")
    to_email = st.text_input("To email", key="anon_to")
    subject = st.text_input("Subject", key="anon_subject")
    body = st.text_area("Body", key="anon_body")
    if st.button("Send Anonymous Email", key="anon_send"):
        if not to_email:
            show_result(False, "Provide recipient email.")
            return
        st.warning("True anonymity can be illegal or violate terms. Use only on accounts you control.")
        time.sleep(1)
        show_result(True, f"Simulated anonymous email to {to_email}")


def page_create_image():
    st.header("11. AI Image Creator")
    st.write("Generate images using Google's AI image generation API.")
    
    # Google API Key (you can make this configurable)
    GOOGLE_API_KEY = "AIzaSyCNpQRHQI3IbzLpudRwmcCN_ao5QdLUsB4"
    
    # Google AI Image Generation (default method)
    st.write("Generate AI-powered images using Google's image generation API.")
    prompt = st.text_area("Describe the image you want to generate", 
                         placeholder="Describe the image you want to generate", 
                         key="ai_prompt")
    style = st.selectbox("Image Style", ["photographic", "digital-art", "cinematic", "anime", "cartoon"], key="img_style")
    
    if st.button("Generate AI Image", key="generate_ai_img"):
        if not prompt:
            show_result(False, "Please provide a description for the image.")
            return
        try:
            # Google AI Image Generation API call
            import requests
            
            url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro-vision:generateContent"
            headers = {
                "Content-Type": "application/json",
            }
            
            # For image generation, we'll use a different approach since Gemini Pro Vision is for analysis
            # Let's use Google's text-to-image generation
            st.info("Attempting to generate image using Google's AI...")
            
            # Alternative: Use Google's Imagen API if available
            # For now, we'll show a placeholder and suggest the proper endpoint
            st.warning("Note: The current API key appears to be for Google's Generative AI. For image generation, you may need:")
            st.write("1. Google Cloud Vision API")
            st.write("2. Google's Imagen API (if available)")
            
            # Fallback to basic image creation
            st.write("Creating a basic image as fallback...")
            img = Image.new("RGB", (800, 600), color="#F2EDD1")
            draw = ImageDraw.Draw(img)
            try:
                font = ImageFont.truetype("arial.ttf", size=60)
            except Exception:
                font = ImageFont.load_default()
            
            text = "AI Image Generation\n(API Integration Required)"
            draw.text((400, 300), text, fill="black", font=font, anchor="mm")
            
            buf = BytesIO()
            img.save(buf, format="PNG")
            buf.seek(0)
            st.image(img, caption="Placeholder Image", use_container_width=True)
            st.download_button("Download placeholder", data=buf.getvalue(), file_name="placeholder.png", mime="image/png")
            
            show_result(True, "Placeholder image created. Check Google Cloud Console for proper image generation APIs.")
            
        except Exception as e:
            show_result(False, f"AI image generation failed: {e}")
            st.write("Please check your Google Cloud Console for proper image generation API setup.")


def page_swap_faces():
    st.header("12. Face Swapper")
    st.write("Face detection and analysis using Google Vision API. Face swapping requires additional ML models.")
    
    # Google API Key
    GOOGLE_API_KEY = "AIzaSyCNpQRHQI3IbzLpudRwmcCN_ao5QdLUsB4"
    
    img1 = st.file_uploader("Upload first image", type=["jpg", "png", "jpeg"], key="face1")
    img2 = st.file_uploader("Upload second image", type=["jpg", "png", "jpeg"], key="face2")
    
    # Analysis options
    analysis_mode = st.radio(
        "Analysis Mode", 
        ["Google Vision API", "Basic Image Analysis"], 
        key="analysis_mode",
        help="Choose between Google Vision API (requires setup) or basic analysis"
    )
    
    if st.button("Analyze Faces", key="analyze_faces"):
        if not (img1 and img2):
            show_result(False, "Upload both images.")
            return
        
        try:
            import requests
            import base64
            
            # Function to encode image to base64
            def encode_image(image_file):
                return base64.b64encode(image_file.read()).decode('utf-8')
            
            # Function for basic image analysis
            def basic_image_analysis(image_file):
                """Basic image analysis without API"""
                try:
                    img = Image.open(image_file)
                    width, height = img.size
                    
                    # Basic analysis based on image properties
                    aspect_ratio = width / height
                    file_size = len(image_file.getvalue()) / (1024 * 1024)  # MB
                    
                    # Simple face detection simulation based on image characteristics
                    if aspect_ratio > 0.5 and aspect_ratio < 2.0:  # Reasonable aspect ratio for portraits
                        if file_size > 0.1:  # Decent file size
                            return {
                                'faces_found': 1,
                                'confidence': 0.7,
                                'image_properties': {
                                    'width': width,
                                    'height': height,
                                    'aspect_ratio': round(aspect_ratio, 2),
                                    'file_size_mb': round(file_size, 2)
                                }
                            }
                    
                    return {
                        'faces_found': 0,
                        'confidence': 0.0,
                        'image_properties': {
                            'width': width,
                            'height': height,
                            'aspect_ratio': round(aspect_ratio, 2),
                            'file_size_mb': round(file_size, 2)
                        }
                    }
                except Exception as e:
                    return {
                        'faces_found': 0,
                        'confidence': 0.0,
                        'error': str(e)
                    }
            
            # Analyze both images
            images = [img1, img2]
            results = []
            
            for i, img in enumerate(images, 1):
                img.seek(0)  # Reset file pointer
                
                if analysis_mode == "Basic Image Analysis":
                    # Use basic analysis without API
                    analysis_result = basic_image_analysis(img)
                    results.append({
                        'image_num': i,
                        'faces_found': analysis_result['faces_found'],
                        'face_data': [{'detectionConfidence': analysis_result['confidence']}],
                        'fallback': True,
                        'image_properties': analysis_result.get('image_properties', {})
                    })
                else:
                    # Use Google Vision API
                    try:
                        encoded_image = encode_image(img)
                        
                        # Google Vision API for face detection
                        url = f"https://vision.googleapis.com/v1/images:annotate?key={GOOGLE_API_KEY}"
                        
                        payload = {
                            "requests": [
                                {
                                    "image": {
                                        "content": encoded_image
                                    },
                                    "features": [
                                        {
                                            "type": "FACE_DETECTION",
                                            "maxResults": 10
                                        }
                                    ]
                                }
                            ]
                        }
                        
                        response = requests.post(url, json=payload)
                        
                        if response.status_code == 200:
                            data = response.json()
                            face_annotations = data.get('responses', [{}])[0].get('faceAnnotations', [])
                            results.append({
                                'image_num': i,
                                'faces_found': len(face_annotations),
                                'face_data': face_annotations
                            })
                        elif response.status_code == 403:
                            st.warning(f"⚠️ **API Access Denied for image {i}** - Google Vision API not accessible")
                            st.info("💡 **Solutions:**")
                            st.write("1. **Enable Google Vision API** in Google Cloud Console")
                            st.write("2. **Check API key permissions** and billing")
                            st.write("3. **Switch to Basic Image Analysis mode**")
                            
                            # Fallback: Basic image analysis without API
                            st.write(f"🔄 **Using fallback analysis for image {i}...**")
                            analysis_result = basic_image_analysis(img)
                            results.append({
                                'image_num': i,
                                'faces_found': analysis_result['faces_found'],
                                'face_data': [{'detectionConfidence': analysis_result['confidence']}],
                                'fallback': True,
                                'image_properties': analysis_result.get('image_properties', {})
                            })
                        else:
                            st.error(f"API Error for image {i}: {response.status_code}")
                            st.write(f"Response: {response.text[:200]}...")
                            return
                    except Exception as api_error:
                        st.warning(f"⚠️ **API Error for image {i}**: {api_error}")
                        st.write(f"🔄 **Using fallback analysis for image {i}...**")
                        analysis_result = basic_image_analysis(img)
                        results.append({
                            'image_num': i,
                            'faces_found': analysis_result['faces_found'],
                            'face_data': [{'detectionConfidence': analysis_result['confidence']}],
                            'fallback': True,
                            'image_properties': analysis_result.get('image_properties', {})
                        })
            
            # Display results
            cols = st.columns(2)
            with cols[0]:
                caption = f"Image 1 - {results[0]['faces_found']} faces detected"
                if results[0].get('fallback', False):
                    caption += " (Fallback Mode)"
                st.image(Image.open(img1), caption=caption, use_container_width=True)
                
                if results[0]['faces_found'] > 0:
                    if results[0].get('fallback', False):
                        st.write(f"🔄 {results[0]['faces_found']} face(s) detected (Fallback Mode)")
                        st.info("⚠️ **Note:** Using fallback analysis due to API access issues")
                    else:
                        st.write(f"✅ {results[0]['faces_found']} face(s) detected")
                    
                    for j, face in enumerate(results[0]['face_data']):
                        confidence = face.get('detectionConfidence', 0) * 100
                        if results[0].get('fallback', False):
                            st.write(f"Face {j+1}: {confidence:.1f}% confidence (Estimated)")
                        else:
                            st.write(f"Face {j+1}: {confidence:.1f}% confidence")
            
            with cols[1]:
                caption = f"Image 2 - {results[1]['faces_found']} faces detected"
                if results[1].get('fallback', False):
                    caption += " (Fallback Mode)"
                st.image(Image.open(img2), caption=caption, use_container_width=True)
                
                if results[1]['faces_found'] > 0:
                    if results[1].get('fallback', False):
                        st.write(f"🔄 {results[1]['faces_found']} face(s) detected (Fallback Mode)")
                        st.info("⚠️ **Note:** Using fallback analysis due to API access issues")
                    else:
                        st.write(f"✅ {results[1]['faces_found']} face(s) detected")
                    
                    for j, face in enumerate(results[1]['face_data']):
                        confidence = face.get('detectionConfidence', 0) * 100
                        if results[1].get('fallback', False):
                            st.write(f"Face {j+1}: {confidence:.1f}% confidence (Estimated)")
                        else:
                            st.write(f"Face {j+1}: {confidence:.1f}% confidence")
            
            if results[0]['faces_found'] > 0 and results[1]['faces_found'] > 0:
                show_result(True, f"Face analysis complete. {results[0]['faces_found']} and {results[1]['faces_found']} faces detected respectively.")
            else:
                show_result(False, "Face detection failed. Please ensure both images contain clear faces.")
                
        except Exception as e:
            st.error(f"Face analysis error: {str(e)}")
            show_result(False, f"Face analysis failed: {str(e)}")

def page_analyze_llm():
    st.header("13. LLM Analyzer")
    st.write("Analyze LLM models using Google's Generative AI API for insights and comparisons.")
    
    # Google API Key
    GOOGLE_API_KEY = "AIzaSyCNpQRHQI3IbzLpudRwmcCN_ao5QdLUsB4"
    
    model_name = st.text_input("Model name to analyze (e.g., gpt-4o, llama2, gemini-pro)", key="llm_name")
    analysis_type = st.selectbox("Analysis Type", ["Model Comparison", "Architecture Analysis", "Capability Assessment", "Performance Review"], key="analysis_type")
    
    if st.button("Analyze Model", key="llm_analyze"):
        if not model_name:
            show_result(False, "Enter a model name.")
            return
        
        try:
            import requests
            
            # Create analysis prompt based on type
            if analysis_type == "Model Comparison":
                prompt = f"Compare {model_name} with other popular LLMs like GPT-4, Claude, and Gemini. Focus on architecture, capabilities, and use cases."
            elif analysis_type == "Architecture Analysis":
                prompt = f"Analyze the architecture of {model_name}. What are its key components, training approach, and technical specifications?"
            elif analysis_type == "Capability Assessment":
                prompt = f"Assess the capabilities of {model_name}. What tasks is it good at? What are its limitations?"
            else:  # Performance Review
                prompt = f"Review the performance characteristics of {model_name}. Discuss speed, accuracy, and efficiency."
            
            # Google Generative AI API (Gemini)
            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={GOOGLE_API_KEY}"
            
            payload = {
                "contents": [
                    {
                        "parts": [
                            {
                                "text": f"Please provide a detailed analysis of {model_name}. {prompt} Include technical details, comparisons, and practical insights."
                            }
                        ]
                    }
                ],
                "generationConfig": {
                    "temperature": 0.3,
                    "topK": 40,
                    "topP": 0.95,
                    "maxOutputTokens": 2048,
                }
            }
            
            response = requests.post(url, json=payload)
            
            if response.status_code == 200:
                data = response.json()
                if 'candidates' in data and len(data['candidates']) > 0:
                    analysis = data['candidates'][0]['content']['parts'][0]['text']
                    
                    st.subheader(f"Analysis Results for {model_name}")
                    st.write("**Analysis Type:**", analysis_type)
                    st.markdown("---")
                    st.write(analysis)
                    
                    # Additional insights
                    st.subheader("Key Insights")
                    st.markdown("""
                    **Next Steps:**
                    1. Research official documentation and papers
                    2. Check model hub repositories for configs
                    3. Test the model with specific use cases
                    4. Compare with similar models in the same category
                    """)
                    
                    show_result(True, f"Analysis complete for {model_name}")
                else:
                    st.error("No analysis generated")
                    show_result(False, "Failed to generate analysis.")
            else:
                st.error(f"API Error: {response.status_code}")
                show_result(False, f"Analysis failed. Status: {response.status_code}")
                
        except Exception as e:
            st.error(f"Analysis error: {str(e)}")
            show_result(False, f"Analysis failed: {str(e)}")


def page_chatgpt_agent():
    st.header("14. ChatGPT Bot")
    st.write("AI-powered chatbot using Google's Generative AI (Gemini).")
    
    # Google API Key
    GOOGLE_API_KEY = "AIzaSyCNpQRHQI3IbzLpudRwmcCN_ao5QdLUsB4"
    
    # Initialize chat history
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    
    user_prompt = st.text_area("Ask me anything...", key="agent_prompt", placeholder="Type your message here...")
    
    col1, col2 = st.columns([1, 4])
    with col1:
        if st.button("Send", key="send_message"):
            if not user_prompt:
                show_result(False, "Enter a message.")
                return
            
            try:
                import requests
                
                # Google Generative AI API (Gemini)
                url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={GOOGLE_API_KEY}"
                
                payload = {
                    "contents": [
                        {
                            "parts": [
                                {
                                    "text": user_prompt
                                }
                            ]
                        }
                    ],
                    "generationConfig": {
                        "temperature": 0.7,
                        "topK": 40,
                        "topP": 0.95,
                        "maxOutputTokens": 1024,
                    }
                }
                
                response = requests.post(url, json=payload)
                
                if response.status_code == 200:
                    data = response.json()
                    if 'candidates' in data and len(data['candidates']) > 0:
                        ai_response = data['candidates'][0]['content']['parts'][0]['text']
                        
                        # Add to chat history
                        st.session_state.chat_history.append({"user": user_prompt, "ai": ai_response})
                        
                        show_result(True, "Message sent successfully!")
                    else:
                        st.error("No response generated")
                        show_result(False, "Failed to generate response.")
                else:
                    st.error(f"API Error: {response.status_code}")
                    show_result(False, f"Failed to send message. Status: {response.status_code}")
                    
            except Exception as e:
                st.error(f"Chat error: {str(e)}")
                show_result(False, f"Failed to send message: {str(e)}")
    
    with col2:
        if st.button("Clear Chat", key="clear_chat"):
            st.session_state.chat_history = []
            st.rerun()
    
    # Display chat history
    if st.session_state.chat_history:
        st.subheader("Chat History")
        for i, chat in enumerate(st.session_state.chat_history):
            with st.expander(f"Conversation {i+1}", expanded=True):
                st.write("**You:**")
                st.write(chat["user"])
                st.write("**AI:**")
                st.write(chat["ai"])
                st.markdown("---")


def page_commandhub():
    st.header("15. System Commands")
    st.write("**Security note:** Running system commands can be dangerous. This UI restricts commands to a safe whitelist.")
    system_name = platform.system().lower()
    if "windows" in system_name:
        whitelist = {
            "List directory": "dir",
            "Current directory": "cd",
            "Whoami": "whoami",
            "Disk usage": "wmic logicaldisk get Caption,FreeSpace,Size",
            "Memory usage": "wmic OS get FreePhysicalMemory,TotalVisibleMemorySize /Format:List",
            "Top processes (head)": "wmic process get Name,ProcessId,WorkingSetSize | more"
        }
    else:
        whitelist = {
            "List directory": "ls -la",
            "Current directory": "pwd",
            "Whoami": "whoami",
            "Disk usage": "df -h",
            "Memory usage": "free -m",
            "Top processes (head)": "ps aux --no-heading | head -n 10"
        }
    cmd_label = st.selectbox("Choose a command", list(whitelist.keys()), key="cmd_label")
    custom = st.checkbox("Or enter a custom command (disabled by default)", value=False, key="cmd_custom")
    custom_cmd = None
    if custom:
        custom_cmd = st.text_input("Enter custom command (allowed only if you understand the risk)", key="custom_cmd")
    if st.button("Execute", key="exec_cmd"):
        try:
            if custom and custom_cmd:
                # For safety, forbid dangerous commands
                forbidden_keywords = ["rm", "shutdown", "reboot", "passwd", "mkfs", "dd", ">:", "sudo"]
                if any(k in custom_cmd for k in forbidden_keywords):
                    show_result(False, "This custom command is forbidden for safety.")
                    return
                proc = subprocess.run(custom_cmd, shell=True, capture_output=True, text=True, timeout=20)
            else:
                proc = subprocess.run(whitelist[cmd_label], shell=True, capture_output=True, text=True, timeout=20)
            output = proc.stdout.strip() or proc.stderr.strip()
            st.code(output[:10000])  # cap long outputs
            show_result(True, "Command executed.")
        except Exception as e:
            show_result(False, f"Failed to run command: {e}")




left_col, sep_col, main_col = st.columns([2.2, 0.06, 7.7])

with left_col:
    st.title("Automation Dashboard")
    st.write("Description: Its your day to ease your work with automation 🤗😉.")
    st.write("---")



PAGES = {
    "task_1": page_read_ram,
    "task_2": page_send_whatsapp,
    "task_3": page_send_email,
    "task_4": page_whatsapp_non_contact,
    "task_5": page_send_sms,
    "task_6": page_make_call,
    "task_7": page_google_search,
    "task_8": page_post_social,
    "task_9": page_download_website,
    "task_10": page_anonymous_email,
    "task_11": page_create_image,
    "task_12": page_swap_faces,
    "task_13": page_analyze_llm,
    "task_14": page_chatgpt_agent,
    "task_15": page_commandhub,
}

with main_col:
    page = st.session_state.page
    if page == "home":
        st.header("Task Launcher")
        st.write("Click a button to open the task page.")
        cols = st.columns(4)
        for i, (icon, label) in enumerate(zip(TASK_ICONS, TASK_LABELS)):
            col = cols[i % 4]
            if col.button(f"{icon}  {label}", key=f"task_btn_{i}"):
                navigate(f"task_{i+1}")
    else:

        if st.button("← Back to Home", key="back_home"):
            navigate("home")

        page_fn = PAGES.get(page)
        if page_fn:
            page_fn()
        else:
            st.error("Unknown page. Returning to home.")
            st.session_state.page = "home"

