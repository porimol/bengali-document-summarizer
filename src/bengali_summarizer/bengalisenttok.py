# coding=utf-8
import re
from os.path import dirname, realpath


class BengaliSentTok:
    def __init__(self, corpus):
        self._bangla_corpus = corpus

    def bn_corpus(self):
        bn_paragraphs = self._bangla_corpus

        return bn_paragraphs.strip('\n')

    def bn_stop_words(self, file_name='stop_words.txt'):
        # get the files path
        file_dir_path = dirname(realpath(__file__))
        file = file_dir_path + "/" + file_name
        with open(file, 'r') as bn_stw:
            stop_words = "".join(bn_stw.readlines())

        return set(stop_words.split())

    def file_write(self, token_list, file_name):
        with open(file_name, 'w') as file:
            for index, token in enumerate(token_list):
                file.write(str(index + 1) + ') ' + token + '। \n')

    def bn_sentence_tok(self, pattern):
        corpus = self.bn_corpus()
        bn_tokens = re.split(pattern, corpus)

        return bn_tokens

    def bn_word_tok(self, pattern):
        word_tokens = []
        for tokenized_sent in self.bn_sentence_tok(pattern):
            word_list = tokenized_sent.split()
            word_tokens.append([word for word in word_list if word not in self.bn_stop_words()])

        return word_tokens

    def connecting_word(self, sentences):
        cw_file = 'connecting_words.txt'
        # get the files path
        file_dir_path = dirname(realpath(__file__))
        file = file_dir_path + "/" + cw_file
        with open(file) as cw:
            connecting_words = cw.readlines()

        cw = 0
        for cword in connecting_words:
            if cword.strip() in sentences:
                cw = 1

        return cw


if __name__ == "__main__":
    import operator
    from .tfidf import TFIDF

    cw_file = 'connecting_words.txt'
    bangla_corpus = 'bangla_corpus.txt'
    pattern = r'[?|।!]'
    tfidf_obj = TFIDF()
    bn_tok = BengaliSentTok(bangla_corpus)
    tokenized_sentences = bn_tok.bn_sentence_tok(pattern)
    tokenized_documents = bn_tok.bn_word_tok(pattern)
    term_frequency = {}
    inverse_df = {}
    tfidf = {}
    corpora = ' '.join(bn_tok.bn_sentence_tok(pattern))
    stf_list = []
    pv_counter = 5
    sent_count = 0
    with open(cw_file) as cw:
        connecting_words = cw.readlines()

    top_weighting_sentences = {}
    for index, doc in enumerate(tokenized_documents):
        stf = 0
        if len(doc) > 0:
            for word in set(doc):
                stf = round(stf + tfidf_obj.tf(word, corpora), 6)
                term_frequency[word] = tfidf_obj.tf(word, corpora)
                inverse_df[word] = tfidf_obj.idf(word, tokenized_documents)
                tfidf[word] = tfidf_obj.tf_idf(word, doc, tokenized_documents)
                print("{0}[TF: {1}]".format(
                    word,
                    tfidf_obj.tf(word, corpora)
                ))

            sentence = ' '.join(doc)
            # pv_counter = round(pv_counter-0.01, 2)
            pv_counter = 1 / (index + 1)
            # S=α*STF+β*PV+δ+λ
            alpha = 1
            beta = 1
            # if pv_counter >= 3 and len(sentence.split()) >= 4:
            if len(sentence.split()) >= 4:
                sent_count += 1
                cw = bn_tok.connecting_word(connecting_words, sentence)
                sent_score = round(alpha + stf + beta * pv_counter + cw, 6)
                # top_weighting_sentences[sentence] = sent_score
                top_weighting_sentences[tokenized_sentences[index]] = sent_score
                stf_list.append("{0} [STF: {1}][PV: {2}][CW: {3}][Sent. Score: {4}]".format(
                    sentence,
                    stf,
                    pv_counter,
                    cw,
                    sent_score
                ))
                print("{0}) {1}[STF: {2}][PV: {3}][CW: {4}][Sent. Score: {5}]".format(
                    sent_count,
                    sentence,
                    stf,
                    pv_counter,
                    cw,
                    sent_score
                ))
            print("-------------------------------------------------------------------------------------------------")

    # call tokenized file writer function
    bn_tok.file_write(stf_list, 'tokenized.txt')
    top_sentence = [
        sentence[0] for sentence in sorted(
            top_weighting_sentences.items(),
            key=operator.itemgetter(1),
            reverse=True
        )[:10]]
    # call top sentence list file writer function
    bn_tok.file_write(top_sentence, 'top_sentence.txt')
