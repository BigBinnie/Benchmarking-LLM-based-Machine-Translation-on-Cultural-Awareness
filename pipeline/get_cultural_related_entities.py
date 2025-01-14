import argparse
import json

category_list = [
"Culture.Food and drink",
"Culture.Visual arts.Architecture",
"History and Society.Transportation", 
"Culture.Sports", 
"Culture.Media.Entertainment",
"History and Society.Politics and government",
"Culture.Philosophy and religion",
"Culture.Literature",
"Culture.Visual arts.Visual arts*",
"Culture.Visual arts.Fashion",
"Culture.Visual arts.Comics and Anime",
"Culture.Performing arts",
"Culture.Media.Music",
"Culture.Media.Films",
"Culture.Media.Books",
"History and Society.History",
"STEM.Biology",
"Geography.Regions.Americas.North America"
]

def get_cultural_related_entities(input_file, output_file):
    with open(input_file) as f:
        wikidata = json.load(f)

    output = {}
    for key in wikidata.keys():
        if wikidata[key]["tag"] in category_list:
            output[key] = wikidata[key]
    
    # use utf-8 to write the file
    with open(output_file, 'w', encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=1)
                
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Categorize entities')
    parser.add_argument('--input', type=str, required=True, help='Input file')
    parser.add_argument('--output', type=str, required=True, help='Output file')
    args = parser.parse_args()
    get_cultural_related_entities(args.input, args.output)