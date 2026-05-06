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
st.markdown("<div class='subtitle'>Poster simple & elegan (Versi WhatsApp Story)</div>", unsafe_allow_html=True)

# ================= INPUT GLOBAL =================
st.markdown("<div class='section'>", unsafe_allow_html=True)
st.subheader("📦 Data Produk")
nama_barang = st.text_input("Nama Produk", value="Raja Lele") 
harga_barang = st.text_input("Harga", value="5000") 
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
            # Load input image
            img_input = Image.open(foto)

            # --- 1. SET CANVAS UKURAN WHATSAPP STORY (9:16) ---
            target_w = 1080
            target_h = 1920
            # Buat kanvas biru tua (biru dongker)
            image = Image.new("RGB", (target_w, target_h), (13, 71, 161))

            # --- 2. PASTE FOTO KE KANVAS (CENTERED) ---
            img_input.thumbnail((target_w - 200, target_h - 200), Image.Resampling.LANCZOS)
            img_w, img_h = img_input.size
            paste_x = (target_w - img_w) // 2
            paste_y = (target_h - img_h) // 2
            image.paste(img_input, (paste_x, paste_y))

            width, height = image.size
            draw = ImageDraw.Draw(image)

            # ===== BORDER (DIPERBARUI) =====
            border_size = int(min(width, height) * 0.05) 
            draw_border = ImageDraw.Draw(image)
            radius = int(border_size * 2)

            # Garis Rounded Rectangle (Garis 1: Merah)
            offset1 = int(border_size * 0.25)
            draw_border.rounded_rectangle(
                [offset1, offset1, width-offset1-1, height-offset1-1],
                radius=radius,
                outline=(211,47,47),
                width=int(border_size*0.7)
            )

            # Garis Rounded Rectangle (Garis 2: Kuning)
            offset2 = int(border_size * 0.75)
            draw_border.rounded_rectangle(
                [offset2, offset2, width-offset2-1, height-offset2-1],
                radius=radius,
                outline=(255,235,59),
                width=int(border_size*0.6)
            )

            # --- BORDER BIRU DALAM TELAH DIHAPUS ---

            # Garis Diagonal di Sudut (TETAP)
            line_len = int(border_size * 3) 
            draw_border.line((0, line_len, line_len, 0), fill=(255,235,59), width=8)
            draw_border.line((0, line_len+15, line_len+15, 0), fill=(211,47,47), width=7)

            draw_border.line((width-line_len, 0, width, line_len), fill=(255,235,59), width=8)
            draw_border.line((width-line_len-15, 0, width, line_len+15), fill=(211,47,47), width=7)

            draw_border.line((0, height-line_len, line_len, height), fill=(255,235,59), width=8)
            draw_border.line((0, height-line_len-15, line_len+15, height), fill=(211,47,47), width=7)

            draw_border.line((width-line_len, height, width, height-line_len), fill=(255,235,59), width=8)
            draw_border.line((width-line_len-15, height, width, height-line_len-15), fill=(211,47,47), width=7)


            # ===== LOGO (DIPERBESAR) =====
            try:
                logo = Image.open("image.png") 
                logo_w = int(width * 0.22) 
                ratio = logo_w / logo.width
                logo_h = int(logo.height * ratio)
                logo = logo.resize((logo_w, logo_h), Image.Resampling.LANCZOS)

                if logo.mode != "RGBA":
                    logo = logo.convert("RGBA")

                logo_offset = int(border_size * 1.5)
                image.paste(logo, (logo_offset, logo_offset), logo)
            except:
                pass


            # ===== FONT (DIPERBESAR) =====
            font_size = int(width * 0.1)

            try:
                font_title = ImageFont.truetype("arialbd.ttf", font_size)
                font_price = ImageFont.truetype("arialbd.ttf", int(font_size*1.2)) 
            except:
                font_title = ImageFont.load_default()
                font_price = ImageFont.load_default()

            # ===== TEXT & KOTAK TRANSPARAN =====
            text_margin = int(width * 0.08) 
            price_text = f"Rp {harga_barang}"

            try:
                name_bbox = draw.textbbox((0, 0), nama_barang, font=font_title)
                price_bbox = draw.textbbox((0, 0), price_text, font=font_price)
                text_width = max(name_bbox[2], price_bbox[2])
                text_height = (name_bbox[3] - name_bbox[1]) + (price_bbox[3] - price_bbox[1]) + 40 
            except:
                text_width = width * 0.8
                text_height = font_size * 2.5

            box_w = int(text_width + (text_margin * 2))
            box_h = int(text_height + (text_margin * 1.5))
            box_x = (width - box_w) // 2
            box_y = height - box_h - int(height * 0.08) 

            overlay_box = Image.new('RGBA', (box_w, box_h), (0,0,0,160)) 
            image.paste(overlay_box, (box_x, box_y), overlay_box)

            name_x = box_x + text_margin
            name_y = box_y + int(text_margin * 0.7)
            price_x = box_x + text_margin
            price_y = name_y + (name_bbox[3] - name_bbox[1]) + 20

            draw.text((name_x, name_y), nama_barang, fill="white", font=font_title)
            draw.text((price_x, price_y), price_text, fill="#ffd54f", font=font_price)

            buf = io.BytesIO()
            image.save(buf, format="JPEG", quality=95)
            image_final = Image.open(buf)

            st.subheader("✨ Hasil Poster (WhatsApp Story)")
            st.image(image_final, use_container_width=True)

            col1, col2 = st.columns(2)
            with col1:
                st.download_button("💾 Download", buf.getvalue(), file_name="produk_sumini_story.jpg")
            with col2:
                pesan = f"*TOKO SUMINI*\n\n{nama_barang}\nRp {harga_barang}\n\nOrder sekarang"
                link = f"https://wa.me/6289504810142?text={urllib.parse.quote(pesan)}"
                st.link_button("📲 WhatsApp", link)

# ================= HALAMAN VIDEO =========================
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
                if not ret: break
                canvas = np.ones((h+border*2, w+border*2, 3), dtype=np.uint8) * 255
                canvas[border:border+h, border:border+w] = frame
                cv2.rectangle(canvas, (0,0), (w+border*2-1,h+border*2-1), (211,47,47), border)
                cv2.putText(canvas, nama_barang, (50, h), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2)
                cv2.putText(canvas, f"Rp {harga_barang}", (50, h+40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,255), 2)
                out.write(canvas)

            cap.release()
            out.release()
            video_bytes = open(out_path, 'rb').read()
            st.video(video_bytes)
            st.download_button("💾 Download Video", video_bytes, "video_poster.mp4")
            st.success("✅ Video berhasil dibuat!")
