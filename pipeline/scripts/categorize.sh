# filter out entitis which are person names
data_dir=../demo
# python clean_name_in_entities.py --input $data_dir/entity.json --output $data_dir/entity_cleaned.json
# # categorize entities
# python categorize_entities.py --input $data_dir/entity_cleaned.json --output $data_dir/entity_categorized.json
# filter out entities which are not in the cultural category list
python get_cultural_related_entities.py --input $data_dir/entity_categorized.json --output $data_dir/entity_cultural.json