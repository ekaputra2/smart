import streamlit as st
from PIL import Image, ImageDraw, ImageFont, ImageFilter
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

# ===== THEME CERAH MINIMAL =====
st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #ffffff, #fff8e1);
}

.main {
    background: white;
    padding: 28px;
    border-radius: 18px;
    box-shadow: 0 6px 20px rgba(0,0,0,0.08);
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
st.markdown("<div class='subtitle'>Poster simple & elegan (WhatsApp Story)</div>", unsafe_allow_html=True)

# ================= INPUT =================
st.markdown("<div class='section'>", unsafe_allow_html=True)
st.subheader("📦 Data Produk")
nama_barang = st.text_input("Nama Produk", value="Raja Lele")
harga_barang = st.text_input("Harga", value="5000")
st.markdown("</div>", unsafe_allow_html=True)

# ================= FONT FIX (ANTI CRASH STREAMLIT CLOUD) =================
def get_font(size, bold=False):
    font_paths = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/dejavu/DejaVuSans-Bold.ttf",
        "/usr/share/fonts/dejavu/DejaVuSans.ttf",
    ]

    for path in font_paths:
        try:
            if os.path.exists(path):
                return ImageFont.truetype(path, size)
        except:
            pass

    # SAFE FALLBACK (TIDAK CRASH)
    return ImageFont.load_default()

# =====================================================
# ================= FOTO POSTER =======================
# =====================================================
if menu == "📸 FOTO POSTER":

    st.markdown("<div class='section'>", unsafe_allow_html=True)
    st.subheader("📸 Upload Foto")
    foto_kamera = st.camera_input("Kamera")
    foto_galeri = st.file_uploader("Galeri", type=['jpg','png','jpeg'])
    st.markdown("</div>", unsafe_allow_html=True)

    foto = foto_kamera if foto_kamera else foto_galeri

    if st.button("✨ BUAT POSTER CLEAN"):

        if not foto or not nama_barang or not harga_barang:
            st.error("⚠️ Lengkapi data dulu!")
        else:
            img_input = Image.open(foto)

            # ===== CANVAS STORY =====
            target_w = 1080
            target_h = 1920
            image = Image.new("RGB", (target_w, target_h), (13, 71, 161))

            img_input.thumbnail((target_w - 200, target_h - 200), Image.Resampling.LANCZOS)
            img_w, img_h = img_input.size
            image.paste(img_input, ((target_w - img_w)//2, (target_h - img_h)//2))

            width, height = image.size
            draw = ImageDraw.Draw(image)

            # ===== BORDER =====
            border_size = int(min(width, height) * 0.05)
            radius = int(border_size * 2)

            draw.rounded_rectangle(
                [10, 10, width-10, height-10],
                radius=radius,
                outline=(211,47,47),
                width=int(border_size*0.7)
            )

            draw.rounded_rectangle(
                [30, 30, width-30, height-30],
                radius=radius,
                outline=(255,235,59),
                width=int(border_size*0.6)
            )

            # ===== LOGO =====
            try:
                logo = Image.open("image.png")
                logo_w = int(width * 0.22)
                ratio = logo_w / logo.width
                logo = logo.resize((logo_w, int(logo.height * ratio)))
                if logo.mode != "RGBA":
                    logo = logo.convert("RGBA")
                image.paste(logo, (40,40), logo)
            except:
                pass

            # ================= FONT =================
            font_size = int(width * 0.09)
            font_title = get_font(font_size, bold=True)
            font_price = get_font(int(font_size * 1.2), bold=True)

            # ================= TEXT CONTAINER =================
            price_text = f"Rp {harga_barang}"

            name_bbox = draw.textbbox((0,0), nama_barang, font=font_title)
            price_bbox = draw.textbbox((0,0), price_text, font=font_price)

            text_w = max(name_bbox[2], price_bbox[2])
            text_h = (name_bbox[3]-name_bbox[1]) + (price_bbox[3]-price_bbox[1]) + 40

            padding = int(width * 0.05)

            box_w = text_w + padding*2
            box_h = text_h + padding*2

            box_x = (width - box_w)//2
            box_y = height - box_h - int(height*0.08)

            # container gelap transparan
            container = Image.new("RGBA", (box_w, box_h), (0,0,0,170))
            image.paste(container, (box_x, box_y), container)

            x = box_x + padding
            y = box_y + padding

            draw.text((x, y), nama_barang, fill="white", font=font_title)
            draw.text((x, y + (name_bbox[3]-name_bbox[1]) + 10),
                      price_text,
                      fill="#ffd54f",
                      font=font_price)

            buf = io.BytesIO()
            image.save(buf, format="JPEG", quality=95)

            st.subheader("✨ Hasil Poster")
            st.image(image, use_container_width=True)

            col1, col2 = st.columns(2)

            with col1:
                st.download_button("💾 Download", buf.getvalue(), file_name="poster.jpg")

            with col2:
                pesan = f"*TOKO SUMINI*\n\n{nama_barang}\nRp {harga_barang}"
                link = f"https://wa.me/6289504810142?text={urllib.parse.quote(pesan)}"
                st.link_button("📲 WhatsApp", link)

# =====================================================
# ================= VIDEO POSTER ======================
# =====================================================
if menu == "🎬 VIDEO POSTER":

    st.markdown("<div class='section'>", unsafe_allow_html=True)
    st.subheader("🎥 Upload Video")
    video_file = st.file_uploader("Upload Video", type=['mp4','mov','avi'])
    st.markdown("</div>", unsafe_allow_html=True)

    if st.button("🎬 BUAT VIDEO POSTER"):

        if not video_file:
            st.error("⚠️ Upload video dulu!")
        else:
            tfile = tempfile.NamedTemporaryFile(delete=False)
            tfile.write(video_file.read())

            cap = cv2.VideoCapture(tfile.name)

            fps = int(cap.get(cv2.CAP_PROP_FPS)) or 30
            w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

            border = int(min(w,h) * 0.05)

            out_path = tempfile.NamedTemporaryFile(delete=False, suffix=".mp4").name
            out = cv2.VideoWriter(out_path, cv2.VideoWriter_fourcc(*'mp4v'), fps, (w+border*2, h+border*2))

            while True:
                ret, frame = cap.read()
                if not ret:
                    break

                canvas = np.ones((h+border*2, w+border*2, 3), dtype=np.uint8)*255
                canvas[border:border+h, border:border+w] = frame

                cv2.rectangle(canvas,(0,0),(w+border*2-1,h+border*2-1),(211,47,47),border)
                cv2.putText(canvas,nama_barang,(50,h),cv2.FONT_HERSHEY_SIMPLEX,1,(255,255,255),2)
                cv2.putText(canvas,f"Rp {harga_barang}",(50,h+40),cv2.FONT_HERSHEY_SIMPLEX,1,(0,255,255),2)

                out.write(canvas)

            cap.release()
            out.release()

            video_bytes = open(out_path,'rb').read()

            st.video(video_bytes)
            st.download_button("💾 Download Video", video_bytes, "video.mp4")
