import threading
import time
import json
from kivy.app import App
from kivy.lang import Builder
from kivy.clock import Clock
from kivy.core.audio import SoundLoader

try:
    from plyer import vibrator, notification
except:
    vibrator = None
    notification = None

import websocket

SERVER_WS = "wss://seu-dominio.com/ws/signals"
API_KEY = "MY_SECRET_TOKEN"

signals = []

def on_message(ws, message):
    try:
        data = json.loads(message)
        if data.get("type") == "signal":
            s = f"{data.get('strategy')} - {data.get('side')}"
            signals.append(s)

            if notification:
                notification.notify(title="BacBo Signal", message=s)

            if vibrator:
                vibrator.vibrate(150)

            try:
                sfx = SoundLoader.load('ping.wav')
                if sfx:
                    sfx.play()
            except:
                pass

    except:
        pass


def ws_thread(update_callback):
    headers = []
    if API_KEY:
        headers.append(f"Authorization: Bearer {API_KEY}")

    while True:
        try:
            ws = websocket.WebSocketApp(
                SERVER_WS,
                header=headers,
                on_message=lambda ws, msg: (on_message(ws, msg), update_callback())
            )
            ws.run_forever()
        except:
            pass

        time.sleep(2)


KV = """
BoxLayout:
    orientation: "vertical"
    padding: 10
    spacing: 10

    Label:
        text: "BacBo Signals"
        font_size: 28
        size_hint_y: None
        height: 40

    Label:
        id: status
        text: "Conectando..."
        font_size: 18
        size_hint_y: None
        height: 30

    Label:
        text: "Últimos sinais:"
        size_hint_y: None
        height: 30

    Label:
        id: log
        text: "Aguardando..."
        font_size: 16
        text_size: self.width, None
        height: 200
        size_hint_y: None
"""

class MainApp(App):
    def build(self):
        self.root = Builder.load_string(KV)
        threading.Thread(target=ws_thread, args=(self.update,), daemon=True).start()
        Clock.schedule_interval(self.update, 0.5)
        return self.root

    def update(self, dt=None):
        self.root.ids.log.text = "\n".join(signals[-8:]) or "Sem sinais"
        self.root.ids.status.text = f"Sinais recebidos: {len(signals)}"


if __name__ == "__main__":
    MainApp().run()[app]
title = BacBo Signals
package.name = bacbo_signals
package.domain = org.example
source.dir = .
source.include_exts = py,kv,png,jpg,wav
requirements = python3,kivy,websocket-client,plyer
orientation = portrait
android.permissions = INTERNET,VIBRATE,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE

[buildozer]
log_level = 2
warn_on_root = 0
