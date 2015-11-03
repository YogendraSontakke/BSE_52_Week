#standard
import sys
import json
from multiprocessing.dummy import Pool as ThreadPool
from multiprocessing import Pool as ProcessPool
import datetime
import subprocess
#standard addon
from bs4 import BeautifulSoup
#local
import get_post_services as gps

# Debug Flags : Start
debug = True
single_thread = False    
# Debug Flags : End

def print_dump_array(i_array, i_input_json_name):
    column_header = ['Security_Code', 'Market_Cap', 'Debt_to_Equity', 'RoCE', 'RoNW', 'Operating_Profit_per_share', 'Secutity_Id']
    i_input_json_name = i_input_json_name.replace('\\','/')
    path_split = i_input_json_name.split('/')
    ouput_file_name = "/".join(path_split[:-1]) + "/csv/" + path_split[-1] + '.csv'    
    fp = open(ouput_file_name, 'w')
    fp.write(", ".join(column_header) + '\n')
    for elems in i_array:        
        if elems is not None:
            fp.write(", ".join(elems) + '\n')
    fp.close()

def find_elem_in_soup(soup_for_ratios, iText):
    elements = [e for e in soup_for_ratios.find_all('td',attrs={'class':'det'}) if e.text == iText]    
    for e in elements:
        return e.find_next_sibling().text    
    return None

def debug_dump(error_text, i_company_info):
    if True == debug:
        fp = open("./log/error.log", 'a')        
        fp.write( error_text +"\t" + " ".join(i_company_info) + "\n" )
        fp.close()

def dump_url(url):
    if True == debug:
        fp = open('./log/link.txt','a')
        fp.write(url + '\n')
        fp.close()
        
def parse_the_ratios_page(html_for_ratios, parser):
    soup_for_ratios = BeautifulSoup(html_for_ratios, parser)
    RoCE_text = 'Return On Capital Employed(%)'
    debt_to_equity_text = 'Debt Equity Ratio'
    RoNW_text = 'Return On Net Worth(%)'
    operating_profit_per_share_text = 'Operating Profit Per Share (Rs)'
    debt_to_equity = find_elem_in_soup(soup_for_ratios, debt_to_equity_text)
    RoCE = find_elem_in_soup(soup_for_ratios, RoCE_text)
    RoNW = find_elem_in_soup(soup_for_ratios, RoNW_text)
    operating_profit_per_share = find_elem_in_soup(soup_for_ratios, operating_profit_per_share_text)    
    if debt_to_equity is None:        
        return None
    return {'debt_to_equity' : debt_to_equity, 'RoCE' : RoCE, 'RoNW' : RoNW, 'operating_profit_per_share' : operating_profit_per_share}

def get_ratios(ratio_urls):
    ratios = {}
    for url in ratio_urls:
        html_for_ratios = gps.get_html_data(url)
        if html_for_ratios is None:
            continue        
        parsers = ['html.parser', 'lxml', 'html5lib']
        for parser in parsers:
            ratios = parse_the_ratios_page(html_for_ratios, parser)
            if ratios is not None:
                break
    return ratios

def get_company_names_for_url(search_keywords):
    url = 'http://www.moneycontrol.com/stocks/cptmarket/compsearchnew.php'
    data = {
        'search_data' : '',
        'cid' : '',
        'mbsearch_str' : '',
        'topsearch_type' : '1',
        'search_str': ''
    }
    for keyword in search_keywords:
        data['search_str'] = keyword
        html = gps.get_html_data(url, params=data)
        soup = BeautifulSoup(html, 'lxml')
        standalone = soup.find(attrs={'class':'home act'})
        if standalone is not None:
            break
    if standalone is None:
        return None
    return standalone
    
    
def get_mc(i_company_info):
    search_keywords = [i_company_info[0]]
    if len(i_company_info) == 4:
        search_keywords.append(i_company_info[3]) 
        
    standalone = get_company_names_for_url(search_keywords)
    if standalone is None:    
        debug_dump("HTML Error:- Could not get the monecontrol page. ", i_company_info)
        return None
    key_variables = standalone.a.get('href').split('/')[-2:]
    # example urls as below:
    #   http://www.moneycontrol.com/financials/aiaengineering/ratios/AIE01#AIE01
    #   http://www.moneycontrol.com/financials/fluidomat/ratios/F02#F02  
    #   http://www.moneycontrol.com/financials/arrowcoated/consolidated-ratios/ACP
    url_for_ratios_consolidated = 'http://www.moneycontrol.com/financials/' + key_variables[0] + '/consolidated-ratios/' + key_variables[1]     
    url_for_ratios = 'http://www.moneycontrol.com/financials/' + key_variables[0] + '/ratios/' + key_variables[1] + '#' + key_variables[1]
    ratio_urls = []
    ratio_urls.append(url_for_ratios_consolidated)
    ratio_urls.append(url_for_ratios)
    ratios = get_ratios(ratio_urls)
    if ratios is None:        
        debug_dump("Ratio Error:- Could not get the ratio debt to equity. ", i_company_info)
        dump_url(url_for_ratios_consolidated)
        dump_url(url_for_ratios)
        return None    
    company_details = [i_company_info[0], i_company_info[1]] # Security Code, Market Cap
    encoding = 'ascii'
    action = 'ignore'
    company_details.append(ratios['debt_to_equity'].encode(encoding, action).replace(',', '')) #debt_to_equity
    company_details.append(ratios['RoCE'].encode(encoding, action).replace(',', '')) #RoCE
    company_details.append(ratios['RoNW'].encode(encoding, action).replace(',', '')) #RoNW
    company_details.append(ratios['operating_profit_per_share'].encode(encoding, action).replace(',', '')) #operating_profit_per_share
    company_details.append( i_company_info[2]) 
    return company_details

def read_json(i_json):
    if len(i_json) < 1:
        return None
    companies_data = json.load(open(i_json))  
    print 'Total Companies\t',len(companies_data)    
    if single_thread == True:
        results = []
        for company_data in companies_data:
            results.append(get_mc(company_data))
    else:
        threadpool = ThreadPool(8)
        results = threadpool.map(get_mc, companies_data)
        threadpool.close()
        threadpool.join()    

    print_dump_array(results, i_json)
    
if __name__ == '__main__':
    if len(sys.argv) != 2 and len(sys.argv) != 3:
        print "Usage: moneycontrol.py <json> <optional: input is directory>"
        exit(-1)
    del sys.argv[0]
    start = datetime.datetime.now()
    if len(sys.argv) == 1:
        read_json(sys.argv[0])
    else:
        files = subprocess.check_output(["ls", sys.argv[0] + "*.json"]).split('\r\n')
        pool = ProcessPool(8)
        pool.map(read_json, files)
        pool.close()
        pool.join()
    end = datetime.datetime.now()
    print end-start
