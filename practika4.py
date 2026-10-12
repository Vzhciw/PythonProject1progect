import sys
import time
import random


# Эффектный вывод текста, как в визуальных новеллах
def anime_print(text, delay=0.03):
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    print()


def show_opening():
    print("=" * 60)
    anime_print("поздравляю вы зашли в игру", 0.05)
    print("=" * 60)
    time.sleep(0.5)
    anime_print("мир прогрузился", 0.04)
    anime_print("что-то вылезло из мрачного леса...", 0.04)
    anime_print("что-то мне подсказывает что ты не справишься юноша", 0.04)
    anime_print("готовся будет сложно не каждый после такого выживает!", 0.04)
    print("=" * 60)
    time.sleep(1)


class Hero:
    def __init__(self, name, character_type):
        self.name = name
        self.type = character_type
        self.level = 1
        self.exp = 0
        self.max_hp = 100
        self.hp = 100
        self.mana = 50
        self.max_mana = 50

        # настройки классов ЫЫ
        if character_type == "1":
            self.class_name = "подчиненный)"
            self.atk = 25
            self.defense = 5
            self.ultimate_name = "удар ЧЕРНОЙ ДЫРЫ исчезновение в тумане!"
        elif character_type == "2":
            self.class_name = "черт высокий ранг"
            self.atk = 35
            self.defense = 2
            self.ultimate_name = "УДАР ОГНЕМ, туши одежду!!!"
        else:
            self.class_name = "ниндзя из темных глубин японии..."
            self.atk = 20
            self.defense = 8
            self.ultimate_name = "ТЫСЯЧА ножевых ранениц в спину!"

    def show_stats(self):
        print(f"\n профиль персонажа")
        print(f"нейм: {self.name} | класс: {self.class_name}")
        print(f"уровень: {self.level} | EXP: {self.exp}/100")
        print(f"здоровье (HP): {self.hp}/{self.max_hp}")
        print(f"мана (MP): {self.mana}/{self.max_mana}")
        print(f"атака: {self.atk} | Защита: {self.defense}")
        print(f"ульта: {self.ultimate_name}")
        print(f"-------------------------\n")

    def rest(self):
        anime_print(f"» {self.name} делает перерыв, кушает и обматывает раны...")
        self.hp = self.max_hp
        self.mana = self.max_mana
        time.sleep(1)
        print("здоровье и мана полностью восстановлены")

    def gain_exp(self, amount):
        self.exp += amount
        print(f"получено {amount} опыта!")
        if self.exp >= 100:
            self.level += 1
            self.exp -= 100
            self.max_hp += 20
            self.hp = self.max_hp
            self.atk += 5
            self.defense += 2
            print(f" ваш уровень повысился до {self.level} характеристики выросли ")


def battle_enemy(hero, enemy_name, enemy_hp, enemy_atk, is_boss=False):
    print("\n" + "⚔️" * 20)
    if is_boss:
        anime_print(f"ОБОЖЕ ЭТО ОН появился финальный босс: {enemy_name} !!!", 0.05)
    else:
        print(f"враг заблокировал путь и слегка улыбнулся злобной улыбкой: {enemy_name}!")
    print("⚔️" * 20 + "\n")

    initial_enemy_hp = enemy_hp

    while enemy_hp > 0 and hero.hp > 0:
        print(f"\nваше хп: {hero.hp}/{hero.max_hp} | мана: {hero.mana}/{hero.max_mana}")
        print(f"враг {enemy_name} хп: {enemy_hp}/{initial_enemy_hp}")
        print("ваше действие:")
        print("1. обычный удар ")
        print("2. использовать ульту (тратит 25 маны)")
        print("3. попытаться увернуться (шанс заблокать урон)")

        choice = input("выбор (1-3): ")

        if choice == "1":
            damage = max(1, hero.atk - random.randint(0, 3))
            enemy_hp -= damage
            print(f"» вы выкрикиваете БАНКАЙ и наносите {damage} урона")
        elif choice == "2":
            if hero.mana >= 25:
                hero.mana -= 25
                damage = hero.atk * 2
                enemy_hp -= damage
                anime_print(f"ЭПИЧНЫЙ удар катаной вы активируете: {hero.ultimate_name}")
                print(f" Нанесено {damage} критического урона")
            else:
                print(" недостаточно маны, пришлось бить просто рукой(")
                enemy_hp -= 5
        elif choice == "3":
            if random.random() > 0.4:
                print("вы уклонились от следующей атаки")
                continue
            else:
                print("вы не смогли уклониться, и споткнулись об камень")

        if enemy_hp <= 0:
            break

        # ход врага
        enemy_damage = max(1, enemy_atk - hero.defense + random.randint(-2, 2))
        hero.hp -= enemy_damage
        print(f"« {enemy_name} атакует в ответ и наносит вам {enemy_damage} урона")

        if hero.hp <= 0:
            print("твое хп упало до нуля в глазах плывет... неужели это конец?")
            return False

    if enemy_hp <= 0:
        print(f"\n ПОБЕДА враг {enemy_name} повержен!")
        if is_boss:
            return "boss_win"
        hero.gain_exp(50)
        return True


def main():
    show_opening()

    name = input("введите имя вашего персонажа: ")
    if not name:
        name = "орихиме"

    print("\nвыберите твою скрытую силу:")
    print("1. сила физичиского урона (воин)")
    print("2. стихийная магия (маг)")
    print("3. лечение и защита (доктор)")

    class_choice = input("выбор (1-3): ")
    hero = Hero(name, class_choice)

    anime_print(f"\nсистема: Персонаж {hero.name} успешно призван в этот мир!")
    hero.show_stats()

    # Сюжетные шаги
    stages = [
        {"name": "страшный гоблин", "hp": 40, "atk": 10, "boss": False},
        {"name": "сумашедший сталкер", "hp": 65, "atk": 15, "boss": False},
        {"name": "ФИНАЛЬНЫЙ БОСС людоед", "hp": 150, "atk": 22, "boss": True}
    ]

    stage_idx = 0
    while stage_idx < len(stages) and hero.hp > 0:
        current_enemy = stages[stage_idx]

        print("\n меню")
        print("1. идти вперёд по сюжету (в бой на смерть)")
        print("2. посмотреть свои статы")
        print("3. почилить (восстановить хп и ману)")
        print("4. выйти из игры (признать поражение)")

        action = input("что выберешь путник? (1-4): ")

        if action == "1":
            result = battle_enemy(
                hero,
                current_enemy["name"],
                current_enemy["hp"],
                current_enemy["atk"],
                current_enemy["boss"]
            )
            if result == "boss_win":
                print("\n" + "👑" * 30)
                anime_print("ПОЗДАВЛЯЕМ ВЫ ПРОШЛИ ИГРУ медалька от меня! спасибо за участие!")
                print("👑" * 30 + "\n")
                break
            elif result:
                stage_idx += 1
            else:
                print("\n[GAME OVER] ну в следуйщий раз выиграешь, вы всегда можете перезапустить игру")
                break
        elif action == "2":
            hero.show_stats()
        elif action == "3":
            hero.rest()
        elif action == "4":
            print("вы вышли из игры, ха ну и трус оказался")
            break
        else:
            print("персонаж растеряно смотрит по сторонам")


if __name__ == "__main__":
    main()