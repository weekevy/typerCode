import curses
import time
import textwrap
from core import config, utils
from ui.results_menu import show_results

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
        self.wpm_data = []
        self.error_words = []
        self.last_wpm_time = None
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
        if not wrapped or (len(wrapped) == 1 and not wrapped[0]):
            return
        max_line_length = max(len(line) for line in wrapped)
        
        h, w = self.stdscr.getmaxyx()
        padding_y = (h - len(wrapped)) // 2
        if padding_y < 0:
            padding_y = 0

        padding_x = (w - max_line_length) // 2
        if padding_x < 0:
            padding_x = 0

        index = 0
        y = padding_y
        for i, line in enumerate(wrapped):
            x = padding_x
            line_has_error = False
            for ch_idx, ch in enumerate(line):
                if index < len(self.user_input):
                    if self.user_input[index] != self.text[index]:
                        line_has_error = True
                    
                    if line_has_error:
                        color = curses.color_pair(config.COLOR_WRONG)
                    elif self.user_input[index] == ch:
                        color = curses.color_pair(config.COLOR_CORRECT)
                    else:
                        color = curses.color_pair(config.COLOR_WRONG)
                else:
                    color = curses.color_pair(config.COLOR_NORMAL)

                if y < h and x < w:
                    if y == h - 1 and x == w - 1:
                        # Don't write to the bottom-right corner
                        pass
                    else:
                        try:
                            self.stdscr.addstr(y, x, ch, color)
                        except curses.error:
                            # Fallback to prevent crash
                            pass
                x += 1
                index += 1
            if self.mode == "Code Typing":
                index += 1 # Account for newline character
            y += 1
        # cursor position
        cursor_y = padding_y
        cursor_x = padding_x
        remaining = len(self.user_input)
        for line in wrapped:
            if remaining <= len(line):
                cursor_x += remaining
                break
            remaining -= len(line)
            if self.mode == "Code Typing":
                remaining -= 1 # Account for newline character
            cursor_y += 1
        
        if cursor_y >= h:
            cursor_y = h-1
        if cursor_x >= w:
            cursor_x = w-1

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
        
        h, w = self.stdscr.getmaxyx()
        x_pos = (w - len(stats)) // 2
        self.stdscr.addstr(1, x_pos, stats)

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
            self.last_wpm_time = self.start_time

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
                while len(self.user_input) < len(self.text) and self.text[len(self.user_input)].isspace():
                    self.user_input += self.text[len(self.user_input)]


        if 32 <= key <= 126 or key == ord('\n'):
            if len(self.user_input) < len(self.text):
                ch = chr(key)
                expected = self.text[len(self.user_input)]
                if ch == expected:
                    self.correct_chars += 1
                else:
                    self.errors += 1
                    # Store error words
                    words = self.text.split()
                    word_index = len(self.user_input.split()) -1
                    if word_index < len(words) and words[word_index] not in self.error_words:
                        self.error_words.append(words[word_index])

                self.user_input += ch

                # Record WPM data
                if self.start_time and time.time() - self.last_wpm_time > 1:
                    elapsed = time.time() - self.start_time
                    total = self.correct_chars + self.errors
                    wpm = utils.calculate_wpm(total, elapsed)
                    self.wpm_data.append(wpm)
                    self.last_wpm_time = time.time()

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
        return show_results(self.stdscr, self.start_time, self.correct_chars, self.errors, self.wpm_data, self.error_words)