import joblib
import pandas as pd
from pathlib import Path
import streamlit as st
from utils import validate_car_data

# ==========================================
# 1. Car Brands and Models Mapping
# ==========================================
CAR_MODELS = {
 "Maruti": [
 "Swift",
 "Alto",
 "Alto 800",
 "Alto K10",
 "Wagon R",
 "Dzire",
 "Swift Dzire",
 "Baleno",
 "Vitara Brezza",
 "Ertiga",
 "Celerio",
 "Ritz",
 "Omni",
 "Eeco",
 "Ciaz",
 "Ignis",
 "S-Cross",
 "Zen",
 "SX4",
 "Estilo",
 "Gypsy",
 "XL6",
 "S-Presso",
 "800",
 ],
 "Hyundai": [
 "i10",
 "i20",
 "Grand i10",
 "Verna",
 "Creta",
 "Santro",
 "Eon",
 "Elantra",
 "Tucson",
 "Venue",
 "Xcent",
 "Getz",
 "Accent",
 "Sonata",
 "Kona Electric",
 "Aura",
 ],
 "Tata": [
 "Tiago",
 "Nexon",
 "Harrier",
 "Safari",
 "Altroz",
 "Indica",
 "Indigo",
 "Hexa",
 "Zest",
 "Nano",
 "Bolt",
 "Tigor",
 "Aria",
 "Sumo",
 "Safari Storme",
 ],
 "Mahindra": [
 "Bolero",
 "Scorpio",
 "XUV500",
 "XUV300",
 "Thar",
 "KUV100",
 "TUV300",
 "Marazzo",
 "Verito",
 "Xylo",
 "Quanto",
 "NuvoSport",
 "Jeep",
 ],
 "Honda": [
 "City",
 "Amaze",
 "Civic",
 "Jazz",
 "WR-V",
 "CR-V",
 "Brio",
 "BR-V",
 "Accord",
 "Mobilio",
 ],
 "Toyota": [
 "Innova",
 "Innova Crysta",
 "Fortuner",
 "Etios",
 "Etios Liva",
 "Etios Cross",
 "Corolla",
 "Corolla Altis",
 "Yaris",
 "Glanza",
 "Camry",
 "Land Cruiser",
 "Qualis",
 ],
 "Ford": [
 "EcoSport",
 "Endeavour",
 "Figo",
 "Aspire",
 "Freestyle",
 "Fiesta",
 "Ikon",
 "Mustang",
 ],
 "Volkswagen": [
 "Polo",
 "Vento",
 "Ameo",
 "Jetta",
 "Tiguan",
 "Passat",
 "CrossPolo",
 ],
 "Renault": [
 "Kwid",
 "Duster",
 "Triber",
 "Pulse",
 "Lodgy",
 "Scala",
 "Fluence",
 ],
 "Nissan": ["Micra", "Sunny", "Kicks", "Terrano", "Evalia", "Teana"],
 "Skoda": [
 "Rapid",
 "Octavia",
 "Superb",
 "Kodiaq",
 "Fabia",
 "Laura",
 "Yeti",
 "Karoq",
 ],
 "Kia": ["Seltos", "Sonet", "Carnival"],
 "MG": ["Hector", "Hector Plus", "ZS EV", "Gloster"],
 "BMW": [
 "3 Series",
 "5 Series",
 "6 Series",
 "7 Series",
 "X1",
 "X3",
 "X4",
 "X5",
 "X6",
 "Z4",
 ],
 "Mercedes-Benz": [
 "A-Class",
 "B-Class",
 "C-Class",
 "E-Class",
 "S-Class",
 "CLA",
 "GLA",
 "GLC",
 "GLE",
 "GLS",
 "M-Class",
 ],
 "Audi": [
 "A3",
 "A4",
 "A6",
 "A8",
 "Q3",
 "Q5",
 "Q7",
 "RS5",
 "S4",
 "S5 Sportback",
 ],
 "Chevrolet": [
 "Beat",
 "Spark",
 "Cruze",
 "Sail",
 "Enjoy",
 "Aveo",
 "Optra",
 "Tavera",
 "Captiva",
 ],
 "Datsun": ["GO", "GO Plus", "redi-GO"],
 "Fiat": [
 "Punto",
 "Punto EVO",
 "Linea",
 "Palio",
 "Uno",
 "Avventura",
 "Urban Cross",
 ],
 "Jeep": ["Compass", "Wrangler", "Grand Cherokee"],
 "Jaguar": ["XE", "XF", "XJ", "F-Pace", "F-Type"],
 "Land Rover": [
 "Range Rover",
 "Range Rover Evoque",
 "Range Rover Sport",
 "Discovery",
 "Discovery Sport",
 "Freelander 2",
 ],
 "Volvo": ["S60", "S90", "XC60", "XC90", "V40"],
 "Mitsubishi": ["Pajero", "Pajero Sport", "Lancer", "Outlander"],
 "Porsche": ["Cayenne", "Macan", "Panamera", "718"],
 "Mini": ["Cooper", "Countryman"],
 "Isuzu": ["D-Max", "mu-X"],
 "Force": ["Gurkha", "One"],
 "Ambassador": ["CLASSIC", "Grand", "Avigo"],
 "Bentley": ["Continental GT", "Flying Spur"],
 "Daewoo": ["Cielo", "Matiz"],
 "Lexus": ["ES", "NX", "RX"],
 "Opel": ["Astra", "Corsa"],
 "Peugeot": ["309"],
}

CAR_BRANDS = sorted(list(CAR_MODELS.keys()))

# ==========================================
# 2. Page Configuration & Dark Styling
# ==========================================
st.set_page_config(
 page_title="Car Price Predictor",
 page_icon="🚘",
 layout="centered",
 initial_sidebar_state="collapsed",
)

st.markdown(
 """
<style>
 /* Dark Page Background */
 .stApp {
 background-color: #0e1117;
 color: #e0e6ed;
 }

 /* Main Header Styling */
 .header-container {
 text-align: center;
 padding: 20px 0 10px 0;
 }
 
 .title-text {
 font-size: 38px !important;
 font-weight: 800;
 background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
 -webkit-background-clip: text;
 -webkit-text-fill-color: transparent;
 margin-bottom: 5px;
 }

 .subtitle-text {
 font-size: 16px;
 color: #94a3b8;
 }

 /* Input Card Container */
 .card-box {
 background: #1a1f2c;
 border: 1px solid #2d3748;
 border-radius: 12px;
 padding: 20px;
 margin-bottom: 20px;
 box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
 }

 /* Prediction Button */
 div.stButton > button:first-child {
 background: linear-gradient(135deg, #00c6ff 0%, #0072ff 100%);
 color: #ffffff;
 font-size: 18px;
 font-weight: bold;
 border: none;
 border-radius: 10px;
 padding: 12px 24px;
 width: 100%;
 transition: all 0.3s ease;
 box-shadow: 0 4px 15px rgba(0, 114, 255, 0.4);
 }

 div.stButton > button:first-child:hover {
 transform: translateY(-2px);
 box-shadow: 0 6px 20px rgba(0, 114, 255, 0.6);
 }

 /* Price Output Card */
 .price-card {
 background: linear-gradient(135deg, #132e27 0%, #0d231d 100%);
 border: 1px solid #10b981;
 border-radius: 12px;
 padding: 25px;
 text-align: center;
 margin-top: 25px;
 box-shadow: 0 0 25px rgba(16, 185, 129, 0.25);
 }

 .price-primary {
 font-size: 42px;
 font-weight: 800;
 color: #10b981;
 margin-bottom: 5px;
 }

 .price-secondary {
 font-size: 22px;
 font-weight: 600;
 color: #34d399;
 margin-bottom: 8px;
 }

 .price-tertiary {
 font-size: 14px;
 color: #a7f3d0;
 }

 /* Data Insight Box */
 .insight-box {
 background-color: #1e293b;
 border-left: 4px solid #38bdf8;
 padding: 15px;
 border-radius: 8px;
 margin-top: 20px;
 font-size: 13px;
 color: #cbd5e1;
 }
</style>
""",
 unsafe_allow_html=True,
)

# Header Section
st.markdown(
 """
 <div class='header-container'>
 <div class='title-text'>🚘 Used Car Price Predictor</div>
 <div class='subtitle-text'>Get an instant USD, EGP & INR fair market valuation using Machine Learning</div>
 </div>
""",
 unsafe_allow_html=True,
)
st.markdown("<br>", unsafe_allow_html=True)


# ==========================================
# 3. Model Loading
# ==========================================
@st.cache_resource
def load_model():
 current_dir = Path.cwd()
 model_path = current_dir / "models" / "car_price_model.pkl"
 if model_path.exists():
  return joblib.load(model_path)
 return None


model = load_model()

if not model:
 st.error(
 "❌ Model file not found. Please ensure 'car_price_model.pkl' exists inside the 'models' directory."
 )
 st.stop()

# ==========================================
# 4. User Interface Inputs
# ==========================================
st.subheader("📋 Vehicle Specifications")

col1, col2 = st.columns(2)

with col1:
 brand = st.selectbox(
 "Car Brand", options=CAR_BRANDS, index=CAR_BRANDS.index("Maruti")
 )

 # Filter available models based on selected brand
 available_models = CAR_MODELS.get(brand, ["Other"])
 model_name = st.selectbox("Car Model", options=available_models)

 car_age = st.number_input(
 "Car Age (Years)", min_value=0, max_value=40, value=6, step=1
 )
 km_driven = st.number_input(
 "Kilometers Driven", min_value=0, value=50000, step=1000
 )

with col2:
 fuel = st.selectbox("Fuel Type", ["Petrol", "Diesel", "CNG", "LPG"])
 transmission = st.selectbox("Transmission", ["Manual", "Automatic"])
 seller_type = st.selectbox(
 "Seller Type", ["Individual", "Dealer", "Trustmark Dealer"]
 )
 owner = st.selectbox(
 "Owner Status",
 [
 "First Owner",
 "Second Owner",
 "Third Owner",
 "Fourth & Above Owner",
 ],
 )

st.markdown("---")

# ==========================================
# 5. Prediction Logic & Output
# ==========================================

# 5. Prediction Logic & Output
# ==========================================
if st.button("✨ Predict Fair Price", use_container_width=True):

    input_data = {
        "car_age": car_age,
        "km_driven": km_driven,
        "brand": brand,
        "fuel": fuel,
        "seller_type": seller_type,
        "transmission": transmission,
        "owner": owner,
        "model": model_name,
    }

    input_df = pd.DataFrame([input_data])

    with st.spinner("Analyzing market data & predicting valuation..."):
        clean_df = validate_car_data(input_df)

        if not clean_df.empty:
            # Predict base price in INR (Base model from 2020 dataset)
            predicted_rupee = model.predict(clean_df)[0]

            # Current Exchange Rates
            usd_to_inr = 84.0
            usd_to_egp = 53.0
            
            # Egyptian Market Customs & Import Multiplier (Taxes/Customs overhead)
            egp_customs_multiplier = 2.2  

            # Conversions
            predicted_usd = predicted_rupee / usd_to_inr
            predicted_egp = (predicted_usd * usd_to_egp) * egp_customs_multiplier

            # Display prediction card
            st.markdown(
                f"""
            <div class='price-card'>
                <div style='color: #94a3b8; font-size: 14px; text-transform: uppercase; letter-spacing: 1px;'>Estimated Valuation</div>
                <div class='price-primary'>${predicted_usd:,.0f} USD</div>
                <div class='price-secondary'>≈ {predicted_egp:,.0f} EGP <span style='font-size: 13px; color: #94a3b8;'>(Incl. Customs & Taxes)</span></div>
                <div class='price-tertiary'>Base Valuation: ₹{predicted_rupee:,.0f} INR</div>
            </div>
            """,
                unsafe_allow_html=True,
            )

            # Methodology & Insights Box
            st.markdown(
                """
            <div class='insight-box'>
                💡 <b>Model & Valuation Methodology:</b><br>
                • <b>Base Market Model (2020 Baseline):</b> The ML model evaluates car depreciation using historical 2020 Indian market data.<br>
                • <b>Optimal Accuracy (Cars Aged 6+ Years):</b> Predictions are most accurate for vehicles aged 6 years or older (2020 & earlier models) as they strictly align with natural depreciation curves.<br>
                • <b>Egyptian Market Adjustment:</b> The EGP price includes a 2.0x local market multiplier to account for local customs, import tariffs, and taxes on top of the base exchange rate (1 USD = 53 EGP).
            </div>
            """,
                unsafe_allow_html=True,
            )
        else:
            st.error(
                "⚠️ Validation Error: Please verify input numbers and parameters."
            )