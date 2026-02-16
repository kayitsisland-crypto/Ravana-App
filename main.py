from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from plyer import gps
import requests
import threading

class RavanaApp(App):
    def build(self):
        self.is_running = False
        layout = BoxLayout(orientation='vertical', padding=30, spacing=20)
        self.label = Label(text="RAVANA AGENT READY", font_size='22sp')
        self.btn = Button(text="START MISSION", size_hint=(1, 0.2), background_color=(0, 0.7, 0.3, 1))
        self.btn.bind(on_release=self.toggle)
        layout.add_widget(self.label)
        layout.add_widget(self.btn)
        return layout

    def toggle(self, instance):
        if not self.is_running:
            try:
                gps.configure(on_location=self.on_location)
                gps.start(minTime=5000, minDistance=1)
                self.is_running = True
                self.btn.text = "STOP MISSION"
                self.btn.background_color = (0.8, 0, 0, 1)
                self.label.text = "TRANSMITTING..."
            except: self.label.text = "GPS Error"
        else:
            gps.stop()
            self.is_running = False
            self.btn.text = "START MISSION"
            self.btn.background_color = (0, 0.7, 0.3, 1)
            self.label.text = "TERMINATED"

    def on_location(self, **kwargs):
        lat, lon = kwargs.get('lat'), kwargs.get('lon')
        self.label.text = f"LAT: {lat:.4f}\nLON: {lon:.4f}"
        threading.Thread(target=self.send, args=(lat, lon), daemon=True).start()

    def send(self, lat, lon):
        url = "https://unfineable-suzie-prodisarmament.ngrok-free.dev/update_location"
        headers = {"ngrok-skip-browser-warning": "69420"}
        try: requests.post(url, json={"uid": "AGENT-001", "lat": lat, "lon": lon}, headers=headers, timeout=5)
        except: pass

if __name__ == "__main__":
    RavanaApp().run()
