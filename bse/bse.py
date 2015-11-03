from bs4 import BeautifulSoup
import get_post_services

def data_52_week_high():
    data = post_download_button_data()
    high_html = get_52_week_high_html()
    data.update(get_viewstate_and_eventvalidation(high_html))
    #52 week high data
    url = 'http://www.bseindia.com/markets/equity/EQReports/HighLow.aspx?expandable=2'
    high_data = None
    while high_data is None:
        high_data = get_post_services.post_request(url, data)
    return high_data
    
def data_52_week_low():
    data = post_download_button_data()
    low_html = get_52_week_low_html()
    #52 week low data    
    data.update(get_viewstate_and_eventvalidation(low_html))
    
    url = 'http://www.bseindia.com/markets/equity/EQReports/HighLow.aspx?expandable=2'
    low_data = None
    while low_data is None:
        low_data = get_post_services.post_request(url, data)
    return low_data    

def get_market_cap_and_name(i_security_code):    
    url = 'http://www.bseindia.com/stock-share-price/SiteCache/Stock_Trading.aspx'
    data = {
         'Type' : 'EQ',
         'text' : i_security_code
         }
    headers = {
        'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:41.0) Gecko/20100101 Firefox/41.0',
        'Accept' : 'text/html, */*; q=0.01',
        'X-Requested-With' : 'XMLHttpRequest',
        'Referer' : ''
    }
    headers['Referer'] = get_requester_url(i_security_code)
    
    html = get_post_services.get_html_data(url, params=data, headers=headers)
    while html is None:
        html = get_post_services.get_html_data(url, params=data, headers=headers)
    soup = BeautifulSoup(html, 'lxml')    
    
    return [i_security_code, soup.find(id='ehd6')['value'].replace(',','').replace('-','0'), headers['Referer'].split('/')[4]]

def get_52_week_high_html():
    #52 week high html
    url = 'http://www.bseindia.com/markets/equity/EQReports/HighLow.aspx?expandable=2'
    high_html = None
    while  high_html is None:
        high_html = get_post_services.get_html_data(url)
    return high_html

def get_52_week_low_html():
    high_html = get_52_week_high_html()
    #52 week low html
    data = post_52_week_low_data()
    data.update(get_viewstate_and_eventvalidation(high_html))    

    url = 'http://www.bseindia.com/markets/equity/EQReports/HighLow.aspx?expandable=2'
    low_html = None
    while low_html is None:
        low_html = get_post_services.post_request(url, data)
    return low_html

def get_requester_url(i_security_code):    
    url = 'http://www.bseindia.com/SiteCache/1D/GetQuoteData.aspx'
    data = {
             'Type' : 'EQ',
             'text' : i_security_code
             }
    html = get_post_services.get_html_data(url, params=data)
    while html is None:
        html = get_post_services.get_html_data(url, params=data)

    soup = BeautifulSoup(html, 'lxml')        
    tag = soup.find('a')
    
    if tag is None:
        data['Type'] = 'MF'
        html = get_post_services.get_html_data(url, params=data)    
        while html is None:
            html = get_post_services.get_html_data(url, params=data)    
        soup = BeautifulSoup(html, 'lxml')
        tag = soup.find('a')
        
    return tag['href']    

def get_viewstate_and_eventvalidation(i_html):
    '''
    '__VIEWSTATE'
    '__EVENTVALIDATION'    
    '''
    soup = BeautifulSoup(i_html, 'html.parser')    
    data = {
        '__VIEWSTATE' : soup.find(id="__VIEWSTATE")['value'],
        '__EVENTVALIDATION' : soup.find(id="__EVENTVALIDATION")['value'],
    }
    return data
        

def post_download_button_data():
    data = {
        'ctl00$ContentPlaceHolder1$btnDownload.x':'9',
        'ctl00$ContentPlaceHolder1$btnDownload.y':'8'
    }    
    data.update(post_common_data())
    return data
    

def post_52_week_high_data():
    data = {
        '__EVENTTARGET' : 'ctl00$ContentPlaceHolder1$lnkHigh'
    }
    data.update(post_common_data())
    return data
    
def post_52_week_low_data():
    data = {
        '__EVENTTARGET' :	'ctl00$ContentPlaceHolder1$lnkLow'
    }
    data.update(post_common_data())
    return data
    
def post_common_data():
    data = {
        '__VIEWSTATEGENERATOR':'40927446',
        '__EVENTARGUMENT':'',
        'myDestination':'#',
        'WINDOW_NAMER':'1',        
        'ctl00$ContentPlaceHolder1$hdnCode':'',
        'ctl00$ContentPlaceHolder1$hdnScrip':'',        
        'ctl00$ContentPlaceHolder1$chk':'rdnScrip',
        'ctl00$ContentPlaceHolder1$Hidden1':'',	
        'ctl00$ContentPlaceHolder1$GetQuote1_smartSearch':'Enter Security Name / Code / ID',
        'ctl00$ContentPlaceHolder1$ddlType':'AllMkt',
        'ctl00$ContentPlaceHolder1$ddlGrp':'A',
        'ctl00$ContentPlaceHolder1$ddlIndx':'S&P BSE SENSEX'
    }
    return data
