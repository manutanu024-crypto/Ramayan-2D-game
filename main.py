from kivy.config import Config
Config.set('graphics', 'fullscreen', 'auto')
Config.set('graphics', 'resizable', False)

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.graphics import Rectangle, Color
from kivy.clock import Clock
from kivy.core.window import Window
import time


class GameWidget(Widget):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.level = 1
        self.reset_game()

        with self.canvas:
            # Background
            self.bg = Rectangle(source='fight_bg.png', pos=self.pos, size=self.size)

            # Rama LEFT
            self.rama = Rectangle(source='rama.png', pos=(0,0), size=(150,200))

            # Ravana RIGHT
            self.ravana = Rectangle(source='ravan.png', pos=(0,0), size=(150,200))

            # Allies (hidden)
            self.lakshman = Rectangle(source='lakshman.png', pos=(-500,-500), size=(120,180))
            self.hanuman = Rectangle(source='hanuman.png', pos=(-500,-500), size=(120,180))

            # Health Bars
            Color(0,1,0)
            self.rama_bar = Rectangle(pos=(0,0), size=(300,20))

            Color(1,0,0)
            self.ravana_bar = Rectangle(pos=(0,0), size=(300,20))

            # Arrow
            Color(1,1,0)
            self.arrow = Rectangle(pos=(-100,-100), size=(40,5))

            # Fireball
            Color(1,0.3,0)
            self.fireball = Rectangle(pos=(-100,-100), size=(30,30))

        self.bind(size=self.update_positions, pos=self.update_positions)

        # Buttons
        self.attack_btn = Button(text="ATTACK",
                                 size_hint=(None,None),
                                 size=(150,60))
        self.attack_btn.bind(on_press=self.attack)
        self.add_widget(self.attack_btn)

        self.heal_btn = Button(text="HEAL",
                               size_hint=(None,None),
                               size=(150,60))
        self.heal_btn.bind(on_press=self.heal)
        self.add_widget(self.heal_btn)

        self.summon_btn = Button(text="SUMMON",
                                 size_hint=(None,None),
                                 size=(150,60))
        self.summon_btn.bind(on_press=self.summon_ally)
        self.add_widget(self.summon_btn)

        Clock.schedule_interval(self.update, 1/60)

    def reset_game(self):
        self.rama_health = 200
        self.ravana_health = 1000 if self.level == 1 else 1500
        self.heal_cooldown = 0
        self.arrow_active = False
        self.fireball_active = False
        self.ally_active = False

    def update_positions(self, *args):
        self.bg.size = self.size
        self.bg.pos = self.pos

        self.rama.pos = (self.width*0.1, self.height*0.3)
        self.ravana.pos = (self.width*0.75, self.height*0.3)

        self.rama_bar.pos = (self.width*0.05, self.height*0.9)
        self.ravana_bar.pos = (self.width*0.6, self.height*0.9)

        self.attack_btn.pos = (50, 40)
        self.heal_btn.pos = (self.width-200, 40)
        self.summon_btn.pos = (self.width-200, 120)

    def attack(self, instance):
        self.ravana_health -= 20
        self.arrow_active = True
        self.arrow.pos = (self.rama.pos[0]+100, self.rama.pos[1]+80)

        # Ravana counter fireball
        self.fireball_active = True
        self.fireball.pos = (self.ravana.pos[0], self.ravana.pos[1]+80)

    def heal(self, instance):
        if time.time() > self.heal_cooldown:
            self.rama_health += 35
            if self.rama_health > 200:
                self.rama_health = 200
            self.heal_cooldown = time.time() + 10

    def summon_ally(self, instance):
        if not self.ally_active:
            self.ally_active = True
            self.ravana_health -= 20   # 10+10 damage

            self.lakshman.pos = (self.width*0.2, self.height*0.3)
            self.hanuman.pos = (self.width*0.3, self.height*0.3)

            Clock.schedule_once(self.hide_allies, 2)

    def hide_allies(self, dt):
        self.lakshman.pos = (-500,-500)
        self.hanuman.pos = (-500,-500)
        self.ally_active = False

    def update(self, dt):

        # Update health bars
        max_health = 1000 if self.level == 1 else 1500
        self.ravana_bar.size = (300 * self.ravana_health / max_health, 20)
        self.rama_bar.size = (300 * self.rama_health / 200, 20)

        # Arrow animation
        if self.arrow_active:
            x,y = self.arrow.pos
            self.arrow.pos = (x+15, y)
            if x > self.ravana.pos[0]:
                self.arrow_active = False
                self.arrow.pos = (-100,-100)

        # Fireball animation
        if self.fireball_active:
            x,y = self.fireball.pos
            self.fireball.pos = (x-12, y)
            if x < self.rama.pos[0]:
                damage = 10 if self.ravana_health > 400 else 20
                self.rama_health -= damage
                self.fireball_active = False
                self.fireball.pos = (-100,-100)

        # Level progression
        if self.ravana_health <= 0:
            if self.level == 1:
                self.level = 2
                self.reset_game()
            else:
                self.attack_btn.disabled = True
                self.heal_btn.disabled = True
                self.summon_btn.disabled = True

        if self.rama_health <= 0:
            self.attack_btn.disabled = True
            self.heal_btn.disabled = True
            self.summon_btn.disabled = True


class RamayanApp(App):
    def build(self):
        return GameWidget()

if __name__ == "__main__":
    RamayanApp().run()