Colors = {
    'GREEN' : '\033[32m',
    'RED': '\033[31m',
    'YELLOW': '\033[33m',
    'ENDC' : '\033[0m'
}

def print_colored_title(text, color, rest = ''):
    color = color.upper()
    text = text.split(' ')
    text[0] = Colors[color] + text[0] + Colors['ENDC']
    text = ' '.join(text)
    print(text, rest)