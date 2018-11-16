from gensim.summarization import summarize

def text_summarize(text):
    return summarize(text, word_count=100)
