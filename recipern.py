import streamlit as st
import base64
import os
from google.generativeai import types
import google.generativeai as genai
from PIL import Image
import io

















st.title("カメラで献立")
st.caption("画像ファイルを元に献立を考えます。")

image = Image.open('./images/recipern.png')
st.image(image, width=700)
st.caption("カメラで食材を撮るか画像ファイルをアップロード")

upfile = st.file_uploader("食材の写った画像をアップロード", type=["jpg", "jpeg", "png"])

image = st.camera_input("カメラで食材を撮影してください")

if upfile is not None:
    image = Image.open(upfile)
    st.image(image, caption="アップロードされた画像", use_column_width=True)
    
if image is not None:
    # カメラで撮影した場合の処理
    st.image(image, caption='撮影した画像', use_column_width=True)