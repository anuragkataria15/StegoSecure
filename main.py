import streamlit as st
from steg import hide_data, extract_data
from crypto import encrypt_message, decrypt_message
import os

st.set_page_config(page_title="StegoSecure", layout="centered")
st.title("🔐 StegoSecure - Hide Encrypted Messages in Images")

tab1, tab2 = st.tabs(["🔏 Hide Message", "🔓 Extract Message"])

with tab1:
    st.header("🔏 Hide & Encrypt")
    uploaded_img = st.file_uploader("Upload an Image", type=["png", "jpg", "jpeg"])
    message = st.text_area("Secret Message")
    password = st.text_input("Password", type="password")
    if st.button("Hide in Image"):
        if uploaded_img and message and password:
            with open("input_image.png", "wb") as f:
                f.write(uploaded_img.read())
            enc = encrypt_message(message, password)
            output_img = hide_data("input_image.png", enc)
            st.success("Message hidden successfully!")
            st.image(output_img, caption="Stego Image")
            with open(output_img, "rb") as f:
                st.download_button("Download Stego Image", f, file_name="stego_image.png")

with tab2:
    st.header("🔓 Extract & Decrypt")
    stego_img = st.file_uploader("Upload Stego Image", type=["png", "jpg"])
    password2 = st.text_input("Password to Decrypt", type="password")
    if st.button("Extract Message"):
        if stego_img and password2:
            with open("stego_input.png", "wb") as f:
                f.write(stego_img.read())
            try:
                hidden = extract_data("stego_input.png")
                dec = decrypt_message(hidden, password2)
                st.success("Message successfully extracted:")
                st.code(dec)
            except Exception as e:
                st.error("Failed to extract or decrypt message.")
