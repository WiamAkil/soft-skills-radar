import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import io
import pandas as pd
import os

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
    st.session_state.page = -1  # -1 = welcome page
if "answers" not in st.session_state:
    st.session_state.answers = {}
if "info" not in st.session_state:
    st.session_state.info = {}

# ---------- Welcome / Info page ----------
if st.session_state.page == -1:
    st.title("🧭 Soft Skills Assessment Quiz")
    st.write("Réponds à 10 scénarios amusants et découvre ton **profil soft skills** à la fin.")

    with st.form("userinfo"):
        name = st.text_input("Prénom et Nom")
        email = st.text_input("Adresse e-mail")
        dept = st.text_input("Équipe / Département (optionnel)")
        start = st.form_submit_button("🚀 Commencer le quiz")

        if start:
            if not name or not email:
                st.error("Merci de remplir au minimum **Nom + Email**.")
            else:
                st.session_state.info = {"name": name, "email": email, "dept": dept}
                st.session_state.page = 0
                st.rerun()

# ---------- Questions ----------
elif st.session_state.page < len(QUESTIONS):
    q = QUESTIONS[st.session_state.page]
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

    scores = {
        s: round(5 * raw_counts[s] / total_per_skill[s], 2) if total_per_skill[s] else 0
        for s in SKILLS
    }

    # Dominant skill
    top_skill = max(scores, key=scores.get)
    emoji = SKILLS[top_skill]

    st.markdown(
        f"## 🏆 Ton atout majeur : **{emoji} {top_skill}**\n"
        f"Bravo {st.session_state.info['name']} — voici ton profil 👇"
    )

    # Radar chart (labels = mots simples)
    labels = list(SKILLS.keys())
    vals = [scores[s] for s in SKILLS]
    vals += vals[:1]
    angles = np.linspace(0, 2 * np.pi, len(labels) + 1)

    fig, ax = plt.subplots(figsize=(7, 7), subplot_kw=dict(polar=True))
    ax.plot(angles, vals, marker="o", linewidth=3, color="#FF6F61")
    ax.fill(angles, vals, color="#FF6F61", alpha=0.3)
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(labels, fontsize=12, weight="bold")
    ax.set_ylim(0, 5)
    ax.set_title("🌟 Ton radar des soft skills", pad=20, fontsize=16, weight="bold")

    st.pyplot(fig, clear_figure=True)

    # Save results to Excel
    df_new = pd.DataFrame([{
        "Nom": st.session_state.info["name"],
        "Email": st.session_state.info["email"],
        "Département": st.session_state.info["dept"],
        **scores
    }])

    file_path = "results.xlsx"
    if os.path.exists(file_path):
        df_existing = pd.read_excel(file_path)
        df_all = pd.concat([df_existing, df_new], ignore_index=True)
    else:
        df_all = df_new
    df_all.to_excel(file_path, index=False)

    # Download chart
    buf = io.BytesIO()
    fig.savefig(buf, format="png", dpi=180, bbox_inches="tight")
    st.download_button(
        "⬇️ Télécharger ton radar (PNG)",
        data=buf.getvalue(),
        file_name=f"radar_soft_skills_{st.session_state.info['name'].replace(' ', '_')}.png",
        mime="image/png",
    )

    if st.button("🔁 Refaire le test"):
        st.session_state.page = -1
        st.session_state.answers = {}
        st.session_state.info = {}
        st.rerun()
