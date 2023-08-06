from typing import List

from flair.data import Tokenizer as flair_tokenizer
from sikriml_core.models.ner.tokenizer import Tokenizer


class FlairTokenizer(flair_tokenizer):
    def __init__(self):
        self.tokenizer = Tokenizer()

    def tokenize(self, text: str) -> List[str]:
        return [token.text for token in self.tokenizer(text)]
