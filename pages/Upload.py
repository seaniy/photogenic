import streamlit as st
import boto3

# AWS S3 Configuration
# Set your AWS credentials
ACCESS_KEY = st.secrets["ACCESS_KEY"]
SECRET_KEY = st.secrets["SECRET_KEY"]
BUCKET_NAME = st.secrets["BUCKET_NAME"]
s3_client = boto3.client('s3', aws_access_key_id=ACCESS_KEY, aws_secret_access_key=SECRET_KEY)

st.set_page_config(
    page_title="Sean & Carissa's Wedding Photo Repository",
    page_icon="📷",
    layout="wide",
    initial_sidebar_state="expanded"
)

def upload_to_s3(file):
    """Uploads the given file to the S3 bucket."""
    s3_client.upload_fileobj(file, BUCKET_NAME, file.name)

def download_from_s3(filename):
    """Downloads the given filename from the S3 bucket."""
    s3_obj = s3_client.get_object(Bucket=BUCKET_NAME, Key=filename)
    return s3_obj['Body'].read()

def upload():
    # Upload Section
    st.subheader("Upload your Image")
    uploaded_file = st.file_uploader("Choose an image...", type=["jpg","png"])
    if uploaded_file is not None:
        # st.image(uploaded_file, caption="Uploaded Image.", use_column_width=True)
        if st.button("Upload to Gallery"):
            upload_to_s3(uploaded_file)
            st.balloons()
            st.success(f"Uploaded {uploaded_file.name} to S3!")
            uploaded_file = None  # Reset the uploaded_file to avoid re-uploading

upload()
