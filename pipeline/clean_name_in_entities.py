from flair.data import Sentence
from flair.models import SequenceTagger
import json
from tqdm import tqdm
import argparse

def clean_names(input_file, output_file):
    # open the file and load the data
    with open(input_file, 'r', encoding='utf-8') as f:
        wikidata = json.load(f)

    output = {}
    tagger = SequenceTagger.load('ner')
    for key in tqdm(wikidata.keys()):
        # make a sentence
        sentence = Sentence(wikidata[key]["value"])
        # # run NER over sentence
        tagger.predict(sentence)

        # # iterate over entities and print each entity
        for entity in sentence.get_spans('ner'):
            entity_type = str(entity).split('→')[1].split('(')[0].strip()
            # print(entity_type)
            if entity_type != 'PER':
                output[key] = wikidata[key]
                break
        
    print(len(output))

    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(output, f, ensure_ascii=False, indent=4)

def main():
    argparser = argparse.ArgumentParser()
    argparser.add_argument("--input", type=str, help="Input file")
    argparser.add_argument("--output", type=str, help="Output file")
    args = argparser.parse_args()
    clean_names(args.input, args.output)


if __name__ == "__main__":
    main()
