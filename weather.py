import tkinter as tk
import requests
from tkinter import messagebox
from PIL import Image, ImageTk
import ttkbootstrap


def get_weather(city):
    API_Key = "blah"
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_Key}&=imperial"
    res = requests.get(url)

    if res.status_code == 404:
        messagebox.showerror("Error", "City not found")
        return None
    
    weather_json = res.json()
    icon_id = weather_json['weather'][0]['icon']
    temperature = ((weather_json['main']['temp'] - 273.15) * 1.8) + 32
    description = weather_json['weather'][0]['description']
    city = weather_json['name']
    country = weather_json['sys']['country']

    icon_url = f"http://openweathermap.org/img/wn/{icon_id}@2x.png"
    return (icon_url, temperature, description, city, country)

def search():
    city = city_entry.get()
    result = get_weather(city)
    if result is None:
        return
    icon_url, temperature, description, city, country = result
    loc_label.configure(text=f"{city}, {country}")

    image = Image.open(requests.get(icon_url, stream=True).raw)
    icon = ImageTk.PhotoImage(image)
    icon_label.configure(image=icon)
    icon_label.image = icon

    temp_label.configure(text=f"Temperature: {temperature:.2f}°F")
    desc_label.configure(text=f"Description: {description}")


root = ttkbootstrap.Window(themename="morph")
root.title("Weather App")
root.geometry("500x400")

city_entry = ttkbootstrap.Entry(root, font="Helvetica, 18")
city_entry.pack(pady=10)

search_button = ttkbootstrap.Button(root, text="Search", command=search, bootstyle="warning")
search_button.pack(pady=10)

loc_label = tk.Label(root, font="Helvetica, 25")
loc_label.pack(pady=20)

icon_label = tk.Label(root)
icon_label.pack(pady=20)

temp_label = tk.Label(root, font="Helvetica, 20")
temp_label.pack(pady=20)

desc_label = tk.Label(root, font="Helvetica, 20")
temp_label.pack(pady=20)

root.mainloop()
