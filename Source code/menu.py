import os


# Менюшка
def menu(dehtml_exemplar):
    settings_path = os.getcwd()  # Запоминаем текущий рабочий путь, дабы без проблем открыть файл с настройками
    os.chdir(settings_path)
    while True:
        os.system('cls')
        print('=' * 25)
        print('1. Save URL\'s text in file')
        print('2. Open last file')
        print('3. Open settings')
        print('4. Exit')
        print('=' * 25)
        cho = input()
        if cho == '1':
            os.chdir(settings_path)
            os.system('cls')
            print('=' * 25)
            print('Enter full URL (http(s)://...):')
            print('=' * 25)
            url = input()
            dehtml_exemplar.create_complete_file(url)
            os.system('pause')
        elif cho == '2':
            try:
                dehtml_exemplar.last_path_file()
                print('Close file to continue')
                os.system('index.txt')
            except:
                print('Enter URL first')
                os.system('pause')
        elif cho == '3':
            os.chdir(settings_path)
            print('Close file to continue')
            os.system('Settings.ini')
        elif cho == '4':
            break
        else:
            os.system('cls')
