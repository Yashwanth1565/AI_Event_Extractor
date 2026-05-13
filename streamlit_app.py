import streamlit as st

from app.main import process_event_input

# ---------- PAGE CONFIG ---------- #

st.set_page_config(
    page_title="AI Event Information Extractor",
    page_icon="🎬",
    layout="centered"
)

# ---------- CUSTOM CSS ---------- #

st.markdown("""
<style>

/* Main Background */

.stApp {
    background: linear-gradient(
        135deg,
        #0f0f0f,
        #141e30,
        #243b55
    );
    color: white;
}

/* Remove Streamlit Default */

#MainMenu {
    visibility: hidden;
}

footer {
    visibility: hidden;
}

header {
    visibility: hidden;
}

/* Main Title */

.main-title {
    text-align: center;
    font-size: 3rem;
    font-weight: 800;
    color: white;
    margin-top: 10px;
    margin-bottom: 10px;
    letter-spacing: 1px;
}

/* Subtitle */

.subtitle {
    text-align: center;
    font-size: 1.1rem;
    color: #d1d5db;
    margin-bottom: 40px;
}

/* Glass Container */

.glass-box {
    background: rgba(255,255,255,0.08);
    padding: 30px;
    border-radius: 24px;
    backdrop-filter: blur(14px);
    border: 1px solid rgba(255,255,255,0.12);
    box-shadow: 0px 8px 32px rgba(0,0,0,0.4);
}

/* Button */

.stButton>button {
    width: 100%;
    border-radius: 14px;
    height: 3.2em;
    font-size: 18px;
    font-weight: bold;
    border: none;
    background: linear-gradient(
        90deg,
        #00c6ff,
        #0072ff
    );
    color: white;
    transition: 0.3s ease-in-out;
}

.stButton>button:hover {
    transform: scale(1.02);
    box-shadow: 0px 0px 20px rgba(0,114,255,0.5);
}

/* Text Area */

textarea {
    background-color: rgba(255,255,255,0.05) !important;
    color: white !important;
    border-radius: 12px !important;
}

/* Upload Box */

[data-testid="stFileUploader"] {
    background-color: rgba(255,255,255,0.05);
    padding: 15px;
    border-radius: 15px;
}

/* JSON Output */

[data-testid="stJson"] {
    background: rgba(255,255,255,0.06);
    border-radius: 16px;
    padding: 15px;
}

/* Footer */

.footer {
    text-align: center;
    margin-top: 40px;
    color: #cbd5e1;
    font-size: 0.9rem;
}

</style>
""", unsafe_allow_html=True)

# ---------- HEADER ---------- #

st.markdown(
    """
    <div class="main-title">
        🎬 AI Event Information Extractor
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <div class="subtitle">
        Extract structured event information from text, posters, banners, and conference flyers using Generative AI.
    </div>
    """,
    unsafe_allow_html=True
)

# ---------- GLASS CARD ---------- #

st.markdown('<div class="glass-box">', unsafe_allow_html=True)

# ---------- TEXT INPUT ---------- #

event_text = st.text_area(
    "📝 Enter Event Description",
    placeholder="Example: Join us for the AI Summit on July 20 at 10 AM in Hyderabad hosted by TechNova."
)

# ---------- IMAGE UPLOAD ---------- #

uploaded_file = st.file_uploader(
    "🖼 Upload Poster/Image",
    type=["png", "jpg", "jpeg"]
)

# ---------- IMAGE PREVIEW ---------- #

if uploaded_file is not None:

    st.image(
        uploaded_file,
        caption="Uploaded Event Poster",
        use_container_width=True
    )

# ---------- BUTTON ---------- #

if st.button("✨ Extract Event Information"):

    if (
        event_text.strip() == ""
        and uploaded_file is None
    ):

        st.warning(
            "Please enter event text or upload an image."
        )

    else:

        with st.spinner(
            "Analyzing event details using AI..."
        ):

            result = process_event_input(
                text=event_text,
                image=uploaded_file
            )

        # ---------- OUTPUT ---------- #

        if "error" not in result:

            st.success(
                "Extraction Completed Successfully"
            )

        else:

            st.error(
                "Extraction completed with issue."
            )

        st.json(result)

st.markdown('</div>', unsafe_allow_html=True)

# ---------- FOOTER ---------- #

st.markdown(
    """
    <div class="footer">
        Built with ❤️ using Streamlit + Groq + LangFuse
    </div>
    """,
    unsafe_allow_html=True
)