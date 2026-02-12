import curses
import subprocess

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
            if MENU[current_row] == rtl_words("בחר רשת"):
                wifi_menu(stdscr)
            elif MENU[current_row] == "יציאה":
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


def get_wifi_networks():
    try:
        result = subprocess.run(
            ["nmcli", "-t", "-f", "SSID,SECURITY,SIGNAL", "dev", "wifi", "list"],
            capture_output=True,
            text=True,
            check=True,
        )

        networks = []
        for line in result.stdout.strip().split("\n"):
            if line:
                parts = line.split(":")
                ssid = parts[0] if parts[0] else "<Hidden>"
                security = parts[1]
                signal = parts[2]
                networks.append(f"{ssid} | {signal}% | {security}")

        return networks if networks else ["לא נמצאו רשתות"]

    except Exception as e:
        return [f"שגיאה: {str(e)}"]


def connect_to_network(stdscr, ssid):
    pass


def wifi_menu(stdscr):
    networks = get_wifi_networks()
    current_row = 0

    while True:
        stdscr.clear()
        h, w = stdscr.getmaxyx()
        stdscr.box()

        title = rtl_words("בחר רשת")
        stdscr.addstr(1, (w - len(title)) // 2, title, curses.A_BOLD)

        for idx, net in enumerate(networks):
            y = 3 + idx

            if y >= h - 2:
                break

            net_display = net[: w - 4]

            if idx == current_row:
                stdscr.attron(curses.A_REVERSE)
                stdscr.addstr(y, 2, net_display)
                stdscr.attroff(curses.A_REVERSE)
            else:
                stdscr.addstr(y, 2, net_display)

        stdscr.refresh()
        key = stdscr.get_wch()

        if key in ("ל", curses.KEY_UP) and current_row > 0:
            current_row -= 1
        elif key in ("ח", curses.KEY_DOWN) and current_row < len(MENU) - 1:
            current_row += 1
        elif key in (10, 13, curses.KEY_ENTER):
            selected = networks[current_row].split(" | ")[0]
            if selected not in ("לא נמצאו רשתות",) and not selected.startswith("שגיאה"):
                connect_to_network(stdscr, selected)
                break
        elif key == "/":
            break


def rtl_words(text):
    return " ".join(text.split()[::-1])


if __name__ == "__main__":
    curses.wrapper(main)
