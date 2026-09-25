# Deterministic Matching & Compatibility Engine

> **Transparent, auditable, and mathematically grounded opportunity matching.**

---

## 1. Engine Design Philosophy

Unlike typical "AI job platforms" that send candidate resumes and job postings directly to an LLM to hallucinate arbitrary percentages, ZyncRole AI implements a **deterministic 8-dimension matching formula**.

- **Auditable & Reproducible:** Two evaluations with the same profile and job posting will always produce the identical score.
- **Explainable by Design:** Every percentage is broken down into constituent sub-scores, letting candidates understand exactly why they matched or where the gap lies.
- **Zero Hallucination:** AI embeddings are strictly used to compute high-dimensional semantic cosine similarity between candidate skills and job descriptions, not to guess an arbitrary score.

---

## 2. The 8-Dimension Mathematical Formula

The total compatibility score $S_{total} \in [0, 100]$ is computed as:

$$S_{total} = 100 \times \sum_{i=1}^{8} \left( w_i \times s_i \right)$$

Where $w_i$ represents the normalized dimension weight and $s_i \in [0.0, 1.0]$ represents the dimension score.

### Normalized Dimension Weights

As verified in `backend/app/core/config.py`:

| Dimension $i$ | Name | Weight ($w_i$) | Description |
|:---|:---|:---:|:---|
| 1 | **Skill Compatibility** | `0.30` | Overlap of candidate skills against required & preferred skills. |
| 2 | **Role Alignment** | `0.15` | Fuzzy string similarity between desired roles and job title. |
| 3 | **Domain Alignment** | `0.10` | Match between user's preferred domains and classified job domain. |
| 4 | **Experience Level** | `0.10` | Candidate career level / years vs job requirements (fresher friendly). |
| 5 | **Education Fit** | `0.05` | Degree level and technical specialization alignment. |
| 6 | **Location & Mobility** | `0.10` | Geographic overlap or remote eligibility. |
| 7 | **Preferences Fit** | `0.05` | Work mode (Remote/Hybrid/Onsite) & salary expectation alignment. |
| 8 | **Semantic Embeddings** | `0.15` | Cosine similarity between candidate embedding & job embedding. |
| **Total** | | **`1.00`** | Strict validation enforced at configuration bootstrap. |

---

## 3. Sub-Score Algorithms

### 3.1 Skill Compatibility ($s_1$)
- Uses a canonical skills taxonomy (`backend/app/data/skills_dictionary.json`).
- If a job defines required skills:
  $$s_{req} = \frac{|\text{User Skills} \cap \text{Required Skills}|}{|\text{Required Skills}|}$$
- If preferred skills are defined:
  $$s_{pref} = \frac{|\text{User Skills} \cap \text{Preferred Skills}|}{|\text{Preferred Skills}|}$$
  $$s_1 = 0.75 \times s_{req} + 0.25 \times s_{pref}$$
- If no skills are explicitly declared, extracts skills from job description text.

### 3.2 Role Alignment ($s_2$)
- Employs `RapidFuzz` token set ratio with abbreviation expansion:
  $$\text{Ratio} = \max_{r \in \text{Desired Roles}} \text{token\_set\_ratio}(r, \text{Job Title})$$
  $$s_2 = \frac{\text{Ratio}}{100}$$

### 3.3 Experience Level ($s_3$)
- **Fresher Candidates:** If the job is tagged `eligible_for_fresher == True` or `experience_min <= 1.0`, award $1.0$. If $1.0 < \text{experience\_min} \le 2.0$, award $0.65$. If $> 2.0$, award $0.20$.
- **Experienced Candidates:** Computes candidate experience duration against $[\text{experience\_min}, \text{experience\_max}]$.

### 3.4 Semantic Cosine Similarity ($s_8$)
- Embeddings are generated using **Gemini Embedding 2** (`text-embedding-004`, 768 dimensions).
- When operating in fully offline mode without an API key, the engine gracefully falls back to a deterministic **TF-IDF Vectorizer with Sublinear Term Frequency Scaling**.
- Cosine similarity:
  $$\text{sim}(\vec{u}, \vec{v}) = \frac{\vec{u} \cdot \vec{v}}{\|\vec{u}\|_2 \|\vec{v}\|_2}$$
  $$s_8 = \max(0.0, \min(1.0, \text{sim}(\vec{u}, \vec{v})))$$

---

## 4. Match Explanation & Actionable Guidance

The `explanation_agent` synthesizes the 8-dimension breakdown into human-centered microcopy:

1. **Compatibility Level:**
   - $\ge 85\%$: "Strong Match"
   - $70\% - 84\%$: "High Compatibility"
   - $55\% - 69\%$: "Moderate Compatibility"
   - $< 55\%$: "Developing Fit"
2. **Missing Required Skills:** Pinpointed directly from job requirements.
3. **Missing Preferred Skills:** Pinpointed as bonus differentiation opportunities.
4. **Concrete Action Plan:** Generates tailored advice on projects to build or keywords to add to maximize ATS pass rate for this exact role.
