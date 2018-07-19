# Главный модуль для работы
import re
import urllib.request
import urllib.error
import textwrap
import os
from . import templates


class htmlToText:
    def __init__(self):
        # Инициализируем шаблоны поиска
        self.htmlH1 = re.compile(r'(<h1.*?>)(.*?)(</h1>)', re.DOTALL)
        self.htmlP = re.compile(r'(<p.*?>)(.*?)(</p>)', re.DOTALL)
        self.links_start = re.compile(r'<a.*?href="', re.DOTALL)
        self.links_end = re.compile(r'".*?>', re.DOTALL)
        self.script_tag = re.compile(r'<script.*?>.*?</script>', re.DOTALL)
        self.tags = re.compile(r'<.*?>', re.DOTALL)
        self.lentaru_article = re.compile(r'(https://lenta.ru/)(.*)')
        self.stackoverflow_questions = re.compile(r'(https://stackoverflow.com/questions)(.*)')

    @staticmethod
    def create_settings_file():  # Создаём файл с настройками
        if not os.path.exists('Settings.ini'):
            settings = {'LineWidth': 80,
                        'TextWrap': 1,
                        'ViewInConsole': 0,
                        'Method': 0}
            f = open('Settings.ini', 'w', encoding='utf-8')
            f.write('# LineWidth - Ширина строки (по умолчанию 80)\n'
                    '# TextWrap - Вкл/Выкл перенос текста (по умолчанию 1)\n'
                    '# ViewInConsole - Вкл/Выкл отображение текста сайта в консоли (по умолчанию 0)\n'
                    '# Metod - шаблон редактирования текста (по умолчанию 0; доступные 0, 1)\n'
                    '# 0 - стандартный (оформление ссылок в [ ], чистка "мусора")\n'
                    '# 1 - эксперементальный (попытка обработать весь видимый текст сайта),\n'
                    '# менее читабельно, рекомендуется выключить перенос текста\n\n')
            f.write('[Settings]\n')
            for i in settings:
                f.write(i + ': ' + str(settings[i]) + '\n')
            f.close()

    def check_url(self, url):  # Проверка введенного URL для применения шаблонов
        try:
            if self.stackoverflow_questions.search(url).group(2):
                print('stackoverflow.com questions topic detected')
                return 'stackoverflow'
        except AttributeError:
            pass
        try:
            if self.lentaru_article.search(url).group(2):
                print('lenta.ru article topic detected')
                return 'lentaru'
        except AttributeError:
            pass

    def create_path(self, url):  # Создание путей
        pathtml = urllib.request.url2pathname(url)  # Чтение пути URL
        cwd = os.getcwd()  # Запомнинаем путь где на данный момент лежит программа
        pathtml = re.sub(r'.*?:\\', '',
                         pathtml)  # Чистим URL путь от начальной ненужной информации (S:\\ or P:\\)
        pathtml = re.sub(r'[?&]', '/', pathtml)  # Заменяем "?" и "&" для максимально корректого создания пути
        pathtml = re.sub(r'[:*"<>|]', '', pathtml)  # Чистим от недопустимых символов для создания путей
        self.fullname = os.path.join(cwd, pathtml)  # Создаём полный готовый путь
        if not os.path.exists(self.fullname):
            os.makedirs(self.fullname)

    def create_complete_file(self, url):  # Главный механизм
        try:
            opend_url = urllib.request.urlopen(url)
            check = self.check_url(url)
            if check == 'lentaru':
                self.create_path(url)
                self.htmlSource = opend_url.read().decode('utf-8')
                self.htmlSource = templates.lenta(self.htmlSource)
                open(os.path.join(self.fullname, 'index.txt'), 'w', encoding='utf-8').write(self.htmlSource)
                self.base_text_format()
                self.wrap_text()
                self.view_in_console()
                print('Save in file (' + os.path.join(self.fullname, 'index.txt') + ') complete...')
            elif check == 'stackoverflow':
                self.create_path(url)
                self.htmlSource = opend_url.read().decode('utf-8')
                self.htmlSource = templates.stackoverflow(self.htmlSource)
                open(os.path.join(self.fullname, 'index.txt'), 'w', encoding='utf-8').write(self.htmlSource)
                # self.wrap_text()
                self.view_in_console()
                print('Save in file (' + os.path.join(self.fullname, 'index.txt') + ') complete...')
            else:
                self.create_path(url)
                self.htmlSource = opend_url.read().decode('utf-8')
                if self.to_plain_text() == 0:  # Запуск работы "универсального" алгоритма
                    self.wrap_text()  # Перенос текста
                    self.view_in_console()  # Вывод консоли
        except UnicodeDecodeError:  # Если не можем декодировать страницу
            print('Unsupported site, enter another URL (cant decode)')
        except ValueError:  # При неправильном вводе URL
            print('Incorrect URL')

    def standart_method(self):
        # Стандартный метод обработки
        plainText = open(os.path.join(self.fullname, 'index.txt'), 'w', encoding='utf-8')
        for i in self.h1:  # Записываем найденные заголовки
            plainText.write(i[1] + '\n')
        for i in self.pTag:  # Записываем найденный текст
            plainText.write(i[1] + '\n')
        plainText.close()
        print('Save in file (' + os.path.join(self.fullname, 'index.txt') + ') complete...')
        self.base_text_format()  # Чистка от остатков

    def experemental_method(self):
        # Эксперементальный метод поиска
        plainText = open(os.path.join(self.fullname, 'index.txt'), 'w', encoding='utf-8')
        self.htmlSource = re.sub(self.script_tag, '',
                                 self.htmlSource)  # Поиск и удаление всех тегов <script> и его содержимого
        self.htmlSource = re.sub(self.links_start, '[', self.htmlSource)  # Оформление ссылок
        self.htmlSource = re.sub(self.links_end, ']', self.htmlSource)  # Оформление ссылок
        self.htmlSource = re.sub(r'<.*?]', '',
                                 self.htmlSource)  # Поиск и удаление пострадавших от форматирования тегов '<...]'
        self.htmlSource = re.sub(r'\&.*?;', '', self.htmlSource)  # Поиск и удаление специальных кодов '&...;'
        self.htmlSource = re.sub(r'\r', '', self.htmlSource)  # Поиск и удаление \r
        self.htmlSource = re.sub(self.tags, '', self.htmlSource)  # Поиск и удаление всех тегов '<...>'
        self.htmlSource = re.sub(r'\[{{.*?}}\]', '', self.htmlSource)  # Поиск и удаление \
        self.htmlSource = re.sub(r'{{.*?}}', '', self.htmlSource)  # от прочих \
        self.htmlSource = re.sub(r'\[java.*?\]', '', self.htmlSource)  # остатков тега '<script>'
        plainText.write(self.htmlSource)
        plainText.close()
        print('Save in file (' + os.path.join(self.fullname, 'index.txt') + ') complete...')

    def to_plain_text(self):
        # Применение функций форматирования текста в зависимости от выбранного шаблона
        if self.selected_method() == 1:
            self.experemental_method()
            return 0
        if self.selected_method() == 0:
            self.h1 = self.htmlH1.findall(self.htmlSource)
            self.pTag = self.htmlP.findall(self.htmlSource)
            if not self.pTag or not self.h1:
                print('Cant recognize text, enter another URL or try with experemental method')
                return 1
            else:
                self.standart_method()
                return 0

    def base_text_format(self):
        # Базовое форматирование текста
        f = open(os.path.join(self.fullname, 'index.txt'), 'r', encoding='utf-8').read()
        f = re.sub(self.script_tag, '', f)
        f = self.format_links(f)
        f = re.sub('<.*?]', '', f)
        f = f.replace(' ]', '')
        f = f.replace('&nbsp;', ' ')
        f = re.sub(r'\&.*?;', '', f)
        f = re.sub(self.tags, '', f)
        f = re.sub(r'{{.*?}}', '', f)
        open(os.path.join(self.fullname, 'index.txt'), 'w', encoding='utf-8').write(f)

    def format_links(self, text_of_file):
        # Функция оформления ссылок
        text_of_file = re.sub(self.links_start, '[', text_of_file)
        text_of_file = re.sub(self.links_end, ']', text_of_file)
        return text_of_file

    def wrap_text(self):
        # Переноса текста
        f = open(os.path.join(self.fullname, 'index.txt'), 'r', encoding='utf-8').read()
        if self.wrap_text_on_off() == 1:  # Если Вкл. в настройках, то переносим
            f = textwrap.wrap(f, width=self.wrap_text_width(),
                              replace_whitespace=False)  # Ширина строки задаётся в настройках
            comlete_file = open(os.path.join(self.fullname, 'index.txt'), 'w', encoding='utf-8')
            for i in f:
                comlete_file.write('\n' + i)
            comlete_file.close()

    def view_in_console(self):
        # Отображение текста в консоли если Вкл. в настройках
        if self.value_for_console() == 1:
            print(open(os.path.join(self.fullname, 'index.txt'), encoding='utf-8').read())

    def last_path_file(self):
        # Возвращаем путь последнего записанного URL
        return os.chdir(self.fullname)

    # Методы считывания и возращения значений из настроек
    @staticmethod
    def value_for_console():
        settings_values = open('Settings.ini').read()
        value_search = re.compile(r'(viewinconsole: )(\d)', re.I)
        value = value_search.search(settings_values)
        return int(value.group(2))

    @staticmethod
    def wrap_text_on_off():
        settings_values = open('Settings.ini').read()
        value_search = re.compile(r'(textwrap: )(\d)', re.I)
        value = value_search.search(settings_values)
        return int(value.group(2))

    @staticmethod
    def wrap_text_width():
        settings_values = open('Settings.ini').read()
        value_search = re.compile(r'(linewidth: )(.*)', re.I)
        value = value_search.search(settings_values)
        return int(value.group(2))

    @staticmethod
    def selected_method():
        settings_values = open('Settings.ini').read()
        value_search = re.compile(r'(Method: )(.*)', re.I)
        value = value_search.search(settings_values)
        return int(value.group(2))
