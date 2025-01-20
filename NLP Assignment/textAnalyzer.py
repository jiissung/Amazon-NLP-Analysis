from collections import defaultdict, Counter
from pdfminer.high_level import extract_text
from textException import AnalyzerException
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import os
import re
from wordcloud import WordCloud


class Analyzer:

    def __init__(self):
        # creates the dictionary for reviews and the maximum load
        self.data = defaultdict(dict)
        self.max_text = 9

    def txt_to_string(self, filename):
        """
        given a .txt file, returns the text as string
        """
        with open(filename, 'r', encoding='utf-8') as f:
            text_string = f.read()
        return text_string

    def pdf_to_string(self, filename):
        """
        given a .pdf file, returns the text as string
        """
        text_string = extract_text(filename)
        return text_string

    def get_file_type(self, filename):
        """
        given a filename, returns the type of file it is (.pdf/.txt)
        """
        return os.path.splitext(filename)[1].lower()

    def parser(self, filename):
        """
        finds whether the file is pdf or .txt
        returns the text
        """
        if self.get_file_type(filename) == '.txt':
            text = self.txt_to_string(filename)
        elif self.get_file_type(filename) == '.pdf':
            text = self.pdf_to_string(filename)

        elif isinstance(filename, str):
            text = filename
        else:
            raise ValueError("Unsupported file type.")
        return text

    def pre_processor(self, text):
        """
        given text
        returns a cleaned version of text
        """
        # Remove removes lines, empty spaces, and turns all text to lowercase
        text = text.replace("\n", " ")
        text = re.sub(r'\s+', ' ', text)
        text = text.lower()

        # Split the sentences into individual words and removes all punctuation
        all_words = text.split(" ")
        all_words = [word for word in all_words if word.strip() != '']
        for index, word in enumerate(all_words):
            all_words[index] = re.sub(r'[^\w\s]', '', word).strip()

        # Filters stopwords
        filtered_words = self.stop_words(all_words)

        # analyzes sentence lengths and average sentence word count
        sentences = re.split(r'[.!?]', text)
        sentences = [sentence.strip() for sentence in sentences if sentence.strip()]
        sentence_lengths = [len(sentence.split()) for sentence in sentences]
        avg_sentence_length = sum(sentence_lengths) / len(sentence_lengths) if sentence_lengths else 0

        return filtered_words, avg_sentence_length, sentences

    def default_parser(self, filename):
        # checks if .pdf, .txt, or string and gets text
        text = self.parser(filename)
        # pre-processes the text
        filtered_words, avg_sentence_length, sentences = self.pre_processor(text)
        # gets sentiment values of the reivew
        sentiment = self.get_sentiment(filtered_words)

        # createsthe format of data
        results = {
            'wordcount': Counter(filtered_words),
            'number of words': len(filtered_words),
            'average sentence length': avg_sentence_length,
            'sentiment': sentiment
        }

        return results

    def load_text(self, filename, label='', parser = None):
        """
        given file, loads the text into the analyzer
        """
        # if the data length is greater than 10, the analyzer will reject loading
        if len(self.data['wordcount']) > self.max_text:
            raise AnalyzerException("Cannot load more than 10 files.")

        # if no parser is given, use default processor
        if parser is None:
            results = self.default_parser(filename)
        else:
            results = parser(filename)

        # if no label is given, name by the file name
        if label is None:
            label = filename
        # if the given parser does not return a dictionary format, reject the parser
        if not isinstance(results, dict):
            raise AnalyzerException("Parser must show results in dictionary format.")
        # return the data in dictionary format
        for k, v in results.items():
            self.data[k][label] = v

    def load_stop_words(self, stopfile):
        """
        given stop file, loads stop words to analyzer
        """
        with open(stopfile, 'r', encoding='utf-8') as f:
            self.stop_words_list = [line.strip().lower() for line in f if line.strip()]

    def stop_words(self, all_words):
        """
        removes stop_words from list of words
        """
        return [word for word in all_words if word not in self.stop_words_list]

    def word_count_sankey(self, word_list=None, k = 8, **kwargs):
        """
        creates a sankey plot based off user parameters.
        word_list -> specific words for plot
        k =  minimum amt of word appearances to be plotted
        """
        words = []
        frequencies = []

        # finds all the labels and frequences of each word
        cat = list(self.data['wordcount'].keys())
        for label in cat:
            words.extend(list(self.data['wordcount'][label].keys()))
            frequencies.extend(list(self.data['wordcount'][label].values()))

        # gets the filtered_words
        filtered_words = [words[i] for i in range(len(words)) if frequencies[i] >= k]

        # labels are turned into the category + the words associated with the category
        labels = cat + list(set(filtered_words))
        index_label = {label: index for index, label, in enumerate(labels)}

        source = []
        target = []
        values = []

        # if there is no word_list given, counts all words
        if word_list is None:
          for label in cat:
            for word, freq in self.data['wordcount'][label].items():
                if freq >= k:
                    source.append(index_label[label])  # Category index
                    target.append(index_label[word])  # Word index
                    values.append(freq)
        else: # if a word list is given, only count words in word_list
            for label in cat:
                for word, freq in self.data['wordcount'][label].items():
                    if freq >= k and word in word_list:
                        source.append(index_label[label])  # Categories
                        target.append(index_label[word])  # Words
                        values.append(freq) # Frequenc ies

        # creates sankey nodes and links
        node = dict(
            label=labels,
            thickness=kwargs.get("thickness", 50),
            pad=kwargs.get("pad", 50)
        )
        link = dict(
            source=source,
            target=target,
            value=values
        )

        # plots the sankey plot and shows it
        sk = go.Sankey(link=link, node=node)
        fig = go.Figure(sk)
        fig.show()

    def load_negative_words(self, negative_file):
        """
        given .txt file with negative words turns to readable text
        """
        with open(negative_file, 'r', encoding='utf-8') as f:
            self.negative_words_list = [line.strip().lower() for line in f if line.strip()]

    def load_positive_words(self, positive_file):
        """
        given .txt file with positive words turns to readable text.
        """
        with open(positive_file, 'r', encoding='utf-8') as f:
            self.positive_words_list = [line.strip().lower() for line in f if line.strip()]

    def negative_words(self):
        """
        creates list of negative wrods
        """
        negat_words = self.neg_words
        negative_words_list = []
        for word in negat_words:
            negative_words_list.append(word.lower().strip("\n"))
        return negative_words_list

    def positive_words(self):
        """
        creates list of positive wrods
        """
        posit_words = self.pos_words
        positive_words_list = []
        for word in posit_words:
            positive_words_list.append(word.lower().strip("\n"))
        return positive_words_list

    def get_sentiment(self, filtered_words):
        """
        given filtered_words, gets the sentiment value of words
        """
        sentiment = 0
        for word in filtered_words:
            if word in self.positive_words_list:
                sentiment += 1
            elif word in self.negative_words_list:
                sentiment -= 1
        return sentiment

    def sentiment_graph(self):
        """
        graphs each products sentiment value as a bar graph
        """
        sentiments = []
        # changes the plt font to Times New Roman
        plt.rc('font', family='Times New Roman')
        # colors for each bar
        colors = ['red', 'blue', 'green', 'purple', 'orange', 'pink', 'brown', 'cyan', 'yellow', 'gray']
        # finds the label of each product
        cat = list(self.data['sentiment'].keys())
        # gets all sentiment values of each product
        for label in cat:
            sentiments.append(self.data['sentiment'][label])

        # plots the label and product value
        fig, ax = plt.subplots()
        plt.xticks(fontsize = 8)
        bar_colors = colors[:len(cat)]
        ax.bar(cat, sentiments, color = bar_colors, width = 0.75)
        plt.subplots_adjust(bottom=0.2)

        # caption necessary for using positive/negative words from a study
        plt.figtext(
            0.5, 0.05,
            "Sentiment words derived from Minqing Hu and Bing Liu, "
            "'Mining and Summarizing Customer Reviews,' "
            "Proceedings of the ACM SIGKDD International Conference on Knowledge "
            "Discovery and Data Mining (KDD-2004), Aug 22-25, 2004, Seattle, WA, USA.",
            ha="center", fontsize= 6, wrap=True
        )


        ax.axhline(0, color='black', linewidth=0.8)
        plt.title("Sentiment Analysis")
        plt.xlabel("Text Labels")
        plt.ylabel("Sentiment Score")

        plt.show()

    def word_cloud_visualization(self, rows=2, cols=5):
        """
        given rows and columns, creates word cloud
        """
        if len(self.data['wordcount']) == 0:
            raise AnalyzerException("No data loaded for visualization.")

        # Create subplots
        fig, axes = plt.subplots(rows, cols, figsize=(30, 20))

        # In case the axes is not a 2d array
        if rows * cols == 1:
            axes = [axes]  # Make it a list for uniformity
        elif rows == 1 or cols == 1:
            axes = axes.flatten()
        else:
            axes = axes.ravel()

        # if the length of files is more than available subplots, then stop
        for index, (label, word_count) in enumerate(self.data['wordcount'].items()):
            if index >= len(axes):
                break
            # creates word_cloud
            wordcloud = WordCloud(width=1000, height=600, background_color='white').generate_from_frequencies(word_count)
            axes[index].imshow(wordcloud, interpolation='bilinear')
            axes[index].set_title(label)
            axes[index].axis('off')

        plt.tight_layout()
        plt.show()




