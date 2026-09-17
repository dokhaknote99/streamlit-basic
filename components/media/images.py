import streamlit as st

def show_images():
    st.header("🖼️ 이미지 및 로고 (st.image & st.logo)")

    # 1. 온라인 이미지 표시
    st.subheader("1. 웹 이미지 표시 (st.image)")
    st.caption("URL 또는 로컬 이미지 파일 경로를 전달하여 이미지를 표시합니다.")

    sample_img_url = "https://images.unsplash.com/photo-1579783900882-c0d3dad7b119?w=600"
    st.image(
        sample_img_url,
        caption="Unsplash 샘플 이미지 (use_container_width=True)",
        use_container_width=True,
    )

    # 2. 너비 고정 이미지
    st.subheader("2. 너비 고정 이미지 (width=200)")
    st.image(sample_img_url, width=200, caption="너비 200px 고정")

