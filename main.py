import curses


MENU = ["בחר רשת", "הגדרות", "עזרה", "יציאה"]


def main(stdscr):
    MENU[0] = rtl_words(MENU[0])

    curses.curs_set(0)
    stdscr.nodelay(False)
    stdscr.keypad(True)

    current_row = 0

    while True:
        stdscr.clear()
        h, w = stdscr.getmaxyx()

        stdscr.box()

        title = "מצאון"
        stdscr.addstr(1, (w - len(title)) // 2, title, curses.A_BOLD)

        for idx, item in enumerate(MENU):
            x = (w - len(item)) // 2
            y = 3 + idx

            if idx == current_row:
                stdscr.attron(curses.A_REVERSE)
                stdscr.addstr(y, x, item)
                stdscr.attroff(curses.A_REVERSE)
            else:
                stdscr.addstr(y, x, item)

        footer = rtl_words(
            "השתמש ביחלך על מנת לזוז, הכנס על מנת ללחוץ, ו / על מנת לצאת"
        )
        stdscr.addstr(h - 2, (w - len(footer)) // 2, footer)

        stdscr.refresh()

        key = stdscr.get_wch()

        if key in ("ל", curses.KEY_UP) and current_row > 0:
            current_row -= 1
        elif key in ("ח", curses.KEY_DOWN) and current_row < len(MENU) - 1:
            current_row += 1
        elif key == "/":
            break
        elif key in (curses.KEY_ENTER, 10, 13, "\n", "\r"):
            if MENU[current_row] == "יציאה":
                break
            else:
                stdscr.addstr(
                    h - 4,
                    2,
                    rtl_words(
                        f"הפונקצייה '{rtl_words(MENU[current_row])}' עדיין בבטא, נא להיות סבלניים"
                    ),
                )
                stdscr.getch()


def rtl_words(text):
    return " ".join(text.split()[::-1])


if __name__ == "__main__":
    curses.wrapper(main)
