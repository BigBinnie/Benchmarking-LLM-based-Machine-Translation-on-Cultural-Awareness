# filter out entitis which are person names
python clean_name_in_entities.py --input ../data/entity.json --output ../data/entity_cleaned.json
# categorize entities
python categorize_entities.py --input ../data/entity_cleaned.json --output ../data/entity_categorized.json
# filter out entities which are not in the cultural category list
# python filter_cultural_entities.py --input ../data/entity_categorized.json --output ../data/entity_cultural.json