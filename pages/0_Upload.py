import streamlit as st
import boto3
from PIL import Image, ImageOps
from io import BytesIO

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

def upload_to_s3(file, filename):
    """Uploads the given file to the S3 bucket."""
    s3_client.upload_fileobj(file, BUCKET_NAME, filename)

def upload():
    # Upload Section
    st.subheader("Upload your Image")
    uploaded_file = st.file_uploader("Choose an image...", type=["jpg","png"])
    if uploaded_file:
        # Convert uploaded file to PIL image
        img = Image.open(uploaded_file)
        # st.image(img, caption="Uploaded Image.", use_column_width=True)

        # Orientation edit options
        st.subheader("Edit Image Orientation")
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

        if st.button("Upload to Gallery"):
            # Convert the PIL image back to a byte stream for uploading
            buffer = BytesIO()
            img_format = "PNG" if uploaded_file.name.endswith(".png") else "JPEG"
            img.save(buffer, format=img_format)
            buffer.seek(0)

            upload_to_s3(buffer, uploaded_file.name)
            st.success(f"Uploaded {uploaded_file.name} successfully!")
            st.balloons()
    # if uploaded_file is not None:
    #     # st.image(uploaded_file, caption="Uploaded Image.", use_column_width=True)
    #     if st.button("Upload to Gallery"):
    #         upload_to_s3(uploaded_file)
    #         st.balloons()
    #         st.success(f"Successfully uploaded {uploaded_file.name}!")
    #         uploaded_file = None  # Reset the uploaded_file to avoid re-uploading

upload()
