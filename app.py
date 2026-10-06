import streamlit as st
from deepface import DeepFace
from PIL import Image
import tempfile
import os

# ---------------------------------------------------------
# PAGE CONFIGURATION
# ---------------------------------------------------------
st.set_page_config(
    page_title="AI Emotion Detector",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------------------------------------------------
# CUSTOM CSS
# ---------------------------------------------------------
st.markdown("""
<style>

    /* Main background */
    .stApp {
        background:
            radial-gradient(circle at 10% 10%, rgba(99,102,241,0.15), transparent 25%),
            radial-gradient(circle at 90% 20%, rgba(168,85,247,0.12), transparent 25%),
            #0b1020;
        color: #ffffff;
    }

    /* Hide Streamlit default menu/footer */
    #MainMenu {
        visibility: hidden;
    }

    footer {
        visibility: hidden;
    }

    header {
        background: transparent !important;
    }

    /* Main title */
    .main-title {
        text-align: center;
        font-size: 3.2rem;
        font-weight: 800;
        margin-top: 10px;
        margin-bottom: 5px;
        background: linear-gradient(
            90deg,
            #60a5fa,
            #a78bfa,
            #f472b6
        );
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    .subtitle {
        text-align: center;
        color: #b8c1d9;
        font-size: 1.1rem;
        margin-bottom: 35px;
    }

    /* Glass cards */
    .glass-card {
        background: rgba(255,255,255,0.06);
        border: 1px solid rgba(255,255,255,0.10);
        border-radius: 20px;
        padding: 25px;
        backdrop-filter: blur(12px);
        box-shadow: 0 10px 35px rgba(0,0,0,0.25);
        margin-bottom: 20px;
    }

    /* Emotion result */
    .emotion-card {
        text-align: center;
        padding: 30px;
        border-radius: 24px;
        background: linear-gradient(
            135deg,
            rgba(99,102,241,0.22),
            rgba(168,85,247,0.15)
        );
        border: 1px solid rgba(167,139,250,0.25);
        box-shadow: 0 15px 40px rgba(0,0,0,0.3);
    }

    .emotion-emoji {
        font-size: 5rem;
        margin-bottom: 5px;
    }

    .emotion-name {
        font-size: 2.5rem;
        font-weight: 800;
        color: #ffffff;
        text-transform: uppercase;
    }

    .confidence {
        font-size: 1.2rem;
        color: #c4b5fd;
        margin-top: 8px;
    }

    /* Section titles */
    .section-title {
        font-size: 1.5rem;
        font-weight: 700;
        color: #e2e8f0;
        margin-top: 10px;
        margin-bottom: 15px;
    }

    /* Feature cards */
    .feature-card {
        background: rgba(255,255,255,0.055);
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 16px;
        padding: 20px;
        text-align: center;
        min-height: 150px;
    }

    .feature-icon {
        font-size: 2.2rem;
    }

    .feature-title {
        font-size: 1.05rem;
        font-weight: 700;
        margin-top: 8px;
        color: #ffffff;
    }

    .feature-text {
        color: #9ca8c0;
        font-size: 0.9rem;
        margin-top: 5px;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background:
            linear-gradient(
                180deg,
                #11182d 0%,
                #0b1020 100%
            );
        border-right: 1px solid rgba(255,255,255,0.08);
    }

    /* Buttons */
    .stButton > button {
        border-radius: 12px;
        border: 1px solid rgba(255,255,255,0.12);
        background: linear-gradient(90deg, #6366f1, #8b5cf6);
        color: white;
        font-weight: 700;
        padding: 10px 22px;
    }

    .stButton > button:hover {
        border-color: #a78bfa;
        box-shadow: 0 0 20px rgba(139,92,246,0.35);
    }

    /* Footer */
    .custom-footer {
        text-align: center;
        padding: 30px 10px 10px 10px;
        color: #77829b;
        font-size: 0.9rem;
    }

    /* Info box */
    .info-box {
        padding: 15px;
        border-radius: 14px;
        background: rgba(96,165,250,0.08);
        border: 1px solid rgba(96,165,250,0.15);
        color: #cbd5e1;
    }

</style>
""", unsafe_allow_html=True)


# ---------------------------------------------------------
# EMOTION INFORMATION
# ---------------------------------------------------------
EMOTION_DATA = {
    "happy": {
        "emoji": "😊",
        "description": "The face appears happy and positive."
    },
    "sad": {
        "emoji": "😢",
        "description": "The face appears sad or emotionally low."
    },
    "angry": {
        "emoji": "😡",
        "description": "The face appears angry or frustrated."
    },
    "fear": {
        "emoji": "😨",
        "description": "The face appears fearful or anxious."
    },
    "surprise": {
        "emoji": "😲",
        "description": "The face appears surprised or shocked."
    },
    "disgust": {
        "emoji": "🤢",
        "description": "The face appears to show disgust."
    },
    "neutral": {
        "emoji": "😐",
        "description": "The face appears emotionally neutral."
    }
}


# ---------------------------------------------------------
# SIDEBAR
# ---------------------------------------------------------
with st.sidebar:

    st.markdown(
        """
        <h2 style="text-align:center;">🧠 AI Emotion</h2>
        <p style="text-align:center;color:#9ca8c0;">
        Facial Emotion Recognition
        </p>
        """,
        unsafe_allow_html=True
    )

    st.markdown("---")

    st.markdown("### ⚙️ Technology")

    st.markdown("""
    **Python**  
    **Streamlit**  
    **DeepFace**  
    **TensorFlow**  
    **OpenCV**
    """)

    st.markdown("---")

    st.markdown("### 🎯 Supported Emotions")

    emotions = [
        "😊 Happy",
        "😢 Sad",
        "😡 Angry",
        "😨 Fear",
        "😲 Surprise",
        "🤢 Disgust",
        "😐 Neutral"
    ]

    for emotion in emotions:
        st.write(emotion)

    st.markdown("---")

    st.markdown(
        """
        <div class="info-box">
        <b>💡 How it works</b><br><br>
        Upload or capture a face image. The AI model analyzes
        facial expressions and predicts the most likely emotion.
        </div>
        """,
        unsafe_allow_html=True
    )


# ---------------------------------------------------------
# HEADER
# ---------------------------------------------------------
st.markdown(
    '<div class="main-title">🧠 AI Emotion Detector</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">Understand human emotions using Artificial Intelligence & Computer Vision</div>',
    unsafe_allow_html=True
)


# ---------------------------------------------------------
# FEATURE CARDS
# ---------------------------------------------------------
col1, col2, col3, col4 = st.columns(4)

features = [
    ("📷", "Image Analysis", "Analyze facial expressions from images."),
    ("🤖", "AI Powered", "DeepFace and TensorFlow based detection."),
    ("📊", "Confidence", "View emotion prediction confidence."),
    ("⚡", "Fast Results", "Get predictions within seconds.")
]

for col, (icon, title, text) in zip(
    [col1, col2, col3, col4],
    features
):
    with col:
        st.markdown(
            f"""
            <div class="feature-card">
                <div class="feature-icon">{icon}</div>
                <div class="feature-title">{title}</div>
                <div class="feature-text">{text}</div>
            </div>
            """,
            unsafe_allow_html=True
        )


st.markdown("<br>", unsafe_allow_html=True)


# ---------------------------------------------------------
# INPUT SECTION
# ---------------------------------------------------------
st.markdown(
    '<div class="section-title">📸 Analyze a Face</div>',
    unsafe_allow_html=True
)

input_col1, input_col2 = st.columns(2)

with input_col1:

    st.markdown(
        """
        <div class="glass-card">
        <h3>📁 Upload Image</h3>
        <p style="color:#9ca8c0;">
        Upload a JPG, JPEG or PNG image containing a face.
        </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    uploaded_file = st.file_uploader(
        "Choose an image",
        type=["jpg", "jpeg", "png"],
        label_visibility="collapsed"
    )


with input_col2:

    st.markdown(
        """
        <div class="glass-card">
        <h3>📷 Camera</h3>
        <p style="color:#9ca8c0;">
        Take a photo directly using your camera.
        </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    camera_image = st.camera_input(
        "Take a picture",
        label_visibility="collapsed"
    )


# ---------------------------------------------------------
# SELECT IMAGE
# ---------------------------------------------------------
image_source = uploaded_file if uploaded_file else camera_image


# ---------------------------------------------------------
# ANALYSIS
# ---------------------------------------------------------
if image_source:

    st.markdown("---")

    st.markdown(
        '<div class="section-title">🔍 Analysis Result</div>',
        unsafe_allow_html=True
    )

    result_col1, result_col2 = st.columns([1, 1])

    # Save uploaded/captured image temporarily
    image = Image.open(image_source)

    with result_col1:

        st.image(
            image,
            caption="Analyzed Image",
            use_container_width=True
        )

    with result_col2:

        with st.spinner("🤖 AI is analyzing the facial expression..."):

            temp_file = tempfile.NamedTemporaryFile(
                delete=False,
                suffix=".jpg"
            )

            image.convert("RGB").save(temp_file.name)

            try:

                analysis = DeepFace.analyze(
                    img_path=temp_file.name,
                    actions=["emotion"],
                    enforce_detection=False
                )

                # DeepFace can return either a dictionary or list
                if isinstance(analysis, list):
                    analysis = analysis[0]

                emotion_scores = analysis["emotion"]

                dominant_emotion = analysis["dominant_emotion"]

                confidence = emotion_scores[dominant_emotion]

                emotion_info = EMOTION_DATA.get(
                    dominant_emotion.lower(),
                    {
                        "emoji": "🧠",
                        "description": "Emotion detected."
                    }
                )

                st.markdown(
                    f"""
                    <div class="emotion-card">

                        <div class="emotion-emoji">
                            {emotion_info["emoji"]}
                        </div>

                        <div class="emotion-name">
                            {dominant_emotion}
                        </div>

                        <div class="confidence">
                            Confidence: <b>{confidence:.2f}%</b>
                        </div>

                        <p style="color:#aeb9cf;margin-top:15px;">
                            {emotion_info["description"]}
                        </p>

                    </div>
                    """,
                    unsafe_allow_html=True
                )

            except Exception as e:

                st.error(
                    "Unable to analyze the image. "
                    "Please try another image containing a clear face."
                )

                st.code(str(e))

                emotion_scores = None

            finally:

                try:
                    os.remove(temp_file.name)
                except:
                    pass


    # -----------------------------------------------------
    # EMOTION PROBABILITIES
    # -----------------------------------------------------
    if emotion_scores:

        st.markdown("---")

        st.markdown(
            '<div class="section-title">📊 Emotion Analysis</div>',
            unsafe_allow_html=True
        )

        # Sort emotions from highest to lowest
        sorted_emotions = sorted(
            emotion_scores.items(),
            key=lambda x: x[1],
            reverse=True
        )

        # Create two columns
        left_col, right_col = st.columns(2)

        for index, (emotion, score) in enumerate(sorted_emotions):

            target_col = left_col if index % 2 == 0 else right_col

            with target_col:

                emoji = EMOTION_DATA.get(
                    emotion.lower(),
                    {"emoji": "🧠"}
                )["emoji"]

                st.markdown(
                    f"""
                    <div style="
                        display:flex;
                        justify-content:space-between;
                        align-items:center;
                        margin-top:12px;
                        margin-bottom:3px;
                    ">
                        <span style="font-weight:600;">
                            {emoji} {emotion.title()}
                        </span>

                        <span style="color:#aeb9cf;">
                            {score:.2f}%
                        </span>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

                st.progress(
                    min(int(score), 100)
                )


# ---------------------------------------------------------
# ABOUT PROJECT
# ---------------------------------------------------------
st.markdown("---")

st.markdown(
    '<div class="section-title">🚀 About This Project</div>',
    unsafe_allow_html=True
)

about_col1, about_col2 = st.columns(2)

with about_col1:

    st.markdown(
        """
        <div class="glass-card">

        <h3>🧠 What is Emotion Detection?</h3>

        <p style="color:#b8c1d9;line-height:1.7;">

        Emotion detection is an Artificial Intelligence technique
        that analyzes facial expressions and predicts the emotional
        state represented by a person's face.

        </p>

        <p style="color:#b8c1d9;line-height:1.7;">

        This project uses DeepFace and TensorFlow to analyze facial
        expressions and identify seven common emotions.

        </p>

        </div>
        """,
        unsafe_allow_html=True
    )


with about_col2:

    st.markdown(
        """
        <div class="glass-card">

        <h3>⚙️ Technologies Used</h3>

        <p style="color:#b8c1d9;line-height:2;">

        🐍 <b>Python</b> — Programming language<br>
        🎨 <b>Streamlit</b> — Interactive web interface<br>
        🤖 <b>DeepFace</b> — Facial analysis framework<br>
        🧠 <b>TensorFlow</b> — Machine learning backend<br>
        📷 <b>OpenCV</b> — Computer vision

        </p>

        </div>
        """,
        unsafe_allow_html=True
    )


# ---------------------------------------------------------
# FOOTER
# ---------------------------------------------------------
st.markdown(
    """
    <div class="custom-footer">

        <b>🧠 AI-Based Emotion Detection System</b><br>

        Built with Python • Streamlit • DeepFace • TensorFlow • OpenCV

        <br><br>

        Made with ❤️ for AI & Computer Vision

    </div>
    """,
    unsafe_allow_html=True
)