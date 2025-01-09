import json
import random
from typing import Type

class Character:
    max_level = 11
    _experience_required_per_level = [100, 200, 400, 800, 1600, 3200, 6400, 12800, 25600, 51200]

    def __init__(self, level: int, experience: int):
        self.level = level
        self.experience = experience
        self._health_points = self.base_health_points * self.level
        self._attack_power = self.base_attack_power + self.level

    def gain_experience(self, amount: int):
        self.experience += amount
        while self.level < self.max_level and self.experience >= self._experience_required_per_level[self.level - 1]:
            self.level_up()

    def level_up(self):
        if self.level < self.max_level:
            self.level += 1
            self._health_points += int(self.max_health_points / 2)
            self._attack_power = self.base_attack_power * self.level
            print(f"{self.character_name} достиг уровня {self.level}")

    def attack(self, target: "Character"):
        target.take_damage(damage=self._attack_power)

    def take_damage(self, damage: int):
        effective_damage = int(damage * (100 - self.defence) / 100)
        self._health_points -= effective_damage

    def is_alive(self):
        return self._health_points > 0

    @property
    def defence(self):
        return self.base_defence + self.level

    @property
    def max_health_points(self):
        return self.level * self.base_health_points

    @property
    def health_points_percent(self):
        return 100 * self._health_points // self.max_health_points

    def save_progress(self):
        with open(f"{self.character_name}.json", 'w') as file:
            json.dump({'level': self.level, 'experience': self.experience}, file)

    def load_progress(self):
        try:
            with open(f"{self.character_name}.json", 'r') as file:
                data = json.load(file)
                self.level = data['level']
                self.experience = data['experience']
                self._health_points = self.base_health_points * self.level
                self._attack_power = self.base_attack_power * self.level
        except FileNotFoundError:
            print(f"No saved progress found for {self.character_name}.")

    def reset_progress(self):
        self.level = 1
        self.experience = 0
        self._health_points = self.base_health_points
        self._attack_power = self.base_attack_power

    def __str__(self):
        return f"{self.character_name} (уровень: {self.level}, опыт: {self.experience}, здоровье: {self._health_points})"

class Ork(Character):
    base_health_points = 100
    base_attack_power = 10
    character_name = "Орк"
    base_defence = 15

    @property
    def defence(self) -> int:
        defence = super().defence
        if self.health_points_percent < 30:
            defence *= 5
        return defence

class Elf(Character):
    base_health_points = 50
    base_attack_power = 20
    character_name = "Эльф"
    base_defence = 10

    def attack(self, target: "Character") -> None:
        attack_power = self._attack_power
        if target.health_points_percent < 50:
            attack_power = self._attack_power * 8
        target.take_damage(damage=attack_power)

class Human(Character):
    base_health_points = 80
    base_attack_power = 12
    character_name = "Человек"
    base_defence = 12

    @property
    def defence(self) -> int:
        defence = super().defence
        if self.health_points_percent < 30:
            defence *= 2
        return defence

    def attack(self, target: "Character") -> None:
        attack_power = self._attack_power
        if target.health_points_percent < 30:
            attack_power = self._attack_power * 2
        target.take_damage(damage=attack_power)






class Mob(Character):
    max_level = 10

    def __init__(self, level: int, experience: int):
        super().__init__(level, experience)


class Goblin_Collector(Mob):
    base_health_points = 100
    base_attack_power = 10
    character_name = "Собиратель Гоблинов"
    base_defence = 10

class Goblin_Scout(Mob):
    base_health_points = 250
    base_attack_power = 15
    character_name = "Разведчик Гоблинов"
    base_defence = 15

class Goblin_Hunter(Mob):
    base_health_points = 500
    base_attack_power = 25
    character_name = "Охотник Гоблинов"
    base_defence = 25

class Goblin_King(Mob):
    base_health_points = 1000
    base_attack_power = 40
    character_name = "Король Гоблинов"
    base_defence = 40

class Game:
    def __init__(self, player_character: Character):
        self.player_character = player_character
        self.enemies = []

    def start_game(self):
        print("Добро пожаловать в игру!")
        self.main_loop()

    def show_player_stats(self):
        print(f"\nТекущие характеристики вашего персонажа:")
        print(f"Расса: {self.player_character.character_name}")
        print(f"Уровень: {self.player_character.level}")
        print(f"Опыт: {self.player_character.experience}/{self.player_character._experience_required_per_level[self.player_character.level - 1]} до следующего уровня")
        print(f"Здоровье: {self.player_character._health_points}/{self.player_character.max_health_points}")
      
    def main_loop(self):
        while True:
            print("\nЧто вы хотите сделать?")
            print("1. Сражаться")
            print("2. Отдохнуть")
            print("3. Просмотреть статистику персонажа")
            print("4. Сохранить прогресс")
            print("5. Выйти из игры")

            choice = input("Введите номер действия: ")

            if choice == "1":
                self.fight()
            elif choice == "2":
                self.rest()
            elif choice == "3":
                self.show_player_stats()
            elif choice == "4":
                self.save_progress()
            elif choice == "5":
                break
            else:
                print("Неверный выбор. Попробуйте снова.")

    def fight_in_location(self, location: str):
        if location == "Лесная опушка":
            enemies = [Goblin_Collector(random.randint(1, 3), 0)]
        elif location == "Лесная чаща":
            enemies = [Goblin_Scout(random.randint(4, 6), 0)]
        elif location == "Лесные дебри":
            enemies = [
                Goblin_Hunter(random.randint(7, 9), 0),
                Goblin_King(10, 0)
            ]
        
        for enemy in enemies:
            print(f"Вам предстоит бой с {enemy.character_name} уровнем {enemy.level}. Количество HP{enemy._health_points} ")
            
            # Добавляем выбор начать бой или сбежать
            action = input("Выберите действие:\n1. Начать бой\n2. Сбежать\nВаш выбор: ")
            
            if action == "1":
                while self.player_character.is_alive() and enemy.is_alive():
                    # Показываем текущие HP игрока и врага
                    print(f"\nУ вас осталось {self.player_character._health_points} HP")
                    print(f"У врага осталось {enemy._health_points} HP")
                    
                    self.player_character.attack(enemy)
                    if enemy.is_alive():
                        enemy.attack(self.player_character)
                
                if not self.player_character.is_alive():
                    print("Вы проиграли бой...")
                    break  # Прекращаем бой, если игрок умер
                else:
                    print(f"Вы победили! Получено опыта: {enemy.level * 55}")
                    self.player_character.gain_experience(amount=enemy.level * 55)
            elif action == "2":
                print("Вы успешно сбежали.")
                break  # Прерывание боя и переход к следующей локации
            else:
                print("Неверный выбор. Попробуйте снова.")

    def choose_location(self) -> str:
        locations = ["Лесная опушка", "Лесная чаща", "Лесные дебри"]
        print("Выберите одну из локаций:")
        for i, location in enumerate(locations):
            print(f"{i+1}. {location}")

        selection = int(input("Введите номер локации: "))
        chosen_location = locations[selection - 1]
        print(f"Вы выбрали {chosen_location}.")
        return chosen_location

    def fight(self):
        chosen_location = self.choose_location()
        self.fight_in_location(chosen_location)

    def rest(self):
        print("Вы отдохнули и восстановили здоровье.")
        self.player_character._health_points = self.player_character.max_health_points

    def generate_enemy(self) -> Character:
        enemy_types = [Goblin_Collector, Goblin_Scout, Goblin_Hunter, Goblin_King]
        enemy_type = random.choice(enemy_types)
        enemy_level = random.randint(1, self.player_character.level + 2)
        return enemy_type(level=enemy_level, experience=0)

    def save_progress(self):
        self.player_character.save_progress()
        print("Прогресс сохранен.")

# Создание отдельных экземпляров для Орка, Эльфа, Человека
characters = {
    "орк": Ork,
    "эльф": Elf,
    "человек": Human
}

print("Выберите вашего персонажа:")
for index, char in enumerate(characters.keys()):
    print(f"{index+1}. {char.capitalize()}")

selection = int(input("Введите номер персонажа: "))
selected_char_class = list(characters.values())[selection - 1]
player = selected_char_class(level=1, experience=0)

game = Game(player)
game.start_game()