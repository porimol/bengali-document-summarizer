# coding=utf-8


class TFIDF():
    def word_frequency(self, word, document):
        return document.count(word)

    def word_count(self, document):
        return len(document)

    def word_contain_documents(self, word, documents):
        # number of documents that contain word w
        count = 0
        for doc in documents:
            if (self.word_frequency(word, doc)) > 0:
                count += 1

        return count + 1

    def tf(self, word, document):
        return self.word_frequency(word, document) / self.word_count(document)

    def idf(self, word, documents):
        return len(documents) / self.word_contain_documents(word, documents)

    def tf_idf(self, word, document, documents):
        return self.tf(word, document) * self.idf(word, documents)

