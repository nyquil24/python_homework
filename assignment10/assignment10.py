# get_books.py
# Requires: selenium, webdriver_manager, pandas, json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import json
import time
import os

# --- CONFIG ---
SEARCH_URL = "https://durhamcounty.bibliocommons.com/v2/search?query=learning%20spanish&searchType=smart"
OUTPUT_DIR = "assignment10"
CSV_OUT = os.path.join(OUTPUT_DIR, "get_books.csv")
JSON_OUT = os.path.join(OUTPUT_DIR, "get_books.json")
# polite wait between page loads / requests (increase if required by robots.txt)
POLITE_WAIT_SECONDS = 1.5

os.makedirs(OUTPUT_DIR, exist_ok=True)

def make_driver():
    # headful mode is useful for debugging; to run headless, add options.headless = True
    from selenium.webdriver.chrome.options import Options
    opts = Options()
    # opts.headless = True   # uncomment to run headless
    # set a descriptive user-agent string (helps identify your crawler; still obey robots.txt)
    opts.add_argument("user-agent=get_books_script/1.0 (+your_email@example.com)")
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=opts)
    return driver

def extract_from_result_li(li):
    """
    Given a selenium WebElement pointing at a candidate <li> for a search result,
    try to extract Title, Author(s) and Format-Year.
    We use try/except liberally because pages may have slightly different structure.
    """
    title_text = ""
    authors_text = ""
    format_year_text = ""

    # TITLE: try a few plausible selectors within the li
    for sel in [
        "h3 a",           # common: <h3><a>Title</a></h3>
        "h2 a",
        "a.title",        # sometimes anchor has class 'title'
        "a.card-title",   # site-specific guesses
        "a"               # fallback: first anchor
    ]:
        try:
            el = li.find_element(By.CSS_SELECTOR, sel)
            title_text = el.text.strip()
            if title_text:
                break
        except Exception:
            continue

    # AUTHOR(S): try to find author link(s) inside the li
    try:
        # many BiblioCommons results place author links in an element with class 'contributors' or similar
        author_links = li.find_elements(By.CSS_SELECTOR, "a[class*='author'], a[class*='contributor'], a[href*='/author/'], .contributors a, .byline a")
        if not author_links:
            # fallback: any anchor that looks like an author (short text, contains comma or capitalized names)
            candidate_anchors = li.find_elements(By.TAG_NAME, "a")
            author_texts = []
            for a in candidate_anchors:
                t = a.text.strip()
                if not t:
                    continue
                # heuristics: author names are short (no more than, say, 60 chars) and contain letters
                if len(t) < 80 and any(c.isalpha() for c in t):
                    # skip known unrelated anchors (like "Check out now on Hoopla")
                    if "hoopla" in t.lower() or "add" in t.lower() or "for later" in t.lower():
                        continue
                    author_texts.append(t)
            # take unique ones as authors
            if author_texts:
                # try to pick the first 1-3 likely authors
                authors_text = ";".join(dict.fromkeys(author_texts[:3]))
        else:
            authors_text = ";".join([a.text.strip() for a in author_links if a.text.strip()])
    except Exception:
        authors_text = ""

    # FORMAT & YEAR: often in a small metadata area; try to find spans or divs with keywords like 'eBook', comma, or a year
    try:
        # look for a span or div that contains 'eBook' or a 4-digit year
        meta_spans = li.find_elements(By.CSS_SELECTOR, "span, div")
        meta_texts = []
        for s in meta_spans:
            text = s.text.strip()
            if not text:
                continue
            # if it contains 'eBook' or 'Audiobook' or a 4-digit year, capture
            if ("ebook" in text.lower() or "audiobook" in text.lower() or
                any(tok.isdigit() and len(tok) == 4 for tok in text.split())):
                meta_texts.append(text)
        if meta_texts:
            # choose the shortest reasonable meta string that contains year/format
            format_year_text = meta_texts[0]
        else:
            # fallback: look for a small element with comma separators (e.g. "eBook , 2025")
            smalls = li.find_elements(By.CSS_SELECTOR, "small, .metadata, .format")
            for sm in smalls:
                t = sm.text.strip()
                if t:
                    format_year_text = t
                    break
    except Exception:
        format_year_text = ""

    return {"Title": title_text, "Author": authors_text, "Format-Year": format_year_text}

def main():
    driver = make_driver()
    wait = WebDriverWait(driver, 15)
    try:
        driver.get(SEARCH_URL)
        # Wait until some results text appears in the page. (This CSS/locator may vary; we wait for body to load.)
        wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        time.sleep(POLITE_WAIT_SECONDS)  # politeness

        # Find all <li> elements on the page and filter them to probable search results
        li_elements = driver.find_elements(By.TAG_NAME, "li")
        print(f"Found {len(li_elements)} li elements; filtering for likely results...")

        results = []
        for li in li_elements:
            try:
                # quick heuristics: consider li elements that contain an anchor and some text
                if not li.text or len(li.text) < 5:
                    continue
                # attempt to extract from li
                data = extract_from_result_li(li)
                # require at least a Title or Author to consider it a result
                if data["Title"] or data["Author"]:
                    # avoid blank duplicates
                    if data["Title"] or data["Format-Year"] or data["Author"]:
                        results.append(data)
            except Exception:
                continue

        # Deduplicate by Title while preserving order
        seen = set()
        deduped = []
        for r in results:
            key = r.get("Title", "") or r.get("Author", "")
            if key in seen:
                continue
            seen.add(key)
            deduped.append(r)

        df = pd.DataFrame(deduped)
        print(df.head(20))
        # Write CSV and JSON
        df.to_csv(CSV_OUT, index=False)
        with open(JSON_OUT, "w", encoding="utf-8") as f:
            json.dump(deduped, f, ensure_ascii=False, indent=2)

        print(f"Wrote {len(deduped)} records to {CSV_OUT} and {JSON_OUT}")

    finally:
        driver.quit()

if __name__ == "__main__":
    main()
