import tkinter as tk
from tkinter import messagebox
import datetime
import requests
import json

class TripPlanner():
    def __init__(self, username):
        self.username = username
        self.tripData = []
        self.addDestinationCallNum = 0
        self.entries = {}
        self.labels = {}
        self.baseCurrency = ""
        self.jsonFileName = ""

    def get_exchange_rate(self, base_currency, target_currency):
        try:
            url = f"https://api.exchangerate-api.com/v4/latest/{base_currency}"
            response = requests.get(url)
            data = response.json()
            return data["rates"][target_currency]
        except Exception as e:
            print(f"Error fetching exchange rate: {e}")
            return None

    def addDestination(self):
        if self.addDestinationCallNum == 0:
            self.baseCurrency = self.entries["Base Currency"].get()
        try:
            destination_currency = self.entries["Currency"].get()
            destination = self.entries["Destination"].get()
            accommodation_cost = float(self.entries["Accommodation Cost"].get())
            transportation_cost = float(self.entries["Transportation Cost"].get())
            food_cost = float(self.entries["Food Cost"].get())
            entertainment_cost = float(self.entries["Entertainment Cost"].get())
            num_travelers = int(self.entries["Number of Travelers"].get())
            trip_duration = int(self.entries["Trip Duration"].get())
        except Exception as e:
            messagebox.showerror("Error", "At least one of the values you entered is not valid.")
            return
            
        exchange_rate = self.get_exchange_rate(self.baseCurrency, destination_currency)
        if exchange_rate is None:
            messagebox.showerror("Error", "Failed to fetch exchange rate. Please check your currencies.")
            return

        total_cost = (
            (accommodation_cost + transportation_cost + food_cost + entertainment_cost) * num_travelers * trip_duration
        ) / exchange_rate

        daily_budget_per_traveler = (accommodation_cost + transportation_cost + food_cost + entertainment_cost) / exchange_rate

        self.tripData.append({
            "Travelers": num_travelers,
            "Destination": destination,
            "Currency": destination_currency,
            "Exchange Rate": exchange_rate,
            "Total Cost": total_cost,
            "Trip Duration (days)": trip_duration,
            "Daily Budget per Traveler": daily_budget_per_traveler
        })

        for entry in self.entries.values():
            entry.delete(0, tk.END)

        if self.addDestinationCallNum == 0:
            self.labels["Base Currency"].destroy()
            del self.labels["Base Currency"]
            self.entries["Base Currency"].destroy()
            del self.entries["Base Currency"]

        if self.tripData[0] != None:
            self.addDestinationCallNum += 1

        messagebox.showinfo("Total Cost", f"The cost of this trip is: {total_cost:,.2f} {self.baseCurrency}.\nThe daily budget per traveler is: {daily_budget_per_traveler:,.2f}")

        return True

    def done(self, r):
        if self.addDestination():
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            self.jsonFileName = f"{self.username}_{timestamp}.json"
            
            totalCost = 0
            tripDays = 0
            for i in self.tripData:
                totalCost += i["Total Cost"]
                tripDays += i["Trip Duration (days)"]

            self.tripData = {
                "Created on": timestamp,
                "Base Currency": self.baseCurrency,
                "Total Cost of the Whole Trip": totalCost,
                "Total Trip Duration (days)": tripDays,
                "List of Destinations": self.tripData
            }

            with open(self.jsonFileName, 'w') as file:
                json.dump(self.tripData, file, indent=4)

            messagebox.showinfo("Total Cost of the Whole Trip", f"The total cost of the whole trip is: {totalCost:,.2f} {self.baseCurrency}.")
            
            r.destroy()

    def create_trip_planner(self, root):
        r = tk.Toplevel(root)
        r.title("Multi-City Trip Planner")
        r.geometry("400x550")

        labels_text = [
            "Base Currency", "Number of Travelers", "Destination", "Currency",
            "Accommodation Cost", "Transportation Cost", "Food Cost", "Entertainment Cost", "Trip Duration"
        ]
        
        for i, label_text in enumerate(labels_text):
            label = tk.Label(r, text=label_text)
            label.pack()

            entry = tk.Entry(r)
            entry.pack()
            
            self.labels[label_text] = label
            self.entries[label_text] = entry

        add_button = tk.Button(r, text="Add Another Destination", command=self.addDestination)
        add_button.pack()

        done_button = tk.Button(r, text="Done", command=lambda: self.done(r))
        done_button.pack()

        messagebox.showinfo("Cost of the Trip", "Please write the cost per day of accomodation, transportation, food, and entertainment in the local currency.")

'''t = TripPlanner()
t.create_trip_planner()'''
