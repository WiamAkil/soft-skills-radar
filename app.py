import streamlit as st
import numpy as np
import plotly.graph_objects as go
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A4

# ---------- Page setup ----------
st.set_page_config(page_title="Soft Skills Assessment Quiz", page_icon="🧭", layout="centered")

# ---------- Soft skills + emojis ----------
SKILLS = {
    "Empathie": "🤝",
    "Pensée critique": "🧐",
    "Adaptabilité": "🦎",
    "Confiance": "🔒",
    "Intelligence émotionnelle": "💖",
    "Agilité": "⚡"
}

# Explanations for strengths
EXPLANATIONS = {
    "Empathie": "Tu comprends les autres et sais te mettre à leur place.",
    "Pensée critique": "Tu analyses, questionnes et prends des décisions rationnelles.",
    "Adaptabilité": "Tu es flexible et sais rebondir face aux imprévus.",
    "Confiance": "On peut compter sur toi, tu inspires la fiabilité.",
    "Intelligence émotionnelle": "Tu gères tes émotions et celles des autres avec finesse.",
    "Agilité": "Tu agis vite, tu prends des initiatives et tu avances."
}

# Tips for improvement
TIPS = {
    "Empathie": "Prends du temps pour écouter activement et poser des questions ouvertes.",
    "Pensée critique": "Entraîne-toi à questionner les hypothèses et chercher des sources fiables.",
    "Adaptabilité": "Expose-toi volontairement à des situations nouvelles pour renforcer ta flexibilité.",
    "Confiance": "Fixe-toi des petits défis pour bâtir une fiabilité progressive.",
    "Intelligence émotionnelle": "Travaille ta conscience émotionnelle avec des exercices de respiration.",
    "Agilité": "Apprends à tester rapidement des idées sans viser la perfection."
}

# ---------- Questions ----------
QUESTIONS = [
    {
        "id": 1,
        "text": "🚀 Ton équipe s’écrase sur Mars. Le générateur d’oxygène est HS. Première réaction ?",
        "options": [
            ("Vérifier comment va tout le monde", "Empathie"),
            ("Analyser la machine pour trouver une faille", "Pensée critique"),
            ("Réutiliser du matériel pour bricoler un plan B", "Adaptabilité"),
            ("Faire une blague pour calmer les esprits", "Intelligence émotionnelle"),
        ],
    },
    {
        "id": 2,
        "text": "🐱 Un collègue envoie un GIF de chat qui tape au clavier à 2h du matin. Ta réaction ?",
        "options": [
            ("Lui envoyer un message demain pour vérifier s’il va bien", "Empathie"),
            ("Te demander pourquoi il bosse à 2h du matin", "Pensée critique"),
            ("Penser que c’est juste un décalage horaire", "Adaptabilité"),
            ("Répondre avec un mème de soutien", "Intelligence émotionnelle"),
        ],
    },
    {
        "id": 3,
        "text": "📦 En pleine réunion, quelqu’un pose une boîte fermée à clé sur la table. Que fais-tu ?",
        "options": [
            ("Demander si quelqu’un connaît son histoire", "Confiance"),
            ("Essayer de l’ouvrir comme une énigme", "Pensée critique"),
            ("Accepter qu’elle reste fermée et passer à autre chose", "Adaptabilité"),
            ("Proposer que ce soit la mascotte de l’équipe 😂", "Agilité"),
        ],
    },
    {
        "id": 4,
        "text": "✈️ Ton voyage de rêve est annulé la veille du départ. Réaction ?",
        "options": [
            ("Refaire direct un plan B", "Adaptabilité"),
            ("Vérifier si tes potes sont pas trop déçus", "Empathie"),
            ("Chercher des alternatives malines", "Pensée critique"),
            ("Gérer ta frustration et rebondir", "Intelligence émotionnelle"),
        ],
    },
    {
        "id": 5,
        "text": "🐉 Tu trouves un bébé dragon sous ton bureau. Première instinct ?",
        "options": [
            ("Le nourrir et le rassurer", "Empathie"),
            ("L’observer avant d’agir", "Pensée critique"),
            ("Appeler ton équipe pour décider ensemble", "Confiance"),
            ("Arriver à la prochaine réunion en le montant fièrement", "Agilité"),
        ],
    },
    {
        "id": 6,
        "text": "📊 On te parachute sur un projet totalement hors de ton expertise. Ton mindset ?",
        "options": [
            ("Prendre une petite partie et apprendre vite", "Agilité"),
            ("Monter un sprint d’apprentissage pour t’adapter", "Adaptabilité"),
            ("Bosser en binôme avec un expert", "Confiance"),
            ("Reconnaître ton stress mais organiser des check-ins", "Intelligence émotionnelle"),
        ],
    },
    {
        "id": 7,
        "text": "🤐 Un collègue te confie ses doutes confidentiels sur le projet. Que fais-tu ?",
        "options": [
            ("Garder ça pour toi et l’aider à trouver un plan", "Confiance"),
            ("Lui laisser de l’espace et revenir demain", "Empathie"),
            ("Chercher la racine du problème avant de réagir", "Pensée critique"),
            ("Proposer un mini-test rapide pour valider une piste", "Agilité"),
        ],
    },
    {
        "id": 8,
        "text": "📉 Tu reçois un feedback négatif inattendu. Ta première réaction ?",
        "options": [
            ("Remercier et demander des détails", "Intelligence émotionnelle"),
            ("Séparer le bruit des signaux utiles", "Pensée critique"),
            ("Adapter ton plan pour la prochaine fois", "Adaptabilité"),
            ("Rassurer sur ton engagement et ta fiabilité", "Confiance"),
        ],
    },
    {
        "id": 9,
        "text": "🔄 Changement de scope à la dernière minute (encore 😅). Ton move ?",
        "options": [
            ("Reprioriser vite ce qui est faisable", "Adaptabilité"),
            ("Revalider les hypothèses et contraintes", "Pensée critique"),
            ("Lancer un micro-plan pour avancer quand même", "Agilité"),
            ("Clarifier les attentes avec tout le monde", "Confiance"),
        ],
    },
    {
        "id": 10,
        "text": "🏃 Tu mènes un sprint et un membre galère à suivre. Réaction ?",
        "options": [
            ("Vérifier en privé et écouter", "Empathie"),
            ("Rééquilibrer les tâches pour l’aider", "Agilité"),
            ("Reposer clairement les attentes mutuelles", "Confiance"),
            ("Identifier les goulots d’étranglement", "Pensée critique"),
        ],
    },
]

# ---------- State ----------
if "page" not in st.session_state:
    st.session_state.page = -1
if "answers" not in st.session_state:
    st.session_state.answers = {}
if "info" not in st.session_state:
    st.session_state.info = {}

# ---------- PDF Generator ----------
def generate_pdf(name, email, scores, top_skill, emoji, low_skill, chart_file):
    file_path = f"report_{name.replace(' ', '_')}.pdf"
    doc = SimpleDocTemplate(file_path, pagesize=A4)
    styles = getSampleStyleSheet()
    story = []

    story.append(Paragraph("<b>Soft Skills Report</b>", styles['Title']))
    story.append(Spacer(1, 12))
    story.append(Paragraph(f"Nom: {name}", styles['Normal']))
    story.append(Paragraph(f"Email: {email}", styles['Normal']))
    story.append(Spacer(1, 12))

    # Strength
    story.append(Paragraph(f"🏆 Ton atout majeur: {emoji} {top_skill}", styles['Heading2']))
    story.append(Paragraph(EXPLANATIONS[top_skill], styles['Normal']))
    story.append(Spacer(1, 12))

    # Weakness tip
    story.append(Paragraph(f"💡 Piste d’amélioration: {low_skill}", styles['Heading2']))
    story.append(Paragraph(TIPS[low_skill], styles['Normal']))
    story.append(Spacer(1, 12))

    # Radar chart image
    story.append(Image(chart_file, width=400, height=400))
    story.append(Spacer(1, 12))

    doc.build(story)
    return file_path

# ---------- Welcome ----------
if st.session_state.page == -1:
    st.title("🧭 Soft Skills Assessment Quiz")
    st.write("Réponds à 10 scénarios amusants et découvre ton **profil soft skills** à la fin.")

    with st.form("userinfo"):
        name = st.text_input("Prénom et Nom")
        email = st.text_input("Adresse e-mail")
        start = st.form_submit_button("🚀 Commencer le quiz")

        if start:
            if not name or not email:
                st.error("Merci de remplir au minimum **Nom + Email**.")
            else:
                st.session_state.info = {"name": name, "email": email}
                st.session_state.page = 0
                st.rerun()

# ---------- Questions ----------
elif st.session_state.page < len(QUESTIONS):
    q = QUESTIONS[st.session_state.page]
    progress = (st.session_state.page) / len(QUESTIONS)
    st.progress(progress)

    st.subheader(f"Question {st.session_state.page+1} / {len(QUESTIONS)}")
    st.write(q["text"])

    for i, (opt_text, _skill) in enumerate(q["options"]):
        if st.button(opt_text, key=f"q{q['id']}-opt{i}", use_container_width=True):
            st.session_state.answers[q["id"]] = opt_text
            st.session_state.page += 1
            st.rerun()

    if st.session_state.page > 0:
        if st.button("⬅️ Retour"):
            st.session_state.page -= 1
            st.rerun()

# ---------- Results ----------
else:
    st.success("✨ Voici ton profil !")

    # Count scores
    raw_counts = {s: 0 for s in SKILLS}
    total_per_skill = {s: 0 for s in SKILLS}
    for q in QUESTIONS:
        for _, skill in q["options"]:
            total_per_skill[skill] += 1
        chosen = st.session_state.answers.get(q["id"])
        if chosen:
            for opt_text, skill in q["options"]:
                if opt_text == chosen:
                    raw_counts[skill] += 1

    scores = {s: round(100 * raw_counts[s] / total_per_skill[s], 1) if total_per_skill[s] else 0 for s in SKILLS}

    # Top and low skills
    top_skill = max(scores, key=scores.get)
    low_skill = min(scores, key=scores.get)
    emoji = SKILLS[top_skill]

    st.markdown(
        f"## 🏆 Ton atout majeur : **{emoji} {top_skill}**\n"
        f"Bravo {st.session_state.info['name']} — voici ton profil 👇"
    )

    # ---------- Fancy Multi-Colored Radar ----------
    colors = {
        "Empathie": "#FF6F61",
        "Pensée critique": "#6A5ACD",
        "Adaptabilité": "#20B2AA",
        "Confiance": "#FFD700",
        "Intelligence émotionnelle": "#FF69B4",
        "Agilité": "#00CED1"
    }

    labels = list(SKILLS.keys())
    vals = [scores[s] for s in labels]
    vals += vals[:1]

    fig = go.Figure()

    fig.add_trace(go.Scatterpolar(
        r=vals,
        theta=labels + [labels[0]],
        fill='toself',
        line=dict(color='black', width=3),
        fillcolor='rgba(255, 182, 193, 0.4)',
        name="Profil global"
    ))

    for skill, val in scores.items():
        fig.add_trace(go.Scatterpolar(
            r=[val],
            theta=[skill],
            mode="markers+text",
            marker=dict(size=16, color=colors[skill], line=dict(width=2, color="black")),
            text=[f"{val}%"],
            textposition="top center",
            name=f"{skill}: {val}%"
        ))

    max_val = max(scores.values()) if max(scores.values()) > 0 else 100
    fig.update_layout(
        polar=dict(
            radialaxis=dict(visible=True, range=[0, max_val + 10]),
            angularaxis=dict(tickfont=dict(size=14))
        ),
        showlegend=True,
        title="🌟 Ton radar"
    )

    st.plotly_chart(fig, use_container_width=True)

    # Save chart as image for PDF
    chart_file = "radar.png"
    fig.write_image(chart_file)

    # Generate PDF
    pdf_file = generate_pdf(
        st.session_state.info["name"],
        st.session_state.info["email"],
        scores,
        top_skill,
        emoji,
        low_skill,
        chart_file
    )
    with open(pdf_file, "rb") as f:
        st.download_button("⬇️ Télécharger ton rapport PDF", f, file_name=pdf_file, mime="application/pdf")

    if st.button("🔁 Refaire le test"):
        st.session_state.page = -1
        st.session_state.answers = {}
        st.session_state.info = {}
        st.rerun()

