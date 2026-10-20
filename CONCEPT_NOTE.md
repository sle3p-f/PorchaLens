# LandTech 2026 Innovation Hackathon
## Track: Digital Land Records, Verification & Digitization
### Project Title: **PorchaLens (পর্চালেন্স) — AI-Powered Handwritten Land Record Digitization & 16-Ana Fraud Audit Engine**
**Problem Statements Addressed**: P1 (Digitize Old Records) & P2 (Verify Deeds & Ownership)  
**Target Beneficiaries**: AC Land & Union Land Offices (Tahsil), Citizens & Buyers, Banks, Civil Courts  

---

### 1. The Chosen Problem
In Bangladesh, historical land records—specifically **CS (Cadastral Survey, ~1920s)**, **SA (State Acquisition, ~1960s)**, and **RS (Revisional Survey, ~1980s)** Khatians and Porchas—form the foundational bedrock of all land titles. However:
1. **Fragile, Decaying Manuscripts**: Millions of original Balam registers and Porchas in Upazila Record Rooms are brittle, torn, insect-damaged, and written in faded Bengali handwriting.
2. **Archaic Fractional Land Notation**: Historical shares are not recorded in modern decimals; they use complex colonial Bengal tenancy notation:
   $$\text{আনা (Ana)} \longrightarrow \text{গণ্ডা (Gonda)} \longrightarrow \text{কড়া (Kora)} \longrightarrow \text{ক্রান্তি (Kranti)} \longrightarrow \text{তিল (Til)}$$
3. **Failure of Traditional OCR**: Conventional OCR engines (Tesseract, standard Abbyy) fail completely on cursive Bengali handwriting and non-standard layout grids, producing garbled text.
4. **Fraud & Document Tampering**: Fraudsters alter ink strokes or add fabricated co-sharer entries. Because clerks manually copy records, these altered fractional entries go undetected, sparking protracted title lawsuits.

---

### 2. Why It Matters in Bangladesh
- **Millions of Land Disputes**: Over 75% of civil litigation in Bangladesh begins with a disputed or altered historical Khatian entry.
- **Citizen Exploitation**: Ordinary citizens cannot read archaic tenancy fractions, forcing them to rely on corrupt middlemen (*dalals*) who extort heavy fees to "explain" family Porchas.
- **Female Disinheritance**: Female heirs (daughters and widows) are routinely omitted during manual copying of old records, permanently depriving them of statutory inheritance rights.
- **Administrative Gridlock**: AC Land officers and Tahsildars spend weeks physically cross-referencing fragile paper books during e-Mutation inquiries.

---

### 3. The Proposed Solution: PorchaLens (পর্চালেন্স)
**PorchaLens** is an intelligent, dual-engine platform designed specifically for Bangladesh's land administration reality. It combines:
1. **Multimodal Bengali Vision AI**: Transcribes cursive Bengali handwriting and archaic tenancy symbols directly from camera photos or scanned images into structured digital fields.
2. **The "16-Ana" Mathematical Integrity Engine**: Encodes the historical legal rule of Bengal Tenancy:
   $$\text{Total Khatian Share} = 16 \text{ Anas} = 320 \text{ Gondas} = 1,280 \text{ Koras} = 3,840 \text{ Krantis} = 76,800 \text{ Tils}$$
   Instead of trusting raw pixels alone, the engine converts every co-sharer's share into normalized **Tils** and validates:
   $$\sum \text{Tils} \stackrel{?}{=} 76,800$$
   * If $\sum > 76,800$: **Fraud Alert (Over-allocation & Tampering Detected)**.
   * If $\sum < 76,800$: **Torn Margin or Concealed Co-sharer Detected**.
   * If $\sum == 76,800$: **Authentic 16-Ana Record Verified**.
3. **Citizen Pre-Purchase Protection**: Integrates a 4-pillar digital verification suite (Khas/Vested land, Bank Mortgage, Court Injunction, Tax arrears) with a composite **0–100 Land Safety Score**.
4. **Automated Faraiz Inheritance Tree**: Converts ancestral shares into exact modern decimals for surviving heirs under the Muslim Family Laws Ordinance 1961.

---

### 4. System Architecture & Tech Stack

```
+-----------------------------------------------------------------------------------+
|                        PORCHALENS SYSTEM ARCHITECTURE                             |
+-----------------------------------------------------------------------------------+

     [ Citizen Smartphone Photo ]            [ AC Land / Record Room Scan ]
                  │                                         │
                  └────────────────────┬────────────────────┘
                                       │
                                       ▼
                     [ Secure Web Gateway / REST API ]
                                       │
                                       ▼
     ┌───────────────────────────────────────────────────────────────────┐
     │ LAYER 1: Multimodal Vision OCR Engine                             │
     │ • Auto-fallback: Gemini 3.5 Flash-Lite -> 3.1 Flash-Lite -> Flash │
     │ • Structured JSON extraction: Administrative + Co-Sharers         │
     └─────────────────────────────────┬─────────────────────────────────┘
                                       │
                                       ▼
     ┌───────────────────────────────────────────────────────────────────┐
     │ LAYER 2: 16-Ana Tenancy Math Engine                               │
     │ • Normalizes: Ana*4800 + Gonda*240 + Kora*60 + Kranti*20 + Til    │
     │ • Validates: Sum(Tils) == 76,800 (16-Ana Share Conservation)      │
     │ • Calculates: Exact modern Decimals (শতাংশ) per owner              │
     └─────────────────────────────────┬─────────────────────────────────┘
                                       │
                                       ▼
     ┌───────────────────────────────────────────────────────────────────┐
     │ LAYER 3: Citizen Protection & Succession Layer                    │
     │ • 4-Pillar Digital Safety Audit (Khas, Mortgage, Court, Tax)      │
     │ • Muslim Succession Engine (Quranic fixed shares + 2:1 residue)   │
     │ • Official Printable e-Porcha with SHA-256 seal & QR code         │
     └───────────────────────────────────────────────────────────────────┘
```

#### Tech Stack:
- **Backend**: Python 3.15, Flask WSGI framework.
- **Vision AI**: Google Gemini Multimodal Vision API (`gemini-3.5-flash-lite` with automatic rate-limit fallback).
- **Math & Logic**: Pure Python symbolic tenancy unit converter and Faraiz algorithm.
- **Frontend**: Responsive HTML5, Tailwind CSS, Google Hind Siliguri font, styled after `mutation.land.gov.bd`.
- **Deployment**: Vercel Serverless Functions ([porchalens.vercel.app](https://porchalens.vercel.app)).

---

### 5. Main Features & Innovations

1. **Self-Correcting 16-Ana Mathematical Engine**:
   Transforms archaic colonial fractions into mathematically verifiable truths, instantly catching forged entries where someone altered an ink stroke to claim excess land.
2. **Instant Decimal (শতাংশ) Conversion**:
   Automatically calculates the exact decimal land area each co-sharer owns, eliminating reliance on brokers.
3. **Human-in-the-Loop Editable Table**:
   If a fragile document has an ink smear, officers can correct individual cells on-screen and click "Recalculate" to watch the 76,800-Til balance adjust in real-time.
4. **4-Pillar Digital Land Safety Score (0–100)**:
   Empowers citizens to check if a plot is state Khas land, mortgaged to a bank, or tied up in a High Court Status Quo order before paying token money.
5. **Female Heir Rights Protection**:
   The Faraiz engine automatically reserves daughters' and widows' shares and displays a legal protection alert against male co-sharer usurpation.
6. **Smart Digital e-Porcha Certificate**:
   Generates a print-ready, government-watermarked certified record with a cryptographic hash and QR code for instant offline verification.


- **Team Leader (DIU)**: [Student Name, DIU ID]  
- **Co-Developer (DIU)**: [Student Name, DIU ID]  
- **Faculty Mentor**: [Faculty Name, Department of CSE / Law, Daffodil International University]  
- **Industry Mentor**: [Industry Expert Name, Land-Tech Specialist]  
