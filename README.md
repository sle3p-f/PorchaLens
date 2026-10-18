# PorchaLens (পর্চালেন্স) 📜🔍
### AI-Powered Handwritten Bengali Land Record Digitization & 16-Ana Fraud Audit Engine
**LandTech 2026 Innovation Hackathon**  
**Track**: Digital Land Records, Verification & Digitization  
**Problem Focus**: P1 (Digitize Old Records) & P2 (Verify Deeds & Ownership)  
**Organized by**: Department of CSE & CSE-TECH, Daffodil International University (Supported by Department of Law, DIU)  
**Live Production URL**: [https://porchalens.vercel.app](https://porchalens.vercel.app)

---

## 📌 1. Project Overview
In Bangladesh, historical **CS (Cadastral Survey, ~1920s)** and **SA (State Acquisition, ~1960s)** Khatians and Porchas are handwritten in archaic Bengali tenancy fractions (আনা, গণ্ডা, কড়া, ক্রান্তি, তিল). Standard OCR engines fail completely on these degraded manuscripts.

**PorchaLens** solves this through a dual-engine architecture:
1. **Multimodal Vision AI**: Transcribes handwritten Bengali tenancy columns (খতিয়ান প্রকার, জেলা, থানা, মৌজা, খতিয়ান নং, দাগ নং, জমির শ্রেণী, মালিকের নাম ও হস্তলিখিত হিস্যা) with automatic model fallback (`Gemini 3.5 Flash-Lite` $\rightarrow$ `Gemini 3.1 Flash-Lite` $\rightarrow$ `Gemini 3.5 Flash`).
2. **16-Ana Tenancy Math Engine**: Applies historical Bengal Tenancy symbolic constraints ($16 \text{ Anas} = 76,800 \text{ Tils}$). If shares exceed $16\text{ Anas}$, it mathematically detects and flags document tampering and over-allocation.
3. **4-Pillar Citizen Land Safety Suite**: Cross-checks government Khas/Vested land, bank mortgages (NEC), court injunctions (*Lis Pendens*), and land tax clearance with a **0–100 Land Safety Score**.
4. **Automated Faraiz Inheritance Calculator**: Splits ancestral land down to present-day living heirs under the Muslim Family Laws Ordinance 1961, with female heir protection warnings.
5. **Official Smart e-Porcha Certificate**: Emits a printable, government-formatted digital Record of Rights with SHA-256 seal and QR code.

---

## 🏛️ 2. User Personas
Designed with the official Bangladesh Government Land Ministry theme ([mutation.land.gov.bd](https://mutation.land.gov.bd)):
* **নাগরিক সেবা (Citizen Mode)**: Easy upload of family Porchas, instant conversion of archaic units to modern শতাংশ (decimals), inheritance calculator, and pre-purchase safety checks.
* **এসি ল্যান্ড ও তহশিলদার ড্যাশবোর্ড (AC Land & Tahsil Mode)**: Record room batch digitization, 16-Ana forensic audit, in-table correction of damaged text, and official e-Porcha seal generation.

---

## 🛠️ 3. How to Run Locally

### Prerequisites
- Python 3.10+ (tested on Python 3.15)
- Modern web browser

### Quick Start
1. Clone the repository:
   ```bash
   git clone https://github.com/sle3p-f/PorchaLens.git
   cd PorchaLens
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the automated unit tests:
   ```bash
   python test_engine.py
   ```

4. Start the local server:
   ```bash
   python app.py
   ```

5. Open your browser:
   ```
   http://127.0.0.1:5000
   ```

---

## ☁️ 4. Vercel Deployment

PorchaLens is pre-configured for Vercel serverless functions:
- `api/index.py`: Serverless WSGI entrypoint.
- `vercel.json`: Zero-config serverless rewrites.
- In-memory base64 preview: Avoids serverless disk-write limits.

### Environment Variable (Vercel)
In your Vercel project settings:
* **Key**: `GEMINI_API_KEY`
* **Value**: Your Google AI Studio API Key *(a default fallback key is also embedded in the backend for public demo access)*.

---

## 🧪 5. Synthetic Data & Ethical Compliance

In strict compliance with **LandTech 2026 Rule 10**:
* **No Real Personal Data**: All test scenarios and names (Tariqul Islam, Fatima Begum, Rahim Uddin) are synthetic and fabricated for hackathon demonstration.
* **Authentic Cadastral Structure**: Uses authentic administrative Mouza hierarchies (Joydebpur, Gazipur; Savar, Dhaka) without scraping live government databases.

---

## 🤖 6. AI Tools Disclosure

In accordance with Hackathon Rules 10 & 14:
* **Multimodal Extraction**: Google Gemini Vision API (`gemini-3.5-flash-lite`) is used for parsing visual Bengali manuscript pixels into structured JSON.
* **Student Logic**: The 16-Ana base-76,800 symbolic math parser, Faraiz inheritance algorithm, 4-pillar risk engine, and government-themed frontend were designed, validated, and explained by the student team.
