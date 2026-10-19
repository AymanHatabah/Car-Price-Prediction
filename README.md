
# 🚘 Used Car Price Predictor

An interactive, end-to-end Machine Learning web application built with **Streamlit** that estimates used car market valuations across multiple currencies (**USD**, **EGP**, and **INR**). The system features dynamic brand-and-model filtering, real-time data validation, localized Egyptian market tariff adjustments, and a responsive dark-themed UI.

---

## 📌 Key Features

- **Dynamic Vehicle Selection**: Cascading UI dropdowns that automatically filter car models based on the selected manufacturer.
- **Multi-Currency Valuation Pipeline**:
  - Base valuation computed in **Indian Rupee (₹ INR)**.
  - Real-time dynamic conversion to **US Dollar ($ USD)**.
  - Localized valuation in **Egyptian Pound (EGP)** incorporating tariff/customs adjustments.
- **Egyptian Market Tariff Multiplier**: Applies a `2.0x` local market multiplier to account for Egyptian import tariffs, customs duties, and local luxury taxes over raw foreign exchange rates.
- **Robust Input Validation**: Integrated data verification via `Pydantic` and custom feature aligners (`custom_transformer.py`) ensuring zero runtime prediction errors.
- **Modern Executive UI**: Customized Streamlit interface with gradient accents and dark-mode styling optimized for scannability.

---

## 💡 Model & Valuation Methodology

> **Valuation Baseline & Depreciation Dynamics**
>
> - **Historical Dataset Baseline (2020)**: The machine learning model was trained on historical benchmark data from the CarDekho dataset (2020).
> - **Optimal Precision Threshold (Age ≥ 6 Years)**: Model accuracy is highest for vehicles manufactured in **2020 or earlier (6+ years old)**. Older cars strictly align with standard linear depreciation curves that remain unaffected by recent post-COVID global supply chain inflation.
> - **Currency & Import Adjustments**: Conversion utilizes baseline exchange rates (1 USD = 84 INR | 1 USD = 53 EGP) combined with localized Egyptian market overhead factors.

---

## 📂 Repository Structure

```

Car-Price-Prediction/
├── models/
│   └── car\_price\_model.pkl      \# Serialized scikit-learn ML pipeline
├── data/
│   └── CarDekho.csv             \# Primary dataset reference
├── .streamlit/
│   └── config.toml              \# Streamlit dark theme configuration
├── car\_app.py                   \# Main Streamlit web application entry point
├── utils.py                     \# Data validation schemas (Pydantic) & helper logic
├── custom\_transformer.py        \# Custom FeatureAligner pipeline transformer
├── price prediction.ipynb       \# Exploratory Data Analysis & model training notebook
├── requirements.txt             \# Production dependency specification
└── README.md                    \# Project documentation

```` 

---

## 🛠️ Tech Stack

- **Language**: Python 3.10+
- **Web Framework**: Streamlit
- **Machine Learning & Data Pipelines**: Scikit-Learn, Pandas, NumPy, Joblib, Pydantic
- **Deployment Platform**: Streamlit Community Cloud

---


<!-- end list -->

``` 
 
