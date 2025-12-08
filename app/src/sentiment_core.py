"""
Initializer of the VADER sentiment analyzer.
"""
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from app.src.lexicon.loader import get_all_lexicons

def _create_analyzer():
    """Creates VADER analyzer with integrated custom lexicons."""
    analyzer = SentimentIntensityAnalyzer()

    custom_lexicon = get_all_lexicons()
    analyzer.lexicon.update(custom_lexicon)

    return analyzer

# Global init
ANALYZER = _create_analyzer()

def get_analyzer():
    return ANALYZER
