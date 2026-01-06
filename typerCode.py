
import curses
from core import race, utils

TEXTS_FILE = "data/texts.json"

def load_text():
    data = utils.load_json(TEXTS_FILE)
    if "texts" in data and data["texts"]:
        return data["texts"][0]
    return "Default typing text."

def main(stdscr):
    text = load_text()
    race.TypingRace(stdscr, text).run()

if __name__ == "__main__":
    curses.wrapper(main)
