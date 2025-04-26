import os
import streamlit as st
import requests
from dotenv import load_dotenv

# 加载环境变量，这里暂时不需要，因为直接使用密钥
# load_dotenv()

# 直接使用提供的 API 密钥
STABLE_DIFFUSION_API_KEY = "M8xJ8Ksg-F6UGuPheQkgVA"
D_ID_API_KEY = "aHp5MTU5Nzc2OTcxMDVAZ21haWwuY29t：m3CWkJF1VH07iooqoifCq"

# 检查 API 密钥是否已设置
if not STABLE_DIFFUSION_API_KEY or not D_ID_API_KEY:
    st.error("请确保已正确设置 Stable Diffusion 和 D-ID 的 API 密钥。")
    st.stop()

# 设置网页标题
st.title("MetaFrame")

# 上传三张角色照片
st.header("上传三张角色照片")
uploaded_files = st.file_uploader("选择三张图片", accept_multiple_files=True, type=["jpg", "jpeg", "png"])

# 输入场景或剧情文本
st.header("输入场景或剧情")
scene_description = st.text_input("请输入场景或剧情描述，例如：'一个古代骑士在森林中漫步'")

# 生成按钮
if st.button("生成内容"):
    if len(uploaded_files) == 3 and scene_description:
        st.write("内容生成中，请稍候...")

        # 调用 Stable Diffusion API 生成场景图片
        stable_diffusion_url = "https://api.stablediffusionapi.com/v1/generate"
        scene_response = requests.post(
            stable_diffusion_url,
            headers={"Authorization": f"Bearer {STABLE_DIFFUSION_API_KEY}"},
            json={"prompt": scene_description}
        )

        # 检查 Stable Diffusion 响应
        if scene_response.status_code == 200:
            scene_image_url = scene_response.json().get("image_url")
            st.image(scene_image_url, caption="生成的场景图片")
        else:
            st.error(f"场景图片生成失败：{scene_response.text}")

        # 调用 D-ID API 生成数字人头像
        d_id_url = "https://api.d-id.com/v1/avatars"
        for i, uploaded_file in enumerate(uploaded_files):
            avatar_response = requests.post(
                d_id_url,
                headers={"Authorization": f"Bearer {D_ID_API_KEY}"},
                files={"image": uploaded_file.getvalue()}
            )

            # 检查 D-ID 响应
            if avatar_response.status_code == 200:
                avatar_url = avatar_response.json().get("avatar_url")
                st.image(avatar_url, caption=f"数字人头像 {i + 1}")
            else:
                st.error(f"数字人头像生成失败：{avatar_response.text}")
    else:
        st.error("请确保上传了三张图片并填写了场景描述。")
