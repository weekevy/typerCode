
import curses
import time
import textwrap
from core import config, utils

class TypingRace:
    def __init__(self, stdscr, text):
        self.stdscr = stdscr
        self.text = text
        self.user_input = ""
        self.correct_chars = 0
        self.errors = 0
        self.start_time = time.time()
        self.finished = False
        self._init_colors()
        self.stdscr.timeout(config.REFRESH_DELAY_MS)

    def _init_colors(self):
        curses.start_color()
        curses.use_default_colors()
        curses.init_pair(config.COLOR_NORMAL, config.WHITE, -1)
        curses.init_pair(config.COLOR_CORRECT, config.GREEN, -1)
        curses.init_pair(config.COLOR_WRONG, config.RED, -1)
        curses.init_pair(config.COLOR_BORDER, config.WHITE, -1)

    def draw_border(self):
        self.stdscr.attron(curses.color_pair(config.COLOR_BORDER))
        self.stdscr.border()
        self.stdscr.attroff(curses.color_pair(config.COLOR_BORDER))

    def has_unfixed_error_before(self, index):
        for i in range(index):
            if i < len(self.user_input) and self.user_input[i] != self.text[i]:
                return True
        return False

    def wrap_text(self):
        max_width = max(curses.COLS - 4, 10)
        return textwrap.wrap(self.text, max_width)

    def draw_text(self):
        wrapped = self.wrap_text()
        index = 0
        y = config.PADDING_Y
        for line in wrapped:
            x = config.PADDING_X
            for ch in line:
                if index < len(self.user_input):
                    if self.has_unfixed_error_before(index):
                        color = curses.color_pair(config.COLOR_WRONG)
                    elif self.user_input[index] == ch:
                        color = curses.color_pair(config.COLOR_CORRECT)
                    else:
                        color = curses.color_pair(config.COLOR_WRONG)
                else:
                    color = curses.color_pair(config.COLOR_NORMAL)
                if y < curses.LINES - 1 and x < curses.COLS - 1:
                    self.stdscr.addstr(y, x, ch, color)
                x += 1
                index += 1
            y += 1
        # cursor position
        cursor_y = config.PADDING_Y
        cursor_x = config.PADDING_X
        remaining = len(self.user_input)
        for line in wrapped:
            if remaining <= len(line):
                cursor_x += remaining
                break
            remaining -= len(line)
            cursor_y += 1
        cursor_y = min(cursor_y, curses.LINES - 2)
        cursor_x = min(cursor_x, curses.COLS - 2)
        self.stdscr.move(cursor_y, cursor_x)

    def draw_stats(self):
        elapsed = time.time() - self.start_time
        total = self.correct_chars + self.errors
        wpm = utils.calculate_wpm(total, elapsed)
        acc = utils.calculate_accuracy(total, self.errors)
        stats = f"WPM: {wpm:.1f} | Acc: {acc:.1f}% | Time: {elapsed:.1f}s"
        self.stdscr.addstr(1, config.PADDING_X, stats)

    def last_locked_index(self):
        locked_index = 0
        user_words = self.user_input.split(" ")
        text_words = self.text.split(" ")
        for i, w in enumerate(user_words[:-1]):
            if i < len(text_words) and w == text_words[i]:
                locked_index += len(w) + 1
            else:
                break
        return locked_index

    def ctrl_w(self):
        locked = self.last_locked_index()
        self.user_input = self.user_input[:locked]

    def handle_key(self, key):
        if key == -1:
            return
        if key in (27, 3):
            self.finished = True
            return
        if key == 23:  # Ctrl+W
            self.ctrl_w()
            return
        if key in (curses.KEY_BACKSPACE, 127, 8):
            locked = self.last_locked_index()
            if len(self.user_input) > locked:
                self.user_input = self.user_input[:-1]
            return
        if 32 <= key <= 126:
            if len(self.user_input) < len(self.text):
                ch = chr(key)
                expected = self.text[len(self.user_input)]
                if ch == expected:
                    self.correct_chars += 1
                else:
                    self.errors += 1
                self.user_input += ch
        if len(self.user_input) >= len(self.text):
            self.finished = True

    def run(self):
        while not self.finished:
            self.stdscr.clear()
            self.draw_border()
            self.draw_stats()
            self.draw_text()
            self.stdscr.refresh()
            key = self.stdscr.getch()
            self.handle_key(key)
        self.show_results()

    def show_results(self):
        self.stdscr.clear()
        self.draw_border()
        elapsed = time.time() - self.start_time
        total = self.correct_chars + self.errors
        wpm = utils.calculate_wpm(total, elapsed)
        acc = utils.calculate_accuracy(total, self.errors)

        lines = [
            "TYPING COMPLETE",
            "",
            f"WPM: {wpm:.1f}",
            f"Accuracy: {acc:.1f}%",
            f"Time: {elapsed:.1f}s",
            "",
            "Press any key to exit..."
        ]

        y = curses.LINES // 2 - len(lines) // 2
        for line in lines:
            self.stdscr.addstr(y, max(curses.COLS // 2 - len(line) // 2, 0), line)
            y += 1

        self.stdscr.refresh()

        self.stdscr.getch()

        input()


