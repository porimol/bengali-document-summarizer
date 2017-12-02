# coding=utf-8

from flask import Blueprint, render_template, request, session, redirect, url_for
import json
from ..bengali_summarizer.bengalisenttok import BengaliSentTok
from ..bengali_summarizer.tfidf import TFIDF
import operator

# summarizer = Blueprint("summarizer", __name__, url_prefix="/wub/")
summarizer = Blueprint("summarizer", __name__)


@summarizer.route("/", methods=["GET", "POST"])
def summery():
    if request.method == "POST":
        document = request.form["bengali_document"]
        summary_frequency = int(request.form["summary_frequency"])
        summary_frequency = summary_frequency if summary_frequency > 0 else 10
        response = {}

        if len(document) > 0:
            top_weighting_sentences = document_summarizer(document)
            top_sentence = [
                sentence[0] for sentence in sorted(
                    top_weighting_sentences.items(),
                    key=operator.itemgetter(1),
                    reverse=True
                )[:summary_frequency]]

            response["original_document"] = document
            response["summary_frequency"] = summary_frequency
            response["summery"] = '। '.join(top_sent.strip() for top_sent in top_sentence)

        print(json.dumps(response))
        return render_template("summarizer/home.html", summary_response=response)

    return render_template("summarizer/home.html")


def document_summarizer(bangla_corpus):

    tfidf_obj = TFIDF()
    pattern = r'[?|।!]'
    bn_tok = BengaliSentTok(bangla_corpus)
    tokenized_sentences = bn_tok.bn_sentence_tok(pattern)
    tokenized_documents = bn_tok.bn_word_tok(pattern)
    term_frequency = {}
    inverse_df = {}
    tfidf = {}
    corpora = ' '.join(bn_tok.bn_sentence_tok(pattern))
    pv_counter = 5
    sent_count = 0

    top_weighting_sentences = {}
    for index, doc in enumerate(tokenized_documents):
        stf = 0
        if len(doc) > 0:
            for word in set(doc):
                stf = round(stf + tfidf_obj.tf(word, corpora), 6)
                term_frequency[word] = tfidf_obj.tf(word, corpora)
                inverse_df[word] = tfidf_obj.idf(word, tokenized_documents)
                tfidf[word] = tfidf_obj.tf_idf(word, doc, tokenized_documents)

            sentence = ' '.join(doc)
            pv_counter = round(pv_counter-0.01, 2)
            # pv_counter = 1 / (index + 1)
            # S=α*STF+β*PV+δ+λ
            alpha = 1
            beta = 1
            # if pv_counter >= 3 and len(sentence.split()) >= 4:
            if len(sentence.split()) >= 4:
                sent_count += 1
                cw = bn_tok.connecting_word(sentence)
                sent_score = round(alpha + stf + beta * pv_counter + cw, 6)
                # top_weighting_sentences[sentence] = sent_score
                top_weighting_sentences[tokenized_sentences[index]] = sent_score

    return top_weighting_sentences

