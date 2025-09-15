import requests
import random
import json
from PIL import Image, ImageDraw, ImageFont
# ======================= Telegram =======================
TOKEN = "7718445747:AAEwC-RX2lRfjevCPK1TAgkR3EeY3r0EsWk"
URL = f"https://api.telegram.org/bot{TOKEN}/"
offset = 0

def get_updates():
    global offset
    r = requests.get(URL + "getUpdates", params={"timeout": 100, "offset": offset})
    return r.json()

def send_message(chat_id, text, reply_markup=None):
    data = {"chat_id": chat_id, "text": text, "parse_mode": "HTML"}
    if reply_markup:
        data["reply_markup"] = json.dumps(reply_markup)
    requests.post(URL + "sendMessage", data=data)

def log(chat_id, text):
    print(text)
    send_message(chat_id, text)

# ======================= БОЕВАЯ ЛОГИКА =======================
class Character:
    def __init__(self, name, hp, attack=0, defense=0, speed=10, mag_defense=0):
        self.name = name
        self.hp = hp
        self.attack = attack
        self.defense = defense
        self.mag_defense = mag_defense
        self.speed = speed

    def is_alive(self):
        return self.hp > 0

    def take_damage(self, damage, mag=False):
        if mag:
            real = max(0, damage - self.mag_defense)
        else:
            real = max(0, damage - self.defense)
        self.hp -= real
        print(f'{self.name} получил урон {real}. HP осталось: {self.hp}')
        return real

# ------------------- Герои -------------------
class HeroMag(Character):
    def __init__(self, name='Маг'):
        super().__init__(name, hp=70, speed=24, mag_defense=50)
        self.mag_damage = random.randint(25, 35)
        self.mana = 100

    def skill_attack(self, target, chat_id):
        dmg = self.mag_damage
        dealt = target.take_damage(dmg, mag=True)
        log(chat_id, f'🔮 {self.name} бьёт {target.name} магией на {dealt}. HP {target.name}: {target.hp}')

    def skill_super_attack(self, target, chat_id):
        if self.mana >= 30:
            dmg = self.mag_damage * 2
            self.mana -= 30
            dealt = target.take_damage(dmg, mag=True)
            log(chat_id, f'💥 {self.name} СУПЕР-удар по {target.name} на {dealt}! Мана: {self.mana}. HP цели: {target.hp}')
        else:
            log(chat_id, '❌ Не хватает маны!')

    def skill_heal_one(self, ally, chat_id):
        if self.mana >= 20:
            heal = random.randint(20, 35)
            self.mana -= 20
            ally.hp += heal
            log(chat_id, f'✨ {self.name} лечит {ally.name} на {heal}. Мана: {self.mana}. HP {ally.name}: {ally.hp}')
        else:
            log(chat_id, '❌ Не хватает маны для лечения!')

    def skill_heal_all(self, allies, chat_id):
        if self.mana >= 40:
            heal = random.randint(10, 20)
            self.mana -= 40
            for a in allies:
                a.hp += heal
            log(chat_id, f'🌟 {self.name} лечит всех на {heal}. Мана: {self.mana}')
        else:
            log(chat_id, '❌ Не хватает маны для массового лечения!')

class HeroTank(Character):
    def __init__(self, name='Танк'):
        super().__init__(name, hp=100, attack=random.randint(13,20), speed=22, defense=50)
        self.rage = 30
        self.agro = False

    def skill_attack(self, target, chat_id):
        dmg = self.attack
        dealt = target.take_damage(dmg)
        self.rage += 10
        log(chat_id, f'🗡️ {self.name} атакует {target.name} на {dealt}. Ярость: {self.rage}. HP цели: {target.hp}')

    def skill_shield_bash(self, target, chat_id):
        if self.rage >= 50:
            dmg = self.attack + random.randint(15,25)
            self.rage -= 50
            dealt = target.take_damage(dmg)
            log(chat_id, f'🛡️ {self.name} УДАР ЩИТОМ по {target.name} на {dealt}. Ярость: {self.rage}. HP цели: {target.hp}')
        else:
            log(chat_id, '❌ Не хватает ярости для удара щитом!')

    def skill_defense_buff(self, ally, chat_id):
        if self.rage >= 20:
            buff = 20
            self.rage -= 20
            ally.defense += buff
            log(chat_id, f'🛡️ {self.name} усиливает защиту {ally.name} на {buff}. Защита {ally.name}: {ally.defense}. Ярость: {self.rage}')
        else:
            log(chat_id, '❌ Не хватает ярости!')

    def skill_provoke(self, dragon, chat_id):
        if self.rage >= 20:
            self.rage -= 20
            self.agro = True
            log(chat_id, f'🎯 {self.name} провоцирует {dragon.name}. Ярость: {self.rage}')
        else:
            log(chat_id, '❌ Не хватает ярости для провокации!')

class HeroHunter(Character):
    def __init__(self, name='Охотник'):
        super().__init__(name, hp=80, attack=random.randint(20,30), speed=30, defense=15, mag_defense=15)
        self.stamina = 50

    def skill_attack(self, target, chat_id):
        dmg = self.attack
        dealt = target.take_damage(dmg)
        self.stamina += 10
        log(chat_id, f'🏹 {self.name} стреляет в {target.name} на {dealt}. Выносливость: {self.stamina}. HP цели: {target.hp}')

    def skill_super_shot(self, target, chat_id):
        if self.stamina >= 30:
            dmg = self.attack + random.randint(15,25)
            self.stamina -= 30
            dealt = target.take_damage(dmg)
            log(chat_id, f'🔥 {self.name} СУПЕР-выстрел в {target.name} на {dealt}. Выносливость: {self.stamina}. HP цели: {target.hp}')
        else:
            log(chat_id, '❌ Не хватает выносливости!')

    def skill_speed_buff(self, ally, chat_id):
        if self.stamina >= 20:
            buff = 10
            self.stamina -= 20
            ally.speed += buff
            log(chat_id, f'⚡ {self.name} ускоряет {ally.name} на {buff}. Скорость {ally.name}: {ally.speed}. Выносливость: {self.stamina}')
        else:
            log(chat_id, '❌ Не хватает выносливости для бафа скорости!')

    def skill_multi_shot(self, targets, chat_id):
        if self.stamina >= 40:
            self.stamina -= 40
            log(chat_id, f'🌪 {self.name} град стрел!')
            for t in targets:
                if t.is_alive():
                    dealt = t.take_damage(self.attack // 2)
                    log(chat_id, f' → по {t.name}: {dealt} урона. HP: {t.hp}')
            log(chat_id, f'Выносливость: {self.stamina}')
        else:
            log(chat_id, '❌ Не хватает выносливости для многоцелевого выстрела!')

# ------------------- Дракон -------------------
class Dragon(Character):
    def __init__(self, name='Дракон'):
        super().__init__(name, hp=500, attack=random.randint(15,25), speed=20, defense=20, mag_defense=20)
        self.speed_buff_turns = 0
        self.minion = None

    def skill_attack(self, target, chat_id):
        dmg = max(0, self.attack - target.defense//2)
        dealt = target.take_damage(dmg)
        log(chat_id, f'🐲 {self.name} атакует {target.name} на {dealt}. HP {target.name}: {target.hp}')

    def skill_attack_all(self, targets, chat_id):
        dmg = self.attack // 2
        log(chat_id, f'🐲 {self.name} массовая атака!')
        for t in targets:
            if t.is_alive():
                dealt = t.take_damage(dmg)
                log(chat_id, f' → по {t.name}: {dealt}. HP: {t.hp}')

    def skill_magic(self, target, chat_id):
        dmg = random.randint(20,35)
        dealt = target.take_damage(dmg, mag=True)
        log(chat_id, f'🐲 {self.name} магический удар по {target.name} на {dealt}. HP {target.name}: {target.hp}')

    def skill_magic_all(self, targets, chat_id):
        dmg = random.randint(15,25)
        log(chat_id, f'🐲 {self.name} магический дождь!')
        for t in targets:
            if t.is_alive():
                dealt = t.take_damage(dmg, mag=True)
                log(chat_id, f' → по {t.name}: {dealt}. HP: {t.hp}')

    def skill_speed_buff(self, chat_id):
        self.speed += 10
        self.speed_buff_turns = 2
        log(chat_id, f'🐲 {self.name} ускоряется! Скорость {self.speed} на 2 хода')

    def skill_summon_minion(self, chat_id):
        if not self.minion or not self.minion.is_alive():
            self.minion = DragonMinion(self)
            log(chat_id, f'🐲 {self.name} призывает прислужника!')

    def choose_action(self, heroes, chat_id):
        actions = [
            lambda: self.skill_attack(random.choice([h for h in heroes if h.is_alive()]), chat_id),
            lambda: self.skill_attack_all(heroes, chat_id),
            lambda: self.skill_magic(random.choice([h for h in heroes if h.is_alive()]), chat_id),
            lambda: self.skill_magic_all(heroes, chat_id),
            lambda: self.skill_speed_buff(chat_id),
            lambda: self.skill_summon_minion(chat_id),
        ]
        random.choice(actions)()

        if self.speed_buff_turns > 0:
            self.speed_buff_turns -= 1
            if self.speed_buff_turns == 0:
                self.speed -= 10
                log(chat_id, f'🐲 {self.name} теряет баф скорости.')

        if self.minion and self.minion.is_alive():
            self.minion.choose_action(heroes, chat_id)

class DragonMinion(Character):
    def __init__(self, dragon, name='Прислужник'):
        super().__init__(name, hp=50, attack=10, speed=15, defense=5, mag_defense=5)
        self.dragon = dragon

    def heal_dragon(self, chat_id):
        heal = random.randint(20,40)
        self.dragon.hp += heal
        log(chat_id, f'🧪 {self.name} лечит {self.dragon.name} на {heal}. HP дракона: {self.dragon.hp}')

    def attack_hero(self, heroes, chat_id):
        target = random.choice([h for h in heroes if h.is_alive()])
        dmg = 10
        dealt = target.take_damage(dmg)
        log(chat_id, f'🗡️ {self.name} бьёт {target.name} на {dealt}. HP {target.name}: {target.hp}')

    def choose_action(self, heroes, chat_id):
        random.choice([
            lambda: self.heal_dragon(chat_id),
            lambda: self.attack_hero(heroes, chat_id)
        ])()

#  STATE + UI
game_state = {
    "heroes": [],
    "dragon": None,
    "turn_order": [],
    "current_turn": 0,
    "in_battle": False,
}

def show_main_menu(chat_id):
    keyboard = {
        "inline_keyboard": [
            [{"text": "🎮 Начать игру", "callback_data": "start_game"}],
            [{"text": "📖 Правила", "callback_data": "rules"}],
            [{"text": "❌ Выйти", "callback_data": "exit"}]
        ]
    }
    send_message(chat_id, "Добро пожаловать в игру!", keyboard)

def start_game(chat_id):
    mag = HeroMag()
    tank = HeroTank()
    hunter = HeroHunter()
    dragon = Dragon()

    game_state["heroes"] = [mag, tank, hunter]
    game_state["dragon"] = dragon

    all_units = [dragon] + game_state["heroes"]
    game_state["turn_order"] = sorted(all_units, key=lambda x: x.speed, reverse=True)
    game_state["current_turn"] = 0
    game_state["in_battle"] = True

    send_message(chat_id, "⚔ Бой начался! На поле — Дракон и Герои!")
    next_turn(chat_id)

# Функция отправки фото
def send_photo(chat_id, photo_path, caption=""):
    files = {"photo": open(photo_path, "rb")}
    data = {"chat_id": chat_id, "caption": caption, "parse_mode": "HTML"}
    requests.post(URL + "sendPhoto", data=data, files=files)

# Функция создания мини-карты с картинками
def draw_battle_map(chat_id):
    width, height = 400, 200
    img = Image.new("RGB", (width, height), color=(50, 50, 50))
    draw = ImageDraw.Draw(img)
    font = ImageFont.load_default()

    dragon = game_state["dragon"]
    heroes = game_state["heroes"]

    # Загружаем картинки (пример: png 50x50)
    dragon_img = Image.open("dragon.png").resize((50,50))
    img.paste(dragon_img, (10, 75), dragon_img)

   #

    img.save("battle_map.png")
    send_photo(chat_id, "battle_map.png", caption="🗺️ Мини-карта боя")


def next_turn(chat_id):
    if not game_state["in_battle"]:
        return

    order = game_state["turn_order"]
    idx = game_state["current_turn"]

    if idx >= len(order):
        game_state["current_turn"] = 0
        idx = 0

    unit = order[idx]

    if isinstance(unit, Character) and not unit.is_alive():
        game_state["current_turn"] += 1
        next_turn(chat_id)
        return

    if isinstance(unit, Dragon):
        heroes_alive = [h for h in game_state["heroes"] if h.is_alive()]
        if heroes_alive:
            unit.choose_action(heroes_alive, chat_id)
            if check_end_game(chat_id):
                return
        game_state["current_turn"] += 1
        next_turn(chat_id)
    else:
        show_hero_skills(chat_id, unit)

    #  мини-карту
    draw_battle_map(chat_id)

def show_hero_skills(chat_id, hero):
    if isinstance(hero, HeroMag):
        keyboard = {"keyboard": [["🧙‍♂️ Маг. атака", "💥 Супер удар"],
                                 ["❤️ Лечение одного", "💞 Лечение группы"]],
                    "resize_keyboard": True}
    elif isinstance(hero, HeroTank):
        keyboard = {"keyboard": [["⚔ Обычная атака", "🛡 Супер удар щитом"],
                                 ["🛡 Баф защиты", "🎯 Провокация (агро)"]],
                    "resize_keyboard": True}
    elif isinstance(hero, HeroHunter):
        keyboard = {"keyboard": [["🏹 Удар", "🔥 Супер удар"],
                                 ["⚡ Баф скорости", "🌪 Удар по всем"]],
                    "resize_keyboard": True}
    send_message(chat_id, f"Ход героя {hero.name}. Выберите действие:", keyboard)

def check_end_game(chat_id):
    dragon = game_state["dragon"]
    heroes = game_state["heroes"]
    if not dragon.is_alive():
        send_message(chat_id, "🎉 Герои победили Дракона!")
        game_state["in_battle"] = False
        return True
    if all(not h.is_alive() for h in heroes):
        send_message(chat_id, "☠️ Все герои пали. Дракон победил!")
        game_state["in_battle"] = False
        return True
    return False

def handle_hero_action(chat_id, text):
    order = game_state["turn_order"]
    if not order:
        return  # Очередь пуста

    idx = game_state["current_turn"]
    if idx >= len(order):
        game_state["current_turn"] = 0
        idx = 0

    hero = order[idx]
    dragon = game_state["dragon"]
    heroes = game_state["heroes"]

    # Проверка, что герой жив
    if not hero.is_alive():
        game_state["current_turn"] += 1
        next_turn(chat_id)
        return

    # Действия в зависимости от класса героя
    if isinstance(hero, HeroMag):
        if text == "🧙‍♂️ Маг. атака":
            hero.skill_attack(dragon, chat_id)
        elif text == "💥 Супер удар":
            hero.skill_super_attack(dragon, chat_id)
        elif text == "❤️ Лечение одного":
            ally = random.choice([h for h in heroes if h.is_alive()])
            hero.skill_heal_one(ally, chat_id)
        elif text == "💞 Лечение группы":
            hero.skill_heal_all([h for h in heroes if h.is_alive()], chat_id)
        else:
            send_message(chat_id, "Неизвестная кнопка!")
            return

    elif isinstance(hero, HeroTank):
        if text == "⚔ Обычная атака":
            hero.skill_attack(dragon, chat_id)
        elif text == "🛡 Супер удар щитом":
            hero.skill_shield_bash(dragon, chat_id)
        elif text == "🛡 Баф защиты":
            ally = random.choice([h for h in heroes if h.is_alive()])
            hero.skill_defense_buff(ally, chat_id)
        elif text == "🎯 Провокация (агро)":
            hero.skill_provoke(dragon, chat_id)
        else:
            send_message(chat_id, "Неизвестная кнопка!")
            return

    elif isinstance(hero, HeroHunter):
        if text == "🏹 Удар":
            hero.skill_attack(dragon, chat_id)
        elif text == "🔥 Супер удар":
            hero.skill_super_shot(dragon, chat_id)
        elif text == "⚡ Баф скорости":
            ally = random.choice([h for h in heroes if h.is_alive()])
            hero.skill_speed_buff(ally, chat_id)
        elif text == "🌪 Удар по всем":
            hero.skill_multi_shot([dragon], chat_id)
        else:
            send_message(chat_id, "Неизвестная кнопка!")
            return

    # Проверка конца боя
    if check_end_game(chat_id):
        return

    # Переходим к следующему ходу
    game_state["current_turn"] += 1
    next_turn(chat_id)

#  MAIN
while True:
    updates = get_updates()
    if "result" in updates:
        for upd in updates["result"]:
            offset = upd["update_id"] + 1
            if "message" in upd:
                chat_id = upd["message"]["chat"]["id"]
                text = upd["message"].get("text", "")
                if text == "/start":
                    show_main_menu(chat_id)
                else:
                    handle_hero_action(chat_id, text)
            elif "callback_query" in upd:
                data = upd["callback_query"]["data"]
                chat_id = upd["callback_query"]["message"]["chat"]["id"]
                if data == "start_game":
                    start_game(chat_id)
                elif data == "rules":
                    send_message(chat_id, "Правила: победи дракона, используя скиллы героев.")
                elif data == "exit":
                    send_message(chat_id, "Игра завершена.")