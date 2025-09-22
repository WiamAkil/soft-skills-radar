import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import io

# ---------- Page setup ----------
st.set_page_config(page_title="Soft Skills Radar – Fun Quiz", page_icon="🧭", layout="centered")

SKILLS = ["Empathy", "Critical Thinking", "Adaptability", "Trust", "Emotional Intelligence", "Agentility"]

QUESTIONS = [
    {
        "id": 1,
        "text": "Your team just crash-landed on Mars 🚀. The oxygen generator is busted. First move?",
        "options": [
            ("Check in with the crew’s state of mind", "Empathy"),
            ("Analyze the machine to find weak points", "Critical Thinking"),
            ("Repurpose other gear to hack a fix", "Adaptability"),
            ("Crack a calm joke & stabilize the mood", "Emotional Intelligence"),
        ],
    },
    {
        "id": 2,
        "text": "A teammate drops a 2 AM cat-typing GIF in chat. You…",
        "options": [
            ("DM them tomorrow to see if they’re okay", "Empathy"),
            ("Ask why they’re online at 2AM (pattern?)", "Critical Thinking"),
            ("Assume time-zone shuffle, keep it light", "Adaptability"),
            ("Reply with a supportive meme to show care", "Emotional Intelligence"),
        ],
    },
    {
        "id": 3,
        "text": "A mysterious locked box appears in a meeting. What’s your move?",
        "options": [
            ("Ask the room who knows its story", "Trust"),
            ("Treat it like a puzzle & test hypotheses", "Critical Thinking"),
            ("If it won’t open, park it and move on", "Adaptability"),
            ("Nominate it as the team mascot 😂", "Agentility"),
        ],
    },
    {
        "id": 4,
        "text": "Your dream trip is canceled last minute. What now?",
        "options": [
            ("Rebuild the plan instantly with options B/C", "Adaptability"),
            ("Check in on others & cheer them up", "Empathy"),
            ("Research smart alternatives within constraints", "Critical Thinking"),
            ("Accept the L, manage emotions, and reset", "Emotional Intelligence"),
        ],
    },
    {
        "id": 5,
        "text": "You find a baby dragon 🐉 under your desk. Instinct?",
        "options": [
            ("Make it feel safe & fed", "Empathy"),
            ("Observe it carefully before acting", "Critical Thinking"),
            ("Call the team & align next steps", "Trust"),
            ("Ride it into stand-up like a boss", "Agentility"),
        ],
    },
    {
        "id": 6,
        "text": "Dropped into a project outside your expertise. Mindset?",
        "options": [
            ("Volunteer for a tiny piece & learn fast", "Agentility"),
            ("Set a 1-week learning sprint & adapt", "Adaptability"),
            ("Pair with a pro & set clear expectations", "Trust"),
            ("Acknowledge nerves, set check-ins", "Emotional Intelligence"),
        ],
    },
    {
        "id": 7,
        "text": "A teammate shares confidential doubts about the project.",
        "options": [
            ("Keep it private & help craft a plan", "Trust"),
            ("Give them space today, follow up tomorrow", "Empathy"),
            ("Map root causes before reacting", "Critical Thinking"),
            ("Propose a small experiment to test a fix", "Agentility"),
        ],
    },
    {
        "id": 8,
        "text": "You get unexpected negative feedback. First reaction?",
        "options": [
            ("Thank them, ask for specifics, breathe", "Emotional Intelligence"),
            ("Extract signals from noise with questions", "Critical Thinking"),
            ("Adjust next sprint plan accordingly", "Adaptability"),
            ("Reconfirm commitments & reliability", "Trust"),
        ],
    },
    {
        "id": 9,
        "text": "Scope changes last minute (again). Your move?",
        "options": [
            ("Re-prioritize deliverables quickly", "Adaptability"),
            ("Re-check assumptions & constraints", "Critical Thinking"),
            ("Cut a micro-plan & charge ahead", "Agentility"),
            ("Align expectations & keep promises visible", "Trust"),
        ],
    },
    {
        "id": 10,
        "text": "You’re leading a sprint; someone’s falling behind. You…",
        "options": [
            ("Check in privately & listen", "Empathy"),
            ("Rebalance workload & unblock", "Agentility"),
            ("Make expectations explicit & mutual", "Trust"),
            ("Trace bottlenecks in the process", "Critical Thinking"),
        ],
    },
]

# Count how many times each skill appears (for scaling to 0–5)
skill_occurrences = {s: 0 for s in SKILLS}
for q in QUESTIONS:
    for _, skill in q["options"]:
        skill_occurrences[skill] += 1

# ---------- Session state ----------
if "page" not in st.session_state:
    st.session_state.page = 0  # index into QUESTIONS
if "answers" not in st.session_state:
    st.session_state.answers = {}  # qid -> option text
if "name" not in st.session_state:
    st.session_state.name = ""

# ---------- Sidebar ----------
with st.sidebar:
    st.header("About")
    st.write("10 quick scenarios → instant **soft skills radar** (0–5). No trick questions.")
    st.text_input("Your name (optional)", key="name")
    st.progress(st.session_state.page / max(1, len(QUESTIONS)))

# ---------- Header ----------
st.title("Soft Skills Radar – Fun Quiz 🧭")

# ---------- Quiz flow (one question per page) ----------
if st.session_state.page < len(QUESTIONS):
    q = QUESTIONS[st.session_state.page]
    st.subheader(f"Question {st.session_state.page+1} of {len(QUESTIONS)}")
    st.write(q["text"])
    if q["id"] in st.session_state.answers:
        st.caption(f"Previously chose: {st.session_state.answers[q['id']]} (you can change)")

    cols = st.columns(2)
    clicked = False
    for i, (opt_text, _skill) in enumerate(q["options"]):
        if cols[i % 2].button(opt_text, use_container_width=True, key=f"opt-{q['id']}-{i}"):
            st.session_state.answers[q["id"]] = opt_text
            st.session_state.page += 1
            clicked = True
            st.rerun()
    st.divider()
    st.button("⬅️ Back", disabled=(st.session_state.page == 0),
              on_click=lambda: st.session_state.update(page=st.session_state.page - 1))
else:
    # ---------- Results ----------
    raw_counts = {s: 0 for s in SKILLS}
    for q in QUESTIONS:
        chosen = st.session_state.answers.get(q["id"])
        if chosen:
            for opt_text, skill in q["options"]:
                if opt_text == chosen:
                    raw_counts[skill] += 1

    scores = {
        s: round(5 * raw_counts[s] / skill_occurrences[s], 2) if skill_occurrences[s] else 0
        for s in SKILLS
    }

    st.success("All done! Here’s your profile 👇")
    col1, col2 = st.columns([1, 1])

    with col1:
        st.write("### Your Scores (0–5)")
        st.json(scores)

    # Radar chart
    labels = SKILLS
    vals = [scores[s] for s in labels]
    vals += vals[:1]
    angles = np.linspace(0, 2 * np.pi, len(labels) + 1)

    fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))
    ax.plot(angles, vals, marker="o", linewidth=2)
    ax.fill(angles, vals, alpha=0.25)
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(labels)
    ax.set_ylim(0, 5)
    title = f"{(st.session_state.name or 'Your')} Soft Skills Radar"
    ax.set_title(title, pad=20)

    with col2:
        st.pyplot(fig, clear_figure=True)

    buf = io.BytesIO()
    fig.savefig(buf, format="png", dpi=180, bbox_inches="tight")
    st.download_button(
        "⬇️ Download your radar (PNG)",
        data=buf.getvalue(),
        file_name=f"{(st.session_state.name or 'soft_skills').replace(' ','_').lower()}_radar.png",
        mime="image/png",
    )

    st.button("🔁 Restart test", type="primary",
              on_click=lambda: st.session_state.update(page=0, answers={}, name=st.session_state.name))
