import streamlit as st
from components.media.images import show_images
from components.media.audio_video import show_audio_video

def show_media_tab():
    st.info("🎬 **Media Elements**: 이미지, 사운드, 영상 등 다양한 멀티미디어 콘텐츠를 렌더링하는 컴포넌트입니다.")

    tab_images, tab_av = st.tabs([
        "🖼️ 이미지 & 로고",
        "🎵 오디오 & 비디오",
    ])

    with tab_images:
        show_images()

    with tab_av:
        show_audio_video()

