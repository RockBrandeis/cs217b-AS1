"""ner.py

Run spaCy NER over an input string and insert XML tags for each entity.

"""

import io
import spacy

nlp = spacy.load("en_core_web_sm")

class SpacyDocument:

    def __init__(self, text: str):
        self.text = text
        self.doc = nlp(text)

    def get_tokens(self) -> list:
        return [token.lemma_ for token in self.doc]

    def get_entities(self) -> str:
        entities = []
        for e in self.doc.ents:
            entities.append((e.start_char, e.end_char, e.label_, e.text))
        return entities

    def get_entities_with_markup(self) -> str:
        entities = self.doc.ents
        starts = {e.start_char: e.label_ for e in entities}
        ends = {e.end_char: True for e in entities}
        buffer = io.StringIO()
        for p, char in enumerate(self.text):
            if p in ends:
                buffer.write('</entity>')
            if p in starts:
                buffer.write('<entity class="%s">' % starts[p])
            buffer.write(char)
        markup = buffer.getvalue()
        return '<markup>%s</markup>' % markup
    
    #Add dependency parse
    def get_dependency_parse(self):
        
        deps = []
        for token in self.doc:
            deps.append({
                "text": token.text,
                "dep": token.dep_, 
                "head_text": token.head.text, 
                "head_pos": token.head.pos_, 
            })
        return deps


if __name__ == '__main__':

    doc = SpacyDocument(example)
    print(doc.get_tokens())
    for entity in doc.get_entities():
        print(entity)
    print(doc.get_entities_with_markup())
