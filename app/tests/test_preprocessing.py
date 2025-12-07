from app.src.utils import *
from app.src.text_preprocessing import soft_clean, hard_clean, combine_csv

# -------------------------
# Testing helper functions
# -------------------------

def test_remove_urls():
    assert remove_urls("Check this https://binance.com now") == "Check this  now"
    assert remove_urls("a http://somethin.com b https://test.org c") == "a  b  c"
    assert remove_urls("clean text") == "clean text"

def test_remove_mentions():
    assert remove_mentions("@elon XRP pumps") == " XRP pumps"
    assert remove_mentions("@a @b hello") == "  hello"
    assert remove_mentions("no usernames") == "no usernames"


def test_remove_markdown():
    assert remove_markdown("Click [here](https://binance.com)") == "Click "
    text = "[a](x) and [b](y)"
    assert remove_markdown(text) == " and "
    assert remove_markdown("nothing here") == "nothing here"

def test_remove_non_ascii():
    assert remove_non_ascii("Bullish 🚀🔥") == "Bullish "
    assert remove_non_ascii("abc123!") == "abc123!"
    assert remove_non_ascii("Holy Crêpes! BTC to the moon🚀") == "Holy Crpes! BTC to the moon"

def test_remove_punctuation():
    assert remove_punctuation("Hello!!!") == "Hello"
    assert remove_punctuation("no punctuation") == "no punctuation"
    assert remove_punctuation("XRP: to-the-moon!") == "XRP tothemoon"

def test_normalize_whitespace():
    assert normalize_whitespace("XRP    pumps   hard") == "XRP pumps hard"
    assert normalize_whitespace("A\n\nB\t\tC") == "A B C"
    assert normalize_whitespace("already normal") == "already normal"

# -------------------
# Testing Soft Clean
# -------------------

def test_soft_clean_remove_url():
    raw = "Check this now!!! https://binance.com"
    cleaned = soft_clean(raw)
    assert "http" not in cleaned
    assert "!!!" in cleaned
    assert cleaned == "Check this now!!!"

def test_soft_clean_mention():
    raw = "@elon XRP pumps!"
    cleaned = soft_clean(raw)
    assert "@elon" not in cleaned
    assert cleaned == "XRP pumps!"

def test_soft_clean_emojis():
    raw = "Bullish 🚀🚀"
    cleaned = soft_clean(raw)
    assert "🚀" in cleaned

# -------------------
# Testing Hard Clean
# -------------------

def test_hard_clean_lowercase_and_punctuation():
    raw = "XRP To The Moon!!!"
    cleaned = hard_clean(raw)
    assert cleaned == "xrp to the moon"

def test_hard_clean_ascii():
    raw = "Bullish 🚀🔥"
    cleaned = hard_clean(raw)
    assert cleaned == "bullish"

def test_hard_clean_markdown():
    raw = "Look at this [link](https://binance.com)"
    cleaned = hard_clean(raw)
    assert "[" not in cleaned
    assert "(" not in cleaned
    assert "link" in cleaned

def test_empty():
    assert soft_clean("") == ""
    assert hard_clean("") == ""
    assert soft_clean(None) == ""
    assert hard_clean(None) == ""

# --------------------
# Testing csv combine
# --------------------

def test_combine(tmp_path):
    pathes = [
        tmp_path / "csv_both.csv",
        tmp_path / "csv_text.csv",
        tmp_path / "csv_title.csv"
    ]

    df_both = pd.DataFrame({
        "title": ["title_test"],
        "text": ["text_test"]
    })

    df_only_text = df_both.copy().drop(columns=["title"])
    df_only_title = df_both.copy().drop(columns=["text"])

    dfs = [df_both, df_only_text, df_only_title]
    combined_csvs = []

    # save + load
    for path, df in zip(pathes, dfs):
        df.to_csv(path, index=False)
        combined_csvs.append(combine_csv(path))

    for i in range(0,3):
        assert "combined" in combined_csvs[i].columns

    assert combined_csvs[0]["combined"].iloc[0] == "title_test text_test"
    assert combined_csvs[1]["combined"].iloc[0] == "text_test"
    assert combined_csvs[2]["combined"].iloc[0] == "title_test"