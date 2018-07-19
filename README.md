# txt-browser

Для реализации действий использовались только встроенные модули

## Принцип работы:
- Создается файл с настройками Settings.ini (описание внутри)
- Задаём определенные регулярные выражения поиска типичных 
  тегов в которых обычно содержится основная информация страницы
- Делаем запрос на введённый URL, считываем код страницы
- Проверяем ссылку для применения готового шаблона форматирования, 
  если таковой имеется, если нет - применяем универсальный 
  выбранный (в настройках) алгоритм
- Записываем найденное в файл по "усложненному" пути 
  (http://lenta.ru/news/2013/03/dtp/index.html => [CUR_DIR]/lenta.ru/news/2013/03/dtp/index.txt)

### На каких ресурсах проверялось (в скобках проверенные примеры, результаты в папке Examples):
Статьи на:
  - http://76.ru/ - не получается декодировать
  - https://ria.ru/ - приемлемо - из-за того что сайт обнаруживает "блокировку рекламы", 
					  сбивается текст в начале и не чистится нормально от скриптов (https://ria.ru/culture/20170124/1486387950.html)
  - http://yarnovosti.com/ - читабельно
  - http://www.vesti.ru/ - читабельно (http://www.vesti.ru/doc.html?id=2846848&cid=7)
  - https://news.yandex.ru/ - только с помощью эксперементального метода (из-за того что текст находится в \<div\>)
   (https://news.yandex.ru/yandsearch?lr=16&cl4url=www.rbc.ru%2Fpolitics%2F24%2F01%2F2017%2F5887be219a794730e5caad11&lang=ru&rubric=index&from=index)
  - https://stackoverflow.com/questions/ - раздел с вопросами, написан шаблон, хорошая читабельность, выключен перенос из-за специфики контента
   (https://stackoverflow.com/questions/14265581/parse-split-a-string-in-c-using-string-delimiter-standard-c)
  - https://news.mail.ru/ - читабельно (https://news.mail.ru/politics/28540252/)
  - https://lenta.ru/ - читабельно, написан шаблон 
   (https://lenta.ru/articles/2017/01/23/smert_patriot/, https://lenta.ru/articles/2017/01/19/gotie/)
  

### Дальнейшее улучшение:
- Оптимизация/рефакторинг кода
- Добавлениея разных шаблонов популярных новостных сайтов
- Не все запросы поддаются декодингу в utf-8, можно исправить с помощью сторонней библиотеки Requests
- Так же можно имитировать запросы с определенного устройства, например Apple, дабы уменьшить количество изначального "мусора" на сайте

### Пример расширения функционала:
- Например при выводе в консоли статьи, внизу дополнительно выводить список найденных ссылок и 
  предлагать пользователю перейти на них.
- В главном меню пункт, в котором можно выбрать популярный новостной сайт, при выборе 
  открывает самую свежую новость => можно сделать сёрфинг по новостям (следующая новость, предыдущая новость)  