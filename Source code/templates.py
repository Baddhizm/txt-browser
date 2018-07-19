import re


# import urllib.request


def lenta(text):
    h1 = re.compile(r'(<h1 class="b-topic__title".*?>)(.*?)(</h1)')
    article = re.compile(r'(<p>)(.*?)(</p>)')
    complete_text = []
    for i in article.findall(text):
        complete_text.append(i[1])
    return h1.search(text).group(2) + '\n\n' + ''.join(complete_text)


def stackoverflow(text):
    h1 = re.compile(r'(<.*?class="question-hyperlink">)(.*?)(</a>)', re.DOTALL)
    question = re.compile(r'(<div class="question".*?>)(.*?)(<div class="post-taglist">)', re.DOTALL)
    question_2 = re.compile(r'(<p>)(.*?)(</div>)', re.DOTALL)
    answer = re.compile(r'(<td class="answercell">)(.*?)(<table class="fw">)', re.DOTALL)
    answer_text = answer.search(text).group(2)
    answer_text = for_stackoverflow(answer_text)
    question_text = question.search(text).group(2)
    question_text = question_2.search(question_text).group(2)
    question_text = for_stackoverflow(question_text)
    complete_text = '=====QUESTION:=====\n' + question_text + '\n=====ANSWER:=====\n' + answer_text
    return format_links_for_stackoverflow(complete_text)


def for_stackoverflow(question_text):
    question_text = re.sub(r'<div.*?>', '', question_text)
    question_text = re.sub(r'(<strong>)', '', question_text)
    question_text = re.sub(r'</strong>', '', question_text)
    question_text = re.sub(r'<br>', '', question_text)
    question_text = re.sub(r'</br>', '', question_text)
    question_text = re.sub(r'<p>', '', question_text)
    question_text = re.sub(r'</p>', '', question_text)
    question_text = re.sub(r'<pre>', '', question_text)
    question_text = re.sub(r'</pre>', '', question_text)
    question_text = re.sub(r'</blockquote>', '', question_text)
    question_text = re.sub(r'\&.*?;', '', question_text)
    question_text = re.sub(r'</a>', '', question_text)
    question_text = re.sub(r'<ul>', '', question_text)
    question_text = re.sub(r'</ul>', '', question_text)
    question_text = re.sub(r'<li>', '', question_text)
    question_text = re.sub(r'</li>', '', question_text)
    question_text = re.sub(r'<hr>', '', question_text)
    question_text = re.sub(r'</hr>', '', question_text)
    question_text = question_text.replace('<code>', '\n<code>\n')
    question_text = question_text.replace('</code>', '\n\n</code>\n')
    question_text = question_text.replace('\n\n', '')
    return question_text


def format_links_for_stackoverflow(text_of_file):
    text_of_file = re.sub(r'<a.*?href="', '[', text_of_file)
    text_of_file = re.sub(r'">', ']', text_of_file)
    return text_of_file

# url = urllib.request.urlopen('https://stackoverflow.com/questions/236129/split-a-string-in-c').read().decode('utf-8')
# print(stackoverflow(url))
