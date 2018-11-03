# coding=utf-8
from flask import render_template, request, make_response, jsonify
from ..bengali_summarizer.bengalisenttok import BengaliSentTok
from ..bengali_summarizer.tfidf import TFIDF
import operator
import math


def summery():
    if request.method == "POST":
        document = request.form["bengali_document"]
        response = {}

        if len(document) > 0:
            top_weighting_sentences = document_summarizer(document)
            summary_frequency = math.ceil(math.sqrt(len(top_weighting_sentences)))
            top_sentence = [
                sentence[0] for sentence in sorted(
                    top_weighting_sentences.items(),
                    key=operator.itemgetter(1),
                    reverse=True
                )[:summary_frequency]]

            response["original_document"] = document
            response["summary_frequency"] = summary_frequency
            response["summery"] = '। '.join(top_sent.strip() for top_sent in top_sentence)+'।'

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
    corpora = ' '.join(tokenized_sentences)
    # pv_counter = 5
    sent_count = 0

    top_weighting_sentences = {}
    for index, doc in enumerate(tokenized_documents):
        stf = 0
        if len(doc) > 0:
            for word in set(doc):
                stf += round(tfidf_obj.tf(word, corpora), 6)
                term_frequency[word] = tfidf_obj.tf(word, corpora)
                inverse_df[word] = tfidf_obj.idf(word, tokenized_documents)
                tfidf[word] = tfidf_obj.tf_idf(word, doc, tokenized_documents)

            sentence = ' '.join(doc)
            pv_counter = round(1 / math.sqrt(index) if index > 4 else 5, 2)
            # pv_counter = round(pv_counter - 0.01, 2)
            # pv_counter = 1 / (index + 1)
            alpha = 1
            beta = 1
            if len(sentence.split()) >= 4:
                sent_count += 1
                cw = bn_tok.connecting_word(sentence)
                # S=α*STF+β*PV+cw
                sent_score = round(alpha * stf + beta * pv_counter + cw, 6)
                # top_weighting_sentences[sentence] = sent_score
                top_weighting_sentences[tokenized_sentences[index]] = sent_score

    return top_weighting_sentences


def summery_download():
    try:
        summery_content = request.form["summery_content"]
        response = make_response(summery_content)
        response.headers['Content-Disposition'] = 'attachment; filename=summery.txt'
        response.mimetype = 'text/txt'

        return response

    except Exception as ex:

        response = {
            # "message": "Error Message: {0}".format(ex),
            "message": "Something went wrong!",
            "status": False
        }

        return jsonify(response)
