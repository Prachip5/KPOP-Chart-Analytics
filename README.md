# K-POP Chart Analytics

### Comeback Momentum • Chart Re-entry • Fandom Intensity • Sustainability

A data-driven K-pop analytics project that studies how songs leave and return to the South Korea Top 50 chart, how strong their comebacks are, how repeated appearances can indicate fandom intensity, and how consistently songs sustain chart presence.

---

## Project Overview

K-POP Chart Analytics is a Data Science project built around the South Korea Top 50 chart.

The project analyzes chart behaviour at both song and artist level and develops analytical measures for:

- Chart re-entry
- Comeback momentum
- Fandom intensity
- Chart sustainability
- Artist sustainability
- Integrated song performance

The final results are presented through an interactive Streamlit dashboard.

---

## Objectives

The main objectives of this project are to:

1. Clean and validate the supplied chart dataset.
2. Identify songs that leave and later return to the Top 50.
3. Measure the strength of comeback events.
4. Analyze repeated chart appearances as a project-specific fandom-intensity signal.
5. Measure how consistently songs maintain chart presence.
6. Compare song and artist-level performance.
7. Integrate multiple analytical dimensions into an overall performance score.
8. Build an interactive dashboard for exploring the results.

---

## Dataset

The project uses the supplied South Korea Top 50 chart dataset.

### Dataset information

- Raw records: **27,800**
- Exact duplicate rows: **16**
- Chart structure: **Top 50**
- Main analytical unit: song and artist
- Final cleaned dataset: validated to contain exactly 50 records per chart date

### Main fields

The dataset contains information including:

- Date
- Chart position
- Song
- Artist
- Popularity
- Duration
- Album information
- Explicit-content indicator
- Album artwork URL

---

## Data Cleaning & Validation

The supplied dataset contains:

- 27,800 raw rows
- 16 exact duplicate rows
- One date (`2025-03-01`) containing 100 records instead of 50
- Duplicate date-position records on that date

The notebook applies the following cleaning process:

1. Remove exact duplicate rows.
2. Resolve duplicate date-position records by keeping the first source record.
3. Validate chart dates.
4. Confirm that every chart date contains exactly 50 records.

The cleaned dataset is then used for all subsequent analysis.

---

# Analytical Framework

## 1. Chart Re-entry

A chart re-entry occurs when a song appears on the chart again after previously leaving the tracked Top 50.

The analysis identifies:

- Previous chart appearance
- Re-entry date
- Gap between appearances
- Re-entry position
- Number of re-entry events

---

## 2. Comeback Momentum

Comeback momentum measures the strength of a song's return using:

- Gap before re-entry
- Re-entry chart position

The resulting momentum score is a project-specific analytical measure designed to compare comeback events.

---

## 3. Fandom Intensity

Fandom intensity is a project-specific index based on:

- Re-entry frequency
- Chart strength
- Average comeback momentum

It is used as an analytical proxy for repeated chart engagement rather than a direct measurement of real-world fandom size.

---

## 4. Chart Sustainability

Sustainability combines several dimensions of repeated chart performance:

- Re-entry frequency
- Chart strength
- Comeback momentum
- Fandom intensity

This provides a comparative measure of how consistently songs maintain chart presence.

---

## 5. Integrated Performance

The final integrated analysis combines:

- Sustainability
- Fandom intensity
- Comeback momentum

These dimensions are normalized and combined into an overall performance score for comparative analysis.

> **Note:** The project scores are analytical indices created specifically for this project. They should not be interpreted as direct measurements of real-world fandom size, popularity, or commercial success.

---

# Project Workflow

```text
Raw Dataset
     │
     ▼
Data Cleaning & Validation
     │
     ▼
Exploratory Data Analysis
     │
     ▼
Chart Re-entry Detection
     │
     ▼
Comeback Momentum
     │
     ▼
Fandom Intensity
     │
     ▼
Chart Sustainability
     │
     ▼
Integrated Performance
     │
     ▼
Interactive Dashboard
