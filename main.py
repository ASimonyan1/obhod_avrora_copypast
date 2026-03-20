import time
import re
import ctypes
from pynput.keyboard import Controller, Key, KeyCode

print("Вставь код. Когда закончишь — напиши END на новой строке.\n")

lines = []
while True:
    line = input()
    if line == "END":
        break
    lines.append(line)

def detect_current_layout():
    user32 = ctypes.WinDLL('user32', use_last_error=True)
    hwnd = user32.GetForegroundWindow()
    thread_id = user32.GetWindowThreadProcessId(hwnd, 0)
    layout_id = user32.GetKeyboardLayout(thread_id)
    lang_id = layout_id & 0xFFFF

    if lang_id == 0x0419:
        return "RU"
    return "EN"

start_layout = detect_current_layout()

print("\nПереключись в Аврору и поставь курсор. Старт через 5 секунд...")
time.sleep(5)

keyboard = Controller()

CHAR_DELAY = 0.25
LINE_DELAY = 1.5

current_layout = start_layout

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
    press_key(Key.home)
    time.sleep(0.05)
    press_key(Key.home)
    time.sleep(0.05)

def press_dot():
    keyboard.press(KeyCode.from_vk(190))  # точка
    keyboard.release(KeyCode.from_vk(190))

first_line = True

for line in lines:
    if not first_line:
        go_to_line_start()

    leading_spaces = len(line) - len(line.lstrip(' '))
    tabs = leading_spaces // 4

    for _ in range(tabs):
        press_key(Key.tab)
        time.sleep(0.05)

    content = line.lstrip(' ')

    for ch in content:
        want_layout = "RU" if is_russian(ch) else "EN"

        if want_layout != current_layout:
            toggle_layout()
            current_layout = want_layout

        if ch == '.':
            press_dot()
        else:
            keyboard.type(ch)

        time.sleep(CHAR_DELAY)

    press_key(Key.enter)
    time.sleep(LINE_DELAY)
    first_line = False

print("Готово!")