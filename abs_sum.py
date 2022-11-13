from transformers import pipeline
import os
from transformers.utils import logging

logging.set_verbosity_info()
logger = logging.get_logger("transformers")
logger.info("INFO")
logger.warning("WARN")

os.environ["CUDA_VISIBLE_DEVICES"] = "0"
summarizer = pipeline("summarization", model="t5-base", tokenizer="t5-base", framework="tf")


def get_abstractive(text, lenn=100):
    summary_text = summarizer(text, max_length=lenn, min_length=5, do_sample=False)[0]['summary_text']
    return summary_text
