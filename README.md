# BhumiGraph (ভূমিগ্রাফ) 🗺️🛡️
### Graph-Theoretic Cadastral Lineage & Anti-Double-Selling Engine
**LandTech 2026 Innovation Hackathon**  
**Track**: Digital Land Records, Verification & Digitization  
**Problem Focus**: P3 (Catch Fraud & Double-Selling) & P4 (Smart e-Mutation & Registry)  
**Organized by**: Department of CSE & CSE-TECH, Daffodil International University (Supported by Department of Law, DIU)

---

## 📌 1. Project Overview
**BhumiGraph** is an intelligent e-governance engine engineered to solve the most pervasive cause of land disputes in Bangladesh: **Broken Title Lineages, Fractional Over-Selling, and Inheritance Depletion Fraud**.

By structuring historical land records (CS $\to$ SA $\to$ RS $\to$ BS) and subsequent transactions as an **Immutable Directed Acyclic Graph (DAG)**, BhumiGraph enforces a strict **Share-Conservation Protocol** and automated **Faraiz (Succession) verification**. Any attempt to sell more than one's remaining legal share, disinherit female heirs, or execute concurrent double-sales across disconnected sub-registries is algorithmically blocked in real time.

---

## 🚀 2. Key Features

- **Interactive Cadastral Lineage Visualizer**: Explores 30+ years of parcel transformations (CS, SA, RS, BS Dags, recorded owners, and mutations) with an interactive Vis.js graph.
- **Mathematical Share-Conservation Engine**: Dynamically calculates legal starting share minus all historical past transfers. Blocks over-selling with exact mathematical deficit proofs.
- **Automated Faraiz Inheritance Validator**: Encodes Bangladesh Muslim Family Law to catch concealed daughters/sisters and illegal share absorption.
- **Inter-Registry Distributed Lock**: Simulates real-time digital lien creation upon deed token generation, eliminating the 48-hour multi-office double-sale window.
- **Court Injunction & Bank Lien (*Lis Pendens*) Detection**: Instantly detects and blocks transfers of plots subject to High Court Status Quo orders or undischarged bank mortgages.
- **Citizen Land Health Index (0 - 100)**: "Check Before You Buy" scoring meter for prospective buyers and commercial bank mortgage vetting.
- **Cryptographic Title Certificate**: Generates tamper-evident digital certificates with SHA-256 hashes and verifiable audit logs.

---

## 🛠️ 3. How to Run the Project

### Prerequisites
- Python 3.10+ (tested on Python 3.15)
- Standard web browser (Chrome, Edge, Firefox)

### Installation & Execution
1. Clone this repository:
   ```bash
   git clone https://github.com/your-username/bhumigraph.git
   cd bhumigraph
   ```

2. Install dependencies (Flask micro-framework):
   ```bash
   pip install flask
   ```

3. Run the automated unit test suite (verifies all 5 fraud test scenarios):
   ```bash
   python test_engine.py
   ```

4. Start the BhumiGraph web platform:
   ```bash
   python app.py
   ```

5. Open your browser and navigate to:
   ```
   http://127.0.0.1:5000
   ```

---

## 🧪 4. Synthetic Data & Ethical Compliance

In strict compliance with **LandTech 2026 Rule 10 (Do's and Don'ts)**:
- **Zero Real Personal Data**: All names, National ID numbers (NID), phone numbers, and deed numbers are completely synthetic and fabricated for simulation purposes.
- **Authentic Bangladeshi Cadastral Structure**: Uses authentic administrative hierarchies (e.g., Mouza: Joydebpur, JL 42, Gazipur Sadar; Mouza: Savar, Dhaka; Mouza: Dhanmondi, Dhaka) with realistic survey lineages (CS $\to$ SA $\to$ RS $\to$ BS).
- **No Scraping**: No data was scraped or bulk-downloaded from live government portals.

---

## 🤖 5. AI Tools Disclosure (Hackathon Transparency)

In accordance with Hackathon Rules 10 & 14:
- **AI Coding Assistant**: Google Antigravity / Gemini was used for code scaffolding, architectural ideation, and rapid test-case synthesis.
- **Student Authorship**: All algorithms, legal constraint logic (Faraiz mathematical modeling, Share Conservation protocol, and distributed lien simulations) were designed, validated, and explained by the student team.

---

## 👥 6. Team & Mentorship
- **Team**: 2 DIU Students (Team Leader & Co-Developer)
- **Mentors**: 1 Faculty Mentor (DIU CSE / Law) + 1 Industry Mentor
- **Institution**: Daffodil International University, Knowledge Tower, Ashulia, Dhaka.
