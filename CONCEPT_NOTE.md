# LandTech 2026 Innovation Hackathon
## Track: Digital Land Records, Verification & Digitization
### Project Title: **BhumiGraph (ভূমিগ্রাফ) — Graph-Theoretic Cadastral Lineage & Anti-Double-Selling Engine**
**Problem Statement Addressed**: P3 (Catch Fraud & Double-Selling) & P4 (Smart e-Mutation & Registry)  
**Target Beneficiaries**: Sub-Registry Offices, AC Land & Union Land Offices, Banks & Financial Institutions, Citizens & Buyers  

---

### 1. The Chosen Problem
In Bangladesh, land disputes account for **over 75% of all civil litigation**, clogging the judiciary with millions of Title and Partition suits that span generations. The fundamental vulnerability in the existing land governance ecosystem is that **land records are fragmented across two distinct ministries**:
- **Ministry of Law (Sub-Registry Office)**: Registers private deeds (*Dalil*) without validating whether the seller's title is unencumbered or already depleted.
- **Ministry of Land (AC Land & Tahsil Offices)**: Maintains mutations (*Namjari*), Khatians (RoR), and surveys.

Because these databases do not interact via real-time mathematical validation, three catastrophic forms of fraud persist:
1. **Fractional Over-Selling (Share Depletion Fraud)**: An owner inherits 8 decimals, previously sells 5 decimals, but later sells 10 decimals to an unsuspecting buyer by presenting outdated Khatians.
2. **Female Heir Concealment (Faraiz Fraud)**: Male heirs forge or alter succession certificates (*Warishnama*), concealing sisters and daughters to illegally sell 100% of parental property.
3. **Inter-Registry Double-Selling Window**: Because deed registration takes weeks to appear in physical Balam registers, fraudsters execute sales for the same plot in multiple Sub-Registry windows within the same 48 hours.

---

### 2. Why It Matters in Bangladesh
- **Economic Deadweight**: Trillions of BDT in asset value remain locked in disputed, unbankable land.
- **Social Violence & Court Congestion**: Rural violent crimes and murder disproportionately stem from contested plot boundaries and fractional usurpation.
- **Bank Collateral Defaults**: Financial institutions disburse billions in mortgage loans against forged certified copies (*Nokol*) or land under active court injunctions (*Lis Pendens*).
- **Deprivation of Women**: Millions of Bangladeshi women are unlawfully stripped of their statutory Quranic/Faraiz inheritance rights through co-sharer deception.

---

### 3. The Proposed Solution: BhumiGraph
**BhumiGraph** is an intelligent, graph-theoretic title verification and fraud-prevention engine. Instead of treating land as static tabular rows in separate databases, BhumiGraph models land tenure as an **Immutable Directed Acyclic Graph (DAG)**:
$$\text{CS Survey (1920s)} \longrightarrow \text{SA Survey (1960s)} \longrightarrow \text{RS Survey (1980s)} \longrightarrow \text{BS Survey (2010s)} \longrightarrow \text{Faraiz Splits} \longrightarrow \text{Mutated Deeds}$$

Every owner node is governed by a strict mathematical **Share-Conservation Protocol**:
$$\sum \text{Historical Outgoing Transfers} + \text{Proposed Transfer} \le \text{Acquired Legal Title}$$

If an attempted transaction violates this inequality, or if a legal heir is missing, or if an active court injunction or bank mortgage exists, BhumiGraph triggers an **instant algorithmic hard-lock** that prevents deed registration.

---

### 4. System Architecture & Tech Stack

```
+-----------------------------------------------------------------------------------+
|                        BHUMIGRAPH SYSTEM ARCHITECTURE                             |
+-----------------------------------------------------------------------------------+

   [ Sub-Registry Office ]       [ AC Land / e-Namjari ]      [ Citizen / Bank Portal ]
         |                                  |                           |
         +----------------------------------+---------------------------+
                                            |
                                            v
                                 [ REST API Gateway ]
                                            |
         +----------------------------------+-----------------------------------+
         |                                  |                                   |
         v                                  v                                   v
[ Layer 1: Distributed Lock ]     [ Layer 2: Graph Engine ]     [ Layer 3: Risk Engine ]
 • Real-time 24hr Token Lock       • Cadastral Lineage DAG        • Land Health Score (0-100)
 • Inter-Registry Collision        • Share-Conservation Protocol • Lis Pendens / Injunction
   Prevention                      • Faraiz Succession Validator • Tax Clearance Auditing
         |                                  |                                   |
         +----------------------------------+-----------------------------------+
                                            |
                                            v
                              [ Cryptographic Trust Layer ]
                     • SHA-256 Title Hash & Verifiable QR Code
                     • Direct API Webhook triggering instant e-Mutation
```

#### Technology Stack:
- **Core Verification & Graph Engine**: Python 3.15, Network Graph Traversals, Symbolic Logic Constraints.
- **RESTful API Backend**: Flask / WSGI Micro-framework.
- **Frontend & Visualization**: Modern HTML5, Tailwind CSS, **Vis.js Network Engine** (interactive force-directed hierarchical graph layout).
- **Cryptographic Hashing**: SHA-256 digital deed fingerprints and state-sealed verification certificates.
- **Data Compliance**: 100% synthetic/dummy datasets representing authentic Bangladeshi Mouza geographies (Joydebpur, Savar, Dhanmondi) adhering strictly to LandTech 2026 data ethics.

---

### 5. Main Features & Innovations

1. **Automated Share-Conservation Protocol**:
   Tracks every decimal ever transferred from an ancestor's plot. Eliminates over-selling and dual-selling with mathematical certainty.
2. **Automated Faraiz Inheritance Integrity Validator**:
   Encodes Bangladesh Muslim Succession Law (Quranic fixed shares for wives, daughters, sons, residuaries). Detects omitted female heirs and blocks transactions until legal shares are settled.
3. **Real-Time Inter-Office Distributed Locking**:
   When a deed token is generated at any Sub-Registry, a 24-hour digital lien is created on the parcel. Any simultaneous sale attempt across other sub-registries or branches is instantly blocked.
4. **Court Injunction & Bank Lien Integration (*Lis Pendens*)**:
   Directly flags High Court Status Quo orders and undischarged bank mortgages on the parcel DAG.
5. **Citizen Land Health Index (0 – 100)**:
   A single-click pre-purchase "credit score" for land, empowering buyers to verify title health before paying token money.
6. **Instant Cryptographic Title Certificate**:
   Generates a tamper-evident digital title certificate equipped with a SHA-256 hash and verifiable audit trail.

---

### 6. Nationwide Scalability & E-Governance Integration
BhumiGraph is designed for seamless progressive rollout in Bangladesh's e-governance framework:
- **Phase 1 (API Bridge)**: Connects as an autonomous middleware between the **Ministry of Land's e-Namjari / e-Khatian APIs** and the **Directorate of Registration’s e-Registration system**.
- **Phase 2 (Sub-Registry Gatekeeper)**: Deployed at Sub-Registry desks as a mandatory pre-registration check before printing deed stamps.
- **Phase 3 (Financial Sector API)**: Integrated into Bangladesh Bank’s CIB and commercial bank loan portals for instant collateral verification.
- **Phase 4 (Judiciary Portal)**: Court benches query parcel lineages in seconds, reducing 20-year title suits to days.

---

### 7. Team & Mentors (LandTech 2026)

- **Student Leader (DIU)**: [Student Name, DIU ID]  
- **Student Member (DIU)**: [Student Name, DIU ID]  
- **Faculty Mentor**: [Faculty Name, Department of CSE / Law, DIU]  
- **Industry Mentor**: [Industry Expert Name, Organization / Land-Tech Specialist]  
