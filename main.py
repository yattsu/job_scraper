from bs4 import BeautifulSoup
import os
import requests
import re
import json

def get_urls():
    urls = [] 
    pattern = r'^(http|https):\/\/([\w.-]+)(\.[\w.-]+)+([\/\w\.-]*)*\/?$'

    if os.path.isfile("urls.txt"):
        f = open("urls.txt", "r")
        lines = f.readlines()
        for line in lines:
            if line != "":
                urls.append(line.strip())
    
    while len(urls) == 0:
        user_input = input("- URLS (comma separated): ")
        if user_input != "".strip():
            for url in user_input.split(","):
                if url.strip() == "":
                    continue
                if bool(re.match(pattern, url)):
                    urls.append(url.strip())

    return urls

def get_soups(urls):
    soups = []
    for url in urls:
        print(f"- Getting {url}")
        r = requests.get(url)

        if r.status_code != 200:
            print(f"- Error getting {url}")
            continue

        soup = BeautifulSoup(r.text, 'html.parser')
        
        soups.append(soup)
        
    return soups

def get_dummy_soups():
    soups = []
    f = open("dummy_doc.txt", "r")
    html_list = f.read().split(">>>")
    for html in html_list:
        soup = BeautifulSoup(html, "html.parser")
        soups.append(soup)

    return soups

def main():
    sites = [
        {
            "name": "ejobs", 
            "list_tag": "ul", 
            "list_class": "JobList__List", 
            "item_tag":"li", 
            "item_class": "JobCardWrapper", 
            "item_title_tag": "h2", 
            "item_company_tag": "h3"
        },
        {
            "name": "bestjobs", 
            "list_tag": "div", 
            "list_class": "card-list", 
            "item_tag":"div", 
            "item_class": "list-card", 
            "item_title_tag": "h2", 
            "item_company_tag": "small"
        },
    ]
    eligible = []
    urls = get_urls()
    soups = get_soups(urls) 
    
    for soup in soups:
        if not soup:
            print("- No soup")
            continue

        for site in sites:
            try:
                jobs = soup.find(site["list_tag"], class_=site["list_class"]).find_all(site["item_tag"], class_=site["item_class"])
                for job in jobs:
                    job_temp = {}
                    try:
                        job_temp["position"] = job.find(site["item_title_tag"]).text.strip()
                        job_temp["company"] = job.find(site["item_company_tag"]).text.strip()
                        eligible.append(job_temp)
                    except:
                        continue
            except:
                continue
                
    f = open("jobs.json", "w")
    print("- Writing to file")
    json.dump(str(eligible), f)

if __name__ == "__main__":
    main()
