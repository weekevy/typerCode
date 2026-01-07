import curses
from curses import wrapper

def display_main_menu(stdscr):
    curses.curs_set(0)
    curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_BLACK)

    current_option = 0
    options = ["Regular Typing", "Code Typing"]
    title = "TYPERCODE"
    subtitle = "A Minimalist Typing Tester"

    while True:
        stdscr.bkgd(' ', curses.color_pair(1))
        stdscr.clear()
        h, w = stdscr.getmaxyx()

        # Title
        stdscr.addstr(h // 2 - 5, w // 2 - len(title) // 2, title, curses.A_BOLD | curses.color_pair(1))
        stdscr.addstr(h // 2 - 4, w // 2 - len(subtitle) // 2, subtitle, curses.color_pair(1))

        for i, option in enumerate(options):
            y, x = h // 2 - 1 + i, w // 2 - len(option) // 2
            if i == current_option:
                stdscr.addstr(y, x, option, curses.color_pair(2) | curses.A_BOLD)
            else:
                stdscr.addstr(y, x, option, curses.color_pair(1))

        stdscr.refresh()

        key = stdscr.getch()

        if key == curses.KEY_UP or key == ord('k'):
            current_option = (current_option - 1) % len(options)
        elif key == curses.KEY_DOWN or key == ord('j'):
            current_option = (current_option + 1) % len(options)
        elif key == curses.KEY_ENTER or key == 10:
            curses.curs_set(1) # Make cursor visible
            return options[current_option]

if __name__ == '__main__':
    wrapper(display_main_menu)
