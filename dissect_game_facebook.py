import streamlit as st
import random
import csv

# Sections and simplified text based on the 2014 Facebook loneliness meta-analysis
sections = {
    "Abstract": {
        "text": "This meta-analysis looked at 18 studies with 8,798 participants to find out if using Facebook makes people feel more or less lonely. The study found a small but significant positive correlation: more Facebook use was linked with more loneliness. The analysis also explored whether loneliness causes people to use Facebook more, or if using Facebook leads to loneliness.",
        "question": "What was the main purpose of the abstract?",
        "options": ["To present detailed statistics", "To summarize the study's purpose and results", "To explain the methods"],
        "answer": "To summarize the study's purpose and results",
        "explanation": "The abstract provides a concise overview of the entire study including its aims, methods, and key findings."
    },
    "Introduction": {
        "text": "Facebook is the most-used social networking site. Some researchers believe it helps reduce loneliness by supporting social interaction, while others argue it increases loneliness by replacing in-person contact. Because past studies showed mixed results, the authors conducted a meta-analysis to find clearer answers.",
        "question": "What is the role of the introduction in a research article?",
        "options": ["To analyze results", "To explain statistical tests", "To provide background and rationale for the study"],
        "answer": "To provide background and rationale for the study",
        "explanation": "The introduction sets up the research question by reviewing past studies and identifying gaps or inconsistencies."
    },
    "Methods": {
        "text": "The researchers searched databases for studies using keywords like 'Facebook' and 'loneliness.' They only included studies with quantitative data that could be used to calculate effect sizes. Different ways of measuring Facebook use and loneliness were categorized, including time spent, compulsive use, and various loneliness scales.",
        "question": "Which best describes a key part of the Methods section?",
        "options": ["Describing survey results", "Explaining how data was collected and selected", "Summarizing prior research"],
        "answer": "Explaining how data was collected and selected",
        "explanation": "The methods describe how the researchers gathered and processed the data used in the study."
    },
    "Results": {
        "text": "The overall correlation between Facebook use and loneliness was small but positive (r = .166). People who used Facebook more tended to report more loneliness. This effect varied depending on how Facebook use and loneliness were measured. The best-fitting model suggested that loneliness causes people to use Facebook—not the other way around.",
        "question": "What does the Results section do in a research article?",
        "options": ["Offers opinions", "Presents data and findings", "Explains theoretical implications"],
        "answer": "Presents data and findings",
        "explanation": "The Results section objectively presents the study’s findings using statistics and data summaries."
    },
    "Discussion": {
        "text": "The authors concluded that lonely people are more likely to use Facebook as a way to feel connected. This supports the 'social compensation' model. They emphasized that more research is needed to examine long-term effects and differences across age groups.",
        "question": "What is the main role of the Discussion section?",
        "options": ["To present raw data", "To connect results to larger theories", "To restate the method"],
        "answer": "To connect results to larger theories",
        "explanation": "The discussion interprets results, suggests implications, and recommends areas for future study."
    }
}

# Set up Streamlit state
if "score" not in st.session_state:
    st.session_state.score = 0
    st.session_state.round = 0
    st.session_state.history = []

st.set_page_config(page_title="Facebook & Loneliness Game", layout="centered")
st.title("📘 Facebook & Loneliness: Research Dissection Game")
st.markdown("Explore and learn from a real journal article. Match each excerpt to its section, and test your knowledge.")

# Random section for this round
section_name, section_data = random.choice(list(sections.items()))
st.session_state.round += 1

st.subheader(f"🔎 Round {st.session_state.round}: Read This Excerpt")
st.info(section_data["text"])

user_guess = st.selectbox("Which section is this from?", list(sections.keys()))
submit_guess = st.button("Submit Answer")

if submit_guess:
    correct = user_guess == section_name
    if correct:
        st.success(f"✅ Correct! This is the **{section_name}** section.")
        st.session_state.score += 1
    else:
        st.error(f"❌ Nope — this is actually from the **{section_name}** section.")

    with st.expander("🧠 Explanation"):
        st.write(section_data["explanation"])

    st.subheader("🧪 Bonus Question")
    st.write(section_data["question"])
    answer = st.radio("Choose your answer:", section_data["options"], key=f"bonus_{st.session_state.round}")
    submit_bonus = st.button("Submit Bonus", key=f"submit_bonus_{st.session_state.round}")

    if submit_bonus:
        correct_bonus = answer == section_data["answer"]
        if correct_bonus:
            st.success("🎉 Correct! You earned an extra point.")
            st.session_state.score += 1
        else:
            st.error(f"🧐 Not quite. The correct answer is: **{section_data['answer']}**")

        with st.expander("📘 Bonus Explanation"):
            st.write(section_data["explanation"])

        st.session_state.history.append({
            "round": st.session_state.round,
            "guess": user_guess,
            "correct_section": section_name,
            "bonus_answer": answer,
            "correct_bonus": section_data["answer"],
            "score": st.session_state.score
        })

        if st.button("Next Round ▶️"):
            st.experimental_rerun()

# Download CSV
if st.session_state.history:
    st.subheader("📥 Download Results")
    with open("results.csv", "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=st.session_state.history[0].keys())
        writer.writeheader()
        writer.writerows(st.session_state.history)

    with open("results.csv", "rb") as f:
        st.download_button("Download CSV", f, "facebook_game_results.csv", mime="text/csv")

st.sidebar.markdown("### 🎯 Your Progress")
st.sidebar.write(f"**Rounds Played:** {st.session_state.round}")
st.sidebar.write(f"**Total Score:** {st.session_state.score}")