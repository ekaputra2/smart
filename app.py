import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import io
import urllib.parse
import cv2
import numpy as np
import tempfile
import os

# CONFIG
st.set_page_config(page_title="Sumini Mart Pro", layout="centered")

# ================= SIDEBAR =================
menu = st.sidebar.radio("📌 MENU", ["📸 FOTO POSTER", "🎬 VIDEO POSTER"])

# ================= STYLE =================
st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #ffffff, #fff8e1);
}

h1 {
    text-align: center;
    font-weight: 700;
    color: #2e7d32;
}

.subtitle {
    text-align: center;
    color: #888;
    margin-bottom: 15px;
}

.section {
    background: #fffdf5;
    padding: 18px;
    border-radius: 12px;
    border: 1px solid #eee;
    margin-bottom: 12px;
}

div.stButton > button:first-child {
    background: #ff9800;
    color: white;
    font-size: 16px;
    font-weight: 600;
    border-radius: 10px;
    padding: 10px;
    border: none;
}
</style>
""", unsafe_allow_html=True)

# ================= HEADER =================
st.markdown("<h1>🛒 TOKO SUMINI</h1>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>Poster simple & elegan</div>", unsafe_allow_html=True)

# ================= INPUT =================
st.markdown("<div class='section'>", unsafe_allow_html=True)
st.subheader("📦 Data Produk")
nama_barang = st.text_input("Nama Produk", value="Raja Lele")
harga_barang = st.text_input("Harga", value="5000")
st.markdown("</div>", unsafe_allow_html=True)

# ================= FONT FIX TOTAL =================
def get_font(size):
    font_paths = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    ]

    for p in font_paths:
        if os.path.exists(p):
            return ImageFont.truetype(p, size)

    return ImageFont.load_default()

# =====================================================
# ================= FOTO POSTER =======================
# =====================================================
if menu == "📸 FOTO POSTER":

    st.markdown("<div class='section'>", unsafe_allow_html=True)
    foto_kamera = st.camera_input("Kamera")
    foto_galeri = st.file_uploader("Galeri", type=['jpg','png','jpeg'])
    st.markdown("</div>", unsafe_allow_html=True)

    foto = foto_kamera if foto_kamera else foto_galeri

    if st.button("✨ BUAT POSTER"):

        if not foto:
            st.error("Upload dulu!")
        else:
            img = Image.open(foto)

            # ===== CANVAS FIX =====
            W, H = 1080, 1920
            canvas = Image.new("RGB", (W, H), (13, 71, 161))

            img.thumbnail((W-200, H-200))
            canvas.paste(img, ((W-img.width)//2, (H-img.height)//2))

            draw = ImageDraw.Draw(canvas)

            # ================= SCALE FIX (INI PENTING) =================
            base = min(W, H)

            font_size = max(int(base * 0.12), 90)
            price_size = max(int(base * 0.14), 110)

            font_title = get_font(font_size)
            font_price = get_font(price_size)

            # ================= TEXT =================
            price_text = f"Rp {harga_barang}"

            name_bbox = draw.textbbox((0,0), nama_barang, font=font_title)
            price_bbox = draw.textbbox((0,0), price_text, font=font_price)

            text_w = max(name_bbox[2], price_bbox[2])
            text_h = (name_bbox[3]-name_bbox[1]) + (price_bbox[3]-price_bbox[1]) + 50

            padding = max(int(W * 0.06), 70)

            box_w = text_w + padding*2
            box_h = text_h + padding*2

            box_x = (W - box_w)//2
            box_y = H - box_h - 150

            # ================= CONTAINER (BESAR & JELAS) =================
            overlay = Image.new("RGBA", (box_w, box_h), (0,0,0,180))
            canvas.paste(overlay, (box_x, box_y), overlay)

            x = box_x + padding
            y = box_y + padding

            draw.text((x, y), nama_barang, fill="white", font=font_title)
            draw.text((x, y + (name_bbox[3]-name_bbox[1]) + 15),
                      price_text,
                      fill="#ffd54f",
                      font=font_price)

            st.image(canvas, use_container_width=True)

            buf = io.BytesIO()
            canvas.save(buf, format="JPEG", quality=95)

            col1, col2 = st.columns(2)

            with col1:
                st.download_button("Download", buf.getvalue(), "poster.jpg")

            with col2:
                link = f"https://wa.me/6289504810142?text={urllib.parse.quote('Order ' + nama_barang)}"
                st.link_button("WhatsApp", link)

# =====================================================
# ================= VIDEO (STABIL) =====================
# =====================================================
if menu == "🎬 VIDEO POSTER":

    video = st.file_uploader("Upload Video", type=['mp4','mov','avi'])

    if st.button("BUAT VIDEO"):

        if not video:
            st.error("Upload video dulu")
        else:
            tfile = tempfile.NamedTemporaryFile(delete=False)
            tfile.write(video.read())

            cap = cv2.VideoCapture(tfile.name)

            fps = int(cap.get(cv2.CAP_PROP_FPS)) or 30
            w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

            border = int(min(w,h)*0.05)

            out_path = tempfile.NamedTemporaryFile(delete=False, suffix=".mp4").name
            out = cv2.VideoWriter(out_path, cv2.VideoWriter_fourcc(*'mp4v'), fps, (w+border*2, h+border*2))

            while True:
                ret, frame = cap.read()
                if not ret:
                    break

                canvas = np.ones((h+border*2, w+border*2, 3), dtype=np.uint8)*255
                canvas[border:border+h, border:border+w] = frame

                cv2.rectangle(canvas,(0,0),(w+border*2-1,h+border*2-1),(211,47,47),border)

                cv2.putText(canvas, nama_barang,(50,h),cv2.FONT_HERSHEY_SIMPLEX,1,(255,255,255),2)
                cv2.putText(canvas,f"Rp {harga_barang}",(50,h+40),cv2.FONT_HERSHEY_SIMPLEX,1,(0,255,255),2)

                out.write(canvas)

            cap.release()
            out.release()

            st.video(open(out_path,'rb').read())
