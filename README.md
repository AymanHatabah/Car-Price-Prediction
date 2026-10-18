🚘 Used Car Price Predictor
An interactive, end-to-end Machine Learning web application built with Streamlit that estimates used car market valuations across multiple currencies (USD, EGP, and INR). The system features dynamic brand-and-model filtering, real-time data validation, localized Egyptian market tariff adjustments, and a responsive dark-themed UI.
📌 Key Features
Dynamic Vehicle Selection: Cascading UI dropdowns that automatically filter car models based on the selected manufacturer.
Multi-Currency Valuation Pipeline:
Base valuation computed in Indian Rupee (₹ INR).
Real-time dynamic conversion to US Dollar ($ USD).
Localized valuation in Egyptian Pound (EGP) incorporating tariff/customs adjustments.
Egyptian Market Tariff Multiplier: Applies a 2.0x local market multiplier to account for Egyptian import tariffs, customs duties, and local luxury taxes over raw foreign exchange rates.
Robust Input Validation: Integrated data verification via Pydantic and custom feature aligners (custom_transformer.py) ensuring zero runtime prediction errors.
Modern Executive UI: Customized Streamlit interface with gradient accents and dark-mode styling optimized for scannability.
💡 Model & Valuation Methodology
Valuation Baseline & Depreciation Dynamics
Historical Dataset Baseline (2020): The machine learning model was trained on historical benchmark data from the CarDekho dataset (2020).
Optimal Precision Threshold (Age ≥ 6 Years): Model accuracy is highest for vehicles manufactured in 2020 or earlier (6+ years old). Older cars strictly align with standard linear depreciation curves that remain unaffected by recent post-COVID global supply chain inflation.
Currency & Import Adjustments: Conversion utilizes baseline exchange rates ($1\text{ USD} = 84\text{ INR} \mid 1\text{ USD} = 53\text{ EGP}$) combined with localized Egyptian market overhead factors.
📂 Repository Structure
car-price-predictor/
├── models/
│   └── car_price_model.pkl      # Serialized scikit-learn ML pipeline
├── data/
│   └── CarDekho.csv             # Primary dataset reference
├── .streamlit/
│   └── config.toml              # Streamlit dark theme configuration
├── car_app.py                   # Main Streamlit web application entry point
├── utils.py                     # Data validation schemas (Pydantic) & helper logic
├── custom_transformer.py        # Custom FeatureAligner pipeline transformer
├── price prediction.ipynb       # Exploratory Data Analysis & model training notebook
├── requirements.txt             # Production dependency specification
└── README.md                    # Project documentation
🛠️ Tech Stack
Language: Python 3.10+
Web Framework: Streamlit
Machine Learning & Data Pipelines: Scikit-Learn, Pandas, NumPy, Joblib, Pydantic
Deployment Platform: Streamlit Community Cloud
🚀 Local Setup & Installation
Clone the Repository:
git clone https://github.com/your-username/car-price-predictor.git
cd car-price-predictor
Create and Activate a Virtual Environment:
Linux/macOS:
python3 -m venv venv
source venv/bin/activate
Windows:
python -m venv venv
venv\Scripts\activate
Install Dependencies:
pip install -r requirements.txt
Launch the Application:
streamlit run car_app.py
🌐 Deploying to Streamlit Cloud
Commit and push all repository files to GitHub (ensure temporary files, kaggle.json, and __pycache__ are excluded via .gitignore).
Log in to Streamlit Community Cloud.
Click New App, select your GitHub repository and main branch (main).
Set the Main file path to car_app.py.
Click Deploy.
