import streamlit as st
from PIL import Image
import tempfile
import os
from fpdf import FPDF
import cv2
import numpy as np

# ✅ Streamlit config
st.set_page_config(page_title="🧸 Life Rewind", layout="centered", initial_sidebar_state="collapsed")

# ✅ Simple Sign-in / Sign-up simulation
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.title("🔐 Welcome to Life Rewind")
    menu = st.radio("Login or Register", ["Login", "Register"], horizontal=True)

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if menu == "Register":
        if st.button("Register"):
            st.success("✅ Registered successfully! Now login.")
    else:
        if st.button("Login"):
            if username and password:
                st.session_state.logged_in = True
                st.success("🎉 Logged in successfully!")
                st.rerun()
            else:
                st.error("❌ Please enter both fields.")
    st.stop()

# ✅ Theme toggle
theme = st.radio("🎨 Select Theme", ["Light", "Dark"], horizontal=True, index=0)

if theme == "Light":
    background = "#f9f9f9"
    text_color = "#222222"
else:
    background = "#1a1a1a"
    text_color = "#ffffff"

# ✅ CSS
st.markdown(f"""
    <style>
        .block-container {{
            padding-top: 1rem !important;
        }}
        header, footer {{
            visibility: hidden;
            height: 0px;
        }}
        h1, p, label, .stRadio, .stButton, .stTextArea label {{
            color: {text_color} !important;
        }}
    </style>
""", unsafe_allow_html=True)

# ✅ Title
st.markdown(f"""
    <h1 style='text-align: center; color: white; font-size: 48px;'>🧸 Life Rewind</h1>
    <p style='text-align: center; font-size: 16px; color: {text_color};'>Reconstruct your fictional childhood from a selfie!</p>
""", unsafe_allow_html=True)

# ✅ Upload selfie
uploaded_file = st.file_uploader("📸 Upload your selfie", type=["jpg", "jpeg", "png"])

if uploaded_file:
    img = Image.open(uploaded_file)
    st.image(img, caption="👶 Your uploaded selfie", use_container_width=True)

    with st.spinner("🔍 Analyzing face..."):
        age = 10
        gender = "Female"
        race = "Indian"
        st.success(f"🎯 Age: {age}, Gender: {gender}, Ethnicity: {race}")
        st.warning("⚠️ Face analysis is mocked for demo.")

    # ✅ Generate diary
    st.markdown("### 📖 AI-Generated Childhood Diary")

    story = (
        "Dear Diary,\n\nThey used to call me Chinki at home. I still remember spilling ink on my homework and pretending it was modern art. "
        "I once brought my pet turtle to class, and the teacher screamed louder than the fire drill. I always loved tamarind candies and aloo paratha.\n\n"
        "My favorite memory? Dancing to 'Lakdi Ki Kaathi' in front of the whole family during Diwali."
    )

    st.text_area("📝 Diary Entry", story, height=300)

    # ✅ Cartoonized Childhood Photo
    st.markdown("### 🧒 Cartoonized Childhood Photo")
    image = np.array(img.convert('RGB'))
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    cartoon = cv2.stylization(image, sigma_s=150, sigma_r=0.25)
    cartoon_rgb = cv2.cvtColor(cartoon, cv2.COLOR_BGR2RGB)
    st.image(cartoon_rgb, caption="🎨 Cartoon Version", use_container_width=True)

    # ✅ Download diary
    if story and st.button("📄 Download Diary as PDF"):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.multi_cell(0, 10, story)
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
            pdf.output(tmp_file.name)
            with open(tmp_file.name, "rb") as file:
                st.download_button(
                    label="⬇️ Download PDF",
                    data=file,
                    file_name="life_rewind_diary.pdf",
                    mime="application/pdf"
                )
        os.remove(tmp_file.name)

# ✅ Quiz Section
st.markdown("### 🎯 Mini Quiz: How Well Do You Remember Your Childhood?")

questions = [
    {"q": "👶 What is the name of the bear in 'The Jungle Book'?", "options": ["Baloo", "Bing Bong", "Pooh", "Kaa"], "answer": "Baloo"},
    {"q": "🧃 What drink came with a straw poked through a box?", "options": ["Coke", "Pepsi", "Frooti", "Red Bull"], "answer": "Frooti"},
    {"q": "📺 Which cartoon featured a robot cat from the future?", "options": ["Pokemon", "Doraemon", "Ben 10", "Tom & Jerry"], "answer": "Doraemon"},
    {"q": "✏️ What was the most popular exam pencil?", "options": ["Apsara", "Nataraj", "Faber-Castell", "Camlin"], "answer": "Nataraj"},
    {"q": "🎒 Which bag brand was every kid crazy for?", "options": ["Skybags", "American Tourister", "VIP", "Wildcraft"], "answer": "Skybags"},
    {"q": "🍫 Which chocolate was known for layers and crisp?", "options": ["5 Star", "Munch", "Perk", "KitKat"], "answer": "Munch"},
    {"q": "📻 Which music player did we use before Spotify?", "options": ["Walkman", "BoomBox", "JioSaavn", "MP3 Discman"], "answer": "Walkman"},
    {"q": "📱 Which mobile game did 2000s kids love the most?", "options": ["Subway Surfers", "Angry Birds", "Snake", "Temple Run"], "answer": "Snake"},
    {"q": "📖 What would your slam book friends write?", "options": ["Best of luck", "BFFL", "Keep in touch", "All of the above"], "answer": "All of the above"},
    {"q": "🏏 What cricket bat did most school kids use?", "options": ["Kookaburra", "SS", "MRF", "Cosco"], "answer": "Cosco"}
]

user_answers = {}
for i, q in enumerate(questions):
    with st.expander(f"Q{i+1}: {q['q']}"):
        user_answers[i] = st.radio("Choose one:", q["options"], key=f"user_q{i}")

if st.button("✅ Submit Quiz"):
    score = 0
    st.markdown("### 🧾 Quiz Results:")
    for i, q in enumerate(questions):
        user_ans = user_answers.get(i)
        correct_ans = q["answer"]
        is_correct = user_ans == correct_ans

        st.write(f"**Q{i+1}: {q['q']}**")
        st.write(f"Your answer: `{user_ans}`")
        if is_correct:
            st.success("✅ Correct!")
            score += 1
        else:
            st.error(f"❌ Correct answer: `{correct_ans}`")

    st.markdown(f"## 🏆 Final Score: `{score}/10`")
    if score >= 8:
        st.balloons()
        st.success("🥳 You're a certified childhood nostalgia master!")
    elif score >= 5:
        st.info("👍 Good job! You remember quite a bit!")
    else:
        st.warning("😅 Time to refresh those memories!")
else:
    st.info("📌 Answer all questions, then click **Submit Quiz** to see your score!")

# ✅ Footer
st.markdown("---")
st.image("https://media.tenor.com/IznDmFtVqFgAAAAC/baby-milk.gif", width=150)
st.markdown("""
<center>
    Made with ❤️ for your memories.<br>
    🙌 Thanks for visiting Life Rewind!<br>
    Come back soon and enjoy reliving your memories again.
    Byeeee
</center>
""", unsafe_allow_html=True)
