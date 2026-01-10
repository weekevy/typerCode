import curses
import os
import random
import time
from core import race, utils
from ui.main_menu import draw_main_menu
from ui.language_menu import display_language_menu
from ui.curses_ui import init_curses

DATA_DIR = "data"
TEXTS_FILE = os.path.join(DATA_DIR, "texts.json")

def load_text(text_type="regular", code_file=None):
    if text_type == "Code Typing" and code_file:
        with open(os.path.join(DATA_DIR, code_file), "r") as f:
            return f.read()
    else:
        data = utils.load_json(TEXTS_FILE)
        if "texts" in data and data["texts"]:
            return data["texts"][0]
        return "Default typing text."

def main(stdscr):
    init_curses(stdscr)

    current_option = 0
    options = ["Regular Typing", "Code Typing", "Neovim Practice", "Exit"]
    
    while True:
        draw_main_menu(stdscr, current_option, options)
        
        key = stdscr.getch()

        if key != -1:
            if key == curses.KEY_UP or key == ord('k'):
                current_option = (current_option - 1) % len(options)
            elif key == curses.KEY_DOWN or key == ord('j'):
                current_option = (current_option + 1) % len(options)
            elif key == curses.KEY_ENTER or key == 10:
                selected_option = options[current_option]
                
                if selected_option == "Exit":
                    break

                if selected_option == "Code Typing":
                    code_file = display_language_menu(stdscr)
                    text = load_text(selected_option, code_file)
                else:
                    text = load_text(selected_option)

                if text:
                    result = race.TypingRace(stdscr, text, mode=selected_option).run()
                    if result == "Exit":
                        # Return to main menu, so do nothing here
                        pass
                
                # After race, reset the screen options
                curses.curs_set(0)
                stdscr.timeout(100)

if __name__ == "__main__":
    curses.wrapper(main)