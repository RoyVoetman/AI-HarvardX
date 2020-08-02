import os
import random
import re
import sys
import math

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    print(corpus)
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
    model = {}

    allPages = list(corpus.keys())
    linkedPages = corpus[page]

    # if a page has no links, we can pretend it has links to all pages in the corpus, including itself.
    if len(linkedPages) == 0:
        Pall = 1 / len(allPages)

        for i in allPages:
            model[i] = Pall

        return model

    Prandom = (1 - damping_factor) / len(allPages)
    Plinked = damping_factor / len(linkedPages)

    # choose a link at random chosen from all pages in the corpus
    for i in allPages:
        model[i] = Prandom

    # choose a link at random linked to by `page`
    for i in linkedPages:
        model[i] = model[i] + Plinked

    return model
        

def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    normalisationCoefficient = 1 / n
    
    # initalize all page ranks to zeros
    pageRank = {}
    for page in list(corpus.keys()):
        pageRank[page] = 0

    # start on random page
    currentPage = random.choice(list(corpus.keys()))
    pageRank[currentPage] = pageRank[currentPage] + normalisationCoefficient

    # create markov chain
    for _ in range(n - 1):
        transitions = (transition_model(corpus, currentPage, damping_factor)).items()
        transitions = list(zip(*transitions))

        pages = transitions[0]
        weights = transitions[1]

        currentPage = random.choices(pages, weights=weights)[0]
        pageRank[currentPage] = pageRank[currentPage] + normalisationCoefficient

    return pageRank

def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    allPages = list(corpus.keys())
    n = len(allPages)

    normalisationCoefficient = 1 / n

    # initalize all page ranks to 1/n
    pageRank = {}
    for page in allPages:
        pageRank[page] = normalisationCoefficient

    # iteratively apply pagerank formula 
    hasConverged = False
    while not hasConverged:
        newPageRank = pageRank.copy()

        # calculate new pagerank voor all pages
        for page in allPages:
            sigma = 0
            for linkedPage in corpus[page]:
                numLinks = len(corpus[linkedPage])
                # A page that has no links at all should be interpreted 
                # as having one link for every page
                if numLinks == 0:
                    numLinks = len(allPages)
                
                sigma = sigma + pageRank[linkedPage] / numLinks

            newPageRank[page] = ((1 - damping_factor) / n) + damping_factor * sigma

        hasConverged = has_converged(pageRank, newPageRank, allPages)
        pageRank = newPageRank
        
    return pageRank

def has_converged(oldPageRank, newPageRank, allPages):
    for page in allPages:
        if math.floor(newPageRank[page] * 1000) != math.floor(oldPageRank[page] * 1000):
            return False

    return True

if __name__ == "__main__":
    main()
