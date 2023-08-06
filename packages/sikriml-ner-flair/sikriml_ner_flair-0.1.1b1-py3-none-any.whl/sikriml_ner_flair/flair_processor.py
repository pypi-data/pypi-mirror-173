from typing import Set

import pydash as py_
from flair.data import Sentence, Span, Tokenizer
from flair.models import SequenceTagger
from sikriml_core.models.ner import ProcessorBase, ScoreEntity


class FlairProcessor(ProcessorBase):
    def __init__(self, flair_model: SequenceTagger, tokenizer: Tokenizer = None):
        self.flair_model = flair_model
        self.__tokenizer = tokenizer() if tokenizer else True
        super().__init__()

    flair_model: SequenceTagger

    def __apend_entity(self, result: Set[ScoreEntity], value: Span) -> Set[ScoreEntity]:
        result.add(
            ScoreEntity(value.text, value.start_position, value.end_position, value.tag)
        )
        return result

    def process(self, text: str) -> Set[ScoreEntity]:
        sentence = Sentence(text, use_tokenizer=self.__tokenizer)
        self.flair_model.predict(sentence)
        return py_.reduce_(sentence.get_spans("ner"), self.__apend_entity, set())
