data_dir=../demo
python augment.py --input $data_dir/entity_cultural.json --output $data_dir/entity_augmented.json --tgtlang zh
python get_cultural_specific_entities.py --input $data_dir/entity_augmented.json --output $data_dir/entity_cultural_augmented.json