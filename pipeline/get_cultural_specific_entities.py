import argparse
import json

def get_cultural_specific_entities(input_file, output_file):
    with open(input_file) as f:
        wikidata = json.load(f)

    output = {}
    for key in wikidata.keys():
        if wikidata[key]["country_of_origin"] is not None:
            output[key] = wikidata[key]
    
    with open(output_file, 'w', encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=1)
                
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Categorize entities')
    parser.add_argument('--input', type=str, required=True, help='Input file')
    parser.add_argument('--output', type=str, required=True, help='Output file')
    args = parser.parse_args()
    get_cultural_specific_entities(args.input, args.output)