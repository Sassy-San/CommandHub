# 🚀 Automation Dashboard

A **Streamlit-based Automation Dashboard** designed to execute, manage, and monitor multiple automation tasks from a simple web interface.  
It integrates **system monitoring, messaging, web automation, AI tools, and secure system commands** into one unified platform.  

---

## ✨ Features
- 📊 **RAM Monitor** – Real-time system memory usage  
- 💬 **WhatsApp & SMS Sender** – Automate communication via APIs  
- ✉️ **Email Client** – Send emails via SMTP  
- 📱 **WhatsApp Non-Contact** – Send messages without saving contacts  
- 📞 **Phone Calls** – Placeholder for Twilio/Vonage APIs  
- 🔍 **Google Search** – API-based search integration  
- 📢 **Social Media Auto-Posting** – Instagram, Twitter (X), Facebook, LinkedIn  
- 🌐 **Website Downloader** – Fetch HTML, links, and images  
- 🕵️ **Anonymous Mailer** – Simulated anonymous emails  
- 🎨 **AI Image Generator** – Generate images using AI models  
- 😎 **Face Swapper** – Placeholder for OpenCV/dlib integration  
- 🤖 **LLM Analyzer & ChatGPT Agent** – AI-driven analysis and automation  
- 🛠️ **CommandHub** – Secure system command execution with whitelist  

---

## 🛠️ Technologies Used
- **Frontend/UI**: Streamlit + Custom CSS  
- **Backend**: Python (`psutil`, `Pillow`, `requests`, `BeautifulSoup4`, `selenium`, `pywhatkit`)  
- **Messaging/Calls**: Twilio, Vonage, SMTP  
- **AI & Automation**: ChatGPT, LLM Analyzers, Image Generation APIs  
- **System Monitoring**: psutil for RAM/CPU stats  
- **Security**: CommandHub with restricted command execution  

---

## ⚙️ Installation
```bash
# Clone repository
git clone https://github.com/your-username/automation-dashboard.git
cd automation-dashboard

# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run CommandHub.py
