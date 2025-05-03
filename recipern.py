import streamlit as st
import base64
import os
from google.generativeai import types
import google.generativeai as genai
from PIL import Image
import io



# API キーをグローバルに設定
#genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

#モデルを指定
model = genai.GenerativeModel(model_name="gemini-2.5-pro-exp-03-25")



def generate_recipe(image_part):
    try:
        
        contents = [
            {
                "role": "user",
                "parts": [
                    image_part,
                    {"text": "写真イメージに写っている食材を使ってレシピを考えてください。"},
                ],
            }
        ]

        response = model.generate_content(contents, stream=False)
        
        # for chunk in response:
        #     #st.write(chunk.text, end="", flush=True)
        #     st.write(chunk.text, end="")
        # st.write()  # 最後の改行
        
        return response.text
    except Exception as e:
        print(f"エラーが発生しました: {e}")
        return None








##########################################################################################

st.title("カメラで献立")
st.text("画像ファイルを元に献立を考えます。")

image = Image.open('./images/recipern.png')
st.image(image, width=700)
st.caption("カメラで食材を撮るか画像ファイルをアップロード")

upfile = st.file_uploader("食材の写った画像をアップロード", type=["jpg", "jpeg", "png"])

imagecam = st.camera_input("カメラで食材を撮影してください")



if upfile is not None:
    image = Image.open(upfile)
    st.image(image, caption="アップロードされた画像", use_column_width=True)
    data_load_state = st.text("レシピ考え中...")
    res = generate_recipe(image)
    st.write(res)
    data_load_state.text("レシピを作成しました！")

    
if imagecam is not None:
    # カメラで撮影した場合の処理
    st.image(imagecam, caption='撮影した画像', use_container_width=True)
    #st.image(imagecam, caption='撮影した画像', use_column_width=True)
    data_load_state = st.text("レシピ考え中...")
    res = generate_recipe(image)
    st.write(res)
    data_load_state.text("レシピを作成しました！")
