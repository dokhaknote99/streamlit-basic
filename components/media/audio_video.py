import streamlit as st

def show_audio_video():
    st.header("🎵 오디오 및 비디오 (st.audio & st.video)")

    # 1. 오디오 플레이어 (st.audio)
    st.subheader("1. 오디오 플레이어 (st.audio)")
    st.caption("사운드 파일 URL이나 로컬 mp3/wav 파일, 오디오 바이트 스트림을 재생합니다.")
    sample_audio_url = "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3"
    st.audio(sample_audio_url, format="audio/mp3")

    st.divider()

    # 2. 비디오 플레이어 (st.video)
    st.subheader("2. 비디오 플레이어 (st.video)")
    st.caption("mp4 동영상 URL이나 유튜브(YouTube) 영상 링크를 바로 임베드할 수 있습니다.")
    youtube_url = "https://www.youtube.com/watch?v=B2iAODr0fOo"
    st.video(youtube_url)

