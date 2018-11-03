from flask import Blueprint
from .summarizer import summery,\
    summery_download


document_summarizer = Blueprint("document_summarizer", __name__)


document_summarizer.add_url_rule(
    "/",
    strict_slashes=False,
    endpoint="summery",
    view_func=summery,
    methods=['GET', 'POST']
)

document_summarizer.add_url_rule(
    "/download",
    strict_slashes=False,
    endpoint="summery_download",
    view_func=summery_download,
    methods=['POST']
)
