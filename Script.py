# This file is part of Windows App Remover
# Licensed under the MIT License

import curses
import subprocess
import locale

locale.setlocale(locale.LC_ALL, '')

apps = {
    "3D Builder": "Microsoft.3DBuilder",
    "Alarms & Clock": "Microsoft.WindowsAlarms",
    "Calculator": "Microsoft.WindowsCalculator",
    "Camera": "Microsoft.WindowsCamera",
    "Cortana": "Microsoft.549981C3F5F10",
    "Get Help": "Microsoft.GetHelp",
    "Get Started": "Microsoft.Getstarted",
    "Mail & Calendar": "microsoft.windowscommunicationsapps",
    "Maps": "Microsoft.WindowsMaps",
    "Microsoft Edge": "Microsoft.MicrosoftEdge",
    "Microsoft Solitaire": "Microsoft.MicrosoftSolitaireCollection",
    "Microsoft Sticky Notes": "Microsoft.MicrosoftStickyNotes",
    "Movies & TV": "Microsoft.ZuneVideo",
    "MSN Weather": "Microsoft.BingWeather",
    "OneNote": "Microsoft.Office.OneNote",
    "Paint 3D": "Microsoft.MSPaint",
    "Photos": "Microsoft.Windows.Photos",
    "Skype": "Microsoft.SkypeApp",
    "Store": "Microsoft.WindowsStore",
    "Xbox": "Microsoft.XboxApp",
}

app_names = list(apps.keys())
selected = [False] * len(app_names)

def draw_menu(stdscr, current_row):
    stdscr.clear()

    stdscr.addstr("=== App Remover ===\n", curses.color_pair(2))
    stdscr.addstr("Автор: ты :)\n", curses.color_pair(3))
    stdscr.addstr("Управление: ↑↓ - навигация | Пробел - выбор | a - все | d - снять | Enter - удалить | q - выход\n\n")

    for idx, name in enumerate(app_names):
        mark = "[X]" if selected[idx] else "[ ]"
        if idx == current_row:
            stdscr.attron(curses.color_pair(1))
            stdscr.addstr(f"{mark} {name}\n")
            stdscr.attroff(curses.color_pair(1))
        else:
            stdscr.addstr(f"{mark} {name}\n")

    stdscr.refresh()

def remove_selected(stdscr):
    stdscr.clear()
    stdscr.addstr("Удаление выбранных приложений...\n", curses.color_pair(3))
    for idx, sel in enumerate(selected):
        if sel:
            pkg = apps[app_names[idx]]
            stdscr.addstr(f"Удаляю: {app_names[idx]} ({pkg})...\n")
            stdscr.refresh()
            cmd = f"Get-AppxPackage *{pkg}* | Remove-AppxPackage"
            subprocess.run([
                "powershell.exe",
                "-NoProfile",
                "-ExecutionPolicy", "Bypass",
                "-Command", cmd
            ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    stdscr.addstr("\nГотово. Нажмите любую клавишу...\n")
    stdscr.getch()

def main(stdscr):
    curses.curs_set(0)
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_CYAN)  # выделение
    curses.init_pair(2, curses.COLOR_MAGENTA, curses.COLOR_BLACK)  # заголовок
    curses.init_pair(3, curses.COLOR_YELLOW, curses.COLOR_BLACK)  # описание
    current_row = 0

    while True:
        draw_menu(stdscr, current_row)
        key = stdscr.getch()

        if key == curses.KEY_UP and current_row > 0:
            current_row -= 1
        elif key == curses.KEY_DOWN and current_row < len(app_names) - 1:
            current_row += 1
        elif key == ord(" "):
            selected[current_row] = not selected[current_row]
        elif key == ord("a"):
            selected[:] = [True] * len(app_names)
        elif key == ord("d"):
            selected[:] = [False] * len(app_names)
        elif key == 10:  # Enter
            remove_selected(stdscr)
        elif key == ord("q"):
            break

if __name__ == "__main__":
    curses.wrapper(main)
