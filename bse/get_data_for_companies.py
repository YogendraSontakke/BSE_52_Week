#standard
import datetime
from multiprocessing.dummy import Pool as ThreadPool
import json
import sys
#local
import mc
import bse
import get_post_services as gps

def get_security_code_vs_data_dict(i_data):
    security_codes_vs_data = {}
    for line in i_data.split('\n'):
        line_data_array = line.split(',')
        if True == line_data_array[0].isdigit():            
            security_codes_vs_data[line_data_array[0]] = line_data_array[1:]
    return security_codes_vs_data

def write_output(i_sorted_security_code_vs_market_cap_and_name, output_json_folder):
    combined_data = []
    for security, mc in i_sorted_security_code_vs_market_cap_and_name:
        line = security + ' '+ str(mc[0]).rjust(11) + ' ' + mc[1] + ' ' + mc[2]
        line_array = [security] + mc
        print line_array
        combined_data.append(line_array)    
    json_file = output_json_folder + '/' + str(datetime.datetime.now()).replace(':','_').replace(' ','__') + '.json'
    fp = open(  json_file, 'wb')
    json.dump(combined_data,fp)
    fp.close()
    return json_file
    
def main(output_json_folder):
    data = bse.data_52_week_high()
    security_codes_vs_data = get_security_code_vs_data_dict(data)
    
    security_code_vs_market_cap_and_name = {}    
    p = ThreadPool(len(security_codes_vs_data.keys()))    
    results = p.map(bse.get_market_cap_and_name, security_codes_vs_data.keys()) 
    p.close()
    p.join()
    
    security_id_and_codes = []
    
    for tup in results:
        security_code_vs_market_cap_and_name[tup[0]] = tup[1:]  + [security_codes_vs_data[tup[0]][0]]
        security_id_and_codes.append( (security_codes_vs_data[tup[0]][0], tup[0]))
    func = lambda x : float(x[1][0])
    sorted_security_code_vs_market_cap_and_name = sorted(security_code_vs_market_cap_and_name.items(), key=func)
    json_file = write_output(sorted_security_code_vs_market_cap_and_name, output_json_folder)    
    mc.read_json(json_file) # creates csv

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print "Usage: get_data_for_companies.py <output_json_folder>"
        exit(-1)
    start = datetime.datetime.now()
    del sys.argv[0]
    main(sys.argv.pop())
    end = datetime.datetime.now()
    print end-start

    
'''
def get_company_data(i_security_id_and_code):    
    url_pre = 'https://www.screener.in/api/company/' + i_security_id_and_code[0] + '/'
    pythonic_data = gps.get_html_data(url_pre)
    if pythonic_data is None:                
        url_pre = 'https://www.screener.in/api/company/' + i_security_id_and_code[1] + '/'
        pythonic_data = gps.get_html_data(url_pre)

    return [i_security_id_and_code[1], pythonic_data]
       
def get_data_from_Screener(i_security_id_and_codes):
    results = []
    for sec_id_and_code in i_security_id_and_codes:
        session = Session()
        url = 'https://www.screener.in/login/'
        response_login = session.get(url)
        url_pre = 'https://www.screener.in/api/company/' + sec_id_and_code[0] + '/'
        pythonic_data = session.get(url_pre)
        if pythonic_data is None:                
            url_pre = 'https://www.screener.in/api/company/' + sec_id_and_code[1] + '/'
            pythonic_data = session.get(url_pre)
        session.close()
        print sec_id_and_code
        results.append([sec_id_and_code[1], pythonic_data.content])
    return results
    '''
    