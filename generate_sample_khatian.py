"""
Generates authentic-looking sample Bengali Khatian images using Nirmala.ttc font.
"""

import os
from PIL import Image, ImageDraw, ImageFont

FONT_PATH = "C:/Windows/Fonts/Nirmala.ttc"

def get_font(size):
    try:
        return ImageFont.truetype(FONT_PATH, size=size, index=0)
    except Exception:
        return ImageFont.load_default()

def create_sample_khatian(filename: str, is_fraud: bool = False):
    width, height = 1100, 850
    # Aged yellowish-parchment background
    bg_color = (250, 246, 233)
    img = Image.new("RGB", (width, height), color=bg_color)
    draw = ImageDraw.Draw(img)

    font_title = get_font(28)
    font_sub = get_font(18)
    font_bold = get_font(18)
    font_regular = get_font(16)
    font_small = get_font(14)

    # Outer vintage border
    draw.rectangle([(20, 20), (width - 20, height - 20)], outline=(80, 60, 40), width=3)
    draw.rectangle([(26, 26), (width - 26, height - 26)], outline=(140, 110, 80), width=1)

    # Title & Header
    draw.text((400, 35), "সি. এস. খতিয়ান (স্বত্বলিপি)", font=font_title, fill=(30, 20, 10))
    draw.text((370, 75), "বাংলাদেশ ফরম নং ৫৪৬৩ (সংশোধিত)", font=font_sub, fill=(70, 50, 30))
    draw.line([(40, 110), (width - 40, 110)], fill=(80, 60, 40), width=2)

    # Administrative Metadata
    draw.text((50, 125), "জেলা: গাজীপুর", font=font_bold, fill=(30, 20, 10))
    draw.text((320, 125), "থানা: জয়দেবপুর", font=font_bold, fill=(30, 20, 10))
    draw.text((600, 125), "মৌজা: জয়দেবপুর", font=font_bold, fill=(30, 20, 10))
    draw.text((870, 125), "জে.এল. নং: ৪২", font=font_bold, fill=(30, 20, 10))

    draw.text((50, 160), "খতিয়ান নং: ৮১০", font=font_bold, fill=(30, 20, 10))
    draw.text((320, 160), "দাগ নং: ৪৫৫", font=font_bold, fill=(30, 20, 10))
    draw.text((600, 160), "জমির শ্রেণী: নাল", font=font_bold, fill=(30, 20, 10))
    draw.text((870, 160), "মোট জমি: ২০.০০ শতাংশ", font=font_bold, fill=(30, 20, 10))

    draw.line([(40, 200), (width - 40, 200)], fill=(80, 60, 40), width=2)

    # Table Header
    draw.rectangle([(40, 205), (width - 40, 245)], fill=(235, 225, 205), outline=(100, 80, 60))
    draw.text((55, 215), "ক্রম", font=font_bold, fill=(40, 30, 20))
    draw.text((120, 215), "মালিক / স্বত্বাধিকারীর নাম ও ঠিকানা", font=font_bold, fill=(40, 30, 20))
    draw.text((520, 215), "পিতা বা স্বামীর নাম", font=font_bold, fill=(40, 30, 20))
    draw.text((800, 215), "অংশ (আনা-গণ্ডা)", font=font_bold, fill=(40, 30, 20))

    # Table Rows
    y = 260
    # Row 1: Tariqul Islam
    # In authentic: 6 ana 8 gonda (0.40 = 40% = 8 decimals)
    # In fraud: 10 ana 0 gonda (illegal inflation)
    tariqul_share = "১০ আনা ০ গণ্ডা" if is_fraud else "৬ আনা ৮ গণ্ডা"
    draw.text((60, y), "১", font=font_regular, fill=(20, 20, 20))
    draw.text((120, y), "তারিকুল ইসলাম", font=font_bold, fill=(20, 20, 20))
    draw.text((520, y), "মৃত রহিম উদ্দিন সরকার", font=font_regular, fill=(20, 20, 20))
    draw.text((800, y), tariqul_share, font=font_bold, fill=(180, 20, 20) if is_fraud else (20, 20, 20))
    draw.line([(40, y + 45), (width - 40, y + 45)], fill=(180, 160, 140), width=1)

    y += 60
    # Row 2: Rafiqul Islam (6 ana 8 gonda)
    draw.text((60, y), "২", font=font_regular, fill=(20, 20, 20))
    draw.text((120, y), "রফিকুল ইসলাম", font=font_bold, fill=(20, 20, 20))
    draw.text((520, y), "মৃত রহিম উদ্দিন সরকার", font=font_regular, fill=(20, 20, 20))
    draw.text((800, y), "৬ আনা ৮ গণ্ডা", font=font_regular, fill=(20, 20, 20))
    draw.line([(40, y + 45), (width - 40, y + 45)], fill=(180, 160, 140), width=1)

    y += 60
    # Row 3: Fatima Begum (3 ana 4 gonda = 0.20 = 20% = 4 decimals)
    draw.text((60, y), "৩", font=font_regular, fill=(20, 20, 20))
    draw.text((120, y), "ফাতেমা বেগম", font=font_bold, fill=(20, 20, 20))
    draw.text((520, y), "মৃত রহিম উদ্দিন সরকার", font=font_regular, fill=(20, 20, 20))
    draw.text((800, y), "৩ আনা ৪ গণ্ডা", font=font_regular, fill=(20, 20, 20))
    draw.line([(40, y + 45), (width - 40, y + 45)], fill=(180, 160, 140), width=1)

    y += 70
    draw.line([(40, y), (width - 40, y)], fill=(80, 60, 40), width=2)
    # Total row
    if is_fraud:
        total_text = "মোট হিস্যা: ১৯ আনা ১২ গণ্ডা (অতিরিক্ত হিস্যা!)"
        color = (180, 20, 20)
    else:
        total_text = "মোট হিস্যা: ১৬ আনা ০ গণ্ডা ০ কড়া ০ ক্রান্তি (পূর্ণাঙ্গ ১৬ আনা)"
        color = (10, 120, 40)

    draw.text((500, y + 15), total_text, font=font_bold, fill=color)

    # Footnote
    draw.text((50, y + 55), "* এই খতিয়ানের অনুলিপি রাজস্ব আইন মোতাবেক প্রস্তুত ও সত্যায়িত।", font=font_small, fill=(100, 80, 60))

    # Revenue stamp box
    draw.rectangle([(width - 180, height - 160), (width - 50, height - 40)], outline=(140, 50, 50), width=2)
    draw.text((width - 165, height - 110), "বাংলাদেশ রাজস্ব", font=font_bold, fill=(140, 50, 50))
    draw.text((width - 150, height - 85), "৫০ টাকা", font=font_small, fill=(140, 50, 50))

    # Save
    out_path = os.path.join(r"C:\Users\valfo\.gemini\antigravity\scratch\bhumigraph\static\samples", filename)
    img.save(out_path, format="JPEG", quality=95)
    print(f"Generated clean rendered image: {out_path}")

if __name__ == "__main__":
    create_sample_khatian("sample_authentic_cs_khatian.jpg", is_fraud=False)
    create_sample_khatian("sample_fraud_cs_khatian.jpg", is_fraud=True)
