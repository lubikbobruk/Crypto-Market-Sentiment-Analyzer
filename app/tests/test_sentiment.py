import pandas as pd
from app.src.utils import classify_sentiment, compute_sentiment, get_analyzer
from app.src.sentiment import analyze_sentiment

def test_classify_sentiment():
    assert classify_sentiment(0.5) == "positive"
    assert classify_sentiment(-0.5) == "negative"
    assert classify_sentiment(0.0) == "neutral"
    assert classify_sentiment(0.049) == "neutral"
    assert classify_sentiment(-0.049) == "neutral"

def test_analyzer_lexicon():
    # ---------------
    # Lexicon check
    # ---------------

    analyzer = get_analyzer()

    # Neutral check
    assert analyzer.lexicon["ecosystem"] == 0.0
    assert analyzer.lexicon["community"] == 0.0
    assert analyzer.lexicon["transaction"] == 0.0

    # Negative check
    assert analyzer.lexicon["rugpull"] == -4.0
    assert analyzer.lexicon["scam"] == -3.5
    assert analyzer.lexicon["ponzi"] == -4.0

    # Positive check
    analyzer = get_analyzer()
    assert analyzer.lexicon["bullish"] == 2.8
    assert analyzer.lexicon["growth"] == 1.3
    assert analyzer.lexicon["strength"] == 1.5
  
    # Emoji check
    assert analyzer.lexicon["🚀"] == 3.0
    assert analyzer.lexicon["📈"] == 1.5
    assert analyzer.lexicon["🏛️"] == 0.0
    assert analyzer.lexicon["🐻"] == -2.0
    assert analyzer.lexicon["😭"] == -2.3

def test_compute_sentiment():

    # --------------
    # Context check
    # --------------

    # Neutral check
    assert abs(compute_sentiment("The blockchain processes transactions.")) < 0.05
    assert abs(compute_sentiment("Bitcoin is a digital asset.")) < 0.05
    assert abs(compute_sentiment("The price of XRP is 0.53 USD.")) < 0.05
    assert abs(compute_sentiment("I don't know anything about crypto."))  < 0.05
    assert abs(compute_sentiment("just text")) < 0.05

    # Negative check
    assert compute_sentiment("I hate bitcoin") < 0
    assert compute_sentiment("I doubt if to invest in crypro anymore.") < 0
    assert compute_sentiment("We have been manipulate by Elon Musk, it's a scam.") < 0
    assert compute_sentiment("This project is absolute garbage!") < 0
    assert compute_sentiment("The devs messed up everything terrible update.") < 0
    assert compute_sentiment("Worst experience ever with this token.") < 0
    assert compute_sentiment("BTC 😢") < 0

    # Positive check
    assert compute_sentiment("LOL this chart looks hilarious 😂") > 0
    assert compute_sentiment("ROFL the dip was insane but funny 😂😂") > 0
    assert compute_sentiment("LMAO crypto never stops surprising me") > 0
    assert compute_sentiment("I love DOGE, it is amazing!") > 0
    assert compute_sentiment("My portfolio have recently blew up with profit.") > 0
    assert compute_sentiment("S&P500 just has reached new ath!!!") > 0
    assert compute_sentiment("ETH is going to the moon 🚀🚀") > 0
    assert compute_sentiment("Feeling happy about the market 😀") > 0