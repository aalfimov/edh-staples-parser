# Competitive edh staple statistics
from html.parser import HTMLParser
from config import *
import requests
import time


# import threading


class MyDeckHTMLParser(HTMLParser):
    def error(self, message):
        pass

    def handle_data(self, data):
        if data == 'Flip' or data == '\n     ' or data == '\\n    \xa0':
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
        if attrs[0][0] == 'href' and attrs[0][1] != '/mtg-decks/search/':
            list_of_decks.append("https://tappedout.net" + attrs[0][1])


def catch_url_from_tappedout():
    print("Catch urls...")
    for i in range(pages_to_grabe):
        url_to_search_deck = f'https://tappedout.net/mtg-decks/search/' \
                             f'?q=&format=edh&cards=mana-crypt&hubs=competitive' \
                             f'&price_min=&price_max=&o=-date_updated&submit=Filter+results&p={i + 1}&page={i + 1} '
        tappedout_cedh_deck_searcher(url_to_search_deck)
    print("Found ", len(list_of_decks), " decks")


def tappedout_decks_work():
    for link_index in range(len(list_of_decks)):
        tappedout_deck_parser(list_of_decks[link_index])
        print(link_index + 1, "deck done")


def tappedout_cedh_deck_searcher(url_searcher):
    index_start = 0
    list_of_deck_req = requests.get(url_searcher)
    html = str(list_of_deck_req.content)
    parser = MySearchDeckHTMLParser()
    # 20 deck urls on page
    for iterator in range(20):
        index_start = html.find('<a href="/mtg-decks/', index_start)
        index_finish = html.find('</a>', index_start)
        parser.feed(html[index_start:index_finish])
        index_start = index_finish


def tappedout_deck_parser(url_to_parse):
    index_start = 0
    deck_req = requests.get(url_to_parse)
    html = str(deck_req.content)
    parser = MyDeckHTMLParser()
    # 100 cards in edh deck
    for iterator in range(100):
        index_start = html.find('<span class="card', index_start)
        index_finish = html.find('</span>', index_start)
        parser.feed(html[index_start:index_finish])
        index_start = index_finish


def result_sorted():
    print("Sort the result")
    sorted_tuples = sorted(parsed_staple_dictionary.items(), key=lambda item: item[1])
    return {k: v for k, v in sorted_tuples[::-1]}


def save_file():
    print(f"Save the result in {file}")
    f = open(file, 'a')
    for card in parsed_staple_dictionary:
        f.writelines(f"{parsed_staple_dictionary[card]} {card}\n")
    f.writelines(f"{list_of_decks}\n")
    f.close()


# main program
if __name__ == '__main__':
    start = time.perf_counter()  # start timer
    catch_url_from_tappedout()
    tappedout_decks_work()
    result_sorted()
    save_file()

    print(f'parsed_staple_dictionary - {parsed_staple_dictionary}')
    finish = time.perf_counter()  # finish timer
    print(f"Finish in {round(finish - start, 2)} seconds")
