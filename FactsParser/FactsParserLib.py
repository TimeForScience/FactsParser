import requests, re
from bs4 import BeautifulSoup as bs

def clear(facts):
    """Clean up the facts"""
    pure_facts = []
    for fact in facts:
        pure_facts += [fact[0].upper()+fact[1:-1].replace(word, "")+fact[-1:].replace(fact[-1:], '.') for word in words_for_clean]
    return pure_facts

def check(facts_for_check):
    """Check fact or superfluous"""
    new_facts = []
    for fact in facts_for_check:
        if len(fact) > 100 and not any([False if word not in fact.lower() else True for word in stop_words]):
            new_facts += [fact]
    return new_facts

def sites_parser(request):
    """Get links to sites from google"""
    urls = []
    r = requests.get(
        f"https://www.google.com/search?q=Facts+about+{request.replace(' ', '+')}"
    )
    html_code = r.text
    while '<a href="/url?q=' in html_code:
        html_code = html_code[html_code.index('<a href="/url?q=') + 16 :]
        urls += [html_code[: html_code.index("&amp;")]]
        html_code = html_code[html_code.index("&amp;") :]
    return urls[:-2]

def facts_parser(site):
    """Parsing facts from links"""
    r = requests.get(site).text
    soup = bs(r, 'html.parser')
    raw_facts = check(re.split(split_by, soup.get_text()))
    return raw_facts

def get_facts(sites, number_of_facts):
    facts = []
    for i in enumerate(sites):
        facts += facts_parser(sites[i[0]])
        if len(facts) > number_of_facts:
            break
    return facts[:number_of_facts]

split_by = "1.|2.|3.|4.|5.|6.|7.|8.|9.|  |\n\n\n|<li>|</li>"
stop_words = ("blow", "mind", "fact", "youtube", "answer", "product", 'sign up', 'log in', 'support', '&', 'home', 'cookie', 'news', 'post', 'tag', 'thank', 'categories', 'try again')