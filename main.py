import streamlit as st
import google.generativeai as genai

genai.configure(api_key="AIzaSyCOurA7apjW_9x99kiFFm0MeAaIsVWD1T0")
model = genai.GenerativeModel("gemini-2.0-flash")

units : dict = {
    "📏 Length": {
        "Meter": 1,
        "Centimeter": 100,
        "Kilometer": 0.001,
        "Millimeter": 1000, 
        "Mile": 0.000621371, 
        "Yard": 1.09361, 
        "Foot": 3.28084, 
        "Inch": 39.3701
    },
    "⚖️ Mass": {
        "Kilogram": 1,
        "Gram": 1000, 
        "Pound": 2.20462, 
        "Ounce": 35.274
    },
    "🌡️ Temperature": {
        "Celsius": 1,
        "Fahrenheit": 33.8,
        "Kelvin": 274.15,
    },
    "⏳ Time": {
        "Second": 1,
        "Millisecond": 1000,
        "Minute": 0.01667,
        "Hour": 0.0002778,
        "Day": 0.00001157,
        "Week": 0.000001653,
        "Month (Approx)": 0.0000003803,
        "Year (Approx)": 0.0000000317
    },
    "🧪 Volume": {
        "Liter": 1,
        "Milliliter": 1000,
        "Cubic Meter": 0.001,
        "Cubic Centimeter": 1000,
        "Cubic Millimeter": 1000000,
    }

}

def convert(value, from_unit, to_unit, category):
    if category == "🌡️ Temperature":
        if from_unit == "Celsius" and to_unit == "Fahrenheit":
            return (value * 9/5) + 32
        elif from_unit == "Celsius" and to_unit == "Kelvin":
            return value + 273.15
        elif from_unit == "Fahrenheit" and to_unit == "Celsius":
            return (value - 32) * 5/9
        elif from_unit == "Fahrenheit" and to_unit == "Kelvin":
            return (value - 32) * 5/9 + 273.15
        elif from_unit == "Kelvin" and to_unit == "Celsius":
            return value - 273.15
        elif from_unit == "Kelvin" and to_unit == "Fahrenheit":
            return (value - 273.15) * 9/5 + 32
        else: 
            return value
    else:
        if category in units:
            factor_from = units[category][from_unit]
            factor_to = units[category][to_unit]
            return (value / factor_from) * factor_to
    return None

st.set_page_config(page_title='⚖️ MeasureMate', layout="wide")
st.markdown(
    """
    <style>
        .stSidebar {
            background-color:rgb(232, 176, 249); 
            color:#31333F;
            padding: 15px;
        }
        
        #title {
            font-size: 5rem;
            font-weight: bold;
            color: rgb(232, 176, 249);
            text-align: center;
            margin-bottom: 2rem;
        }

        #subtitle {
            font-size: 2rem;
            font-weight: bold;
            margin-bottom: 2rem;
            margin-top: 2rem;
        }
        
        .stRadio label { margin-bottom: 1rem; }

        .stNumberInput, .stTextInput, .stTextArea, .stSelectbox {
            background-color:rgb(232, 176, 249);
            border-radius: 5px;
            padding: 12px;
            width: 100%;
            font-size: 2rem;
            color: black;
        }

        
        .stButton>button { background-color:white; color:rgb(232, 176, 249); border: 2px solid rgb(232, 176, 249); padding: 12px;
                           border-radius: 6px; cursor: pointer; }
        .stButton>button:hover { background-color: rgb(232, 176, 249); color: white; border: 2px solid rgb(232, 176, 249);  }
    </style>
    """,
    unsafe_allow_html=True
)

st.sidebar.markdown('<p id="subtitle">🚀 AI-Powered Unit Converter - MeasureMate</p>', unsafe_allow_html=True)

category = st.sidebar.radio("🔹" , ["📏 Length", "⚖️ Mass", "🧪 Volume", "🌡️ Temperature", "⏳ Time", "💬 Need Help? Ask AI"], label_visibility="hidden")

if category == "💬 Need Help? Ask AI":
    st.markdown('<p id="title">🧠 Your  MeasureMate AI</p>', unsafe_allow_html=True)
    st.markdown("""
        <div>
            <p style="font-size:1.5rem; text-align:center; font-weight:bold">🤖 Confused about units? Just ask!</p>
        </div>
    """, unsafe_allow_html=True)
    
    user_input = st.text_input("You:", "", placeholder="Write and Ask...")

    if st.button("Send"):
        if user_input:
            response = model.generate_content(user_input)
            st.text_area("Bot:", response.text, height=150)
        else:
            st.write("oops! something went wrong")

else:
    is_chatbot = ""
    st.markdown('<p id="title">✨ MeasureMate ✨</p>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    from_unit = col1.selectbox("From:", list(units[category].keys()))
    to_unit = col2.selectbox("To:", list(units[category].keys()))

    value = st.number_input("Enter the Value:", min_value=0.0, step=0.1)

    if st.button("Convert"):
        result = convert(value, from_unit, to_unit, category)
        st.success(f"{value} {from_unit} = {result:.4f} {to_unit}")



