from bs4 import BeautifulSoup, UnicodeDammit
import pandas as pd
import requests
import re



BASE_LINK = "https://eur-lex.europa.eu"
search_result_link = "https://eur-lex.europa.eu/search.html?SUBDOM_INIT=ALL_ALL&orDC_DOM_CODED=DC_TT_CODED%3D5360%2CDC_TT_CODED%3D1360%2CDC_TT_CODED%3D6052%2CDC_TT_CODED%3D1602%2CDC_TT_CODED%3D2416%2CDC_TT_CODED%3D2735%2CDC_TT_CODED%3D2414%2CDC_TT_CODED%3D1115%2CDC_TT_CODED%3D2413%2CDC_TT_CODED%3D1258%2CDC_TT_CODED%3D2412%2CDC_TT_CODED%3D2775%2CDC_TT_CODED%3D2763%2CDC_TT_CODED%3D656%2CDC_TT_CODED%3D239%2CDC_TT_CODED%3D6788%2CDC_TT_CODED%3D5017%2CDC_TT_CODED%3D4314%2CDC_TT_CODED%3D4416%2CDC_TT_CODED%3D2418%2CDC_TT_CODED%3D2737%2CDC_TT_CODED%3D2417%2CDC_TT_CODED%3D2736&DTS_SUBDOM=ALL_ALL&DTS_DOM=ALL&lang=de&type=advanced&qid=1698948321290&page=1"



def download_site_links(crpaed_links):
    celex_pattern = r'CELEX:(\w+)'
    links = []
    texts = []
    celex_num = []
    for index, link in enumerate(crpaed_links):
        if "PDF" in str(link):
            continue
        link = BASE_LINK + str(link.get('href'))[1:]
        # print("link",link)
        page = requests.get(link)
        soup = BeautifulSoup(page.content, "html.parser")
        text_body = soup.get_text()

        text_body = text_body.replace("\n", " ")
        match = re.search(celex_pattern, str(link))
        if match:
            celex_number = match.group(1)
            celex_num.append(celex_number)
        links.append(str(link))
        texts.append(text_body)

    return links, texts, celex_num




def extract_date_clean_text(text):
    #tt = test["text"][1]
    text = text.split(None, 1)[1]
    date = text.split(None, 1)[0]
    text = text.split(None, 1)[1]
    text = text.replace(u'\xa0', u' ')
    return text, date



def get_last_page_link(soup):
    last_page_link = soup.find("a", title="Last Page")
    if last_page_link:
        return last_page_link.get('href')
    else:
        return None  # Or handle the case where the element is not found in your specific way




page = requests.get(search_result_link)
soup = BeautifulSoup(page.content, "html.parser")
test = soup.find_all("a", class_="piwik_download")
titles = soup.find_all("a", class_="title")



titl = []
for p in titles:
        titl.append(p.get_text())
titles = titl




def crap_search_result(search_result_link: str):
    #creat empty datafram
    result_df = pd.DataFrame([], columns = ["title", "text", "date", "celex_number", "link",])
    
    # crap last page number
    page = requests.get(search_result_link)
    soup = BeautifulSoup(page.content, "html.parser")
    last_page = get_last_page_link(soup)
    last_page = int(last_page.split("page=")[1])
    print("last page is the:", last_page)
    # iterate throught all pages in the searchresult
    for page_number in range (1, last_page):
        print(f"get page  {page_number} of {last_page}")
        result_page = str(search_result_link[:-1]) + str(page_number)
        # print("result_page",result_page)
        if str(search_result_link[:-1]) != "1":
            result_page = str(search_result_link).replace("page=1", "") + "&page=" + str(page_number)
        # print("result_page",result_page)
        result_page = requests.get(result_page)
        soup = BeautifulSoup(result_page.content, "html.parser")
        print(f"Page has: {len(soup.text)} characters")
        result_links = soup.find_all("a", class_="piwik_download")
        result_titles = soup.find_all("a", class_="title")
        titl = []
        for p in result_titles:
                titl.append(p.get_text())
        # print("result_links",result_links)
        result_titles = titl
        links, texts, clex = download_site_links(result_links)
        
        texts_cleand = [extract_date_clean_text(text)[0] for text in texts ] 
        dates =  [extract_date_clean_text(text)[1] for text in texts ]
        
        result_df= pd.concat([result_df, pd.DataFrame(list(zip(result_titles, texts_cleand, dates, clex, links)), columns = ["title", "text", "date", "celex_number", "link",])], ignore_index=True)
        # if page_number == last_page:
        #     return result_df
    return result_df


import time
start_time = time.time()
res_link2 = "https://eur-lex.europa.eu/search.html?SUBDOM_INIT=LEGISLATION&orDC_DOM_CODED=DC_TT_CODED%3D5360%2CDC_TT_CODED%3D4630%2CDC_TT_CODED%3D2551%2CDC_TT_CODED%3D2493%2CDC_TT_CODED%3D1063%2CDC_TT_CODED%3D1360%2CDC_TT_CODED%3D6052%2CDC_TT_CODED%3D2723%2CDC_TT_CODED%3D651%2CDC_TT_CODED%3D1115%2CDC_TT_CODED%3D1258%2CDC_TT_CODED%3D2763%2CDC_TT_CODED%3D2443%2CDC_TT_CODED%3D1277%2CDC_TT_CODED%3D2442%2CDC_TT_CODED%3D711%2CDC_TT_CODED%3D656%2CDC_TT_CODED%3D239%2CDC_TT_CODED%3D6788%2CDC_TT_CODED%3D5017%2CDC_TT_CODED%3D5877%2CDC_TT_CODED%3D937%2CDC_TT_CODED%3D2505%2CDC_TT_CODED%3D4363%2CDC_TT_CODED%3D1602%2CDC_TT_CODED%3D2416%2CDC_TT_CODED%3D2735%2CDC_TT_CODED%3D2734%2CDC_TT_CODED%3D2711%2CDC_TT_CODED%3D2414%2CDC_TT_CODED%3D2413%2CDC_TT_CODED%3D2412%2CDC_TT_CODED%3D2775%2CDC_TT_CODED%3D2477%2CDC_TT_CODED%3D2972%2CDC_TT_CODED%3D962%2CDC_TT_CODED%3D2014%2CDC_TT_CODED%3D5962%2CDC_TT_CODED%3D4412%2CDC_TT_CODED%3D4358%2CDC_TT_CODED%3D4314%2CDC_TT_CODED%3D4416%2CDC_TT_CODED%3D2814%2CDC_TT_CODED%3D2418%2CDC_TT_CODED%3D2737%2CDC_TT_CODED%3D3605%2CDC_TT_CODED%3D2417%2CDC_TT_CODED%3D2736&DTS_SUBDOM=LEGISLATION&DTS_DOM=EU_LAW&page=1&type=advanced&lang=en&date0=ALL%3A01012000%7C01012020&qid=1699299902519&wh0=andCOMPOSE%3DENG%2CorEMBEDDED_MANIFESTATION-TYPE%3Dpdf%3BEMBEDDED_MANIFESTATION-TYPE%3Dpdfa1a%3BEMBEDDED_MANIFESTATION-TYPE%3Dpdfa1b%3BEMBEDDED_MANIFESTATION-TYPE%3Dpdfa2a%3BEMBEDDED_MANIFESTATION-TYPE%3Dpdfx%3BEMBEDDED_MANIFESTATION-TYPE%3Dpdf1x%3BEMBEDDED_MANIFESTATION-TYPE%3Dhtml%3BEMBEDDED_MANIFESTATION-TYPE%3Dxhtml%3BEMBEDDED_MANIFESTATION-TYPE%3Ddoc%3BEMBEDDED_MANIFESTATION-TYPE%3Ddocx"
df =crap_search_result(res_link2)
end_time = time.time()

# Calculate the duration
duration = end_time - start_time

print("Time taken by the function: {:.2f} seconds".format(duration))







###### Saving file  ############


## Name of your csv file
path="test.csv"
df.to_csv(path, sep='|')


###### Loading file ################
path="test.csv"
df=pd.read_csv(path, sep='|')



## Change the format of date
df['date'] = pd.to_datetime(df['date'], format='%d.%m.%Y', errors='coerce')
##  Drop the dates rows ,  where data is not in the correct format
df = df.dropna(subset=['date'])
## Dropping unwanted columns ######
df_cleaned = df.drop(columns=['Unnamed: 0'])

## Sorting the dataset
df_sorted = df_cleaned.sort_values(by='column', ascending=True)


## saving cleaend and sorted dataset
path="clean_sorted.csv"
df_sorted.to_csv(path, sep='|')