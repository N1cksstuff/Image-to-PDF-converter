import streamlit as st
import time
from PIL import Image
import io

st.session_state.uploaded = False
st.title("Image to PDF :grey Converter :rocket:")

with st.chat_message("user"):
    st.write("Hello!")
    st.write("To convert images to PDF, please upload your images below.")

uploaded_files = st.file_uploader(
    "Choose Image files", accept_multiple_files=True
)
if uploaded_files:
    st.session_state.uploaded = True
    st.write("You have uploaded the following images:")
for uploaded_file in uploaded_files:
    bytes_data = uploaded_file.read()
    st.write("filename:", uploaded_file.name)
    st.image(bytes_data, caption=uploaded_file.name, use_container_width=True)


if st.session_state.uploaded == True:
    with st.chat_message("user"):
        st.write("Great!")
        st.write("If everything looks correct, click this button to put it all in one PDF!")

if st.button("Convert to PDF"):
    with st.chat_message("assistant"):
        st.write("Converting your images to PDF...")
        
        # Create a list to store the images
        images = []
        
        # Reset the file pointers and read the images
        for uploaded_file in uploaded_files:
            uploaded_file.seek(0)
            img = Image.open(uploaded_file)
            # Convert to RGB mode if necessary (for PNG transparency)
            if img.mode != 'RGB':
                img = img.convert('RGB')
            images.append(img)
        
        # Create PDF in memory
        pdf_buffer = io.BytesIO()
        if images:  # Check if there are any images
            # Save the first image as PDF with the remaining images appended
            images[0].save(
                pdf_buffer,
                format='PDF',
                save_all=True,
                append_images=images[1:]
            )
            
            # Get the PDF value for the download button
            pdf_data = pdf_buffer.getvalue()
            st.write("Your images have been converted to PDF!")
            st.write("Download your PDF below:")

            st.download_button(
                label="Download PDF",
                data=pdf_data,
                file_name="converted_images.pdf",
                mime="application/pdf"
            )
        else:
            st.error("Please upload some images first!")
