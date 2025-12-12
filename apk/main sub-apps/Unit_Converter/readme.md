# 🛠️ UniTool (UTConv)

**UniTool** is a modern, all-in-one utility application built with Python. It features a sleek dark-themed UI, real-time data fetching, and a responsive full-screen mode.

![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)
![UI](https://img.shields.io/badge/UI-CustomTkinter-blueviolet.svg)
![Status](https://img.shields.io/badge/Status-Active-success.svg)

## ✨ Features

* **📏 Length Converter**: Convert between Meters, Kilometers, Miles, Feet, Inches, and Yards instantly.
* **🌡️ Temperature Converter**: Seamless conversion between Celsius, Fahrenheit, and Kelvin.
* **⚖️ BMI Calculator**: Calculate Body Mass Index with a **visual progress bar** indicating health categories (Underweight, Normal, Overweight, Obese).
* **💱 Currency Converter**: Real-time exchange rates (USD, EUR, INR, GBP, etc.) fetched via API.
* **🖥️ Modern UI**: Built with `CustomTkinter` for a Windows 11-style look with Dark Mode.
* **⚡ Full Screen Mode**: Toggle between Windowed and Full Screen using the switch or **F11** key.

## 📸 Screenshots

<img width="1919" height="1029" alt="image" src="https://github.com/user-attachments/assets/30afd44b-5bfc-429e-8c8f-f473d679b36c" />

<img width="1919" height="1018" alt="image" src="https://github.com/user-attachments/assets/d08e88a5-cc92-4605-ac22-23389ca0864d" />

## 🚀 Installation

1.  **Clone the repository**
    ```bash
    git clone [https://github.com/yourusername/utconv.git](https://github.com/yourusername/utconv.git)
    cd utconv
    ```

2.  **Set up the Virtual Environment**
    ```bash
    # Windows
    python -m venv .venv
    .\.venv\Scripts\activate

    # Mac/Linux
    python3 -m venv .venv
    source .venv/bin/activate
    ```

3.  **Install Dependencies**
    ```bash
    pip install customtkinter requests
    ```

## ⚙️ Configuration

To make the **Currency Converter** work with live data:

1.  Get a free API key from [ExchangeRate-API](https://www.exchangerate-api.com/).
2.  Open `app.py`.
3.  Find this line and paste your key:
    ```python
    self.api_key = "YOUR_API_KEY_HERE"
    ```

## 🎮 Usage

Run the application using Python:

```bash
python app.py
