# Project Brief: The "Sugar Trap" Market Gap Analysis

**Client:** Helix CPG Partners (Strategic Food & Beverage Consultancy)  
**Deliverable:** Interactive Dashboard, Code Notebook & Insight Presentation

---
## A. Executive Summary
Analysis of 500,000 products from the Open Food Facts dataset confirms
that the snack market is overwhelmingly concentrated in the high-sugar,
low-protein quadrant, validating the client hypothesis about market
oversaturation. Across eight snack categories analysed, Nuts & Seeds
emerged as the strongest Blue Ocean opportunity with a Market Opportunity
Score of 52.1 out of 100 nearly double that of Chocolate & Candy (11.4),
the most saturated and nutritionally poor category in the dataset.
Ingredient analysis of existing high-protein and low-sugar products
identifies whey, peanut, and soy as the three dominant protein sources,
giving the R&D team a validated and immediately actionable formulation
starting point. The data supports an immediate investment in a
high-protein, low-sugar Nuts & Seeds snack line as the clearest
first-mover opportunity in the current market.

## B. Project Links

- **Notebook:** [Google Colab](https://colab.research.google.com/drive/1kx1MD0HaqwcTR-OWR9VYw4fR9DmXZD1K?usp=sharing)
- **Dashboard:** [Streamlit App](https://the-market-gap-analysis-am4gnbq5haktmra3xq43re.streamlit.app/)
- **Presentation:** [Google Slides](https://docs.google.com/presentation/d/1SRTucnT60J_tzusc_a-7uULXB4Ob4fq-zwONXvH_P-g/edit?usp=sharing)


## C. Technical Explanation

### Data Cleaning (Story 1)
- Loaded the first 500,000 rows from the Open Food Facts .csv.gz file
- Dropped rows with null values in product_name, sugars_100g, and proteins_100g
- Removed biologically impossible values which is any nutrient value above 100g per 100g
- Filtered energy to a realistic range of 0 to 4,000 kJ per 100g since Open
  Food Facts stores energy in kJ not kcal
- Removed duplicate product names keeping the first occurrence to prevent
  category distribution skew

### Candidate's Choice — Market Opportunity Score Leaderboard

What I added:
A weighted Market Opportunity Score (0–100) that ranks every snack category
by its Blue Ocean potential, displayed as an interactive leaderboard on the
dashboard.

Why I added it:
The scatter plot and heatmap show WHERE the gap is but a client sitting
in a boardroom needs to know WHICH category to enter first. I noticed that
presenting multiple charts still required the client to interpret and compare
them mentally before reaching a decision. By collapsing four data signals
into one ranked score per category, the R&D team gets a single, defensible
answer they can act on immediately without any further analysis.

How the score works:
The Market Opportunity Score is built on four weighted signals, 
each chosen for a specific business reason.

Protein content carries the highest weight at 35% because high-protein 
snacking is the number one consumer health trend globally. Low sugar 
follows at 30% as it directly addresses the core client brief of reducing 
sugar oversaturation in the market. Fiber content accounts for 20% as a 
secondary but increasingly demanded health signal among conscious consumers. 
Finally, low competition is weighted at 15% — categories with fewer existing 
products offer easier shelf placement, stronger pricing power, and better 
margin potential for a new entrant.
Together these four signals produce a single score out of 100 per category, 
giving the R&D team one clear, ranked and defensible answer.

What it delivers:
The leaderboard ranks all seven categories from highest to lowest opportunity,
shows a colour-coded bar chart from red to green, and displays a winner
callout box naming the top category with its exact protein and sugar averages.

## 1.Business Context
**Helix CPG Partners** advises major food manufacturers on new product development. Our newest client, a global snack manufacturer, wants to launch a "Healthy Snacking" line. They believe the market is oversaturated with sugary treats, but they lack the data to prove where the specific gaps are.

They have hired us to answer one question: **"Where is the 'Blue Ocean' in the snack aisle?"**

Specifically, they are looking for product categories that are currently under-served—areas where consumer demand for health (e.g., High Protein, High Fiber) is not being met by current product offerings (which are mostly High Sugar, High Fat).

## 2. The Data
You will use the **Open Food Facts** dataset, a free, open, and massive database of food products from around the world.

* **Source:** [Open Food Facts Data](https://world.openfoodfacts.org/data)
* **Format:** CSV (Comma Separated Values)
* **Warning:** The full dataset is massive (over 3GB). You are **not** expected to process the entire file. You should filter the data early or work with a manageable subset (e.g., the first 500,000 rows or specific categories).

## 3. Tooling Requirements
You have the flexibility to choose your development environment:

* **Option A (Recommended):** Use a cloud-hosted notebook like **Google Colab**, or **Deepnote**, etc.
* **Option B:** Use a local **Jupyter Notebook** or **VS Code**.
    * *Condition:* If you choose this, you must ensure your code is reproducible. Do not reference local file paths (e.g., `C:/Downloads/...`). Assume the dataset is in the same folder as your notebook.
* **Dashboarding:** The final output must be a **publicly accessible link** (e.g., Tableau Public, Google Looker Studio, Streamlit Cloud, or PowerBI Web).

---

## 4. User Stories & Acceptance Criteria

### Story 1: Data Ingestion & "The Clean Up"
**As a** Strategy Director,  
**I want** a clean dataset that removes products with erroneous nutritional information,  
**So that** my analysis is not skewed by bad data entry.

* **Acceptance Criteria:**
    * Handle missing values: Decide what to do with rows that have `null` or empty `sugars_100g`, `proteins_100g`, or `product_name`.
    * Handle outliers: Filter out biologically impossible values.
    * **Deliverable:** A cleaned Pandas DataFrame or SQL table export.

### Story 2: The Category Wrangler
**As a** Product Manager,  
**I want** to group products into readable high-level categories,  
**So that** I don't have to look at 10,000 unique, messy tags like `en:chocolate-chip-cookies-with-nuts`.

* **Acceptance Criteria:**
    * The `categories_tags` column is a comma-separated string (e.g., `en:snacks, en:sweet-snacks, en:biscuits`). You must parse this string.
    * Create a logic to assign a "Primary Category" to each product based on keywords.
    * Create at least 5 distinct high-level buckets.

### Story 3: The "Nutrient Matrix" Visualization
**As a** Marketing Lead,  
**I want** to see a Scatter Plot comparing Sugar (X-axis) vs. Protein (Y-axis) for different categories,  
**So that** I can visually spot where the products are clustered.

* **Acceptance Criteria:**
    * Create a dashboard (PowerBI, Tableau, Streamlit, or Python-based charts) displaying this relationship.
    * Allow the user to filter the chart by the "High Level Categories" you created in Story 2.
    * **Key Visual:** Identify the "Empty Quadrant" (e.g., High Protein + Low Sugar).

### Story 4: The Recommendation
**As a** Client,  
**I want** a clear text recommendation on what product we should build,  
**So that** I can take this to the R&D team.

* **Acceptance Criteria:**
    * On the dashboard, include a "Key Insight" box.
    * Complete this sentence: *"Based on the data, the biggest market opportunity is in [Category Name], specifically targeting products with [X]g of protein and less than [Y]g of sugar."*

---

## 5. Bonus User Story: The "Hidden Gem"
**As a** Health Conscious Consumer,  
**I want** to know which specific ingredients are driving the high protein content in the "good" products,  
**So that** I can replicate this in our new recipe.

* **Acceptance Criteria:**
    * Analyze the `ingredients_text` column for products in your "High Protein" cluster.
    * Extract and list the Top 3 most common protein sources (e.g., "Whey", "Peanuts", "Soy").

---

## 6. The "Candidate's Choice" Challenge
**As a** Creative Analyst,  
**I want** to add one additional feature or analysis to this project that I believe provides massive value,  
**So that** I can show off my business acumen.

* **Instructions:**
    * Add one more chart, filter, or metric that wasn't asked for.
    * Explain **why** you added it.
    * **There is no wrong answer, but you must justify your choice.**

---

## 7. Submission Guidelines
Please edit this `README.md` file in your forked repository to include the following three sections at the top:

### A. The Executive Summary
* A 3-5 sentence summary of your findings.

### B. Project Links
* **Link to Notebook:** (e.g., Google Colab, etc.). *Ensure sharing permissions are set to "Anyone with the link can view".*
* **Link to Dashboard:** (e.g., Tableau Public / Power BI Web, etc.).
* **Link to Presentation:** A link to a short slide deck (PDF, PPT) AND (Optional) a 2-minute video walkthrough (YouTube) explaining your results.

### C. Technical Explanation
* Briefly explain how you handled the "Data Cleaning".
* Explain your "Candidate's Choice" addition.

**Important Note on Code Submission:**
* Upload your `.ipynb` notebook file to the repo.
* **Crucial:** Also upload an **HTML or PDF export** of your notebook so we can see your charts even if GitHub fails to render the notebook code.
* Once you are ready, please fill out the [Official Submission Form Here](https://forms.office.com/e/heitZ9PP7y) with your links

---

## 🛑 CRITICAL: Pre-Submission Checklist

**Before you submit your form, you MUST complete this checklist.**

> ⚠️ **WARNING:** If you miss any of these items, your submission will be flagged as "Incomplete" and you will **NOT** be invited to an interview. 
>
> **We do not accept "permission error" excuses. Test your links in Incognito Mode.**

### 1. Repository & Code Checks
- [ ] **My GitHub Repo is Public.** (Open the link in a Private/Incognito window to verify).
- [ ] **I have uploaded the `.ipynb` notebook file.**
- [ ] **I have ALSO uploaded an HTML or PDF export** of the notebook.
- [ ] **I have NOT uploaded the massive raw dataset.** (Use `.gitignore` or just don't commit the CSV).
- [ ] **My code uses Relative Paths.** 

### 2. Deliverable Checks
- [ ] **My Dashboard link is publicly accessible.** (No login required).
- [ ] **My Presentation link is publicly accessible.** (Permissions set to "Anyone with the link can view").
- [ ] **I have updated this `README.md` file** with my Executive Summary and technical notes.

### 3. Completeness
- [ ] I have completed **User Stories 1-4**.
- [ ] I have completed the **"Candidate's Choice"** challenge and explained it in the README.

**✅ Only when you have checked every box above, proceed to the submission form.**

---
