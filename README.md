# 🐞 Jira Bug Creator

An AI-powered **QA assistant** that compares screenshots,
analyzes UI differences, and automatically generates professional bug reports.  
Built with **Flask**, **Gemini API**, and modular AI agents.

---

## 🚀 Features

🔍 **Analyst Agent** — Compares screenshots (Production vs. Development) to detect UI or functional 
differences

🧾 **QA Agent** — Converts visual and textual findings into structured, human-readable bug reports

⚙️ **Modular architecture** — Agents and services separated for clean extensibility

🧠 **Powered by Gemini 2.5 Pro** — Multimodal AI reasoning (text + image inputs)

🧩 **Prompt-based architecture** — Customizable prompts stored in /prompts/

📸 **Built-in image compression & base64 handling**

🧑‍💻 **Easy Flask UI** — Simple upload + text form for instant bug report generation


---

## ⚙️ Setup & Installation

### 1️⃣ Clone the repository

```bash
git clone https://github.com/vourdouyiannis/Jira_Bug_Creator.git
cd Jira_Bug_Creator
```

### 2️⃣ Create a virtual environment and activate it
```bash
python -m venv venv
source venv/bin/activate   # (Mac/Linux)
venv\Scripts\activate      # (Windows)
```

### 3️⃣ Install dependencies
```bash
pip install -r requirements.txt
```

### 4️⃣ Set up environment variables
Create a `.env` file in the project root with the following variables:
```env
GEMINI_API_KEY=your_api_key_here
MODEL_NAME=your_model_name_here
```
You can get your key from https://aistudio.google.com/app/apikey

## ▶️ Run the App
### 1. Run the Flask app:
```bash
python app.py
```

### 2. Open your browser and go to:
```
http://127.0.0.1:5000/
```

### 3. Fill in:

```
A) Bug title
B) Bug description
C) Upload screenshots (Production / Development)
```

### 4. Click **Generate Bug** Report 🪄
```
✅ You’ll get a detailed and professional bug report with:

Clarified title & description

Visual differences detected

Possible root cause

Markdown rendering with screenshots
```

## 🧩 Tech Stack

Python 3.13

Flask

Google Gemini API

Base64 / Pillow (for image handling)
