from wikidata.client import Client
from bs4 import BeautifulSoup
from queue import Queue
from threading import Thread
import json 
import urllib.error
from tqdm import tqdm
from wikidataintegrator import wdi_core,wdi_helpers
from hanziconv import HanziConv
import json
import os
import argparse

def get_metadata_by_Qid(Qid, tgtlang):
    client = Client()
    try:
        entity = client.get(Qid, load=True)
    except:
        return None
    sitelinks = {}
    if "sitelinks" in entity.data.keys():
        url = entity.data['sitelinks']
        for key in url.keys():
            if key == "enwiki" or key == f"{tgtlang}wiki":
                sitelinks[key] = url[key]['url']
    langs = ['en', tgtlang]
    if "claims" in entity.data.keys():
        claims = entity.data['claims']
        if "P495" in claims:
            try:
                country_qid= claims["P495"][0]["mainsnak"]["datavalue"]["value"]["id"]
                country = client.get(country_qid, load=True)
                country = country.data['labels']['en']['value']
            except:
                country = None
        elif "P17" in claims:
            try:
                country_qid = claims["P17"][0]["mainsnak"]["datavalue"]["value"]["id"]
                country = client.get(country_qid, load=True)
                country = country.data['labels']['en']['value']
            except:
                country = None
        else:
            country = None      
    else:
        country = None
    try:
        item = wdi_core.WDItemEngine(wd_item_id=Qid)
    except:
        return {    
            "metadata":{
                "sitelinks": sitelinks,
                "labels": {},
                "descriptions": {},
                "aliases": {}
            },
            "country_of_origin": country
        }
    
    langs = ['en',tgtlang]
    label_dict = {}
    description_dict = {}
    alias_dict = {}

    for lang in langs:
        label_dict[lang] = item.get_label(lang)
        description_dict[lang] = item.get_description(lang)
        alias_dict[lang] = item.get_aliases(lang)
    return{
        # "value": name,
        "metadata":{
            "sitelinks": sitelinks,
            "labels": label_dict,
            "descriptions": description_dict,
            "aliases": alias_dict
        },
        "country_of_origin": country
    }

def get_wikidata(input_file, output_file):
    url_Quene = Queue()
    result_Queue = Queue()

    # load data
    with open(input_file) as f:
        raw_data = json.load(f)
    labels = []
    qid_list = []
    for sample in raw_data:
        for label in sample["labels"]:
            if label["Qid"] is not None:
                qid_list.append(label["Qid"])

    print(len(qid_list))
    input()
    for index, qid in enumerate(qid_list[:]):
        url_Quene.put([index, qid])

    def do_something(in_Quene:Queue, out_Quene:Queue):
        while in_Quene.empty() is not True:
            index, qid = in_Quene.get()
            metadata = get_metadata_by_Qid(qid, tgtlang="zh")
            print(index)
            out_Quene.put([index, metadata])
            in_Quene.task_done()

    n = 1
    print('start spider*{}'.format(n))
    for index in range(n):
        thread = Thread(target=do_something, args=(url_Quene, result_Queue, )) 
        thread.daemon = True # 
        thread.start() 
    
    url_Quene.join()
    print('get id info*{}'.format(url_Quene.qsize()))
    

    result = {}
    while result_Queue.empty() is not True:
        index, result_list= result_Queue.get()
        print(index, result_list)
        result[index]= result_list
        result_Queue.task_done()
    result_Queue.join()

    output_result = {}
    for index, item in enumerate(qid_list[:]):
        if index in result.keys():
            output_result[item]= result[index]

    output_wikidata = output_result
    print(len(output_wikidata.keys()))
    with open(output_file, 'wt', encoding="utf-8") as f:
        json.dump(output_wikidata, f, ensure_ascii=False, indent=1)
    print('done.')

def main():
    argparser = argparse.ArgumentParser()
    argparser.add_argument("--input", type=str, help="Input file")
    argparser.add_argument("--output", type=str, help="Output file")
    args = argparser.parse_args()
    get_wikidata(args.input, args.output)

if __name__ == "__main__":
    main()