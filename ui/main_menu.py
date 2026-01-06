import curses
from curses import wrapper

def display_main_menu(stdscr):
    curses.curs_set(0)
    curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_CYAN)

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

        # Menu Box
        box_h, box_w = 5, 24
        box_y, box_x = h // 2 - 2, w // 2 - 12
        box = curses.newwin(box_h, box_w, box_y, box_x)
        box.box()

        for i, option in enumerate(options):
            y, x = 2, 12 - len(option) // 2
            if i == current_option:
                box.addstr(y + i, x, option, curses.color_pair(2))
            else:
                box.addstr(y + i, x, option, curses.color_pair(1))

        stdscr.refresh()
        box.refresh()

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
