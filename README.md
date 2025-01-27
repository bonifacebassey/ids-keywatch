# Keylogger Detection

This project focuses on detecting and mitigating keylogger threats, 
a type of malware that captures sensitive user input like passwords and credit card details. 
The project introduces a simulated keylogger environment to test detection strategies via
process monitoring and network traffic analysis on SMTP ports and Discord WebHook.

---

## Setup Instructions

Follow these steps to set up the project on your local machine.

---

### **1. Clone the Repository**
1. Clone the repository to your local machine:
   ```bash
   git clone <repository_url>
   ```
2. Navigate to the project folder:
   ```bash
   cd project-name
   ```
   
## 2. Create and Activate a Virtual Environment
1. Create the virtual environment:
   ```bash
   python3 -m venv venv
   ```
2. Activate it:
   ```bash
   source venv/bin/activate
   ```
   
## 3. Install Dependencies

1. With the virtual environment active, install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
   
## 4. Run the Application
1. Run the `main.py` file:
   ```bash
   python main.py
   ```