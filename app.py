import streamlit as st
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import io
import urllib.parse
import cv2
import numpy as np
import tempfile

# CONFIG
st.set_page_config(page_title="Sumini Mart Pro", layout="centered")

# ================= SIDEBAR =================
menu = st.sidebar.radio("📌 MENU", ["📸 FOTO POSTER", "🎬 VIDEO POSTER"])

# ===== THEME CERAH MINIMAL (TETAP ASLI) =====
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

.stTextInput input {
    border-radius: 8px;
}

.stFileUploader, .stCameraInput {
    border: 1px dashed #ccc;
    padding: 12px;
    border-radius: 10px;
    background: #fafafa;
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

# ================= INPUT GLOBAL (TIDAK DIHAPUS) =================
st.markdown("<div class='section'>", unsafe_allow_html=True)
st.subheader("📦 Data Produk")
nama_barang = st.text_input("Nama Produk")
harga_barang = st.text_input("Harga")
st.markdown("</div>", unsafe_allow_html=True)

# =========================================================
# ================= HALAMAN FOTO ==========================
# =========================================================
if menu == "📸 FOTO POSTER":

    st.markdown("<div class='section'>", unsafe_allow_html=True)
    st.subheader("📸 Upload Foto")
    foto_kamera = st.camera_input("Kamera")
    foto_galeri = st.file_uploader("Galeri", type=['jpg','png','jpeg'])
    st.markdown("</div>", unsafe_allow_html=True)

    foto = foto_kamera if foto_kamera else foto_galeri

    proses = st.button("✨ BUAT POSTER CLEAN")

    if proses:
        if not foto or not nama_barang or not harga_barang:
            st.error("⚠️ Lengkapi data dulu!")
        else:
            image = Image.open(foto)

            if image.mode in ("RGBA", "P"):
                image = image.convert("RGB")

            width, height = image.size

            # ===== IG STYLE FILTER (TIDAK DIHAPUS) =====
            blur_bg = image.copy().filter(ImageFilter.GaussianBlur(12))
            image = Image.blend(blur_bg, image, 0.75)

            draw = ImageDraw.Draw(image)

            # ===== OVERLAY (TETAP ASLI) =====
            overlay = Image.new('RGBA', (width, int(height*0.35)), (0,0,0,0))
            for i in range(overlay.height):
                alpha = int(160 * (i / overlay.height))
                line = Image.new('RGBA', (width, 1), (0,0,0,alpha))
                overlay.paste(line, (0, i))
            image.paste(overlay, (0, height - overlay.height), overlay)

            image = image.convert('RGB')

            # ===== BORDER (TIDAK DIUBAH SAMA SEKALI) =====
            border_size = int(min(width, height) * 0.05)

            new_w = width + border_size*2
            new_h = height + border_size*2

            new_img = Image.new("RGB", (new_w, new_h), (255,255,255))
            new_img.paste(image, (border_size, border_size))

            draw_border = ImageDraw.Draw(new_img)

            radius = int(border_size * 2)

            draw_border.rounded_rectangle(
                [0, 0, new_w-1, new_h-1],
                radius=radius,
                outline=(211,47,47),
                width=border_size
            )

            offset1 = int(border_size * 0.5)
            draw_border.rounded_rectangle(
                [offset1, offset1, new_w-offset1-1, new_h-offset1-1],
                radius=radius,
                outline=(255,235,59),
                width=int(border_size*0.6)
            )

            offset2 = int(border_size * 1.1)
            draw_border.rounded_rectangle(
                [offset2, offset2, new_w-offset2-1, new_h-offset2-1],
                radius=radius,
                outline=(13,71,161),
                width=int(border_size*0.6)
            )

            # diagonal (TETAP)
            line_len = int(border_size * 2.5)

            draw_border.line((0, line_len, line_len, 0), fill=(255,235,59), width=5)
            draw_border.line((0, line_len+10, line_len+10, 0), fill=(13,71,161), width=4)

            draw_border.line((new_w-line_len, 0, new_w, line_len), fill=(255,235,59), width=5)
            draw_border.line((new_w-line_len-10, 0, new_w, line_len+10), fill=(13,71,161), width=4)

            draw_border.line((0, new_h-line_len, line_len, new_h), fill=(255,235,59), width=5)
            draw_border.line((0, new_h-line_len-10, line_len+10, new_h), fill=(13,71,161), width=4)

            draw_border.line((new_w-line_len, new_h, new_w, new_h-line_len), fill=(255,235,59), width=5)
            draw_border.line((new_w-line_len-10, new_h, new_w, new_h-line_len-10), fill=(13,71,161), width=4)

            image = new_img
            width, height = image.size
            draw = ImageDraw.Draw(image)

            # ===== LOGO (TIDAK DIHAPUS) =====
            try:
                logo = Image.open("image.png")
                logo_w = int(width * 0.18)
                ratio = logo_w / logo.width
                logo_h = int(logo.height * ratio)
                logo = logo.resize((logo_w, logo_h))

                if logo.mode != "RGBA":
                    logo = logo.convert("RGBA")

                image.paste(logo, (20, 20), logo)
            except:
                pass

            # ===== FONT (TETAP) =====
            font_size = int(width * 0.08)

            try:
                font_title = ImageFont.truetype("arialbd.ttf", font_size)
                font_price = ImageFont.truetype("arial.ttf", int(font_size*1.1))
            except:
                font_title = ImageFont.load_default()
                font_price = ImageFont.load_default()

            # ===== TEXT (TIDAK DIUBAH) =====
            margin = int(width * 0.05)
            text_y = height - int(height*0.25)

            draw.rectangle([
                margin - 20,
                text_y - 20,
                margin + int(width * 0.9),
                text_y + int(font_size * 3.2)
            ], fill=(0,0,0,120))

            draw.text((margin, text_y), nama_barang, fill="white", font=font_title)
            draw.text((margin, text_y + font_size + 10),
                      f"Rp {harga_barang}",
                      fill="#ffd54f",
                      font=font_price)

            st.subheader("✨ Hasil Poster")
            st.image(image, use_container_width=True)

            buf = io.BytesIO()
            image.save(buf, format="JPEG", quality=95)

            col1, col2 = st.columns(2)

            with col1:
                st.download_button("💾 Download", buf.getvalue(), file_name="produk_clean.jpg")

            with col2:
                pesan = f"*TOKO SUMINI*\n\n{nama_barang}\nRp {harga_barang}\n\nOrder sekarang"
                link = f"https://wa.me/6289504810142?text={urllib.parse.quote(pesan)}"
                st.link_button("📲 WhatsApp", link)

# =========================================================
# ================= HALAMAN VIDEO =========================
# =========================================================
if menu == "🎬 VIDEO POSTER":

    st.markdown("<div class='section'>", unsafe_allow_html=True)
    st.subheader("🎥 Upload Video (Fitur Tambahan)")
    video_file = st.file_uploader("Upload Video", type=['mp4','mov','avi'])
    st.markdown("</div>", unsafe_allow_html=True)

    if st.button("🎬 BUAT VIDEO POSTER"):
        if not video_file or not nama_barang or not harga_barang:
            st.error("⚠️ Lengkapi data video!")
        else:
            tfile = tempfile.NamedTemporaryFile(delete=False)
            tfile.write(video_file.read())

            cap = cv2.VideoCapture(tfile.name)

            fps = int(cap.get(cv2.CAP_PROP_FPS))
            w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

            border = int(min(w,h) * 0.05)

            out_path = tempfile.NamedTemporaryFile(delete=False, suffix=".mp4").name
            out = cv2.VideoWriter(out_path, cv2.VideoWriter_fourcc(*'mp4v'), fps, (w+border*2, h+border*2))

            while True:
                ret, frame = cap.read()
                if not ret:
                    break

                canvas = np.ones((h+border*2, w+border*2, 3), dtype=np.uint8) * 255
                canvas[border:border+h, border:border+w] = frame

                cv2.rectangle(canvas, (0,0), (w+border*2-1,h+border*2-1), (211,47,47), border)

                cv2.putText(canvas, nama_barang, (50, h),
                            cv2.FONT_HERSHEY_SIMPLEX, 1,
                            (255,255,255), 2)

                cv2.putText(canvas, f"Rp {harga_barang}", (50, h+40),
                            cv2.FONT_HERSHEY_SIMPLEX, 1,
                            (0,255,255), 2)

                out.write(canvas)

            cap.release()
            out.release()

            video_bytes = open(out_path, 'rb').read()

            st.video(video_bytes)
            st.download_button("💾 Download Video", video_bytes, "video_poster.mp4")

            st.success("✅ Video berhasil dibuat!")
