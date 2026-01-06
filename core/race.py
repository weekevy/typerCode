
import curses
import time
import textwrap
from core import config, utils

class TypingRace:
    def __init__(self, stdscr, text, mode="Regular Typing"):
        self.stdscr = stdscr
        self.text = text
        self.mode = mode
        self.user_input = ""
        self.correct_chars = 0
        self.errors = 0
        self.start_time = None
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
        if self.mode == "Code Typing":
            return self.text.split('\n')
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
            if self.mode == "Code Typing":
                index += 1 # Account for newline character
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
            if self.mode == "Code Typing":
                remaining -= 1 # Account for newline character
            cursor_y += 1
        cursor_y = min(cursor_y, curses.LINES - 2)
        cursor_x = min(cursor_x, curses.COLS - 2)
        self.stdscr.move(cursor_y, cursor_x)

    def draw_stats(self):
        if self.start_time:
            elapsed = time.time() - self.start_time
        else:
            elapsed = 0
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


import curses
import time
import textwrap
from core import config, utils

class TypingRace:
    def __init__(self, stdscr, text, mode="Regular Typing"):
        self.stdscr = stdscr
        self.text = text
        self.mode = mode
        self.user_input = ""
        self.correct_chars = 0
        self.errors = 0
        self.start_time = None
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
        if self.mode == "Code Typing":
            return self.text.split('\n')
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
            if self.mode == "Code Typing":
                index += 1 # Account for newline character
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
            if self.mode == "Code Typing":
                remaining -= 1 # Account for newline character
            cursor_y += 1
        cursor_y = min(cursor_y, curses.LINES - 2)
        cursor_x = min(cursor_x, curses.COLS - 2)
        self.stdscr.move(cursor_y, cursor_x)

    def draw_stats(self):
        if self.start_time:
            elapsed = time.time() - self.start_time
        else:
            elapsed = 0
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

        if not self.start_time and 32 <= key <= 126:
            self.start_time = time.time()

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

        if self.mode == "Code Typing":
            # Skip leading whitespace
            current_line_index = self.text.rfind('\n', 0, len(self.user_input)) + 1
            if len(self.user_input) == current_line_index:
                if key == ord(' '):
                    if self.text[len(self.user_input)].isspace():
                        self.user_input += ' '
                        return
                if key == ord('\t'):
                     if self.text[len(self.user_input)].isspace():
                        self.user_input += '\t'
                        return


        if 32 <= key <= 126 or key == ord('\n'):
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
        self.stdscr.nodelay(True)
        while not self.finished:
            self.stdscr.erase()
            self.draw_border()
            self.draw_stats()
            self.draw_text()
            self.stdscr.refresh()
            key = self.stdscr.getch()
            self.handle_key(key)
            time.sleep(0.01)
        return self.show_results()

    def show_results(self):
        self.stdscr.nodelay(False)
        self.stdscr.clear()
        self.draw_border()
        if self.start_time:
            elapsed = time.time() - self.start_time
        else:
            elapsed = 0
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
        ]

        y = curses.LINES // 2 - len(lines) // 2 -1
        for i, line in enumerate(lines):
            x = max(curses.COLS // 2 - len(line) // 2, 0)
            if i == 0:
                self.stdscr.addstr(y, x, line, curses.A_BOLD)
            else:
                self.stdscr.addstr(y, x, line)
            y += 1

        options = ["Restart", "Exit"]
        current_option = 0
        while True:
            for i, option in enumerate(options):
                x = curses.COLS // 2 - len(option) // 2
                y = curses.LINES // 2 + 2 + i
                if i == current_option:
                    self.stdscr.addstr(y, x, option, curses.A_REVERSE)
                else:
                    self.stdscr.addstr(y, x, option)
            self.stdscr.refresh()

            key = self.stdscr.getch()
            if key == curses.KEY_UP or key == ord('k'):
                current_option = (current_option - 1) % len(options)
            elif key == curses.KEY_DOWN or key == ord('j'):
                current_option = (current_option + 1) % len(options)
            elif key == curses.KEY_ENTER or key == 10:
                return options[current_option]


    def run(self):
        self.stdscr.nodelay(True)
        while not self.finished:
            self.stdscr.erase()
            self.draw_border()
            self.draw_stats()
            self.draw_text()
            self.stdscr.refresh()
            key = self.stdscr.getch()
            self.handle_key(key)
            time.sleep(0.01)
        return self.show_results()

    def show_results(self):
        self.stdscr.nodelay(False)
        self.stdscr.clear()
        self.draw_border()
        if self.start_time:
            elapsed = time.time() - self.start_time
        else:
            elapsed = 0
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
        ]

        y = curses.LINES // 2 - len(lines) // 2 -1
        for i, line in enumerate(lines):
            x = max(curses.COLS // 2 - len(line) // 2, 0)
            if i == 0:
                self.stdscr.addstr(y, x, line, curses.A_BOLD)
            else:
                self.stdscr.addstr(y, x, line)
            y += 1

        options = ["Restart", "Exit"]
        current_option = 0
        while True:
            for i, option in enumerate(options):
                x = curses.COLS // 2 - len(option) // 2
                y = curses.LINES // 2 + 2 + i
                if i == current_option:
                    self.stdscr.addstr(y, x, option, curses.A_REVERSE)
                else:
                    self.stdscr.addstr(y, x, option)
            self.stdscr.refresh()

            key = self.stdscr.getch()
            if key == curses.KEY_UP or key == ord('k'):
                current_option = (current_option - 1) % len(options)
            elif key == curses.KEY_DOWN or key == ord('j'):
                current_option = (current_option + 1) % len(options)
            elif key == curses.KEY_ENTER or key == 10:
                return options[current_option]



