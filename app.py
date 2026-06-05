import io
import os
import random
import time
import requests
from PIL import Image
import streamlit as st
import dotenv
from concurrent.futures import ThreadPoolExecutor

# Load local environment variables (if any)
dotenv.load_dotenv()

# Set Streamlit Page Configurations (optimized for mobile first)
st.set_page_config(
    page_title="Cosmos3-Super-Text2Image App",
    page_icon="🎨",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# --- Sakura (Cherry Blossom) Falling Background Effect ---
st.components.v1.html(
    """
    <script>
    const parentDoc = window.parent.document;
    if (!parentDoc.getElementById('sakura-canvas')) {
        const canvas = parentDoc.createElement('canvas');
        canvas.id = 'sakura-canvas';
        canvas.style.position = 'fixed';
        canvas.style.top = '0';
        canvas.style.left = '0';
        canvas.style.width = '100vw';
        canvas.style.height = '100vh';
        canvas.style.zIndex = '-1';
        canvas.style.pointerEvents = 'none';
        
        parentDoc.body.insertBefore(canvas, parentDoc.body.firstChild);
        
        const ctx = canvas.getContext('2d');
        let width = canvas.width = window.parent.innerWidth;
        let height = canvas.height = window.parent.innerHeight;
        
        window.parent.addEventListener('resize', () => {
            width = canvas.width = window.parent.innerWidth;
            height = canvas.height = window.parent.innerHeight;
        });
        
        class Petal {
            constructor() {
                this.reset();
                this.y = Math.random() * height; // Distribute petals vertically on start
            }
            reset() {
                this.x = Math.random() * width;
                this.y = -20;
                this.r = Math.random() * 6 + 4;
                this.swingSpeed = Math.random() * 0.02 + 0.005;
                this.swingAngle = Math.random() * Math.PI;
                this.fallSpeed = Math.random() * 1.2 + 0.8;
                this.rotation = Math.random() * Math.PI;
                this.rotationSpeed = Math.random() * 0.02 - 0.01;
                const shades = [
                    'rgba(255, 183, 197, 0.65)',
                    'rgba(255, 192, 203, 0.7)',
                    'rgba(255, 209, 220, 0.75)',
                    'rgba(255, 158, 187, 0.6)'
                ];
                this.color = shades[Math.floor(Math.random() * shades.length)];
            }
            update() {
                this.y += this.fallSpeed;
                this.swingAngle += this.swingSpeed;
                this.x += Math.sin(this.swingAngle) * 0.5;
                this.rotation += this.rotationSpeed;
                if (this.y > height + 20 || this.x < -20 || this.x > width + 20) {
                    this.reset();
                }
            }
            draw() {
                ctx.save();
                ctx.translate(this.x, this.y);
                ctx.rotate(this.rotation);
                ctx.beginPath();
                ctx.ellipse(0, 0, this.r, this.r / 2, 0, 0, Math.PI * 2);
                ctx.fillStyle = this.color;
                ctx.fill();
                ctx.restore();
            }
        }
        
        const petals = [];
        const maxPetals = Math.min(50, Math.floor(width / 15));
        for (let i = 0; i < maxPetals; i++) {
            petals.push(new Petal());
        }
        
        function animate() {
            ctx.clearRect(0, 0, width, height);
            petals.forEach(petal => {
                petal.update();
                petal.draw();
            });
            window.parent.requestAnimationFrame(animate);
        }
        animate();
    }
    </script>
    """,
    height=0,
    width=0
)

# Custom CSS for Premium Design & Mobile Aesthetics
st.markdown(
    """
    <style>
    /* Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap');

    /* Global styling */
    html, body, [data-testid="stAppViewContainer"] {
        font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
        background-color: #0f172a;
        color: #f8fafc;
    }
    
    /* Main block styling */
    [data-testid="stMainBlockContainer"] {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 540px; /* Max width tailored for mobile viewports */
        margin: 0 auto;
    }

    /* Vibrant Gradient Title */
    .app-title {
        background: linear-gradient(135deg, #a78bfa 0%, #f43f5e 50%, #6366f1 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 2.2rem;
        font-weight: 800;
        text-align: center;
        margin-bottom: 0.2rem;
        letter-spacing: -0.03em;
    }
    
    .app-subtitle {
        color: #94a3b8;
        text-align: center;
        font-size: 0.95rem;
        margin-bottom: 1.5rem;
    }

    /* Premium Glassmorphism Card for instructions */
    .info-card {
        background: rgba(30, 41, 59, 0.4);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 16px;
        padding: 1.2rem;
        margin-bottom: 1.5rem;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.3);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
    }
    
    .info-title {
        font-size: 1.05rem;
        font-weight: 700;
        color: #f1f5f9;
        margin-bottom: 0.6rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    .info-item {
        font-size: 0.85rem;
        color: #cbd5e1;
        margin-bottom: 0.4rem;
        line-height: 1.4;
    }

    /* Input & Control styling overrides */
    div[data-baseweb="input"], div[data-baseweb="textarea"], div[data-baseweb="select"] {
        border-radius: 10px !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        background-color: rgba(15, 23, 42, 0.6) !important;
        transition: all 0.3s ease;
    }
    
    div[data-baseweb="input"]:focus-within, div[data-baseweb="textarea"]:focus-within {
        border-color: #6366f1 !important;
        box-shadow: 0 0 0 2px rgba(99, 102, 241, 0.2) !important;
    }
    
    /* Button Premium Styling */
    div.stButton > button {
        background: linear-gradient(135deg, #a855f7 0%, #6366f1 100%) !important;
        color: #ffffff !important;
        border: none !important;
        border-radius: 10px !important;
        padding: 0.75rem 1.5rem !important;
        font-weight: 700 !important;
        font-size: 1.05rem !important;
        width: 100% !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        box-shadow: 0 4px 14px 0 rgba(168, 85, 247, 0.4) !important;
        margin-top: 1rem;
    }
    
    div.stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 20px 0 rgba(168, 85, 247, 0.6) !important;
    }
    
    div.stButton > button:active {
        transform: translateY(1px) !important;
    }

    /* Accordion header text */
    .st-emotion-cache-1h9z78s {
        font-weight: 600 !important;
        color: #e2e8f0 !important;
    }

    /* Link list styling */
    .link-list {
        display: flex;
        flex-wrap: wrap;
        gap: 0.8rem;
        justify-content: center;
        margin-top: 1rem;
    }

    .link-button {
        display: inline-block;
        padding: 0.4rem 0.8rem;
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 8px;
        color: #a78bfa !important;
        font-size: 0.8rem;
        font-weight: 500;
        text-decoration: none;
        transition: all 0.2s;
    }

    .link-button:hover {
        background: rgba(167, 139, 250, 0.1);
        border-color: rgba(167, 139, 250, 0.3);
        transform: scale(1.02);
    }
    
    /* Footer styles */
    .footer {
        text-align: center;
        padding: 1.5rem 0;
        color: #475569;
        font-size: 0.75rem;
        border-top: 1px solid rgba(255, 255, 255, 0.05);
        margin-top: 3rem;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Render Application Header
st.markdown('<div class="app-title">Cosmos3 Image Studio</div>', unsafe_allow_html=True)
st.markdown('<div class="app-subtitle">HW3: Text-to-Image Generation App (Mobile Edition)</div>', unsafe_allow_html=True)

# Render Info Card (Model Info, Instructions, Links)
st.markdown(
    """
    <div class="info-card">
        <div class="info-title">💡 說明與資訊 / App Info</div>
        <div class="info-item"><b>🎯 作業目標：</b>使用 Hugging Face 的生成模型透過文字生成圖像。</div>
        <div class="info-item"><b>🤖 預設模型：</b><code>nvidia/Cosmos3-Super-Text2Image</code></div>
        <div class="info-item"><b>📝 使用說明：</b>設定 API Token、輸入文字 Prompt，展開「進階參數」微調設定，點擊「開始生成」即可。</div>
        <div class="link-list">
            <a class="link-button" href="https://github.com/Frank40281-stack/Cosmos3-Super-Text2Image-App-0604" target="_blank">🐙 GitHub Repo</a>
            <a class="link-button" href="https://frank40281-stack.github.io/Cosmos3-Super-Text2Image-App-0604/" target="_blank">🌐 Live Demo (HTML)</a>
            <a class="link-button" href="https://share.streamlit.io" target="_blank">🚀 Streamlit Cloud</a>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

# --- API Key Management ---
# 1. Check Streamlit Secrets (recommended)
# 2. Check Local environment variable
# 3. If neither, ask user for input
api_token = None

try:
    api_token = st.secrets.get("HF_TOKEN")
except Exception:
    # Handle case where secrets.toml does not exist
    pass

if not api_token:
    api_token = os.environ.get("HF_TOKEN")

if not api_token:
    api_token = st.text_input(
        "Enter your Hugging Face API Token",
        type="password",
        help="輸入您的 Hugging Face API Token (以 HF_ 開頭)。若要自動載入，請於 secrets.toml 中設定 HF_TOKEN。"
    )

# Disable generating if key is missing
is_key_missing = not api_token

if is_key_missing:
    st.warning("⚠️ 請輸入 Hugging Face API Token 以繼續。")

# --- UI Controls (Main form inputs) ---
prompt = st.text_area(
    "🎨 Prompt / 畫面描述",
    placeholder="描述你想要生成的圖像，例如: A futuristic city with flying cars at sunset...",
    height=85
)

# --- Expandable Options for Advanced Parameters (Optimized for Mobile) ---
with st.expander("🛠️ 進階設定 / Advanced Parameters", expanded=False):
    # Model Selection (In case Cosmos3 is offline/unsupported on HF serverless)
    model_choice = st.selectbox(
        "🤖 生成模型 (Model)",
        options=[
            "nvidia/Cosmos3-Super-Text2Image",
            "black-forest-labs/FLUX.1-schnell",
            "stabilityai/stable-diffusion-xl-base-1.0"
        ],
        index=0,
        help="作業指定 nvidia/Cosmos3-Super-Text2Image。若 HF 免費伺服器不可用，可切換 FLUX 或 SDXL 進行功能測試。"
    )
    
    # Image Style Presets
    image_style = st.selectbox(
        "✨ 風格預設 (Style Preset)",
        options=["無 (None)", "寫實 (Photorealistic)", "動漫 (Anime)", "奇幻 (Fantasy)", "賽博朋克 (Cyberpunk)", "油畫 (Oil Painting)", "3D 渲染 (3D Render)"]
    )
    
    # Aspect Ratio Map
    aspect_ratio = st.selectbox(
        "📐 寬高比 (Aspect Ratio)",
        options=[
            "1:1 (Square - 1024x1024)",
            "16:9 (Landscape - 1024x576)",
            "9:16 (Portrait - 576x1024)",
            "4:3 (Standard - 1024x768)",
            "3:4 (Vertical - 768x1024)"
        ],
        index=0
    )
    
    # Negative Prompt
    negative_prompt = st.text_area(
        "🚫 負面 Prompt (Negative Prompt)",
        placeholder="不想出現在畫面中的內容，例如: blurry, low quality, bad anatomy...",
        height=65
    )
    
    # Seed Configuration
    use_random_seed = st.checkbox("🎲 隨機隨機種子 (Random Seed)", value=True)
    if use_random_seed:
        seed = random.randint(1, 1000000)
        st.info(f"隨機生成種子: {seed}")
    else:
        seed = st.number_input("種子碼 (Seed)", min_value=1, max_value=99999999, value=42)
        
    # Number of images
    num_images = st.slider("🖼️ 生成圖片張數 (Number of Images)", min_value=1, max_value=4, value=1)


# Apply styles based on selections
style_prompts = {
    "無 (None)": "",
    "寫實 (Photorealistic)": ", photorealistic, highly detailed, 8k resolution, cinematic lighting, dramatic shading",
    "動漫 (Anime)": ", anime style, vibrant colors, detailed digital illustration, cute aesthetic, masterpiece",
    "奇幻 (Fantasy)": ", fantasy digital art, ethereal environment, glowing details, highly imaginative, magical atmosphere",
    "賽博朋克 (Cyberpunk)": ", cyberpunk aesthetic, neon glowing lights, futuristic cityscape, dark synthwave vibe, highly detailed",
    "油畫 (Oil Painting)": ", classical oil painting style, visible brush strokes, textured canvas, fine art",
    "3D 渲染 (3D Render)": ", 3D render, blender style, smooth textures, octane render, stylized character design"
}

aspect_sizes = {
    "1:1 (Square - 1024x1024)": (1024, 1024),
    "16:9 (Landscape - 1024x576)": (1024, 576),
    "9:16 (Portrait - 576x1024)": (576, 1024),
    "4:3 (Standard - 1024x768)": (1024, 768),
    "3:4 (Vertical - 768x1024)": (768, 1024)
}

# Combine raw prompt with style suffix
final_prompt = prompt + style_prompts[image_style] if prompt else ""
width, height = aspect_sizes[aspect_ratio]




# --- API Inference Function (with DNS/Proxy fallback support) ---
def call_huggingface_api(img_index, current_seed):
    domains = [
        "https://router.huggingface.co",
        "https://api-inference.huggingface.co",
        "https://api.huggingface.co"
    ]
    
    last_error = None
    
    for domain in domains:
        api_url = f"{domain}/models/{model_choice}"
        headers = {
            "Authorization": f"Bearer {api_token}",
            "Content-Type": "application/json"
        }
        
        # Build payload parameters
        parameters = {
            "seed": current_seed,
            "width": width,
            "height": height
        }
        if negative_prompt:
            parameters["negative_prompt"] = negative_prompt
            
        payload = {
            "inputs": final_prompt,
            "parameters": parameters
        }
        
        try:
            response = requests.post(api_url, headers=headers, json=payload, timeout=90)
            
            if response.status_code == 200:
                # Check content-type to confirm it's an image
                content_type = response.headers.get("content-type", "")
                if "image" in content_type:
                    image_bytes = response.content
                    image = Image.open(io.BytesIO(image_bytes))
                    return {"index": img_index, "image": image, "seed": current_seed, "success": True}
                else:
                    # API returned 200 but might be JSON status info
                    try:
                        json_data = response.json()
                        return {"index": img_index, "error": f"API JSON: {json_data}", "success": False}
                    except Exception:
                        return {"index": img_index, "error": f"API returned non-image content: {content_type}", "success": False}
            elif response.status_code == 503:
                # Model is loading
                try:
                    error_json = response.json()
                    est_time = error_json.get("estimated_time", 20.0)
                    return {
                        "index": img_index, 
                        "error": f"模型正在載入中 (Model Loading)。預計剩餘時間: {est_time:.1f} 秒，請稍後重試。", 
                        "success": False, 
                        "loading": True
                    }
                except Exception:
                    return {"index": img_index, "error": "模型載入中 (503 Service Unavailable)，請稍後再試。", "success": False, "loading": True}
            else:
                try:
                    error_json = response.json()
                    error_msg = error_json.get("error", f"Error code: {response.status_code}")
                    return {"index": img_index, "error": error_msg, "success": False}
                except Exception:
                    return {"index": img_index, "error": f"HTTP {response.status_code}: {response.text[:200]}", "success": False}
                    
        except requests.exceptions.RequestException as e:
            last_error = e
            # Try the next domain in the loop
            continue
            
    # If all endpoints failed
    error_msg = f"網路連線失敗，無法解析 API 位址或連線逾時。請檢查網路或 Proxy 設定。詳細錯誤：{str(last_error)}"
    return {"index": img_index, "error": error_msg, "success": False}


# --- Generation Process ---
if st.button("✨ 開始生成 (Generate)", disabled=is_key_missing):
    if not prompt:
        st.error("⚠️ 請輸入畫面描述 (Prompt)。")
    else:
        # Create a container for rendering results
        status_box = st.empty()
        result_box = st.empty()
        
        status_box.info("🚀 正在連線至 Hugging Face Inference API...")
        
        # Prepare lists to run requests
        results = []
        seeds_to_use = [seed + i for i in range(num_images)]
        
        # Execute API requests in parallel using thread pool
        with ThreadPoolExecutor(max_workers=min(4, num_images)) as executor:
            future_to_img = {
                executor.submit(call_huggingface_api, i, seeds_to_use[i]): i 
                for i in range(num_images)
            }
            
            # Retrieve responses
            results = [future.result() for future in future_to_img]
            
        # Clear status
        status_box.empty()
        
        # Display images or error messages
        success_count = 0
        error_msgs = []
        
        # Create grid layout based on number of images
        with result_box.container():
            for res in sorted(results, key=lambda x: x["index"]):
                if res["success"]:
                    success_count += 1
                    # Modern card around the image
                    st.markdown(f"**Image #{res['index'] + 1}** (Seed: `{res['seed']}`)")
                    st.image(res["image"], use_column_width=True)
                    
                    # Convert PIL image to bytes for downloading
                    img_byte_arr = io.BytesIO()
                    res["image"].save(img_byte_arr, format='PNG')
                    img_byte_arr = img_byte_arr.getvalue()
                    
                    # Download button
                    st.download_button(
                        label=f"💾 下載 Image #{res['index'] + 1}",
                        data=img_byte_arr,
                        file_name=f"cosmos_gen_{res['seed']}.png",
                        mime="image/png",
                        key=f"dl_{res['index']}"
                    )
                else:
                    error_msgs.append(f"圖片 #{res['index'] + 1} 生成失敗: {res.get('error', '未知錯誤')}")
            
            # Report any issues
            if error_msgs:
                for err in error_msgs:
                    st.error(err)
            
            if success_count > 0:
                st.success(f"🎉 成功生成 {success_count} 張圖片！")

# Render Page Footer
st.markdown(
    """
    <div class="footer">
        <div>Model: nvidia/Cosmos3-Super-Text2Image</div>
        <div style="margin-top: 4px;">HW3 AI Image App © 2026</div>
    </div>
    """,
    unsafe_allow_html=True
)
