## AutoMed Expert Engine: Multi-Agent Clinical Consensus Engine

AutoMed Expert Engine is an advanced AI medical triage simulation application powered by the **AG2 (formerly AutoGen)** multi-agent framework and orchestrated via a high-contrast minimalist **Gradio** web user interface.

Instead of relying on a single isolated large language model, AutoMed spins up a collaborative council of specialized AI agents. These agents debate, analyze, and cross-examine symptom data sequentially to construct a unified clinical triage report.


https://github.com/user-attachments/assets/b32b276b-3bb3-4e9d-afb9-465dadb821d6


---

## ⚙️ Core Agent Architecture

The framework relies on a rule-based `GroupChatManager` configuration executing sequential context logic across specialized AI roles:
1. **Patient Agent (`patient_agent`)**: Ingests and standardizes raw user symptom layouts.
2. **Diagnostic Agent (`diagnosis_agent`)**: Examines physiological anomalies, evaluating risk profiles for conditions like indigestion or gastritis.
3. **Pharmacy Agent (`pharmacy_agent`)**: Analyzes chemical/medicinal applications, counter-indications, and over-the-counter handling variables.
4. **Consultation Agent (`consultation_agent`)**: Acts as the ultimate coordinator, pulling inputs into a crisp, actionable consensus report before triggering the termination signal.

---

## 🚀 Key Features

- **Multi-Agent Consensus Routing:** Dynamically coordinates an automated medical panel to build unified outputs.
- **Monochrome Dark User Interface:** Sleek, high-contrast black-and-white workspace minimizing visual friction.
- **Terminal Buffer Redirection:** Intercepts internal `sys.stdout` streaming printouts from AutoGen directly into the web dashboard layout to trace agent thinking logs.
- **Strict Layout Constraints:** Comprehensive custom CSS properties completely prevent horizontal text overflows across all display scales.

---

## 📁 Project Structure

```text
automed-expert-engine/
├── .gitignore
├── .env.example
├── requirements.txt
├── README.md
└── app.py
🛠️ Setup & Execution Instructions
Follow these steps to run the application locally on your system:

1. Clone the Repository
Bash
git clone [https://github.com/YOUR_GITHUB_USERNAME/automed-expert-engine.git](https://github.com/YOUR_GITHUB_USERNAME/automed-expert-engine.git)
cd automed-expert-engine
2. Set Up a Virtual Environment (Recommended)
Bash
python -m venv venv
# On Windows use: venv\Scripts\activate
# On macOS/Linux use: source venv/bin/activate
3. Install Dependencies
Bash
pip install -r requirements.txt
4. Configure Your API Keys
Create a copy of the .env.example file and name it .env:

Bash
cp .env.example .env
Open the newly created .env file and insert your active API key:

Plaintext
OPENAI_API_KEY=sk-proj-YourActualKeyHere...
5. Launch the Dashboard
Run the standalone script from your terminal:

Bash
python app.py
Once executed, the terminal will provide a local address (e.g., http://127.0.0.1:7860). Open this link in any browser to access the interface.

🔬 Tech Stack Dependencies
Multi-Agent Orchestration Framework: AG2 (pyautogen)

User Interface Layer: Gradio

Environment Variable Parsing: Python-Dotenv

Runtime Environment: Python 3.10+

📄 License
This project is open-source and licensed under the MIT License.
