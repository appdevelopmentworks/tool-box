from langchain_community.document_loaders import YoutubeLoader
import edge_tts
import streamlit as st
from PIL import Image
import asyncio
import os
import io


@st.cache_data
def get_translasion(video_url, lang="en"):
    # YoutubeLoaderを使用して字幕を取得
    loader = YoutubeLoader.from_youtube_url(video_url, add_video_info=False, language=['en'], translation="ja",)  # 日本語字幕を指定
    documents = loader.load()
    # 文字起こし出力
    content = documents[0].page_content
    #改行文字を置換して返す
    return content.replace("\n"," ")

async def dubbing(content, voice="ja-JP-NanamiNeural", rate="+50%", savefile="out.mp3"):
    communicate = edge_tts.Communicate(content, voice,rate=rate)
    await communicate.save(savefile)

#一時ファイル削除用に使用予定
def cleanup_temp_files(file_path):
    if os.path.exists(file_path):
        os.remove(file_path)
        print("一時ファイルが削除されました。")

#コンボボックスのリスト
options = ["en(英語)", "zh(中国語)", "iw(ヘブライ語)", "de(ドイツ語)", "hi(ヒンディー語)", "fr(フランス語)", "ru(ロシア語)", "it(イタリア語)", "es(スペイン語)", "pt(ポルトガル語)", "ko(韓国語)"]

#セッションステートメント
if "text_value" not in st.session_state:
    st.session_state.text_value = ""

 
st.title("Youtube音声吹替アプリ")
st.caption("Youtubeのリンクを送信すると日本語に吹替えます")

image = Image.open('アプリバナー.png')
st.image(image, width=2000)

url = st.text_input("YoutubeのURL:", value="")
rate = st.slider("読み上げ再生速度(50が標準)",min_value=0, max_value=100, value=50)
lang = st.selectbox("元動画の言語:", options)
onsei = st.radio("読み上げる人の音声:", ["女性", "男性"], index=0)
st.markdown(
    """
    <style>
    .stButton > button {
        display: block;
        margin-left: auto;
        margin-right: auto;
        width: 30%;  /* ボタンの幅を調整 */
        background-color:rgb(31, 50, 217);  /* 背景色 */
        color: white;  /* 文字色 */        
    }
    </style>
    """,
    unsafe_allow_html=True
)
btntrans = st.button("翻訳")

txtar = st.text_area("翻訳文:", st.session_state.text_value)
savef = st.text_input("保存ファイル名(*.mp3):", value="out.mp3", disabled=True)

btndub = st.button("吹替")

#翻訳ボタンのイベント
if btntrans:
    st.session_state.text_value = get_translasion(url, lang[:2])
    st.rerun()
    #print("セット完了")

#ダウンロードボタンのイベント
if btndub:
    #読あげ音声
    if onsei=="男性":
        voice = "ja-JP-KeitaNeural"
    else:
        voice = "ja-JP-NanamiNeural"
    #レート
    ra = f"+{rate}%"
    # バッファメモリに音声データを書き出す
    audio_buffer = io.BytesIO()    
    #音声書き出しを非同期で呼ぶ
    asyncio.run(dubbing(st.session_state.text_value, voice=voice, rate=ra, savefile=savef))
    with open(savef, "rb") as f:
        audio_buffer.write(f.read())
    audio_buffer.seek(0)  # バッファの先頭に移動    
    #再生プレイヤー生成
    st.audio(savef, format="audio/mp3")
    # ダウンロードボタン生成
    btdl = st.download_button(
        label="ダウンロード",
        data=audio_buffer,
        file_name=savef,
        mime="audio/mpeg"
    )

    # 一時ファイルの削除
    os.remove(savef)







