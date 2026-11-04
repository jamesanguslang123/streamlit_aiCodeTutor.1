
import streamlit as st
import ollama
import subprocess
import sys

# -----------------------------
# PAGE CONFIGURATION
# -----------------------------

st.set_page_config(
    page_title="CODETUTOR | AI Python Tutor",
    page_icon="🐍",
    layout="wide"
)

# -----------------------------
# CUSTOM DESIGN
# -----------------------------

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700;800&family=Space+Mono:wght@400;700&display=swap');

.stApp {
    background: linear-gradient(135deg, #080d1a 0%, #10172b 55%, #111027 100%);
    color: #edf2ff;
    font-family: 'DM Sans', sans-serif;
}

.block-container {
    max-width: 1150px;
    padding-top: 2.5rem;
    padding-bottom: 4rem;
}

h1, h2, h3, p, label {
    color: #edf2ff !important;
}

.hero {
    padding: 35px 38px;
    border: 1px solid #293657;
    border-radius: 22px;
    background: linear-gradient(120deg, #172440, #211d40);
    margin-bottom: 28px;
}

.brand {
    font-size: 42px;
    font-weight: 800;
    letter-spacing: -2px;
    margin: 0;
}

.brand span {
    color: #8b83ff;
}

.tagline {
    color: #b5c2df !important;
    font-size: 17px;
    margin-top: 8px;
}

.eyebrow {
    color: #9b94ff !important;
    font-size: 12px;
    font-weight: 700;
    letter-spacing: 2px;
    text-transform: uppercase;
}

.panel {
    background: #111b30;
    border: 1px solid #293957;
    border-radius: 17px;
    padding: 22px;
    margin-bottom: 18px;
}

.panel-title {
    font-size: 20px;
    font-weight: 700;
    margin-bottom: 5px;
}

.muted {
    color: #94a4c3 !important;
    font-size: 14px;
}

div[data-testid="stTextArea"] textarea {
    background: #080f1e !important;
    color: #dce7ff !important;
    border: 1px solid #344666 !important;
    border-radius: 12px !important;
    font-family: 'Space Mono', monospace !important;
    font-size: 14px !important;
}

div[data-testid="stTextInput"] input {
    background: #080f1e !important;
    color: #edf2ff !important;
    border: 1px solid #344666 !important;
    border-radius: 10px !important;
}

.stButton button {
    background: linear-gradient(90deg, #655cf5, #8875ff);
    color: white !important;
    border: none;
    border-radius: 10px;
    padding: 10px 22px;
    font-weight: 700;
    transition: 0.2s;
}

.stButton button:hover {
    background: linear-gradient(90deg, #8178ff, #a08fff);
    transform: translateY(-1px);
}

hr {
    border-color: #293957;
    margin-top: 35px;
    margin-bottom: 35px;
}

div[data-testid="stAlert"] {
    border-radius: 12px;
}

.footer {
    text-align: center;
    color: #71809e;
    font-size: 12px;
    padding-top: 35px;
}
</style>
""", unsafe_allow_html=True)


# -----------------------------
# HEADER
# -----------------------------

st.markdown("""
<div class="hero">
    <p class="eyebrow">YOUR PERSONAL AI CODING ASSISTANT</p>
    <p class="brand">CODE<span>TUTOR.</span></p>
    <p class="tagline">
        Write code. Find mistakes. Understand Python.
        Learn to become a better programmer.
    </p>
</div>
""", unsafe_allow_html=True)


# -----------------------------
# CODING WORKSPACE
# -----------------------------

st.markdown('<p class="eyebrow">01 — CODING WORKSPACE</p>',
            unsafe_allow_html=True)

st.markdown("## Python Code Lab")
st.markdown(
    '<p class="muted">Write your Python code below and let CODETUTOR help you understand the result.</p>',
    unsafe_allow_html=True
)

left, right = st.columns([3, 1])

with left:
    st.markdown("**YOUR CODE**")

with right:
    st.markdown(
        '<p class="muted">Python 3 · AI enabled</p>',
        unsafe_allow_html=True
    )

code = st.text_area(
    "Python editor",
    height=300,
    placeholder="# Start writing Python here...\n\nprint('Hello, CODETUTOR!')",
    label_visibility="collapsed"
)

run_button = st.button("▶  Run Code", use_container_width=True)


# -----------------------------
# CODE EXECUTION
# -----------------------------

if run_button:

    if not code.strip():
        st.warning("Write some Python code before running it.")

    else:
        with st.spinner("Running your Python code..."):

            try:
                result = subprocess.run(
                    [sys.executable, "-I", "-c", code],
                    capture_output=True,
                    text=True,
                    timeout=5
                )

                if result.returncode == 0:

                    st.markdown("### <span style='color:#53d6a0'>✓ Execution successful</span>",
                                unsafe_allow_html=True)

                    with st.container(border=True):
                        st.markdown("**PROGRAM OUTPUT**")
                        st.code(result.stdout or "No output was produced.")

                else:

                    st.markdown("### <span style='color:#ff8585'>✕ Execution failed</span>",
                                unsafe_allow_html=True)

                    with st.container(border=True):
                        st.markdown("**ERROR DETAILS**")
                        st.code(result.stderr)

                    st.markdown("### AI Teacher")
                    st.markdown(
                        '<p class="muted">Your personal Python teacher is analysing the error.</p>',
                        unsafe_allow_html=True
                    )

                    with st.spinner("AI Teacher is preparing your explanation..."):

                        response = ollama.chat(
                            model="gpt-oss:20b-cloud",
                            messages=[
                                {
                                    "role": "user",
                                    "content": f"""
You are CODETUTOR, a patient and helpful Python teacher.

A beginner has run this code and received an error.

Their code:
{code}

Their error:
{result.stderr}

Explain the problem in a clear teaching style.

Use these sections:

1. WHAT THE ERROR MEANS
Explain it in simple language.

2. WHY IT HAPPENED
Identify the likely problem in their code.

3. HOW TO FIX IT
Give clear steps.

4. CORRECTED CODE
Show a corrected version of their code where possible.

Do not just give the answer. Help the learner understand.
"""
                                }
                            ]
                        )

                    with st.container(border=True):
                        st.markdown("**YOUR AI EXPLANATION**")
                        st.markdown(response["message"]["content"])

            except subprocess.TimeoutExpired:
                st.error("Your program exceeded the 5-second time limit.")

            except Exception as e:
                st.error(f"Something went wrong: {e}")


# -----------------------------
# ERROR LIBRARY
# -----------------------------

st.divider()

st.markdown('<p class="eyebrow">02 — LEARN PYTHON</p>',
            unsafe_allow_html=True)

st.markdown("## Python Error Library")
st.markdown(
    '<p class="muted">Confused by a Python error? Ask your AI teacher to explain it.</p>',
    unsafe_allow_html=True
)

with st.container(border=True):

    st.markdown("**What error would you like to understand?**")

    error_question = st.text_input(
        "Error name",
        placeholder="For example: TypeError, NameError, IndexError",
        label_visibility="collapsed"
    )

    explain_button = st.button(
        "Explain this error  →",
        use_container_width=True
    )

    if explain_button:

        if not error_question.strip():
            st.warning("Enter an error name first.")

        else:
            with st.spinner("Your AI teacher is preparing a lesson..."):

                try:
                    response = ollama.chat(
                        model="gpt-oss:20b-cloud",
                        messages=[
                            {
                                "role": "user",
                                "content": f"""
You are a friendly Python teacher.

Teach a beginner about this Python error:
{error_question}

Explain:
1. What it means.
2. Why it happens.
3. Common causes.
4. A simple example.
5. How to avoid it.

Make the explanation easy to understand.
"""
                            }
                        ]
                    )

                    st.markdown("### Your lesson")
                    st.markdown(response["message"]["content"])

                except Exception as e:
                    st.error(f"AI connection problem: {e}")


# -----------------------------
# FOOTER
# -----------------------------

st.markdown("""
<div class="footer">
    CODETUTOR · BUILT FOR LEARNING PYTHON · BETA 0.1
</div>
""", unsafe_allow_html=True)
