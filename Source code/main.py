from . import dehtml
from . import menu

if __name__ == '__main__':
    plainText = dehtml.htmlToText()
    plainText.create_settings_file()
    menu.menu(plainText)
