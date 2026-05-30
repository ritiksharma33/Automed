import os
import io
import time
import contextlib
import gradio as gr
from dotenv import load_dotenv
import autogen
from autogen import GroupChat, GroupChatManager

# =====================================================================
# STEP 1: LOAD SECURE ENVIRONMENT KEYS
# =====================================================================
# This pulls your API key securely from your local secret .env file
load_dotenv()

llm_config = {
    "config_list": [
        {
            "model": "gpt-4o",  # Change this to match your active model (e.g., gpt-3.5-turbo, gpt-4, etc.)
            "api_key": os.getenv("OPENAI_API_KEY")
        }
    ],
    "temperature": 0.2,
}

# =====================================================================
# STEP 2: DEFINE THE SPECIFIC COOPERATIVE AGENTS
# =====================================================================
# 1. The Entry Node / Patient Agent
patient_agent = autogen.UserProxyAgent(
    name="patient",
    human_input_mode="NEVER",
    max_consecutive_auto_reply=0,
    code_execution_config=False
)

# 2. The Medical Diagnosis Agent
diagnosis_agent = autogen.AssistantAgent(
    name="diagnosis",
    llm_config=llm_config,
    system_message="""You are an expert diagnostic physician. Analyze the patient's symptoms thoroughly. 
    Provide potential conditions or causes based on medical knowledge, and highlight potential emergency signs. 
    Keep your response structured and professional."""
)

# 3. The Pharmacy / Medication Specialist Agent
pharmacy_agent = autogen.AssistantAgent(
    name="pharmacy",
    llm_config=llm_config,
    system_message="""You are an expert pharmacist. Based on the diagnosis agent's findings, recommend 
    safe over-the-counter remedies, list common medication considerations, and warn about any critical 
    contraindications or drug interactions."""
)

# 4. The Medical Consultation Triage Coordinator
consultation_agent = autogen.AssistantAgent(
    name="consultation",
    llm_config=llm_config,
    system_message="""You are the lead medical consultant and triage manager. Summarize the insights from both 
    the diagnosis and pharmacy agents into a clear, unified, step-by-step patient action plan. 
    Once you have written your complete summary, you MUST end your message with the exact keyword: CONSULTATION_COMPLETE"""
)

# =====================================================================
# STEP 3: CONSTRUCT THE ORCHESTRATION WORKFLOW
# =====================================================================
# Group the agents together into a council network
groupchat = GroupChat(
    agents=[patient_agent, diagnosis_agent, pharmacy_agent, consultation_agent],
    messages=[],
    max_round=5
)

# Setup the manager with custom termination tracking to cleanly catch the end state signal
manager = GroupChatManager(
    name="manager", 
    groupchat=groupchat,
    is_termination_msg=lambda x: "CONSULTATION_COMPLETE" in x.get("content", "") if x.get("content") else False
)

# =====================================================================
# STEP 4: INTERFACING GRADIO HANDLERS WITH THE TERMINAL PIPELINE
# =====================================================================
def run_medical_dashboard(user_symptoms):
    if not user_symptoms.strip():
        return (
            "<div style='padding:15px; color:#ffffff; background-color:#111111; border: 1px solid #ffffff; border-radius:2px;'>⚠️ Please state your symptoms to begin.</div>", 
            "<div style='color:#666666; font-family: monospace;'>System Idle. Waiting for input...</div>"
        )

    # Clear previous history arrays to keep execution clean across separate web runs
    groupchat.messages = [] 
    
    # Hijack standard system terminal prints into a text stream buffer
    terminal_buffer = io.StringIO()
    with contextlib.redirect_stdout(terminal_buffer):
        patient_agent.initiate_chat(
            manager, 
            message=f"I am feeling {user_symptoms}. Can you help?",
            clear_history=True,
            silent=False 
        )
        
    # Gather up raw output text that usually leaks into the background terminal console
    raw_terminal_output = terminal_buffer.getvalue()
    clean_terminal_logs = raw_terminal_output.replace(">>>>>>>> USING AUTO REPLY...", "⚡ [AI THINKING MAP] ")

    # Sift through logs to isolate the final coordinator's message block for the front page layout
    final_verdict = "Summary report compiled successfully. See detailed internal traces below."
    if "consultation (to manager):" in clean_terminal_logs:
        try:
            parts = clean_terminal_logs.split("consultation (to manager):")
            if len(parts) > 1:
                final_verdict = parts[-1].replace("CONSULTATION_COMPLETE", "").strip()
        except Exception:
            pass

    # Build responsive dark-wrapped structural report components (Stops horizontal wrapping issues)
    consensus_card = f"""
    <div style="background-color: #111111; border: 1px solid #ffffff; padding: 25px; border-radius: 2px; color: #ffffff; white-space: pre-wrap; word-break: break-word; overflow-x: hidden;">
        <h3 style="color: #ffffff; margin-top: 0; font-size: 1.2em; border-bottom: 1px solid #333333; padding-bottom: 10px; text-transform: uppercase; letter-spacing: 1px;">
            📋 Automated Consensus Report
        </h3>
        <div style="line-height: 1.6; font-size: 1.05em; color: #eeeeee; font-family: monospace; white-space: pre-wrap; word-break: break-word; margin-top: 15px;">
            {final_verdict}
        </div>
    </div>
    """

    formatted_logs = f"""
    <div style="background-color: #000000; border: 1px solid #222222; padding: 20px; border-radius: 2px; color: #aaaaaa; font-family: monospace; font-size: 0.95em; white-space: pre-wrap; word-break: break-word; overflow-x: hidden; overflow-y: auto; max-height: 500px; width: 100%;">
        <div style="color: #ffffff; font-weight: bold; margin-bottom: 15px; border-bottom: 1px solid #222222; padding-bottom: 5px; text-transform: uppercase; letter-spacing: 1px;">
            🪵 Real-Time Agent Architecture Traces
        </div>
        {clean_terminal_logs}
    </div>
    """
    
    return consensus_card, formatted_logs

# =====================================================================
# STEP 5: BLACK AND WHITE HIGH-CONTRAST GRADIO UI RENDERING
# =====================================================================
custom_dark_css = """
.gradio-container, body, html { background-color: #000000 !important; color: #ffffff !important; overflow-x: hidden !important; }
#component-0 { background-color: #000000 !important; }

p, div, span, pre, code, .gr-markdown, html, body {
    white-space: pre-wrap !important;
    word-wrap: break-word !important;
    word-break: break-word !important;
    overflow-x: hidden !important;
    max-width: 100% !important;
}

textarea, input, .gradio-container textarea, .gradio-container input { 
    background-color: #111111 !important; 
    color: #ffffff !important; 
    border: 1px solid #333333 !important; 
    border-radius: 2px !important;
    font-family: monospace !important;
}
textarea:focus, input:focus { border-color: #ffffff !important; }

.action-btn { 
    background-color: #ffffff !important; 
    color: #000000 !important; 
    border: 1px solid #ffffff !important; 
    font-weight: bold !important; 
    border-radius: 2px !important;
    letter-spacing: 1px !important;
}
.action-btn:hover { background-color: #cccccc !important; }
"""

with gr.Blocks(css=custom_dark_css) as demo:
    gr.HTML("""
        <div style="text-align: center; padding: 20px 0; border-bottom: 1px solid #222222; margin-bottom: 25px;">
            <h1 style="color: #ffffff; margin: 0; font-size: 1.8em; font-weight: 700; letter-spacing: 2px;">AUTOMED EXPERT ENGINE</h1>
            <p style="color: #666666; margin-top: 5px; font-size: 0.9em; letter-spacing: 1px;">MULTI-AGENT AI COORDINATION & HEALTHCARE CONSENSUS PROTOCOL</p>
        </div>
    """)
    
    with gr.Row():
        with gr.Column(scale=1):
            gr.Markdown("### 📥 Patient Intake Port")
            symptom_box = gr.Textbox(
                label="State Current Physical Discomforts",
                placeholder="Enter raw symptoms (e.g., 'Feeling like oil acid type in morning after eating...')",
                lines=6
            )
            submit_action = gr.Button("RUN ANALYSIS", elem_classes=["action-btn"])
            
            gr.HTML("""
            <div style="margin-top: 20px; padding: 15px; background-color: #111111; border: 1px solid #222222; font-size: 0.8em; color: #666666; font-family: monospace;">
                ACTIVE LOGICAL STACK:<br>
                • diagnosis_agent (Analysis)<br>
                • pharmacy_agent (Remedy Check)<br>
                • consultation_agent (Coordinator)
            </div>
            """)
            
        with gr.Column(scale=2):
            gr.Markdown("### 📊 Diagnostic Dashboard")
            consensus_output = gr.HTML(
                value="<div style='padding:40px; border: 1px dashed #222222; text-align:center; color:#444444; font-family: monospace;'>System standing by. Awaiting symptom submission to map agent node matrix.</div>"
            )
            logs_output = gr.HTML(
                value="<div style='color: #444444; font-family: monospace;'>Agent pipeline interaction logs offline.</div>"
            )

    submit_action.click(
        fn=run_medical_dashboard,
        inputs=symptom_box,
        outputs=[consensus_output, logs_output]
    )

# =====================================================================
# STEP 6: BOOT UP EXECUTABLE INSTANCE
# =====================================================================
if __name__ == "__main__":
    # This runs the webserver locally. 
    # Set share=True if you want it to give you a public URL link to share with others!
    demo.launch(share=False)