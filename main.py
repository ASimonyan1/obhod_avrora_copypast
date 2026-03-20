import time
import re
from pynput.keyboard import Controller, Key

print("Вставь код. Когда закончишь — напиши END на новой строке.\n")

lines = []
while True:
    line = input()
    if line == "END":
        break
    lines.append(line)

print("\nПереключись в Аврору и поставь курсор. Старт через 5 секунд...")
time.sleep(5)

keyboard = Controller()

CHAR_DELAY = 0.25
LINE_DELAY = 1.5

current_layout = "EN"  # предполагаем, что перед стартом включён английский

def toggle_layout():
    keyboard.press(Key.alt_l)
    keyboard.press(Key.shift)
    keyboard.release(Key.shift)
    keyboard.release(Key.alt_l)
    time.sleep(0.3)

def is_russian(ch):
    return re.match(r"[А-Яа-яЁё]", ch) is not None

def press_key(key):
    keyboard.press(key)
    keyboard.release(key)

def go_to_line_start():
    # В некоторых редакторах первый Home ведёт к первому символу текста,
    # а второй — в абсолютное начало строки
    press_key(Key.home)
    time.sleep(0.05)
    press_key(Key.home)
    time.sleep(0.05)

first_line = True

for line in lines:
    if not first_line:
        # После Enter жёстко возвращаемся в начало новой строки
        go_to_line_start()

    for ch in line:
        want_layout = "RU" if is_russian(ch) else "EN"

        if want_layout != current_layout:
            toggle_layout()
            current_layout = want_layout

        keyboard.type(ch)
        time.sleep(CHAR_DELAY)

    press_key(Key.enter)
    time.sleep(LINE_DELAY)
    first_line = False

print("Готово!")