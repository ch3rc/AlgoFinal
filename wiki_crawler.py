"""
Author:         Cody Hawkins
Date:           12/1/2020
Class:          5130
File:           wiki_crawler.py
Desc:           With provided start word crawl through wikipedia.org
                to find destination search word. The parent nodes and
                child nodes will be added to a graph and displayed at
                the end of the run.
"""
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.chrome.options import Options
from display_nodes import Graph
from search import file_search
from time import sleep
import getopt
import sys


class Crawler:

    def __init__(self, chrome_path, start, find, graph):
        # Make chrome driver headless so that chrome does not pop up while searching
        options = Options()
        options.add_argument("--headless")
        self.driver = webdriver.Chrome(chrome_path, options=options)
        self.start = start
        self.find = find
        self.graph = graph
        self.urls = []

    def start_crawl(self):
        # go to wikipedia and then search for starting word
        self.driver.get("http://www.wikipedia.org")
        search_bar = self.driver.find_element_by_id("searchInput")
        search_bar.clear()
        search_bar.send_keys(self.start)
        search_bar.send_keys(Keys.RETURN)

        # get title for starting search word
        title = self.driver.find_element_by_id("firstHeading").text
        # get body content of search word so that we only get relevant links
        body = self.driver.find_elements_by_id("mw-content-text")

        self.urls = []
        # get all hyperlinks and set start word as the parent node
        for element in body:
            tags = element.find_elements_by_tag_name("a")
            for tag in tags[:25]:
                try:
                    url_actual = tag.get_attribute("href")
                    if url_actual is None or "CS1" in url_actual or "File" in url_actual or "Help" \
                            in url_actual or "#" in url_actual or "en.wikipedia.org" not in url_actual:
                        continue
                    else:
                        if url_actual not in self.urls:
                            self.urls.append({'Parent': title, 'url': url_actual, 'depth': 1})
                        else:
                            continue
                except Exception as err:
                    print(f"Error has occurred with URL: {url_actual} : {err}")

    def DFS(self):
        visited = []
        # may need to adjust links visited for certain searches
        while len(self.urls) != 0 and len(visited) < 1000:
            new_url = self.urls.pop(0)
            # Search through each link in self.urls and then append new links at each new link if not visited
            if new_url['url'] not in (visited_links['url'] for visited_links in visited):
                visited.append(new_url)

                if new_url['depth'] < 6:
                    new_links = self.find_links(new_url, visited)
                    if len(new_links) != 0:
                        self.urls.extend(new_links)
                    else:
                        # Once the keyword is found then we exit the loop and close chrome
                        self.driver.close()
                        break
        print(f"Total links visited -------{len(visited)}------")

    def find_links(self, new_url, visited):
        try:
            # leaving this here so that you can see each link traversed
            print(f"Parent {new_url['Parent']} URL: {new_url['url']} depth {new_url['depth']} visited {len(visited)} links")
            self.driver.implicitly_wait(5)
            sleep(1)
            self.driver.get(new_url['url'])
            output = []
            # get title of current link and add to graph
            title = self.driver.find_element_by_id("firstHeading").text
            self.graph.add_edges(new_url['Parent'], title)

            # if title is found then return an empty list for exit condition
            if title == self.find:
                print(f"{self.find} found at {new_url['url']} at depth {new_url['depth']}")
                return output

            main_content = self.driver.find_elements_by_id("mw-content-text")
            # find links of new node
            for content in main_content:
                tags = content.find_elements_by_tag_name("a")
                for tag in tags[:25]:
                    link = tag.get_attribute("href")
                    if link is None or "#" in link or "File" in link or "Help" in link or \
                            "CS1" in link or "en.wikipedia.org" not in link:
                        continue
                    else:
                        if link not in output:
                            output.append({'Parent': title, 'url': link, 'depth': new_url['depth'] + 1})
                        else:
                            continue
        except StaleElementReferenceException as err:
            print(f"Error has occurred in find_links: {err}")
            self.driver.close()
            sys.exit(1)

        return output


def help():
    print("----HELP----\n")
    print("To run provide the computer drive your chromedriver.exe is in, e.g C or D")
    print("Provide a single word to start searching from")
    print("Provide a single word to search for that is related to the starting search word")


def capitalize(word):
    # capitalize beginning letter and remove trailing white space
    begin = word[:1]
    end = word[1:]

    if end[-1:] == " ":
        i = len(end) - 1
        end = end[:i]

    if begin.isupper():
        return begin + end
    elif begin.islower():
        return begin.upper() + end


def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "h", ["help"])
    except getopt.GetoptError as err:
        print(err)
        sys.exit(1)

    for o, a in opts:
        if o in ("-h", "--help"):
            help()
            sys.exit(1)
        else:
            assert False, "Unhandled Option!"

    if len(args) < 3:
        print("Not enough arguments")
        help()
    elif len(args) > 3:
        print("Too many arguments")
        help()
    else:
        comp_drive = args[0]
        start_word = args[1]
        word_to_find = args[2]
        chrome = "chromedriver.exe"

    start_word = capitalize(start_word)
    word_to_find = capitalize(word_to_find)
    PATH = file_search(chrome, comp_drive)

    try:
        G = Graph(start_word, word_to_find)
        crawl = Crawler(PATH, start_word, word_to_find, G)
        crawl.start_crawl()
        crawl.DFS()
        G.show_graph()
    except Exception as err:
        print(f"Error has occurred {err}")
        sys.exit(1)

    print("Program finished")
    sys.exit(0)


if __name__ == '__main__':
    main()

