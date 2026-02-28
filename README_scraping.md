# British Airways — Review Scraping & Sentiment Analysis

**British Airways Virtual Internship | Task 1**

---

## 1. What problem are we solving?

British Airways has no systematic way to monitor how passengers feel about their experience across different cabin classes, routes, and traveller types. Reviews are publicly available on Skytrax but exist as unstructured text across hundreds of pages, making them impossible to analyse at scale without automation.

This project solves that by building an end-to-end pipeline: scrape the reviews, clean and structure them, extract sentiment, and surface the patterns that matter to the business.

A second problem is addressed for the Airport Planning team: they have no reliable way to estimate how many passengers will be eligible for each lounge tier at Heathrow Terminal 3 for a given departure. This project delivers a lookup table that answers that question in seconds.

---

## 2. Why does it matter?

Passenger experience is a direct driver of loyalty and repeat bookings. If BA doesn't know which service dimensions are failing and for which customer segments it can't prioritise improvements effectively.

Specifically:
- **Economy class** accounts for the majority of passengers but shows the highest dissatisfaction in reviews. Knowing *what* is driving that dissatisfaction (Food & Entertainment, Value for Money) gives the business a concrete place to act.
- **Lounge staffing** at a major hub like Heathrow T3 is costly to get wrong in either direction overstaffed lounges waste resource, understaffed ones damage premium passenger experience. A data-driven eligibility estimate reduces that uncertainty.

---

## 3. What data did we use?

**Source:** [Skytrax Airline Quality Reviews](https://www.airlinequality.com/airline-reviews/british-airways) scraped across 393 pages using `requests` and `BeautifulSoup`.

**Size:** ~3,900 reviews after cleaning.

| Field | Description |
|---|---|
| `Review Title` | Headline text written by the passenger |
| `Aircraft` | Aircraft type (e.g. Boeing 777, A350) |
| `Type of Traveller` | Business / Couple Leisure / Solo Leisure / Family Leisure |
| `Seat Type` | First / Business / Premium Economy / Economy Class |
| `Route` | Origin–destination pair |
| `Date Flown` | Month and year of travel |
| `Seat Comfort` | Star rating (1–5) |
| `Cabin Staff Service` | Star rating (1–5) |
| `Food & Beverages` | Star rating (1–5) |
| `Inflight Entertainment` | Star rating (1–5) |
| `Ground Service` | Star rating (1–5) |
| `Value For Money` | Star rating (1–5) |

**Key data quality issues:**

| Issue | Resolution |
|---|---|
| Placeholder strings (`'No Aircraft'`, `'No Route'`) | Replaced with `NaN` |
| `Seat Type` missing (2 rows) | Dropped — required for lounge analysis |
| `Type of Traveller` missing | Imputed using group mode by route |
| `Aircraft` missing (~48%) | Predicted using a Random Forest classifier trained on route, seat type, and rating features |

---

## 4. What methods did we apply?

**Scraping**
A pagination loop iterates across all available Skytrax pages. Two helper functions extract text fields and star ratings from each review card. The loop terminates automatically when a page returns no review articles.

**Feature engineering**
- `Overall Rating` — mean of the six individual star rating dimensions
- `Sentiment Score` — VADER compound score computed on review titles
- `Sentiment Label` — Positive / Neutral / Negative (threshold: ±0.05)
- `Review Length` — word count of review title
- `Route Popularity` / `Airline Popularity` — frequency-based features

**Sentiment analysis — two-stage pipeline**
1. **VADER** (rule-based) — assigns compound sentiment scores to review titles without requiring labelled training data
2. **Random Forest Classifier** — trained on VADER scores + engineered features to predict sentiment class; saved to `data/sentiment_model.pkl` for reuse on new review batches

**Exploratory analysis**
- Word frequency analysis on review titles
- Rating distributions by seat type and traveller type
- Feature correlation with overall satisfaction
- Route-level rating analysis (top 30 routes)

**Lounge eligibility modelling**
Routes are grouped into 8 segments (North America, Europe, Asia Pacific, etc.) based on destination keywords. Seat class distributions from the review data serve as a proxy for actual passenger mix. Eligibility percentages are applied per tier:

| Seat Class | Rule |
|---|---|
| First / Business / Premium Economy | 100% eligible for their respective lounge |
| Economy — long-haul | 15% hold top-tier loyalty status |
| Economy — short-haul | 5% hold top-tier loyalty status |

---

## 5. What were the results?

**Satisfaction drivers**
- **Value for Money** and **Cabin Staff Service** are the dimensions most strongly correlated with overall satisfaction — these are BA's highest-leverage improvement areas
- **Business & First Class** rate consistently higher across all dimensions; the biggest class gap is on Food & Beverages and Inflight Entertainment
- **Economy Class** shows the highest variance — a small highly-satisfied segment alongside a large dissatisfied group
- **Solo Leisure travellers** report the most negative experiences; Business travellers are the most consistently satisfied

**Route patterns**
- Long-haul routes (North America, Asia Pacific) show higher average satisfaction than short-haul European routes
- Route-level analysis identifies specific origin–destination pairs where BA consistently over- or under-delivers

**Sentiment**
- Overall sentiment skews negative — dissatisfied passengers are more motivated to write reviews than satisfied ones
- Top terms in negative reviews: *delay*, *poor*, *rude*, *cancelled*, *terrible*
- The trained sentiment model (`sentiment_model.pkl`) can be applied to new review batches quarterly to track trends over time without retraining

**Lounge eligibility**
- North America and Asia Pacific departures have the highest proportion of lounge-eligible passengers, driven by greater Business and First Class loads
- The output `lounge_lookup_table.csv` gives the Airport Planning team a ready-to-use reference: multiply total passenger load by the eligibility rate for each tier to get headcount estimates per lounge

---

## 6. How to run the project?

### Requirements

```bash
pip install requests beautifulsoup4 pandas numpy matplotlib seaborn scikit-learn vaderSentiment wordcloud shap
```

### Steps

```bash
git clone https://github.com/Gopolang24/British-Airways-Review-Scraping-Sentiment-Analysis.git
cd ba-review-analysis
jupyter notebook Scraping.ipynb
```

| Cell range | What it does |
|---|---|
| Cells 1–9 | Scrape reviews from Skytrax → saves `data/reviews.csv` (~10–15 min) |
| Cells 10–48 | Load, clean, engineer features, run sentiment analysis |
| Cells 49–56 | Generate lounge eligibility lookup table |

> **To skip scraping** and use the pre-collected dataset, start from Cell 10: `df = pd.read_csv("data/reviews.csv")`

---

## Repository Structure

```
├── Scraping.ipynb                    # Main notebook (Tasks 1 & 2)
├── BA_Task1_Presentation.pptx        # 7-slide summary presentation
├── data/
│   ├── reviews.csv                   # Scraped & cleaned reviews (~3,900 rows)
│   ├── sentiment_model.pkl           # Trained Random Forest sentiment classifier
│   └── lounge_lookup_table.csv       # Lounge eligibility by route group
└── README.md
```

---

## Limitations

- Skytrax reviews are self-selected — dissatisfied passengers are over-represented; findings reflect perception rather than a random sample of all travellers
- `Aircraft` is imputed for ~48% of rows, adding noise to any aircraft-level analysis
- Lounge eligibility estimates use seat class as a proxy for loyalty tier — actual proportions will vary by route, season, and departure time

---

## Technologies

`Python` · `BeautifulSoup` · `pandas` · `scikit-learn` · `VADER` · `matplotlib` · `seaborn` · `wordcloud` · `SHAP`
