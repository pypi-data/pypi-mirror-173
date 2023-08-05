from transformers import pipeline

class Summarize:

    def __init__(self):
        self.MODELNAME = "facebook/bart-large-cnn"
        self.summarizer = pipeline("summarization", model=self.MODELNAME)

    def setText(self, text):
        self.text = text

    def getSummarizedText(self):
        return self.summarizer(self.text)[0]['summary_text']
