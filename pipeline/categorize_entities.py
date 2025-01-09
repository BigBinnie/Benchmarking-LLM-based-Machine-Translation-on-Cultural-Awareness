# Description: This script is used to classify the category of the wikipedia page.
# The input is the entity file, which contains all the entities and their corresponding wikipedia page title.
import requests
from queue import Queue
from threading import Thread
import json 
import time

import argparse

def classify_category(input_file, output_file):
    url_Quene = Queue()
    result_Queue = Queue()

    with open(input_file) as f2:
        wikidata = json.load(f2)

    STEP = 50
    output = []
    output = [key for key in wikidata.keys()]
    print(len(output))
    
    title_list = []
    for index in range(0, len(wikidata), STEP):
        titles = [wikidata[key]["value"].replace("|","") for key in output[index:index+STEP]]
        title_list.append("|".join(titles))
    print(len(title_list))

    for index, url in enumerate(title_list[:]):
        url_Quene.put([index, url])

    def do_something(in_Quene:Queue, out_Quene:Queue):
        while in_Quene.empty() is not True:
            labels = []
            index, url = in_Quene.get()
            print(index, url)
            try:            
                PARAMS = {
                    "action": "query",
                    "prop": "revisions",
                    "titles": url,
                    # "rvprop": "ids|timestamp",
                    # "rvlimit": 1,
                    "format": "json",
                    # "rvstart":"2022-12-01T00:00:00.000Z"
                }
                # get revison number
                URL = "https://en.wikipedia.org/w/api.php"
                response = requests.get(url=URL, params=PARAMS)
                response.raise_for_status()
                response = response.json()
                print(index, url, response)
                pages = response["query"]["pages"]
                title_list = url.lower().split("|")
                response_title_list = [pages[key]["title"].lower() for key in pages.keys()]

                for title in title_list:
                    label = {}
                    if title in response_title_list:
                        response_index = response_title_list.index(title)
                        pageid = list(pages.keys())[response_index] 
                        if 'revisions' in pages[pageid] :
                            print("page",title, pages[pageid])
                            revid = pages[pageid]["revisions"][0]["revid"]
                            print(url, revid)
                            label["revid"] = str(revid)
                            
                            #get wiki-project tag
                            URL = f"https://ores.wikimedia.org/v3/scores/enwiki/{revid}/articletopic"
                            try:
                                response = requests.get(url=URL).json()
                                if 'enwiki' in response.keys():
                                    if "score" in response['enwiki']["scores"][str(revid)]["articletopic"].keys():
                                        prediction = response['enwiki']['scores'][str(revid)]["articletopic"]["score"]["prediction"]
                                        print(url, prediction)
                                        probability = response['enwiki']['scores'][str(revid)]["articletopic"]["score"]["probability"]
                                    
                                        if len(prediction) != 0:
                                            # filter general tag
                                            prediction_detail = [x for x in prediction if "*" not in x]
                                            if len(prediction_detail)!=0:
                                                prediction = prediction_detail
                                            
                                            #get the most probable tag
                                            tag = prediction[0]
                                            for predict in prediction:
                                                if probability[predict] > probability[tag]:
                                                    tag = predict
                                            label["tag"] = tag
                            except requests.HTTPError as e:
                                print(f"[!] Exception caught: {e}")     
                    labels.append(label)
            except requests.HTTPError as e:
                print(f"[!] Exception caught: {e}")
                time.sleep(1)
            out_Quene.put([index, labels])
            in_Quene.task_done()

    n = 10
    print('start spider*{}'.format(n))
    for index in range(n):
        thread = Thread(target=do_something, args=(url_Quene, result_Queue, )) 
        thread.daemon = True # 
        thread.start() 
    
    url_Quene.join()
    print('get id info*{}'.format(url_Quene.qsize()))
    

    result = {}
    # output_result = {}
    while result_Queue.empty() is not True:
        index, result_list= result_Queue.get()
        print(index, result_list)
        result[index]= result_list
        # output_result[output[index]] = result_list
        result_Queue.task_done()
    result_Queue.join()

    output_result = {}
    for index in range(len(title_list)):
        if index in result.keys():
            labels = result[index]
            if len(labels)!=0:
                for i,label in enumerate(labels):
                    output_result[output[index*50+i]] = dict(wikidata[output[index*50+i]], **label)
    output_wikiproject = dict({}, **output_result)
    print(len(output_wikiproject.keys()))
    print("st")

    with open(output_file, 'wt', encoding="utf-8") as f:
        json.dump(output_wikiproject, f, ensure_ascii=False, indent=1)
    print('done.')


def main():
    # argument parser
    parser = argparse.ArgumentParser(description="Multithread Category Classification")
    parser.add_argument("--input", type=str, help="input file path")
    parser.add_argument("--output", type=str, help="output file path")
    args = parser.parse_args()
    classify_category(args.input, args.output)

if __name__ == "__main__":
    main()