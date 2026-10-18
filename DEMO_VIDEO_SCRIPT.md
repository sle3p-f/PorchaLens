# BhumiGraph — 90-Second Demo Video Script
### LandTech 2026 Innovation Hackathon (Round 1 Submission)
*Target Duration: Exactly 85–90 seconds*  
*Tone: Crisp, authoritative, highly technical, and solutions-oriented.*

---

### [00:00 – 00:15] Hook: The Core Bangladesh Dilemma
- **Visual**: Screen shows the Bangladesh Land Administration dilemma diagram (Ministry of Law vs. Ministry of Land disconnect) or a shot of paper Balam books.
- **Voiceover**: 
  > *"Over 75% of all civil litigation in Bangladesh stems from land fraud. Why? Because Sub-Registry offices register deeds without knowing if the seller's title is already depleted, if sisters were deprived of inheritance, or if a court injunction is active. We built BhumiGraph to fix this."*

---

### [00:15 – 00:35] Solution Introduction & Lineage Graph
- **Visual**: Screen opens `http://127.0.0.1:5000`. Demonstrator selects *Joydebpur, Gazipur (BS Dag 810)*. The dynamic lineage graph animates from CS Dag 104 &rarr; SA 212 &rarr; RS 455 &rarr; BS 810, then expands into the Faraiz family tree.
- **Voiceover**: 
  > *"BhumiGraph models land tenure as a mathematical Directed Acyclic Graph. Here, late Rahim Uddin left 20 decimals in Gazipur. Under Muslim Faraiz law, our engine automatically computes the legal shares: 8 decimals each for two sons, and 4 decimals for daughter Fatima."*

---

### [00:35 – 00:55] Live Fraud Test: Fractional Over-Selling & Sister Depletion
- **Visual**: Demonstrator clicks **"1. Fractional Over-Selling"** on the left panel. The center console flashes bright red with `REJECTED: Fractional Over-Selling Fraud Detected`. The mathematical proof is displayed (-7 decimals deficit). Next, click **"2. Sister Disinheritance"**, showing the pink warning flagging the omission of Fatima Begum.
- **Voiceover**: 
  > *"Watch what happens when son Tariqul—who already sold 5 decimals in 2024—attempts to sell 10 decimals. Our Share-Conservation Protocol detects that only 3 decimals remain, calculates an illegal deficit of 7 decimals, and instantly blocks the Sub-Registrar! When brothers try to omit their sister from the Warishnama, BhumiGraph flags Faraiz fraud immediately."*

---

### [00:55 – 01:15] Inter-Registry Collision & Court Injunction
- **Visual**: Click **"3. Court Injunction Violation"** (showing Dhaka Court Status Quo order block) and **"4. Inter-Registry Collision"** (showing the real-time distributed lock symbol on the graph).
- **Voiceover**: 
  > *"BhumiGraph also bridges the 48-hour inter-registry loophole. When a deed is being processed at Gazipur Sub-Registry, an instant cryptographic lock is placed on the parcel, preventing simultaneous double-selling in other offices. It also halts sales of land under High Court Status Quo orders."*

---

### [01:15 – 01:30] Clean Title & Citizen Due Diligence
- **Visual**: Demonstrator selects *Dhanmondi BS 1104*, clicks **"5. Clean Title Verification"**. The badge lights up green `TRANSACTION APPROVED`. Click **"Title Certificate"** to show the cryptographic modal with SHA-256 hash and Land Health Score 100/100.
- **Voiceover**: 
  > *"For clean properties, BhumiGraph generates an instant SHA-256 cryptographic Title Certificate and feeds directly into e-Namjari. BhumiGraph: Turning Bangladesh’s opaque land records into mathematical truth. Thank you."*
