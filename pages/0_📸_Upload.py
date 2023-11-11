import streamlit as st
from PIL import Image, ImageOps
import time
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload

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

# Define the google api scope
GOOGLE_DRIVE_FOLDER_ID = st.secrets["GOOGLE_DRIVE_FOLDER_ID"]
SERVICE_ACCOUNT_FILE = 'credentials.json'
SCOPES = ['https://www.googleapis.com/auth/drive']

# Authenticate using the service account
# credentials = service_account.Credentials.from_service_account_file(
#     SERVICE_ACCOUNT_FILE, scopes = SCOPES)
credentials = service_account.Credentials.from_service_account_info(
    st.secrets["gcs_connections"], scopes = SCOPES
)

# Build the service
service = build('drive', 'v3', credentials = credentials)

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
        img = ImageOps.exif_transpose(img)

        # Display transformed image
        st.image(img, use_column_width=True)

        st.subheader("3. Confirm Upload")
        if st.button("Upload to Gallery"):
            if user_name:
                # Generate a unique filename
                unique_id = str(int(time.time()))
                ext = uploaded_file.name.split('.')[-1]
                new_filename = f"{user_name}_{unique_id}.{ext}"
                # Create a media upload object
                media = MediaIoBaseUpload(uploaded_file, mimetype=uploaded_file.type)

                # Create a new file on Google Drive
                file_metadata = {'name': new_filename, 'parents': ['1eXGKb3W5WiZcLZRxXF_72crbqoKd0MJn']}
                with st.spinner("Uploading..."):
                    file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()
                
                # success message -> refresh
                st.success(f"Uploaded {new_filename} successfully!\nRefreshing...")
                st.balloons()
                time.sleep(3)
                st.session_state["file_uploader_key"] += 1
                st.experimental_rerun()
            else:
                st.error("Please input your name")

upload()
