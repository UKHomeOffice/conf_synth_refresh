from requests.models import HTTPError
from atlassian import Confluence
from essential_generators import DocumentGenerator
import requests
import json
from requests.auth import HTTPBasicAuth
import logging
from datetime import datetime
import os 
from dotenv import load_dotenv
from random_word import RandomWords
import re
import time


# Configuring variables
load_dotenv()
isotime = datetime.now().isoformat('T', 'seconds')

CRITICAL="\U0001F198" #logging.critical
ERROR="\U00002757"    #logging.error
WARNING="\U000026A0"  #logging.warning
INFO="\U00002139"     #logging.debug
SUCCESS="\U00002705"  #logging.info

logging.basicConfig(format='%(message)s', level=logging.INFO)


# Establish a connection with Confluence 
def connection():
    global confluence
    confluence = Confluence(
        url='https://confluence.shs-dev.dsa-notprod.homeoffice.gov.uk',
        username=os.environ['USERNAME'],
        password=os.environ['PASSWORD'])


# Generates random material 
def generator():
    global gen
    gen = DocumentGenerator()

# Get keys for all the spaces 
def space_keys():
    global space_ids
    space_ids=[]
    all_spaces=confluence.get_all_spaces(start=0, limit=50)
    for key,value in all_spaces.items():
        if key=='results':
            for i in value:
                for a,b in i.items():
                    if a=="key":
                        space_ids.append(b)
    return space_ids
    

# Create spaces 
def create_spaces(spaces):
    access_token=os.environ['ACCESS_TOKEN']
    url = "https://confluence.shs-dev.dsa-notprod.homeoffice.gov.uk/rest/api/space"

    for i in range(spaces):
        headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": "Bearer {}".format(access_token)
        }

        r=RandomWords()
        space_name=r.get_random_word(hasDictionaryDef="true",minLength=6, maxLength=12)
        space_key=space_name[:5].upper()
        i=0

        while space_name.isascii()==False or (space_key in space_ids):
            space_name=r.get_random_word(hasDictionaryDef="true",minLength=6, maxLength=12)
            space_key = space_name[:5].upper()
            i+=1
            if i>10:
                break

        payload = json.dumps({
        "name": space_name,
        "key": space_key
        })
        response = requests.request(
        "POST",
        url,
        data=payload,
        headers=headers
        )

        # print(json.dumps(json.loads(response.text), sort_keys=True, indent=4, separators=(",", ": ")))
        stat=str(response.status_code)
        if re.search('20.',stat):
            logging.info('%s Space created successfully \n Name:%s Key:%s %s \n', SUCCESS, space_name, space_key, isotime )
        elif re.search('40.',stat):
            logging.error('%s Failed to create space - Invalid key \n Name:%s Key:%s %s \n', ERROR, space_name, space_key, isotime)            
        elif re.search('50.',stat):
            logging.critical('%s Failed to create space - Site not available \n Name:%s Key:%s %s \n', CRITICAL, space_name, space_key, isotime) 
            time.sleep(5)
        else:
            logging.critical('%s Failed to create space \n Name:%s Key:%s %s \n', CRITICAL, space_name, space_key, isotime )

        

# Create pages and add comments 
def content(pages,comments):
    try:
        for x in range(pages):
            for id in space_ids:
                status = (confluence).create_page(
                    space=id,
                    title=gen.word(),
                    body=10*(gen.paragraph()))
                page_id = confluence.get_page_id(id, status['title'])
                logging.info('%s Page created successfully. \n Name:%s %s', SUCCESS, status['title'], isotime )

                for y in range(comments):
                    confluence.add_comment(page_id, gen.sentence())
                    logging.info('%s Comment(s) added successfully. %s \n', SUCCESS, isotime )

    except HTTPError:
        print("A page with this Title already exists in this Space ")
        logging.error('%s Error creating page - A page with this Title already exists in this Space  %s', CRITICAL, isotime )



# # Functions 
connection()
generator()
space_keys()
try:
    create_spaces(spaces = int(os.environ['SPACES']))
except:
    logging.raiseExceptions
space_keys() # Have to run this function again to take into account new spaces created. 
content(pages = int(os.environ['PAGES']), comments = int(os.environ['COMMENTS']))
