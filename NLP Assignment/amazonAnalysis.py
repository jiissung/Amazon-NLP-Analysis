from reviewScrapper import AmazonScraper
from textAnalyzer import Analyzer
from collections import Counter
import re

def get_reviews(url, analyzer, label, parser = None):
    """
    given url, analyzer being used, labels, and parser
    loads the reviews into the analyzer
    """
    scraper = AmazonScraper(url)
    reviews = scraper.extract_reviews()
    combined_reviews = "\n".join(reviews)
    analyzer.load_text(combined_reviews, label, parser)

def pre_processor(text, stop_words_list):
    """
    given text and stop_words_list
    returns cleaned text and removal of stop words
    """
    # Remove newlines, excessive spaces, and make text lowercase
    text = text.replace("\n", " ")
    text = re.sub(r'\s+', ' ', text)
    text = text.lower()

    # Split into words, remove punctuation, and clean
    all_words = text.split(" ")
    all_words = [word for word in all_words if word.strip() != '']
    for index, word in enumerate(all_words):
        all_words[index] = re.sub(r'[^\w\s]', '', word).strip()


    # Extract sentences for sentence length analysis
    filtered_words = stop_words(all_words, stop_words_list)

    sentences = re.split(r'[.!?]', text)
    sentences = [sentence.strip() for sentence in sentences if sentence.strip()]
    sentence_lengths = [len(sentence.split()) for sentence in sentences]
    avg_sentence_length = sum(sentence_lengths) / len(sentence_lengths) if sentence_lengths else 0

    return filtered_words, avg_sentence_length, sentences

def load_stop_words(stopfile):
    """
    given a text file of words
    returns list of unnecessary words
    """
    with open(stopfile, 'r', encoding='utf-8') as f:
        stop_words_list = [line.strip().lower() for line in f if line.strip()]
    return stop_words_list

def stop_words(all_words, stop_words_list):
    """
    given a list of words, removes the stop_words
    """
    return [word for word in all_words if word not in stop_words_list]

def custom_parser(filename):
    """
    created custom parser to allow for user inputted Parser testing
    """
    stopfile = 'nltkstopwords.txt'
    text = filename
    stop_words_list = load_stop_words(stopfile)
    filtered_words, avg_sentence_length, sentences = pre_processor(text, stop_words_list)
    sentiment = get_sentiment(filtered_words)
    results = {
        'wordcount': Counter(filtered_words),
        'number of words': len(filtered_words),
        'average sentence length': avg_sentence_length,
        'sentiment': sentiment,
    }
    return results

def get_sentiment(filtered_words):
    """
    given a list of words, returns sentiment
    """
    sentiment = 0
    for word in filtered_words:
        if word == "like":
            sentiment += 1
    return sentiment


def main():
    # the product urls being scraped
    urls = [
        "https://www.amazon.com/Photography-Autofocus-Anti-Shake-Vlogging-180%C2%B0Flip/dp/B0DH28GGNZ?crid=1TMTVL64UDZI8",
        "https://www.amazon.com/Gavonde-Digital-Photography-Vlogging-Batteries/dp/B0D3H36K64?crid=1TMTVL64UDZI8",
        "https://www.amazon.com/Canon-Rebel-T7-18-55mm-II/dp/B07C2Z21X5?crid=1TMTVL64UDZI8",
        "https://www.amazon.com/Photography-Auto-Focus-Vlogging-Anti-Shake-Batteries/dp/B0DBVZC1CX?crid=1TMTVL64UDZI8",
        "https://www.amazon.com/VJIANGER-Photography-Vlogging-Batteries-W02-UBlack2/dp/B09Z26CRBS?crid=1TMTVL64UDZI8",
        "https://www.amazon.com/Saneen-Photography-Vlogging-Interface-Beginner/dp/B0CYT3V8Z3?crid=1BV1LY7EH29W2&dib=eyJ2IjoiMSJ9.qbm7aCYINIHvMzDjLdkKQg1QL9weypUhCH_5y_kGyfO0TQHmYPKm_M8TM77aY6KombNlNGERJkZ0veW0IY8NoLq2PdYpBq06-vU-hb8avCtGjMX-n0HEbEGqLek_qbMijiWnEBI3nxTTi_YJKo6KdRqMLk7gDAYeaihtfxG4pVZQ0I5UypFm1nvdyf0Qu2cb93U1fL7rvS-WYet9lq-qtqEq7hoGtY5g7sZucPyOCN0.p25nCb3KZf0ZJDWjuW0L5Zp-k5M32wWg7KbJrvA80Uc&dib_tag=se&keywords=camera&qid=1732501043&sprefix=camera%2Caps%2C133&sr=8-11",
        "https://www.amazon.com/VJIANGER-Photography-Vlogging-Batteries-W02-UBlack2/dp/B09Z26CRBS?crid=1BV1LY7EH29W2&dib=eyJ2IjoiMSJ9.qbm7aCYINIHvMzDjLdkKQg1QL9weypUhCH_5y_kGyfO0TQHmYPKm_M8TM77aY6KombNlNGERJkZ0veW0IY8NoLq2PdYpBq06-vU-hb8avCtGjMX-n0HEbEGqLek_qbMijiWnEBI3nxTTi_YJKo6KdRqMLk7gDAYeaihtfxG4pVZQ0I5UypFm1nvdyf0Qu2cb93U1fL7rvS-WYet9lq-qtqEq7hoGtY5g7sZucPyOCN0.p25nCb3KZf0ZJDWjuW0L5Zp-k5M32wWg7KbJrvA80Uc&dib_tag=se&keywords=camera&qid=1732501043&sprefix=camera%2Caps%2C133&sr=8-15",
        "https://www.amazon.com/KODAK-PIXPRO-AZ405-BK-Digital-Optical/dp/B0BLLCJ963?crid=1BV1LY7EH29W2&dib=eyJ2IjoiMSJ9.qbm7aCYINIHvMzDjLdkKQg1QL9weypUhCH_5y_kGyfO0TQHmYPKm_M8TM77aY6KombNlNGERJkZ0veW0IY8NoLq2PdYpBq06-vU-hb8avCtGjMX-n0HEbEGqLek_qbMijiWnEBI3nxTTi_YJKo6KdRqMLk7gDAYeaihtfxG4pVZQ0I5UypFm1nvdyf0Qu2cb93U1fL7rvS-WYet9lq-qtqEq7hoGtY5g7sZucPyOCN0.p25nCb3KZf0ZJDWjuW0L5Zp-k5M32wWg7KbJrvA80Uc&dib_tag=se&keywords=camera&qid=1732501043&sprefix=camera%2Caps%2C133&sr=8-21&ufe=INHOUSE_INSTALLMENTS%3AUS_IHI_3M_HARDLINES_AUTOMATED",
        "https://www.amazon.com/Digital-Photography-Vlogging-YouTube-Beginner/dp/B0BQRVCGHC?crid=1BV1LY7EH29W2&dib=eyJ2IjoiMSJ9.MyffU3HezUjV_ThbcFlWFLtR2fkwxsb8nvKGTBrBsJ_GjHj071QN20LucGBJIEps.sRf1PiUfq4p0WQXxw5BzO4rrRtQLXrwyAx2b00-onN4&dib_tag=se&keywords=camera&qid=1732501127&sprefix=camera%2Caps%2C133&sr=8-20",
        "https://www.amazon.com/KODAK-PIXPRO-AZ405-BK-Digital-Optical/dp/B0BLLCJ963?crid=R437Y0O7U1BO&dib=eyJ2IjoiMSJ9.KfPVnWHrMGsUaR6BAKBntuYj2gvuHNTfRIYhNc9uAWNRuzNZkZtRYdqWEOSVJKYXQi3KFoZ1rvYxqa9Q0ySizkrVKw0CQPpFghXe6iUjtNnAOYFXCl3UHKWLg4ZmqcE8O18Kfoql3WpAlr3yv3OD9K56d6qH1c0fURVUEb02z2AYHkXHt2ASGH5WRLBkjXiE5aNsft8krlTecND5dPwkEO6L43A1vsivpF1iT35-hlg.jchll4CHLwWbOD4jX35z5o4ueLc9e2bWeP_FuZS5_ms&dib_tag=se&keywords=camera+for+photography&qid=1732505508&sprefix=camera+for%2Caps%2C146&sr=8-14&ufe=INHOUSE_INSTALLMENTS%3AUS_IHI_3M_HARDLINES_AUTOMATED"
        ]


    # creates the Analyzer and loads positive, negative, and stop words
    tt = Analyzer()
    tt.load_stop_words("nltkstopwords.txt")
    tt.load_negative_words("negative-words.txt")
    tt.load_positive_words("positive-words.txt")

    # loads all reviews
    for index, url in enumerate(urls):
        print(index, url)
        label = f"Product {index + 1}"
        get_reviews(url, tt, label)

    # creates the 3 visualizations for analysis
    tt.word_count_sankey()
    tt.sentiment_graph()
    tt.word_cloud_visualization(rows = 2, cols = 5)

main()