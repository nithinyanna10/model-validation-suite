# 🧠 Model Validation Suite

A comprehensive Python-based framework for validating and monitoring pricing models across asset classes. This suite includes interactive dashboards, automated testing, and PDF/HTML reporting capabilities — ideal for financial analytics, quant research, and model risk functions.

---

## 🚀 Features

| Feature                            | Description                                                                 |
|------------------------------------|-----------------------------------------------------------------------------|
| ✅ Streamlit Dashboard             | Interactive UI to explore vol surfaces, yield curves, prices, Greeks, EE   |
| ✅ Black-Scholes Model             | Analytical option pricing + full Greeks                                     |
| ✅ Monte Carlo Simulator           | Simulates Expected Exposure (EE) for XVA modeling                           |
| ✅ Hull-White Model                | Interest rate modeling for ZCB and swaps                                    |
| ✅ Automated Report Generator      | Generates PDF + HTML reports with embedded plots and metadata               |
| ✅ Base64 Image Embedding          | Robust `wkhtmltopdf` support without broken images                          |
| ✅ Test Suite                      | Unit tests + edge cases (pytest-ready)                                      |
| ✅ Configurable & Extensible       | Add new models or validation rules easily                                   |

---

## 🏗 Project Structure
model-validation-suite/
├── app/ # Streamlit dashboard
│ └── streamlit_app.py
├── data/ # Simulated market data
│ ├── vol_surface.csv
│ └── yield_curve.csv
├── models/ # Pricing model implementations
│ ├── black_scholes.py
│ ├── hull_white.py
│ └── monte_carlo_xva.py
├── reports/ # Output reports
│ ├── report_.pdf
│ └── report_.html
├── templates/ # Jinja2 HTML templates
│ └── report_template.html
├── tests/ # Test suite (pytest)
│ └── test_black_scholes.py ...
├── utils/ # Utilities
│ └── report_generator.py
├── main.py # Standalone report generator
└── requirements.txt

---

## ⚙️ Installation

1. **Clone this repo**
```bash
git clone https://github.com/your-username/model-validation-suite.git
cd model-validation-suite

pip install -r requirements.txt

streamlit run app/streamlit_app.py

python main.py
