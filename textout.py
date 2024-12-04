from colorama import Fore

def move(x, y):
    print("\033[%d;%dH" % (y, x), end="")

def printPos(x, y, text_to_print):   #Function that let us print in desired Position
    move(x, y)
    print(text_to_print)

def clearScreen():
    print('\x1b[2J')

# 현재 버전 수정사항
# 스마트 스토어 엑셀 다운로드 기능 추가

def print_logo(PROGRAM_TITLE, VERSION):
    print(Fore.GREEN)
    move(1, 2)
    print('┌───────────────────────────────────────────────┐')
    print('│                                               │')
    print("│                                               │")
    print('└───────────────────────────────────────────────┘')
    print(Fore.RESET)
    printPos(5, 3, PROGRAM_TITLE)
    print(Fore.RESET)
    printPos(5, 4, f'Version - {VERSION}')
    move(1, 6)