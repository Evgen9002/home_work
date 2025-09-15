import requests
import time
import random
import json

#  КЛАССЫ

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
            real_damage = max(0, damage - self.mag_defense)
        else:
            real_damage = max(0, damage - self.defense)
        self.hp -= real_damage
        print(f'{self.name} получил урон {real_damage}. HP осталось: {self.hp}')
        return real_damage

# персонажи

class HeroMag(Character):
    def __init__(self, name='Маг'):
        super().__init__(name, hp=70, speed=24, mag_defense=50)
        self.mag_damage = random.randint(25, 35)
        self.mana = 100

    def skill_attack(self, target):
        dmg = self.mag_damage
        print(f'{self.name} применяет маг-атаку по {target.name} ({dmg}) урона')
        target.take_damage(dmg, mag=True)

    def skill_super_attack(self, target):
        if self.mana >= 30:
            dmg = self.mag_damage * 2
            self.mana -= 30
            print(f'{self.name} супер-удар по {target.name} ({dmg}), мана {self.mana}')
            target.take_damage(dmg, mag=True)
        else:
            print('Не хватает маны!')

    def skill_heal_one(self, ally):
        if self.mana >= 20:
            heal = random.randint(20, 35)
            self.mana -= 20
            ally.hp += heal
            print(f'{self.name} лечит {ally.name} на {heal} HP. Мана: {self.mana}')
        else:
            print('Не хватает маны для лечения!')

    def skill_heal_all(self, allies):
        if self.mana >= 40:
            heal = random.randint(10, 20)
            self.mana -= 40
            for ally in allies:
                ally.hp += heal
            print(f'{self.name} лечит всех по {heal} HP. Мана: {self.mana}')
        else:
            print('Не хватает маны для массового лечения!')

class HeroTank(Character):
    def __init__(self, name="Танк"):
        super().__init__(name, hp=100, attack=random.randint(13,20), speed=22, defense=50)
        self.rage = 30
        self.agro = False

    def skill_attack(self, target):
        dmg = self.attack
        target.take_damage(dmg)
        self.rage += 10
        print(f'{self.name} атакует {target.name} ({dmg} урона). Ярость: {self.rage}')

    def skill_defense_buff(self, ally):
        if self.rage >= 20:
            buff = 20
            self.rage -= 20
            ally.defense += buff
            print(f'{self.name} усиливает защиту {ally.name} на {buff}. Защита: {ally.defense}, Ярость: {self.rage}')
        else:
            print('Не хватает ярости!')

    def skill_shield_bash(self, target):
        if self.rage >= 50:
            dmg = self.attack + random.randint(15,25)
            self.rage -= 50
            target.take_damage(dmg)
            print(f'{self.name} УДАР ЩИТОМ {target.name} ({dmg} урона). Ярость: {self.rage}')
        else:
            print('Не хватает ярости для удара щитом!')

    def skill_provoke(self, dragon):
        if self.rage >= 20:
            self.rage -= 20
            self.agro = True
            print(f'{self.name} провоцирует {dragon.name}. Ярость: {self.rage}')
        else:
            print('Не хватает ярости для провокации!')

class HeroHunter(Character):
    def __init__(self, name="Охотник"):
        super().__init__(name, hp=80, attack=random.randint(20,30), speed=30, defense=15, mag_defense=15)
        self.stamina = 50

    def skill_attack(self, target):
        dmg = self.attack
        target.take_damage(dmg)
        self.stamina += 10
        print(f'{self.name} стреляет в {target.name} ({dmg}). Выносливость: {self.stamina}')

    def skill_super_shot(self, target):
        if self.stamina >= 30:
            dmg = self.attack + random.randint(15,25)
            self.stamina -= 30
            target.take_damage(dmg)
            print(f'{self.name} супер-выстрел в {target.name} ({dmg}). Выносливость: {self.stamina}')
        else:
            print('Не хватает выносливости!')

    def skill_speed_buff(self, ally):
        if self.stamina >= 20:
            buff = 10
            self.stamina -= 20
            ally.speed += buff
            print(f'{self.name} усиливает скорость {ally.name} на {buff}. Скорость: {ally.speed}, Выносливость: {self.stamina}')
        else:
            print('Не хватает выносливости для бафа скорости!')

    def skill_multi_shot(self, targets):
        if self.stamina >= 40:
            dmg = self.attack // 2
            self.stamina -= 40
            print(f'{self.name} град стрел! Выносливость: {self.stamina}')
            for t in targets:
                if t.is_alive():
                    t.take_damage(dmg)
        else:
            print('Не хватает выносливости для многоцелевого выстрела!')

class Dragon(Character):
    def __init__(self, name="Дракон"):
        super().__init__(name, hp=500, attack=random.randint(15,25), speed=20, defense=20, mag_defense=20)
        self.speed_buff_turns = 0
        self.minion = None

    def skill_attack(self, target):
        dmg = max(0, self.attack - target.defense//2)
        target.take_damage(dmg)
        send_message(chat_id,f'{self.name} атакует {target.name} ({dmg})')
        print(f'{self.name} атакует {target.name} ({dmg})')

    def skill_attack_all(self, targets):
        dmg = self.attack // 2
        send_message(chat_id,f'{self.name} массовая атака!')
        print(f'{self.name} массовая атака!')
        for t in targets:
            if t.is_alive():
                t.take_damage(dmg)

    def skill_magic(self, target):
        dmg = random.randint(20,35)
        real = max(0, dmg - target.mag_defense//2)
        target.take_damage(real, mag=True)
        send_message(chat_id,f'{self.name} магический удар по {target.name} ({real})')
        print(f'{self.name} магический удар по {target.name} ({real})')

    def skill_magic_all(self, targets):
        dmg = random.randint(15,25)
        send_message(chat_id,f'{self.name} магический дождь!')
        print(f'{self.name} магический дождь!')
        for t in targets:
            if t.is_alive():
                real = max(0, dmg - t.mag_defense//2)
                t.take_damage(real, mag=True)

    def skill_speed_buff(self):
        self.speed += 10
        self.speed_buff_turns = 2
        send_message(chat_id,f'{self.name} ускоряется! Скорость {self.speed} на 2 хода')
        print(f'{self.name} ускоряется! Скорость {self.speed} на 2 хода')

    def skill_summon_minion(self):
        if not self.minion or not self.minion.is_alive():
            self.minion = DragonMinion(self)
            send_message(chat_id,f'{self.name} призывает помощника!')
            print(f'{self.name} призывает помощника!')

    def choose_action(self, heroes):
        actions = [self.skill_attack, self.skill_attack_all, self.skill_magic, self.skill_magic_all,
                   self.skill_speed_buff, self.skill_summon_minion]
        action = random.choice(actions)
        if action in [self.skill_attack, self.skill_magic]:
            target = random.choice([h for h in heroes if h.is_alive()])
            action(target)
        elif action in [self.skill_attack_all, self.skill_magic_all]:
            action(heroes)
        else:
            action()

        if self.speed_buff_turns > 0:
            self.speed_buff_turns -= 1
            if self.speed_buff_turns == 0:
                self.speed -= 10
                send_message(chat_id,f'{self.name} теряет баф скорости.')
                print(f'{self.name} теряет баф скорости.')

        if self.minion and self.minion.is_alive():
            self.minion.choose_action(heroes)

class DragonMinion(Character):
    def __init__(self, dragon, name="Прислужник"):
        super().__init__(name, hp=30, attack=10, speed=15, defense=5, mag_defense=5)
        self.dragon = dragon

    def heal_dragon(self):
        heal = random.randint(20,40)
        self.dragon.hp += heal
        send_message(chat_id,f'{self.name} лечит {self.dragon.name} на {heal}. HP: {self.dragon.hp}')
        print(f'{self.name} лечит {self.dragon.name} на {heal}. HP: {self.dragon.hp}')

    def attack_hero(self, heroes):
        target = random.choice([h for h in heroes if h.is_alive()])
        dmg = 10
        target.take_damage(dmg)
        send_message(chat_id,f'{self.name} атакует {target.name} ({dmg})')
        print(f'{self.name} атакует {target.name} ({dmg})')

    def choose_action(self, heroes):
        action = random.choice([self.heal_dragon, lambda: self.attack_hero(heroes)])
        action()



TOKEN = "7718445747:AAEwC-RX2lRfjevCPK1TAgkR3EeY3r0EsWk"
URL = f"https://api.telegram.org/bot{TOKEN}/"

offset = 0

# Состояние игры
game_state = {
    "heroes": [],
    "dragon": None,
    "turn_order": [],
    "current_turn": 0,
    "in_battle": False,
}

# Функции Telegram
def get_updates():
    global offset
    r = requests.get(URL + "getUpdates", params={"timeout": 100, "offset": offset})
    return r.json()

def send_message(chat_id, text, reply_markup=None):
    data = {"chat_id": chat_id, "text": text, "parse_mode": "HTML"}
    if reply_markup:
        data["reply_markup"] = json.dumps(reply_markup)
    requests.post(URL + "sendMessage", data=data)

#  Главное меню
def show_main_menu(chat_id):
    keyboard = {
        "inline_keyboard": [
            [{"text": "🎮 Начать игру", "callback_data": "start_game"}],
            [{"text": "📖 Правила", "callback_data": "rules"}],
            [{"text": "❌ Выйти", "callback_data": "exit"}]
        ]
    }
    send_message(chat_id, "Добро пожаловать в игру!", keyboard)

#  Создание персонажей


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

# ======================= Ход игры =======================
def next_turn(chat_id):
    if not game_state["in_battle"]:
        return

    order = game_state["turn_order"]
    idx = game_state["current_turn"]

    # если вышли за предел очереди → начинаем заново
    if idx >= len(order):
        game_state["current_turn"] = 0
        idx = 0

    unit = order[idx]

    if isinstance(unit, Character) and not unit.is_alive():
        # если мертвый — пропускаем
        game_state["current_turn"] += 1
        next_turn(chat_id)
        return

    if isinstance(unit, Dragon):
        # Дракон атакует сам
        heroes = [h for h in game_state["heroes"] if h.is_alive()]
        if heroes:
            unit.choose_action(heroes)
            if check_end_game(chat_id):
                return
        game_state["current_turn"] += 1
        next_turn(chat_id)
    else:
        # Ход героя — показываем его кнопки
        show_hero_skills(chat_id, unit)

def show_hero_skills(chat_id, hero):
    if isinstance(hero, HeroMag):
        keyboard = {
            "keyboard": [
                ["🧙‍♂️ Маг. атака", "💥 Супер удар"],
                ["❤️ Лечение одного", "💞 Лечение группы"]
            ],
            "resize_keyboard": True
        }
    elif isinstance(hero, HeroTank):
        keyboard = {
            "keyboard": [
                ["⚔ Обычная атака", "🛡 Супер удар щитом"],
                ["🛡 Баф защиты", "🎯 Провокация (агро)"]
            ],
            "resize_keyboard": True
        }
    elif isinstance(hero, HeroHunter):
        keyboard = {
            "keyboard": [
                ["🏹 Удар", "🔥 Супер удар"],
                ["⚡ Баф скорости", "🌪 Удар по всем"]
            ],
            "resize_keyboard": True
        }
    send_message(chat_id, f"Ход героя {hero.name}. Выберите действие:", keyboard)

# ======================= Проверка конца боя =======================
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

#  Обработка действий героев
def handle_hero_action(chat_id, text):
    hero = game_state["turn_order"][game_state["current_turn"]]
    dragon = game_state["dragon"]
    heroes = game_state["heroes"]

    # --- действия героя (оставляем твой код как есть) ---
    if isinstance(hero, HeroMag):
        if text == "🧙‍♂️ Маг. атака": hero.skill_attack(dragon)
        elif text == "💥 Супер удар": hero.skill_super_attack(dragon)
        elif text == "❤️ Лечение одного": hero.skill_heal_one(random.choice([h for h in heroes if h.is_alive()]))
        elif text == "💞 Лечение группы": hero.skill_heal_all([h for h in heroes if h.is_alive()])
        else: send_message(chat_id, "Неизвестная кнопка!"); return

    elif isinstance(hero, HeroTank):
        if text == "⚔ Обычная атака": hero.skill_attack(dragon)
        elif text == "🛡 Супер удар щитом": hero.skill_shield_bash(dragon)
        elif text == "🛡 Баф защиты": hero.skill_defense_buff(random.choice([h for h in heroes if h.is_alive()]))
        elif text == "🎯 Провокация (агро)": hero.skill_provoke(dragon)
        else: send_message(chat_id, "Неизвестная кнопка!"); return

    elif isinstance(hero, HeroHunter):
        if text == "🏹 Удар": hero.skill_attack(dragon)
        elif text == "🔥 Супер удар": hero.skill_super_shot(dragon)
        elif text == "⚡ Баф скорости": hero.skill_speed_buff(random.choice([h for h in heroes if h.is_alive()]))
        elif text == "🌪 Удар по всем": hero.skill_multi_shot([dragon])
        else: send_message(chat_id, "Неизвестная кнопка!"); return

    # проверка конца боя
    if check_end_game(chat_id):
        return

    # после героя — ход дракона
    game_state["current_turn"] += 1
    next_turn(chat_id)

#  Главный цикл бота
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