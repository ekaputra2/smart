import streamlit as st
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import io
import urllib.parse

# CONFIG
st.set_page_config(page_title="Sumini Mart Pro", layout="centered")

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

.stTextInput input {
    border-radius: 8px;
}

.stFileUploader, .stCameraInput {
    border: 1px dashed #ccc;
    padding: 12px;
    border-radius: 10px;
    background: #fafafa;
}

/* Tombol */
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

# HEADER
st.markdown("<h1>🛒 TOKO SUMINI</h1>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>Poster simple & elegan</div>", unsafe_allow_html=True)

# INPUT
st.markdown("<div class='section'>", unsafe_allow_html=True)
st.subheader("📦 Data Produk")
nama_barang = st.text_input("Nama Produk")
harga_barang = st.text_input("Harga")
st.markdown("</div>", unsafe_allow_html=True)

# FOTO
st.markdown("<div class='section'>", unsafe_allow_html=True)
st.subheader("📸 Upload Foto")
foto_kamera = st.camera_input("Kamera")
foto_galeri = st.file_uploader("Galeri", type=['jpg','png','jpeg'])
st.markdown("</div>", unsafe_allow_html=True)

foto = foto_kamera if foto_kamera else foto_galeri

# BUTTON
st.markdown("<br>", unsafe_allow_html=True)
proses = st.button("✨ BUAT POSTER CLEAN")

# PROCESS
if proses:
    if not foto or not nama_barang or not harga_barang:
        st.error("⚠️ Lengkapi data dulu!")
    else:
        image = Image.open(foto)

        if image.mode in ("RGBA", "P"):
            image = image.convert("RGB")

        width, height = image.size

        # ===== IG STYLE FILTER (soft + clean) =====
        blur_bg = image.copy().filter(ImageFilter.GaussianBlur(12))
        image = Image.blend(blur_bg, image, 0.75)

        draw = ImageDraw.Draw(image)

        # ===== GRADIENT OVERLAY BAWAH (IG STYLE) =====
        overlay = Image.new('RGBA', (width, int(height*0.35)), (0,0,0,0))
        for i in range(overlay.height):
            alpha = int(160 * (i / overlay.height))
            line = Image.new('RGBA', (width, 1), (0,0,0,alpha))
            overlay.paste(line, (0, i))
        image.paste(overlay, (0, height - overlay.height), overlay)

        image = image.convert('RGB')

        # ===== BORDER CLEAN (ROUNDED) + DIAGONAL CORNER LINES =====
        border_size = int(min(width, height) * 0.04)

        new_w = width + border_size*2
        new_h = height + border_size*2
        new_img = Image.new("RGB", (new_w, new_h), (255,255,255))
        new_img.paste(image, (border_size, border_size))

        draw_border = ImageDraw.Draw(new_img)

        radius = int(border_size * 2)

        # merah
        draw_border.rounded_rectangle([0, 0, new_w-1, new_h-1], radius=radius, outline=(211,47,47), width=border_size)

        # kuning
        offset1 = int(border_size * 0.5)
        draw_border.rounded_rectangle([offset1, offset1, new_w-offset1-1, new_h-offset1-1], radius=radius, outline=(255,235,59), width=int(border_size*0.5))

        # biru
        offset2 = int(border_size * 1.1)
        draw_border.rounded_rectangle([offset2, offset2, new_w-offset2-1, new_h-offset2-1], radius=radius, outline=(13,71,161), width=2)

        # diagonal lines
        line_len = int(border_size * 2.5)

        draw_border.line((0, line_len, line_len, 0), fill=(255,235,59), width=4)
        draw_border.line((0, line_len+8, line_len+8, 0), fill=(13,71,161), width=3)

        draw_border.line((new_w-line_len, 0, new_w, line_len), fill=(255,235,59), width=4)
        draw_border.line((new_w-line_len-8, 0, new_w, line_len+8), fill=(13,71,161), width=3)

        draw_border.line((0, new_h-line_len, line_len, new_h), fill=(255,235,59), width=4)
        draw_border.line((0, new_h-line_len-8, line_len+8, new_h), fill=(13,71,161), width=3)

        draw_border.line((new_w-line_len, new_h, new_w, new_h-line_len), fill=(255,235,59), width=4)
        draw_border.line((new_w-line_len-8, new_h, new_w, new_h-line_len-8), fill=(13,71,161), width=3)

        image = new_img
        width, height = image.size
        draw = ImageDraw.Draw(image)

        # ===== LOGO =====
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

        # ===== FONT =====
        font_size = int(width * 0.05)
        try:
            font_title = ImageFont.truetype("arialbd.ttf", font_size)
            font_price = ImageFont.truetype("arial.ttf", int(font_size*0.9))
        except:
            font_title = ImageFont.load_default()
            font_price = ImageFont.load_default()

        # ===== TEXT =====
        margin = int(width * 0.05)
        text_y = height - int(height*0.22)

        box_padding = 15
        text_w = int(width * 0.7)
        text_h = int(font_size * 2.5)

        draw.rectangle([
            margin - box_padding,
            text_y - box_padding,
            margin + text_w,
            text_y + text_h
        ], fill=(0,0,0,120))

        draw.text((margin, text_y), nama_barang, fill="white", font=font_title)
        draw.text((margin, text_y + font_size + 5), f"Rp {harga_barang}", fill="#ffd54f", font=font_price)

        # OUTPUT
        st.subheader("✨ Hasil Poster")
        st.image(image, use_container_width=True)

        buf = io.BytesIO()
        image.save(buf, format="JPEG", quality=90)
        byte_im = buf.getvalue()

        col1, col2 = st.columns(2)

        with col1:
            st.download_button("💾 Download", byte_im, file_name="produk_clean.jpg")

        with col2:
            pesan = f"*TOKO SUMINI*\n\n{nama_barang}\nRp {harga_barang}\n\nOrder sekarang"
            link = f"https://wa.me/6289504810142?text={urllib.parse.quote(pesan)}"
            st.link_button("📲 WhatsApp", link)

        st.success("✅ Desain clean siap dipakai!")