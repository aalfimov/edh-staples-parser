import requests
from html.parser import HTMLParser


# Competitive edh staple statistics

list_of_decks = []
parsed_staple_dictionary = {}
pages_to_grabe = 2
file_to_save = 'parsed_data.txt'


class MyDeckHTMLParser(HTMLParser):
    def error(self, message):
        pass

    def handle_data(self, data):
        global parsed_staple_dictionary
        if data == 'Flip' or data == '\n     ' or data == '\\n    \xa0':
            pass
        elif parsed_staple_dictionary.get(data):
            key = parsed_staple_dictionary.get(data)
            parsed_staple_dictionary.update({data: key + 1})
        else:
            parsed_staple_dictionary.update({data: 1})


class MySearchDeckHTMLParser(HTMLParser):
    def error(self, message):
        pass

    def handle_starttag(self, tag, attrs):
        global list_of_decks
        if attrs[0][0] == 'href' and attrs[0][1] != '/mtg-decks/search/':
            list_of_decks.append("https://tappedout.net" + attrs[0][1])


def tappedout_deck_parser(url_to_parse):
    index_start = 0
    deck_req = requests.get(url_to_parse)
    html = str(deck_req.content)
    parser = MyDeckHTMLParser()
    for iterator in range(100):
        index_start = html.find('<span class="card', index_start)
        index_finish = html.find('</span>', index_start)
        parser.feed(html[index_start:index_finish])
        index_start = index_finish


def tappedout_cedh_deck_searcher(url_searcher) -> object:
    index_start = 0
    list_of_deck_req = requests.get(url_searcher)
    html = str(list_of_deck_req.content)
    parser = MySearchDeckHTMLParser()
    for iterator in range(20):
        index_start = html.find('<a href="/mtg-decks/', index_start)
        index_finish = html.find('</a>', index_start)
        parser.feed(html[index_start:index_finish])
        index_start = index_finish


# main program
print("Собираю ссылки...")

for i in range(pages_to_grabe):
    url_to_search_deck = f'https://tappedout.net/mtg-decks/search/?q=&format=edh&cards=mana-crypt&hubs=competitive' \
                         f'&price_min=&price_max=&o=-date_updated&submit=Filter+results&p={i + 1}&page={i + 1} '
    tappedout_cedh_deck_searcher(url_to_search_deck)

print("Нашел", len(list_of_decks), "колод")
for link_index in range(len(list_of_decks)):
    tappedout_deck_parser(list_of_decks[link_index])
    print(link_index + 1, "deck done")

print("Сортирую результат")
sorted_tuples = sorted(parsed_staple_dictionary.items(), key=lambda item: item[1])
parsed_staple_dictionary = {k: v for k, v in sorted_tuples[::-1]}

print(f"Сохраняю результат в {file_to_save}")
f = open(file_to_save, 'a')
for card in parsed_staple_dictionary:
    f.writelines(f"{card} - {parsed_staple_dictionary[card]}\n")
f.writelines(f"{list_of_decks}\n")
f.close()
print("Готово")
print(f'parsed_staple_dictionary - {parsed_staple_dictionary}')
