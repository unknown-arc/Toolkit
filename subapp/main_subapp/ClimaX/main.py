import tkinter as tk
from tkinter import ttk, font, messagebox
import requests
from datetime import datetime
import json
import time

class ModernWeatherApp:
    def __init__(self, root):
        self.root = root
        self.root.title("SkyCast - Weather & AQI Forecast")
        self.root.geometry("1000x750")
        self.root.configure(bg="#1a1a2e")
        
        # WeatherAPI.com Configuration
        self.api_key = "4d308312f6f44d9297545010251212"
        self.base_url = "https://api.weatherapi.com/v1"
        self.current_city = "London"
        self.unit = "metric"
        
        # Weather icons mapping for WeatherAPI.com
        self.weather_icons = {
            "Sunny": "☀️", "Clear": "🌙",
            "Partly cloudy": "⛅", "Cloudy": "☁️",
            "Overcast": "☁️", "Mist": "🌫️",
            "Patchy rain possible": "🌦️", "Patchy snow possible": "❄️",
            "Patchy sleet possible": "🌨️", "Patchy freezing drizzle possible": "🌨️",
            "Thundery outbreaks possible": "⛈️", "Blowing snow": "❄️",
            "Blizzard": "❄️", "Fog": "🌫️", "Freezing fog": "🌫️",
            "Patchy light drizzle": "🌧️", "Light drizzle": "🌧️",
            "Freezing drizzle": "🌧️", "Heavy freezing drizzle": "🌧️",
            "Patchy light rain": "🌦️", "Light rain": "🌧️",
            "Moderate rain at times": "🌧️", "Moderate rain": "🌧️",
            "Heavy rain at times": "🌧️", "Heavy rain": "🌧️",
            "Light freezing rain": "🌧️", "Moderate or heavy freezing rain": "🌧️",
            "Light sleet": "🌨️", "Moderate or heavy sleet": "🌨️",
            "Patchy light snow": "❄️", "Light snow": "❄️",
            "Patchy moderate snow": "❄️", "Moderate snow": "❄️",
            "Patchy heavy snow": "❄️", "Heavy snow": "❄️",
            "Ice pellets": "🧊", "Light rain shower": "🌦️",
            "Moderate or heavy rain shower": "🌧️", "Torrential rain shower": "🌧️",
            "Light sleet showers": "🌨️", "Moderate or heavy sleet showers": "🌨️",
            "Light snow showers": "❄️", "Moderate or heavy snow showers": "❄️",
            "Light showers of ice pellets": "🧊", "Moderate or heavy showers of ice pellets": "🧊",
            "Patchy light rain with thunder": "⛈️", "Moderate or heavy rain with thunder": "⛈️",
            "Patchy light snow with thunder": "⛈️", "Moderate or heavy snow with thunder": "⛈️"
        }
        
        # AQI Color Coding and Categories (US AQI Scale)
        self.aqi_colors = {
            1: {"color": "#00E400", "text": "Good", "emoji": "😊"},
            2: {"color": "#FFFF00", "text": "Moderate", "emoji": "😐"},
            3: {"color": "#FF7E00", "text": "Unhealthy for Sensitive Groups", "emoji": "😷"},
            4: {"color": "#FF0000", "text": "Unhealthy", "emoji": "😷"},
            5: {"color": "#8F3F97", "text": "Very Unhealthy", "emoji": "🤢"},
            6: {"color": "#7E0023", "text": "Hazardous", "emoji": "☠️"}
        }
        
        # Pollutant names
        self.pollutants = {
            "co": "Carbon Monoxide",
            "no2": "Nitrogen Dioxide",
            "o3": "Ozone",
            "so2": "Sulfur Dioxide",
            "pm2_5": "PM2.5",
            "pm10": "PM10"
        }
        
        # Create custom fonts
        self.title_font = font.Font(family="Segoe UI", size=24, weight="bold")
        self.city_font = font.Font(family="Segoe UI", size=18, weight="bold")
        self.temp_font = font.Font(family="Segoe UI", size=48, weight="bold")
        self.desc_font = font.Font(family="Segoe UI", size=14)
        self.detail_font = font.Font(family="Segoe UI", size=12)
        self.forecast_font = font.Font(family="Segoe UI", size=10)
        self.aqi_font = font.Font(family="Segoe UI", size=16, weight="bold")
        
        # Color scheme
        self.colors = {
            "bg": "#1a1a2e",
            "card_bg": "#16213e",
            "highlight": "#0f3460",
            "text": "#ffffff",
            "accent": "#e94560",
            "secondary": "#4cc9f0",
            "aqi_good": "#00E400",
            "aqi_moderate": "#FFFF00",
            "aqi_unhealthy": "#FF7E00",
            "aqi_very_unhealthy": "#FF0000",
            "aqi_hazardous": "#8F3F97"
        }
        
        # Create UI
        self.create_widgets()
        
        # Load initial weather
        self.root.after(1000, lambda: self.search_weather("London"))
    
    def create_widgets(self):
        # Main container with padding
        main_container = tk.Frame(self.root, bg=self.colors["bg"], padx=20, pady=20)
        main_container.pack(fill=tk.BOTH, expand=True)
        
        # Header
        header_frame = tk.Frame(main_container, bg=self.colors["bg"])
        header_frame.pack(fill=tk.X, pady=(0, 20))
        
        # App title
        title_label = tk.Label(header_frame, text="🌤️ SkyCast Pro", 
                              font=self.title_font, 
                              bg=self.colors["bg"], 
                              fg=self.colors["text"])
        title_label.pack(side=tk.LEFT)
        
        # Search frame
        search_frame = tk.Frame(header_frame, bg=self.colors["bg"])
        search_frame.pack(side=tk.RIGHT)
        
        # Search entry
        self.search_var = tk.StringVar()
        self.search_entry = tk.Entry(search_frame, 
                                    textvariable=self.search_var,
                                    font=self.desc_font,
                                    width=25,
                                    bg=self.colors["card_bg"],
                                    fg=self.colors["text"],
                                    insertbackground="white",
                                    relief=tk.FLAT)
        self.search_entry.insert(0, "Enter city name...")
        self.search_entry.bind("<FocusIn>", self.on_entry_focus_in)
        self.search_entry.bind("<FocusOut>", self.on_entry_focus_out)
        self.search_entry.bind("<Return>", lambda e: self.search_weather())
        self.search_entry.pack(side=tk.LEFT, padx=(0, 10))
        
        # Search button
        search_btn = tk.Button(search_frame, 
                              text="🔍 Search",
                              command=self.search_weather,
                              font=self.detail_font,
                              bg=self.colors["accent"],
                              fg="white",
                              relief=tk.FLAT,
                              padx=20,
                              pady=8,
                              cursor="hand2")
        search_btn.pack(side=tk.LEFT)
        
        # Unit toggle
        self.unit_var = tk.StringVar(value="metric")
        unit_frame = tk.Frame(header_frame, bg=self.colors["bg"])
        unit_frame.pack(side=tk.RIGHT, padx=(20, 0))
        
        tk.Label(unit_frame, text="Units:", 
                font=self.detail_font, 
                bg=self.colors["bg"], 
                fg=self.colors["text"]).pack(side=tk.LEFT, padx=(0, 5))
        
        tk.Radiobutton(unit_frame, text="°C", 
                      variable=self.unit_var, 
                      value="metric",
                      command=self.toggle_unit,
                      font=self.detail_font,
                      bg=self.colors["bg"],
                      fg=self.colors["text"]).pack(side=tk.LEFT, padx=5)
        
        tk.Radiobutton(unit_frame, text="°F", 
                      variable=self.unit_var, 
                      value="imperial",
                      command=self.toggle_unit,
                      font=self.detail_font,
                      bg=self.colors["bg"],
                      fg=self.colors["text"]).pack(side=tk.LEFT, padx=5)
        
        # Status label
        self.status_label = tk.Label(header_frame,
                                    text="Ready",
                                    font=self.detail_font,
                                    bg=self.colors["bg"],
                                    fg=self.colors["secondary"])
        self.status_label.pack(side=tk.RIGHT, padx=(0, 20))
        
        # Main content area
        content_frame = tk.Frame(main_container, bg=self.colors["bg"])
        content_frame.pack(fill=tk.BOTH, expand=True)
        
        # Top row - Current weather and AQI
        top_row = tk.Frame(content_frame, bg=self.colors["bg"])
        top_row.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        # Left panel - Current weather
        weather_panel = tk.Frame(top_row, bg=self.colors["card_bg"], 
                                relief=tk.RIDGE, bd=1, padx=20, pady=20)
        weather_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        # Current weather display
        self.create_weather_widgets(weather_panel)
        
        # Right panel - AQI
        aqi_panel = tk.Frame(top_row, bg=self.colors["card_bg"],
                            relief=tk.RIDGE, bd=1, padx=20, pady=20)
        aqi_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # AQI display
        self.create_aqi_widgets(aqi_panel)
        
        # Bottom row - Forecast
        bottom_row = tk.Frame(content_frame, bg=self.colors["card_bg"],
                             relief=tk.RIDGE, bd=1, padx=20, pady=20)
        bottom_row.pack(fill=tk.BOTH, expand=True, pady=(10, 0))
        
        # Forecast display
        self.create_forecast_widgets(bottom_row)
    
    def create_weather_widgets(self, parent):
        # Title
        weather_title = tk.Label(parent,
                                text="Current Weather",
                                font=self.city_font,
                                bg=self.colors["card_bg"],
                                fg=self.colors["text"])
        weather_title.pack(anchor=tk.W, pady=(0, 10))
        
        # Current weather display
        current_frame = tk.Frame(parent, bg=self.colors["card_bg"])
        current_frame.pack(fill=tk.BOTH, expand=True)
        
        # City and time
        self.city_label = tk.Label(current_frame, 
                                  text="Please enter a city", 
                                  font=self.city_font,
                                  bg=self.colors["card_bg"],
                                  fg=self.colors["text"])
        self.city_label.pack(anchor=tk.W, pady=(0, 5))
        
        self.time_label = tk.Label(current_frame,
                                  text="Waiting for data...",
                                  font=self.detail_font,
                                  bg=self.colors["card_bg"],
                                  fg=self.colors["secondary"])
        self.time_label.pack(anchor=tk.W, pady=(0, 20))
        
        # Temperature and icon frame
        temp_icon_frame = tk.Frame(current_frame, bg=self.colors["card_bg"])
        temp_icon_frame.pack(fill=tk.X, pady=10)
        
        # Weather icon
        self.weather_icon = tk.Label(temp_icon_frame, 
                                    text="🌤️",
                                    font=("Segoe UI Emoji", 72),
                                    bg=self.colors["card_bg"])
        self.weather_icon.pack(side=tk.LEFT, padx=(0, 20))
        
        # Temperature and description
        temp_desc_frame = tk.Frame(temp_icon_frame, bg=self.colors["card_bg"])
        temp_desc_frame.pack(side=tk.LEFT, fill=tk.Y)
        
        self.temp_label = tk.Label(temp_desc_frame,
                                  text="--°C",
                                  font=self.temp_font,
                                  bg=self.colors["card_bg"],
                                  fg=self.colors["text"])
        self.temp_label.pack(anchor=tk.W)
        
        self.desc_label = tk.Label(temp_desc_frame,
                                  text="Enter a city to get weather data",
                                  font=self.desc_font,
                                  bg=self.colors["card_bg"],
                                  fg=self.colors["secondary"])
        self.desc_label.pack(anchor=tk.W)
        
        # Weather details grid
        details_frame = tk.Frame(current_frame, bg=self.colors["card_bg"])
        details_frame.pack(fill=tk.X, pady=20)
        
        # Create detail boxes
        self.create_detail_boxes(details_frame)
    
    def create_aqi_widgets(self, parent):
        # Title
        aqi_title = tk.Label(parent,
                            text="🌍 Air Quality Index (AQI)",
                            font=self.city_font,
                            bg=self.colors["card_bg"],
                            fg=self.colors["text"])
        aqi_title.pack(anchor=tk.W, pady=(0, 10))
        
        # Main AQI display
        aqi_main_frame = tk.Frame(parent, bg=self.colors["card_bg"])
        aqi_main_frame.pack(fill=tk.X, pady=10)
        
        # AQI Value
        self.aqi_value_label = tk.Label(aqi_main_frame,
                                       text="--",
                                       font=("Segoe UI", 72, "bold"),
                                       bg=self.colors["card_bg"],
                                       fg="#FFFFFF")
        self.aqi_value_label.pack(side=tk.LEFT, padx=(0, 20))
        
        # AQI Info
        aqi_info_frame = tk.Frame(aqi_main_frame, bg=self.colors["card_bg"])
        aqi_info_frame.pack(side=tk.LEFT, fill=tk.Y)
        
        self.aqi_category_label = tk.Label(aqi_info_frame,
                                          text="No AQI Data",
                                          font=self.aqi_font,
                                          bg=self.colors["card_bg"],
                                          fg="#FFFFFF")
        self.aqi_category_label.pack(anchor=tk.W)
        
        self.aqi_emoji_label = tk.Label(aqi_info_frame,
                                       text="",
                                       font=("Segoe UI Emoji", 36),
                                       bg=self.colors["card_bg"])
        self.aqi_emoji_label.pack(anchor=tk.W, pady=5)
        
        self.aqi_health_label = tk.Label(aqi_info_frame,
                                        text="Health Impact: N/A",
                                        font=self.detail_font,
                                        bg=self.colors["card_bg"],
                                        fg=self.colors["secondary"])
        self.aqi_health_label.pack(anchor=tk.W)
        
        # Pollutants frame
        pollutants_frame = tk.Frame(parent, bg=self.colors["card_bg"])
        pollutants_frame.pack(fill=tk.BOTH, expand=True, pady=(20, 0))
        
        # Pollutants title
        pollutants_title = tk.Label(pollutants_frame,
                                   text="Pollutants Concentration",
                                   font=self.detail_font,
                                   bg=self.colors["card_bg"],
                                   fg=self.colors["text"])
        pollutants_title.pack(anchor=tk.W, pady=(0, 10))
        
        # Create pollutant bars
        self.pollutant_labels = {}
        pollutants = ["pm2_5", "pm10", "o3", "no2", "so2", "co"]
        
        for i, pollutant in enumerate(pollutants):
            frame = tk.Frame(pollutants_frame, bg=self.colors["card_bg"])
            frame.pack(fill=tk.X, pady=3)
            
            # Pollutant name
            name_label = tk.Label(frame,
                                 text=self.pollutants.get(pollutant, pollutant),
                                 font=self.detail_font,
                                 bg=self.colors["card_bg"],
                                 fg=self.colors["text"],
                                 width=20,
                                 anchor=tk.W)
            name_label.pack(side=tk.LEFT)
            
            # Value label
            value_label = tk.Label(frame,
                                  text="-- μg/m³",
                                  font=self.detail_font,
                                  bg=self.colors["card_bg"],
                                  fg=self.colors["secondary"],
                                  width=15)
            value_label.pack(side=tk.RIGHT)
            
            self.pollutant_labels[pollutant] = value_label
    
    def create_forecast_widgets(self, parent):
        # Title
        forecast_title = tk.Label(parent,
                                 text="3-Day Forecast",
                                 font=self.city_font,
                                 bg=self.colors["card_bg"],
                                 fg=self.colors["text"])
        forecast_title.pack(anchor=tk.W, pady=(0, 20))
        
        # Forecast container
        forecast_container = tk.Frame(parent, bg=self.colors["card_bg"])
        forecast_container.pack(fill=tk.BOTH, expand=True)
        
        # Initialize forecast frames
        self.forecast_frames = []
        for i in range(3):
            frame = tk.Frame(forecast_container,
                            bg=self.colors["highlight"],
                            relief=tk.RAISED,
                            bd=1,
                            padx=15,
                            pady=15)
            frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)
            
            # Day label
            day_label = tk.Label(frame, text=f"Day {i+1}", 
                                font=self.forecast_font,
                                bg=self.colors["highlight"],
                                fg=self.colors["text"])
            day_label.pack(anchor=tk.W, pady=(0, 10))
            
            # Weather icon
            icon_label = tk.Label(frame, text="🌤️",
                                 font=("Segoe UI Emoji", 36),
                                 bg=self.colors["highlight"])
            icon_label.pack(pady=5)
            
            # Temperature
            temp_label = tk.Label(frame, text="--°C / --°C",
                                 font=self.forecast_font,
                                 bg=self.colors["highlight"],
                                 fg=self.colors["text"])
            temp_label.pack(pady=5)
            
            # Condition
            cond_label = tk.Label(frame, text="--",
                                 font=self.forecast_font,
                                 bg=self.colors["highlight"],
                                 fg=self.colors["secondary"])
            cond_label.pack(pady=5)
            
            # AQI
            aqi_label = tk.Label(frame, text="AQI: --",
                                font=self.forecast_font,
                                bg=self.colors["highlight"],
                                fg=self.colors["text"])
            aqi_label.pack(pady=5)
            
            self.forecast_frames.append({
                'frame': frame,
                'day': day_label,
                'icon': icon_label,
                'temp': temp_label,
                'cond': cond_label,
                'aqi': aqi_label
            })
    
    def create_detail_boxes(self, parent):
        # Define details to show
        details = [
            ("Feels Like", "feels_like", "🌡️"),
            ("Humidity", "humidity", "💧"),
            ("Wind Speed", "wind_speed", "💨"),
            ("Pressure", "pressure", "📊"),
            ("Visibility", "visibility", "👁️"),
            ("UV Index", "uv", "☀️"),
            ("Precipitation", "precip", "🌧️")
        ]
        
        # Create two columns
        for i in range(0, len(details), 4):
            column_frame = tk.Frame(parent, bg=self.colors["card_bg"])
            column_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
            
            for j in range(i, min(i+4, len(details))):
                label, key, icon = details[j]
                
                # Detail box
                detail_frame = tk.Frame(column_frame,
                                       bg=self.colors["highlight"],
                                       relief=tk.FLAT,
                                       bd=1,
                                       padx=15,
                                       pady=10)
                detail_frame.pack(fill=tk.X, pady=5)
                
                # Icon and label
                icon_label = tk.Label(detail_frame,
                                     text=icon,
                                     font=("Segoe UI Emoji", 14),
                                     bg=self.colors["highlight"],
                                     fg=self.colors["text"])
                icon_label.pack(side=tk.LEFT, padx=(0, 10))
                
                # Text frame
                text_frame = tk.Frame(detail_frame, bg=self.colors["highlight"])
                text_frame.pack(side=tk.LEFT, fill=tk.X, expand=True)
                
                # Title
                title_label = tk.Label(text_frame,
                                      text=label,
                                      font=self.detail_font,
                                      bg=self.colors["highlight"],
                                      fg=self.colors["secondary"])
                title_label.pack(anchor=tk.W)
                
                # Value
                value_label = tk.Label(text_frame,
                                      text="--",
                                      font=self.detail_font,
                                      bg=self.colors["highlight"],
                                      fg=self.colors["text"])
                value_label.pack(anchor=tk.W)
                
                if not hasattr(self, 'detail_labels'):
                    self.detail_labels = {}
                self.detail_labels[key] = value_label
    
    def on_entry_focus_in(self, event):
        if self.search_entry.get() == "Enter city name...":
            self.search_entry.delete(0, tk.END)
            self.search_entry.config(fg=self.colors["text"])
    
    def on_entry_focus_out(self, event):
        if not self.search_entry.get():
            self.search_entry.insert(0, "Enter city name...")
            self.search_entry.config(fg="gray")
    
    def toggle_unit(self):
        self.unit = self.unit_var.get()
        if hasattr(self, 'current_city') and self.current_city:
            self.search_weather(self.current_city)
    
    def search_weather(self, city=None):
        if city is None:
            city = self.search_var.get().strip()
            if city == "Enter city name..." or not city:
                messagebox.showwarning("Warning", "Please enter a city name")
                return
        
        self.current_city = city
        
        # Show loading status
        self.status_label.config(text="Loading...", fg=self.colors["accent"])
        self.root.update()
        
        # Get current weather with AQI
        weather_data = self.get_weather_data(city, "current.json", aqi=True)
        if weather_data:
            self.display_current_weather(weather_data)
        else:
            self.status_label.config(text="Failed to load data", fg="#ff4444")
            return
        
        # Get forecast with AQI
        forecast_data = self.get_weather_data(city, "forecast.json", days=3, aqi=True)
        if forecast_data:
            self.display_forecast(forecast_data)
        
        # Update status
        self.status_label.config(text=f"Last updated: {datetime.now().strftime('%H:%M:%S')}", 
                               fg=self.colors["secondary"])
        
        # Clear search entry
        self.search_var.set("")
        self.search_entry.delete(0, tk.END)
        self.search_entry.insert(0, "Enter city name...")
        self.search_entry.config(fg="gray")
    
    def get_weather_data(self, city, endpoint, days=None, aqi=False):
        url = f"{self.base_url}/{endpoint}"
        
        params = {
            'key': self.api_key,
            'q': city,
            'aqi': 'yes' if aqi else 'no'
        }
        
        if days:
            params['days'] = days
            params['aqi'] = 'yes'
        
        try:
            response = requests.get(url, params=params, timeout=10)
            
            if response.status_code == 200:
                return response.json()
            elif response.status_code == 400:
                error_data = response.json()
                messagebox.showerror("API Error", 
                    f"Error: {error_data.get('error', {}).get('message', 'Unknown error')}")
                return None
            elif response.status_code == 401:
                messagebox.showerror("Invalid API Key", 
                    "Your WeatherAPI.com key is invalid. Please check your API key.")
                return None
            else:
                messagebox.showerror("Error", f"HTTP Error {response.status_code}")
                return None
                
        except requests.exceptions.ConnectionError:
            messagebox.showerror("Connection Error", 
                "No internet connection. Please check your network.")
            return None
        except requests.exceptions.Timeout:
            messagebox.showerror("Timeout Error", 
                "Request timed out. Please try again.")
            return None
        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred: {str(e)}")
            return None
    
    def display_current_weather(self, data):
        try:
            location = data.get('location', {})
            current = data.get('current', {})
            air_quality = current.get('air_quality', {})
            
            # Update city and time
            city_name = location.get('name', 'Unknown City')
            country = location.get('country', '')
            local_time = location.get('localtime', '')
            
            city_text = f"{city_name}"
            if country:
                city_text += f", {country}"
            
            self.city_label.config(text=city_text)
            
            if local_time:
                try:
                    dt = datetime.strptime(local_time, "%Y-%m-%d %H:%M")
                    self.time_label.config(text=dt.strftime("%A, %B %d, %Y %I:%M %p"))
                except:
                    self.time_label.config(text=local_time)
            
            # Update temperature
            temp = current.get('temp_c', 0) if self.unit == "metric" else current.get('temp_f', 0)
            unit_symbol = "°C" if self.unit == "metric" else "°F"
            self.temp_label.config(text=f"{temp:.1f}{unit_symbol}")
            
            # Update weather icon and description
            condition = current.get('condition', {})
            condition_text = condition.get('text', 'No data')
            condition_icon = condition.get('icon', '')
            
            self.weather_icon.config(text=self.weather_icons.get(condition_text, "🌤️"))
            self.desc_label.config(text=condition_text)
            
            # Update details
            details = {
                'feels_like': f"{current.get('feelslike_c' if self.unit == 'metric' else 'feelslike_f', 0):.1f}{unit_symbol}",
                'humidity': f"{current.get('humidity', 0)}%",
                'wind_speed': f"{current.get('wind_kph', 0)} km/h",
                'pressure': f"{current.get('pressure_mb', 0)} mb",
                'visibility': f"{current.get('vis_km', 0)} km",
                'uv': f"{current.get('uv', 0)}",
                'precip': f"{current.get('precip_mm', 0)} mm"
            }
            
            for key, value in details.items():
                if key in self.detail_labels:
                    self.detail_labels[key].config(text=value)
            
            # Update AQI
            self.display_aqi_data(air_quality)
            
        except Exception as e:
            messagebox.showerror("Display Error", f"Error displaying weather data: {str(e)}")
    
    def display_aqi_data(self, air_quality):
        try:
            us_aqi = air_quality.get('us-epa-index', 0)
            
            if us_aqi > 0:
                # Get AQI category
                aqi_info = self.aqi_colors.get(us_aqi, {"color": "#666666", "text": "Unknown", "emoji": "❓"})
                
                # Update AQI display
                self.aqi_value_label.config(text=str(us_aqi), fg=aqi_info["color"])
                self.aqi_category_label.config(text=aqi_info["text"], fg=aqi_info["color"])
                self.aqi_emoji_label.config(text=aqi_info["emoji"])
                
                # Health impact description
                health_impacts = {
                    1: "Air quality is satisfactory",
                    2: "Air quality is acceptable",
                    3: "Members of sensitive groups may experience health effects",
                    4: "Everyone may begin to experience health effects",
                    5: "Health warnings of emergency conditions",
                    6: "Health alert: everyone may experience serious health effects"
                }
                self.aqi_health_label.config(text=f"Health: {health_impacts.get(us_aqi, 'No data')}")
                
                # Update pollutant values
                pollutants = ["pm2_5", "pm10", "o3", "no2", "so2", "co"]
                for pollutant in pollutants:
                    value = air_quality.get(pollutant, 0)
                    unit = "μg/m³" if pollutant not in ["co"] else "ppm"
                    
                    if pollutant in self.pollutant_labels:
                        self.pollutant_labels[pollutant].config(text=f"{value:.2f} {unit}")
            else:
                # No AQI data
                self.aqi_value_label.config(text="--", fg="#666666")
                self.aqi_category_label.config(text="No AQI Data", fg="#666666")
                self.aqi_emoji_label.config(text="❓")
                self.aqi_health_label.config(text="Health Impact: Data unavailable")
                
                for pollutant in self.pollutant_labels.values():
                    pollutant.config(text="-- μg/m³")
                    
        except Exception as e:
            print(f"Error displaying AQI data: {e}")
    
    def display_forecast(self, data):
        try:
            forecast_days = data.get('forecast', {}).get('forecastday', [])
            
            for i, day_data in enumerate(forecast_days[:3]):  # Show only 3 days
                if i >= len(self.forecast_frames):
                    break
                
                frame_data = self.forecast_frames[i]
                date_str = day_data.get('date', '')
                day_astronomy = day_data.get('astro', {})
                day_forecast = day_data.get('day', {})
                air_quality = day_forecast.get('air_quality', {})
                
                # Format date
                if date_str:
                    try:
                        dt = datetime.strptime(date_str, "%Y-%m-%d")
                        if i == 0:
                            day_str = "Today"
                        elif i == 1:
                            day_str = "Tomorrow"
                        else:
                            day_str = dt.strftime("%A")
                    except:
                        day_str = f"Day {i+1}"
                else:
                    day_str = f"Day {i+1}"
                
                frame_data['day'].config(text=day_str)
                
                # Weather icon
                condition = day_forecast.get('condition', {})
                condition_text = condition.get('text', '')
                frame_data['icon'].config(text=self.weather_icons.get(condition_text, "🌤️"))
                
                # Temperature
                max_temp = day_forecast.get('maxtemp_c', 0) if self.unit == "metric" else day_forecast.get('maxtemp_f', 0)
                min_temp = day_forecast.get('mintemp_c', 0) if self.unit == "metric" else day_forecast.get('mintemp_f', 0)
                unit_symbol = "°C" if self.unit == "metric" else "°F"
                frame_data['temp'].config(text=f"{max_temp:.0f}{unit_symbol} / {min_temp:.0f}{unit_symbol}")
                
                # Condition
                frame_data['cond'].config(text=condition_text)
                
                # AQI
                aqi = air_quality.get('us-epa-index', 0)
                if aqi > 0:
                    aqi_color = self.aqi_colors.get(aqi, {}).get("color", "#666666")
                    frame_data['aqi'].config(text=f"AQI: {aqi}", fg=aqi_color)
                else:
                    frame_data['aqi'].config(text="AQI: --", fg="#666666")
                
                # Color code temperature
                avg_temp = (max_temp + min_temp) / 2
                temp_color = self.get_temp_color(avg_temp)
                frame_data['temp'].config(fg=temp_color)
                
        except Exception as e:
            print(f"Error displaying forecast: {e}")
    
    def get_temp_color(self, temp):
        """Get color based on temperature"""
        if self.unit == "metric":
            if temp < 0:
                return "#4cc9f0"  # Very cold - light blue
            elif temp < 10:
                return "#4361ee"  # Cold - blue
            elif temp < 20:
                return "#f72585"  # Mild - pink
            elif temp < 30:
                return "#f8961e"  # Warm - orange
            else:
                return "#e63946"  # Hot - red
        else:
            # Fahrenheit scale
            if temp < 32:
                return "#4cc9f0"  # Freezing - light blue
            elif temp < 50:
                return "#4361ee"  # Cold - blue
            elif temp < 68:
                return "#f72585"  # Mild - pink
            elif temp < 86:
                return "#f8961e"  # Warm - orange
            else:
                return "#e63946"  # Hot - red

def main():
    root = tk.Tk()
    
    # Set window properties
    root.title("SkyCast Pro - Weather & Air Quality")
    
    # Center the window on screen
    window_width = 1000
    window_height = 750
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    center_x = int(screen_width/2 - window_width/2)
    center_y = int(screen_height/2 - window_height/2)
    root.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')
    
    # Prevent window resizing
    root.resizable(False, False)
    
    # Create app instance
    app = ModernWeatherApp(root)
    
    # Run the application
    root.mainloop()

if __name__ == "__main__":
    main()
