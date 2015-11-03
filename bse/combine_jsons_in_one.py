import json
import datetime
import os
import mc
import sys

def process_combine(i_combined, json_consolidated_folder):
    data_map = {}    
    for company_data in i_combined:        
        if company_data[0] in data_map and float(data_map[company_data[0]][1]) < float(company_data[1]):
            data_map[company_data[0]][1] = company_data[1]
        else:
            data_map[company_data[0]] = company_data
    filename = json_consolidated_folder + '/' + str(datetime.datetime.now()).replace(':','_').replace(' ', '__') + '.json'
    func = lambda x : float(x[1])
    fp = open(filename, 'wb')
    json.dump(sorted(data_map.values(),key=func), fp)
    fp.close()
    return filename    

def combine_company_json(json_daily_folder):    
    files = [x for x in os.listdir(json_daily_folder) if -1 != x.find('.json') and -1 == x.find('.json.')]
    combined_company = []
    for file in files:
        print file
        fp = open(json_daily_folder + '/' + file,'rb')
        try:
            data_array = json.load(fp)
        except ValueError as e:
            pass
        fp.close()
        combined_company = combined_company + data_array
    return combined_company
    
def main():
    if len(sys.argv) != 3:
        print "Usage: combine_jsons_in_one.py <json_input_folder> <consolidated_output_folder>"
        exit(-1)
    del sys.argv[0]
    json_consolidated_folder = sys.argv.pop()
    json_daily_folder = sys.argv.pop()    
    combined_company = combine_company_json(json_daily_folder)
    json_file = process_combine(combined_company, json_consolidated_folder)
    mc.read_json(json_file) # creates csv
    
if __name__ == '__main__':
    main()
