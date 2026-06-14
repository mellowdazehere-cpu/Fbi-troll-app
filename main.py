from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.progressbar import ProgressBar
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.graphics import Color, Rectangle
from kivy.utils import get_color_from_hex
import random

Window.clearcolor = get_color_from_hex("#000000")

SCAN_FILES = [
    "/data/user/0/com.browser/cache/history.db",
    "/sdcard/Downloads/suspicious_887.apk",
    "/proc/net/tcp6",
    "/data/misc/wifi/WifiConfigStore.xml",
    "/sdcard/DCIM/.hidden/IMG_4521.jpg",
    "/data/local/tmp/payload_exec.bin",
    "/sdcard/Documents/personal_notes.txt",
    "/proc/1/environ",
]

class ScanScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.scan_index = 0

        with self.canvas.before:
            Color(0, 0, 0, 1)
            self.rect = Rectangle(size=Window.size, pos=self.pos)

        layout = BoxLayout(orientation='vertical', padding=30, spacing=12)

        title = Label(
            text="[b]DEVICE SECURITY SCAN[/b]",
            markup=True,
            font_size='20sp',
            color=get_color_from_hex("#4FC3F7"),
            size_hint=(1, 0.15)
        )
        layout.add_widget(title)

        self.status_label = Label(
            text="Initializing scan...",
            font_size='13sp',
            color=get_color_from_hex("#FFFFFF"),
            size_hint=(1, 0.08),
            halign='left',
            text_size=(Window.width - 60, None)
        )
        layout.add_widget(self.status_label)

        self.progress = ProgressBar(max=len(SCAN_FILES), size_hint=(1, 0.05))
        layout.add_widget(self.progress)

        self.log_label = Label(
            text="",
            font_size='11sp',
            color=get_color_from_hex("#B0BEC5"),
            size_hint=(1, 0.6),
            halign='left',
            valign='top',
            markup=True,
            text_size=(Window.width - 60, None)
        )
        layout.add_widget(self.log_label)

        self.result_label = Label(
            text="",
            font_size='14sp',
            color=get_color_from_hex("#FF1744"),
            size_hint=(1, 0.12),
            bold=True
        )
        layout.add_widget(self.result_label)

        self.add_widget(layout)

    def on_enter(self):
        Clock.schedule_once(self.next_file, 0.8)

    def next_file(self, dt):
        if self.scan_index < len(SCAN_FILES):
            f = SCAN_FILES[self.scan_index]
            flagged = self.scan_index in [1, 5, 6]
            status = "[color=#FF1744]⚠ FLAGGED[/color]" if flagged else "[color=#69F0AE]OK[/color]"
            short = f[-38:] if len(f) > 38 else f
            self.log_label.text += f"{short}  [{status}]\n"
            self.status_label.text = f"Scanning... ({self.scan_index + 1}/{len(SCAN_FILES)})"
            self.progress.value = self.scan_index + 1
            self.scan_index += 1
            Clock.schedule_once(self.next_file, random.uniform(0.25, 0.55))
        else:
            self.result_label.text = "⚠  3 THREATS DETECTED"
            Clock.schedule_once(self.go_next, 2.0)

    def go_next(self, dt):
        self.manager.current = 'warning'


class WarningScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.countdown = 15
        self.blink_state = True

        with self.canvas.before:
            Color(0.08, 0, 0, 1)
            self.rect = Rectangle(size=Window.size, pos=self.pos)

        layout = BoxLayout(orientation='vertical', padding=28, spacing=10)

        layout.add_widget(Label(
            text="[b]⚠  FEDERAL BUREAU OF\n   INVESTIGATION  ⚠[/b]",
            markup=True,
            font_size='19sp',
            color=get_color_from_hex("#FF1744"),
            size_hint=(1, 0.18),
            halign='center',
            text_size=(Window.width - 56, None)
        ))

        layout.add_widget(Label(
            text="[b]THIS DEVICE HAS BEEN LOCKED[/b]\ndue to a violation of federal law.",
            markup=True,
            font_size='14sp',
            color=get_color_from_hex("#FFFFFF"),
            size_hint=(1, 0.12),
            halign='center',
            text_size=(Window.width - 56, None)
        ))

        case_id = f"FBI-{random.randint(10000,99999)}-CY{random.randint(10,99)}"
        ip = f"{random.randint(100,199)}.{random.randint(0,255)}.{random.randint(0,255)}.{random.randint(1,254)}"
        dev_id = ''.join(random.choices('ABCDEF0123456789', k=12))

        info_text = (
            f"[b]Case Ref:[/b]  {case_id}\n"
            f"[b]IP Address:[/b] {ip}\n"
            f"[b]Device ID:[/b]  {dev_id}\n"
            f"[b]Location:[/b]  Triangulated via cell tower"
        )
        layout.add_widget(Label(
            text=info_text,
            markup=True,
            font_size='12sp',
            color=get_color_from_hex("#FFD740"),
            size_hint=(1, 0.18),
            halign='left',
            text_size=(Window.width - 56, None)
        ))

        layout.add_widget(Label(
            text=(
                "[b]Violations detected:[/b]\n"
                "▶ Unauthorized network access\n"
                "▶ Distribution of classified content\n"
                "▶ Suspicious encrypted comms (3x)"
            ),
            markup=True,
            font_size='12sp',
            color=get_color_from_hex("#FFFFFF"),
            size_hint=(1, 0.18),
            halign='left',
            text_size=(Window.width - 56, None)
        ))

        self.timer_label = Label(
            text="COMPLIANCE REQUIRED IN: 15s",
            font_size='16sp',
            bold=True,
            color=get_color_from_hex("#FF1744"),
            size_hint=(1, 0.1)
        )
        layout.add_widget(self.timer_label)

        self.add_widget(layout)

    def on_enter(self):
        Clock.schedule_interval(self.tick, 1)

    def tick(self, dt):
        self.countdown -= 1
        self.blink_state = not self.blink_state
        color = "#FF1744" if self.blink_state else "#FF8A80"
        self.timer_label.text = f"[color={color}]COMPLIANCE REQUIRED IN: {self.countdown}s[/color]"
        self.timer_label.markup = True
        if self.countdown <= 0:
            Clock.unschedule(self.tick)
            self.manager.current = 'reveal'


class RevealScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.frame_index = 0
        self.frames = ["lol", "L O L", "😭😭😭", "GOT YA", "RATIO", "u got trolled\nfr fr no cap 💀"]

        with self.canvas.before:
            Color(0, 0, 0, 1)
            self.rect = Rectangle(size=Window.size, pos=self.pos)

        layout = BoxLayout(orientation='vertical', padding=40, spacing=20)

        self.big_label = Label(
            text="lol",
            font_size='36sp',
            bold=True,
            color=get_color_from_hex("#FFD740"),
            size_hint=(1, 0.5),
            halign='center',
            text_size=(Window.width - 80, None)
        )
        layout.add_widget(self.big_label)

        layout.add_widget(Label(
            text="this wasn't real bestie\nur not getting arrested\n(probably)",
            font_size='15sp',
            color=get_color_from_hex("#B0BEC5"),
            size_hint=(1, 0.3),
            halign='center',
            text_size=(Window.width - 80, None)
        ))

        self.add_widget(layout)

    def on_enter(self):
        Clock.schedule_interval(self.cycle_frame, 0.4)

    def cycle_frame(self, dt):
        if self.frame_index < len(self.frames):
            self.big_label.text = self.frames[self.frame_index]
            self.frame_index += 1
        else:
            Clock.unschedule(self.cycle_frame)


class FBITrollApp(App):
    def build(self):
        sm = ScreenManager(transition=FadeTransition())
        sm.add_widget(ScanScreen(name='scan'))
        sm.add_widget(WarningScreen(name='warning'))
        sm.add_widget(RevealScreen(name='reveal'))
        return sm


if __name__ == '__main__':
    FBITrollApp().run()
