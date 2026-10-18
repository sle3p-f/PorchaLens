# BhumiGraph — Final Round Pitch Deck Structure (10 Slides)
### LandTech 2026 Innovation Hackathon
*Knowledge Tower (Library), Daffodil International University*  
*Presentation Time: 5 Minutes Pitch & Live Demo | 3 Minutes Q&A*

---

### Slide 1: Title & Team
- **Header**: **BhumiGraph (ভূমিগ্রাফ)**
- **Subtitle**: Graph-Theoretic Cadastral Lineage & Anti-Double-Selling Engine
- **Track**: Digital Land Records, Verification & Digitization
- **Team**: 2 DIU Students + 1 Faculty Mentor + 1 Industry Mentor
- **Institution**: Department of CSE & Department of Law, Daffodil International University

---

### Slide 2: The National Crisis: The Broken Land Administration
- **Statistics**: 75–80% of all civil cases in Bangladesh courts are land title disputes.
- **The Core Bottleneck**: The Dual-Ministry Silo.
  - Ministry of Law (Sub-Registry) registers private deeds (*Dalil*) without verifying title.
  - Ministry of Land (AC Land / DLRS) tracks Khatians and Surveys.
- **Result**: The same plot is fractionalized, over-sold, and disputed across generations.

---

### Slide 3: The 3 Main Land Frauds in Bangladesh
1. **Fractional Over-Selling**: Selling 10 decimals when only 3 decimals remain in the inherited share.
2. **Female Heir Disinheritance (Faraiz Fraud)**: Forging Warishnama certificates to omit sisters/mothers.
3. **Inter-Registry 48-Hour Double-Sale Window**: Selling the same plot across two sub-districts before physical Balam books are updated.

---

### Slide 4: Our Solution: BhumiGraph
- Models land tenure not as flat text, but as an **Immutable Directed Acyclic Graph (DAG)**:
  $$\text{CS Survey} \longrightarrow \text{SA} \longrightarrow \text{RS} \longrightarrow \text{BS} \longrightarrow \text{Faraiz Splits} \longrightarrow \text{Mutations}$$
- Turns land verification into **algorithmic certainty** rather than manual discretion.

---

### Slide 5: The Core Innovation: Share-Conservation Protocol
- Mathematical constraint applied to every parcel:
  $$\sum \text{Historical Outgoing Transfers} + \text{Proposed Transfer} \le \text{Acquired Legal Title}$$
- Dynamic title balance tracking stops over-selling at the Sub-Registry desk before paper stamps are printed.

---

### Slide 6: Automated Faraiz (Succession) Integrity Engine
- Fully automated algorithmic model of Bangladesh Muslim Succession Law (Quranic fixed shares).
- Cross-references submitted succession claims (*Warishnama*) with official civil records.
- Blocks transactions if female heirs (daughters, wives, mothers) are concealed or usurped.

---

### Slide 7: Real-Time Inter-Registry Distributed Locking & Lis Pendens
- **Distributed Token Lock**: When Deed processing starts in one Sub-Registry, a 24-hour cryptographic lock prevents concurrent registration anywhere else in Bangladesh.
- **Judicial Lis Pendens**: Live sync with Court registries blocks transactions on plots subject to High Court Status Quo orders or active bank mortgages.

---

### Slide 8: Live Demo & Architecture (Live Software Showcase)
*(Switch to live demo running on `http://127.0.0.1:5000`)*
- Demo 1: Fractional Over-Selling attempt blocked (-7 decimals deficit).
- Demo 2: Sister disinheritance caught.
- Demo 3: Clean Dhanmondi title certified with SHA-256 hash & 100/100 Land Health Score.

---

### Slide 9: National Scalability & E-Governance Integration
- **Zero Heavy Infrastructure Required**: Lightweight REST APIs that plug directly into existing government portals:
  - Ministry of Land: `e-Namjari` and `e-Khatian`
  - Ministry of Law: `e-Registration`
  - Financial Sector: Bangladesh Bank CIB and commercial bank collateral portals.
- Modular, privacy-preserving, and cloud-ready.

---

### Slide 10: Conclusion & Vision
- **From Deed Registration to State-Guaranteed Title (Torrens Model)**.
- Restoring peace of mind to 170 million citizens, unlocking billions in dead capital, and decluttering our judicial system.
- **BhumiGraph**: *Where Law Meets Code for Smart E-Governance.*
- **Q&A**: Ready for the Judges' questions!
