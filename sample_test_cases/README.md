# 📜 PorchaLens Sample Test Cases (নমুনা দলিল ও খতিয়ান পরীক্ষণ সংকলন)

This directory contains real historical Bengali handwritten land deed and tenancy record (*দলিল ও খতিয়ান*) sample test cases, categorized into **Good Deeds** and **Faulty Deeds**, curated for auditing and benchmarking the **PorchaLens** AI vision engine, 16-Ana tenancy math engine, and 4-layer citizen land security audit.

---

## 📁 Directory Structure

```text
sample_test_cases/
├── Good/                       # Authentic, high-legibility deeds with clear cadastral math
│   ├── dolil_7.jpg             # Standard clean CS deed
│   ├── dolil_8.jpg             # High-contrast authentic tenancy porcha
│   ├── dolil_9.jpg             # Complete 16-Ana co-sharer table
│   ├── dolil_99.jpg            # Authentic mutation (খারিজ) deed
│   └── dolil_635.jpg           # Cadastral survey parcel record
│
└── Faulty/                     # Damaged, blurry, torn, or math-tampered deed papers
    ├── dolil_5.jpg             # Blurry cursive handwriting (low paleographic confidence)
    ├── dolil_69.jpg            # Missing / torn Dag (দলিল নম্বর) triggering 4-layer 'Can't Find'
    └── dolil_82.jpg            # Water-damaged / faded margin record with share deficit
```

---

## 🎯 Benchmark Verification Scenarios

| Category | File | Primary Defect / Characteristic | Expected PorchaLens Output |
| :--- | :--- | :--- | :--- |
| **Good** | `dolil_7.jpg` | Clear header, intact 16-Ana breakdown | `AUTHENTIC_PERFECT` (১০০% নির্ভুল), 100/100 Safety Score |
| **Good** | `dolil_8.jpg` | Legible Dag & Mouza metadata | Clean Cadastral Registry Match, Clear Title clearance |
| **Good** | `dolil_9.jpg` | Multi-heir tenancy distribution | Correct Base-76,800 Til to Modern Decimals conversion |
| **Good** | `dolil_99.jpg` | Official Government Stamp format | SHA-256 Digitally Signed e-Porcha Verification |
| **Good** | `dolil_635.jpg`| High-resolution survey record | Complete paleographic OCR & Faraiz tree generator |
| **Faulty** | `dolil_5.jpg` | Paleographic blur / ink degradation | Handwriting Alert: ঝাপসা/অস্পষ্ট, Prompt for re-inspection |
| **Faulty** | `dolil_69.jpg` | Missing / torn parcel ID (দাগ নং) | **4-Pillar Security Audit: `Can't Find`** across all layers |
| **Faulty** | `dolil_82.jpg` | Torn margin / missing co-sharer | `DEFICIT_OR_TORN` (ছেঁড়া পাতা বা হিস্যা ঘাটতি) warning |

---

## 🚀 How to Test These Cases

### 1. Web Inspection (One-Click)
Open the PorchaLens Web App ([porchalens.vercel.app](https://porchalens.vercel.app) or `http://127.0.0.1:5000`), drag-and-drop any image from `sample_test_cases/Good/` or `sample_test_cases/Faulty/` directly into the upload pane.

### 2. Automated Test Suite
Run the automated test suite locally:
```bash
python test_engine.py
```
