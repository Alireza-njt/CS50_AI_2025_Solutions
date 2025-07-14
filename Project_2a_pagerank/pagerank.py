# name : Alireza Nejati
# gmail address : alirezanejatiz27@gmail.com
# github ID : Alireza-njt
# last submit : Monday, July 7, 2025 5:14 PM +0330


import os
import random
import re
import sys

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    result = dict()
    pages_list = list(corpus.keys())
    linked_pages_list = list(corpus[page])

    for p in pages_list:
        result[p] = 0.000

    if not linked_pages_list:
        random_surfer = 1/len(corpus)
        for p in pages_list:
            result[p] = random_surfer
    else:
        random_surfer_1 = damping_factor/(len(linked_pages_list))
        random_surfer_2 = (1-damping_factor)/len(corpus)
        for p in pages_list:
            result[p] += random_surfer_2
            if p in linked_pages_list:
                result[p] += random_surfer_1

    return result


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """

    result = dict()
    pages_list = list(corpus.keys())

    random_number = random.randint(0, len(pages_list) - 1)
    current_page = pages_list[random_number]

    for p in pages_list:
        result[p] = 0.000

    result[current_page] += 1

    for _ in range(n-1):
        t_model_for_current_page = transition_model(corpus, current_page, damping_factor)
        t_model_values = t_model_for_current_page.values()
        next_page = random.choices(list(t_model_for_current_page),
                                   weights=t_model_values, k=1).pop()
        result[next_page] += 1
        current_page = next_page

    for p in pages_list:
        result[p] /= n

    return result


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    result = dict()
    pages_list = list(corpus.keys())

    for p in pages_list:
        result[p] = 1/len(pages_list)

    new_result = result.copy()

    LOOP_SW = True

    while LOOP_SW:
        for page in corpus:
            sigma = 0.000
            for page2 in corpus:
                if corpus[page2]:
                    if page in corpus[page2]:
                        sigma += result[page2] / len(corpus[page2])
                else:
                    sigma += result[page2] / len(pages_list)
            new_result[page] = (1-damping_factor) / len(pages_list) + sigma * damping_factor

        if all(abs(new_result[page] - result[page]) < 0.001 for page in result):
            LOOP_SW = False

        result = new_result.copy()

    return result


if __name__ == "__main__":
    main()
