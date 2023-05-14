import requests
import bs4
import urllib.parse



def key_to_text(words):
    encoded_word = urllib.parse.quote(words.encode('utf-8'))
    url = f'https://www.donga.com/news/search?query={encoded_word}&check_news=91%7C4%7C5%7C92&sorting=1&search_date=1&v1=&v2=&more='
    # data = query=%EA%B2%BD%EC%A0%9C+%EC%A0%84%EB%A7%9D+%ED%95%9C%EA%B5%AD&check_news=91%7C4%7C5%7C92&sorting=1&search_date=1&v1=&v2=&more=
    data = {
    "query": "경제 전망 한국",
    "check_news": "91|4|5|92",
    "sorting": "1",
    "search_date": "1",
    "v1":"", 
    "v2":"", 
    "more":"" 
    }

    temp = requests.get(url)#, data=data)
    temp =  bs4.BeautifulSoup(temp.content, 'html.parser')
    divs = temp.find_all('div', {'class':'articleList'})

    url_list = []
    result_list = []
    text0 = ""
    for div in divs[:3]:  
        line = div.find_all('span', {'class':'tit'})[0].find_all('a')[0]
        print(line['href'])
        print(line['data-ep_button_name'])
        url_list.append(line['href'])
        result_list.append((line['href'], line['data-ep_button_name']))

    for url0 in url_list:
        # print(url0)
        temp0 = requests.get(url0)
        temp0 = bs4.BeautifulSoup(temp0.content, 'html.parser')

        article = temp0.find_all('div', {'id':'article_txt'})
        if article !=[]:
            article = article[0]
            for i in ['articlePhotoC', 'article_footer']:
                div_to_delete = article.find('div', {'class': i})
                if div_to_delete != None:
                    div_to_delete.extract()
            temp_ar = article.text.replace('\n\n','\n').replace('\n\n','\n')
            if len(text0) + len(temp_ar) <3000:
                text0 += temp_ar +'===================='
    return text0, result_list