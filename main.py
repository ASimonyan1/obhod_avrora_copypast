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
current_cap = "OFF"  # предполагаем, что перед стартом Caps Lock выключен

def toggle_cap():
    keyboard.press(Key.shift)
    keyboard.release(Key.shift)
    time.sleep(0.1)

def toggle_layout():
    keyboard.press(Key.alt_l)
    keyboard.press(Key.shift)
    keyboard.release(Key.shift)
    keyboard.release(Key.alt_l)
    time.sleep(0.3)

def is_russian(ch):
    return re.match(r"[А-Яа-яЁё]", ch) is not None

def is_rus_capital(ch):
    return re.match(r"[А-ЯЁ]", ch) is not None

def is_eng_capital(ch):
    return re.match(r"[A-Z]", ch) is not None



for line in lines:
    for ch in line:

        want_layout = "RU" if is_russian(ch) else "EN"

        if want_layout != current_layout:
            toggle_layout()
            current_layout = want_layout

        if current_cap == "RU":
            want_cap = "ON" if is_rus_capital(ch) else "OFF"

        else:
            want_cap = "ON" if is_eng_capital(ch) else "OFF"

        if want_cap != current_cap:
            toggle_cap()
            current_cap = want_cap

        keyboard.type(ch)
        time.sleep(CHAR_DELAY)

    keyboard.press(Key.enter)
    keyboard.release(Key.enter)
    time.sleep(LINE_DELAY)

print("Готово!")
