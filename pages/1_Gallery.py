import streamlit as st
import boto3

# AWS S3 Configuration
# Set your AWS credentials
ACCESS_KEY = st.secrets["ACCESS_KEY"]
SECRET_KEY = st.secrets["SECRET_KEY"]
BUCKET_NAME = st.secrets["BUCKET_NAME"]
s3_client = boto3.client('s3', aws_access_key_id=ACCESS_KEY, aws_secret_access_key=SECRET_KEY)

st.set_page_config(
    page_title="Gallery",
    page_icon="📷",
    layout="centered",
)

def list_files():
    """Return the list of files in the S3 bucket."""
    files = s3_client.list_objects_v2(Bucket=BUCKET_NAME)
    file_list = []
    i = 1
    if "Contents" in files:
        for content in files["Contents"]:
            file_list.append(content["Key"])
    return file_list

def download_from_s3(filename):
    """Downloads the given filename from the S3 bucket."""
    s3_obj = s3_client.get_object(Bucket=BUCKET_NAME, Key=filename)
    return s3_obj['Body'].read()

def generate_s3_url(filename):
    """Generate direct S3 URL for the given filename."""
    url = f"https://{BUCKET_NAME}.s3.amazonaws.com/{filename}"
    return url

def display():
    # Display All Images in S3 Bucket
    st.subheader("Images Gallery")
    files = list_files()
    if files:
        progress_bar = st.sidebar.progress(0)
        status_text = st.sidebar.empty().text("Loading Gallery...")
        # for filename in files:
            # image_data = download_from_s3(filename)
        for i in range(0, len(files), 2):
            col1, col2 = st.columns(2)
            
            filename1 = files[i]
            image_data1 = download_from_s3(filename1)
            status_text.text("%s%% Complete" % str((i+1)*100/len(files)))
            progress_bar.progress((i+1)/len(files))
            col1.image(image_data1, caption=filename1, use_column_width=True)
            
            if i + 1 < len(files):
                filename2 = files[i + 1]
                image_data2 = download_from_s3(filename2)
                status_text.text("%s%% Complete" % str((i+2)*100/len(files)))
                progress_bar.progress((i+2)/len(files))
                col2.image(image_data2, caption=filename2, use_column_width=True)
    else:
        st.write("No images found in the S3 bucket.")

display()
