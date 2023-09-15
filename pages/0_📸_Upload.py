import streamlit as st
import boto3
from PIL import Image, ImageOps
from io import BytesIO
import time

# AWS S3 Configuration
# Set your AWS credentials
ACCESS_KEY = st.secrets["ACCESS_KEY"]
SECRET_KEY = st.secrets["SECRET_KEY"]
BUCKET_NAME = st.secrets["BUCKET_NAME"]
s3_client = boto3.client('s3', aws_access_key_id=ACCESS_KEY, aws_secret_access_key=SECRET_KEY)

st.set_page_config(
    page_title="Upload",
    page_icon="📷",
)

hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

def upload_to_s3(file, filename):
    """Uploads the given file to the S3 bucket."""
    s3_client.upload_fileobj(file, BUCKET_NAME, filename)

def upload():
    if "file_uploader_key" not in st.session_state:
        st.session_state["file_uploader_key"] = 0

    # User's name input
    st.subheader("1. Input Your Name")
    user_name = st.text_input("Enter your name:")
    # Upload Section
    st.subheader("2. Upload Your Image")
    uploaded_file = st.file_uploader("Choose an image...", type=["jpg","png"], key=st.session_state["file_uploader_key"])
    if uploaded_file:
        # Convert uploaded file to PIL image
        img = Image.open(uploaded_file)
        # st.image(img, caption="Uploaded Image.", use_column_width=True)

        # Orientation edit options
        st.subheader("3. Edit Image Orientation")
        rotation_options = st.radio("Rotate Image", ["No rotation", "90°", "180°", "270°"])
        flip_option = st.radio("Flip Image", ["No flip", "Horizontal", "Vertical"])

        # Apply transformations based on user choices
        if rotation_options == "90°":
            img = img.rotate(-90, expand=True)
        elif rotation_options == "180°":
            img = img.rotate(-180, expand=True)
        elif rotation_options == "270°":
            img = img.rotate(-270, expand=True)

        if flip_option == "Horizontal":
            img = ImageOps.mirror(img)
        elif flip_option == "Vertical":
            img = ImageOps.flip(img)

        # Display transformed image
        st.image(img, caption="Transformed Image.", use_column_width=True)

        st.subheader("4. Confirm Upload")
        if st.button("Upload to Gallery"):
            if user_name:
                progress_bar = st.progress(0)
                status_text = st.text("Refreshing...")
                # Generate a unique filename
                unique_id = str(int(time.time()))
                ext = uploaded_file.name.split('.')[-1]
                new_filename = f"{user_name}_{unique_id}.{ext}"

                # Convert the PIL image back to a byte stream for uploading
                buffer = BytesIO()
                img_format = "PNG" if uploaded_file.name.endswith(".png") else "JPEG"
                img.save(buffer, format=img_format)
                buffer.seek(0)

                upload_to_s3(buffer, new_filename)
                st.success(f"Uploaded {new_filename} successfully!")
                st.balloons()
                for i in range(1, 4):
                    progress_bar.text("%i%%" % (100/3*i))
                    status_text.progress(i/3)
                    time.sleep(1)
                st.session_state["file_uploader_key"] += 1
                st.experimental_rerun()
            else:
                st.error("Please input your name")
    # if uploaded_file is not None:
    #     # st.image(uploaded_file, caption="Uploaded Image.", use_column_width=True)
    #     if st.button("Upload to Gallery"):
    #         upload_to_s3(uploaded_file)
    #         st.balloons()
    #         st.success(f"Successfully uploaded {uploaded_file.name}!")
    #         uploaded_file = None  # Reset the uploaded_file to avoid re-uploading

upload()
