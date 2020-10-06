import spacy 
import os
import plac
import random
import warnings
from pathlib import Path
from spacy.util import minibatch, compounding

model_path = "./custom_models/modelo_poc"


def get_all_entity_ner(text):
    
    nlp = spacy.load(model_path)
    doc = nlp(text)
    
    return doc.ents

def train_data(training_data,n_iter):
        
    nlp = spacy.load(model_path)
    # load existing spaCy model
    print("Loaded model '%s'" % model)
    

    # add labels in ner
    ner = nlp.get_pipe("ner")
    for _, annotations in training_data:
        for ent in annotations.get("entities"):
            ner.add_label(ent[2])

    # get names of other pipes to disable them during training
    pipe_exceptions = ["ner", "trf_wordpiecer", "trf_tok2vec"]
    other_pipes = [pipe for pipe in nlp.pipe_names if pipe not in pipe_exceptions]
    # only train NER
    with nlp.disable_pipes(*other_pipes), warnings.catch_warnings():
        # show warnings for misaligned entity spans once
        warnings.filterwarnings("once", category=UserWarning, module='spacy')

        for itn in range(n_iter):
            random.shuffle(training_data)
            losses = {}
            # batch up the examples using spaCy's minibatch
            batches = minibatch(training_data, size=compounding(4.0, 32.0, 1.001))
            for batch in batches:
                texts, annotations = zip(*batch)
                nlp.update(
                    texts,  # batch of texts
                    annotations,  # batch of annotations
                    drop=0.5,  # dropout - make it harder to memorise data
                    losses=losses,
                )
            print("Losses", losses)

    # test the trained model
    for text, _ in training_data:
        doc = nlp(text)
        print("Entities", [(ent.text, ent.label_) for ent in doc.ents])
        print("Tokens", [(t.text, t.ent_type_, t.ent_iob) for t in doc])

    # save model to output directory
    output_dir = Path(model_path)
    nlp.to_disk(output_dir)
    print("Saved model to", output_dir)
