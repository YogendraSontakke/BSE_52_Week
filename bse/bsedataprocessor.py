import get_data_for_companies
import combine_jsons_in_one
import sys

def main():
    if len(sys.argv) != 3:
        print "Usage: bsedataprocessor.py <json_daily_folder> <consolidated_output_folder>"
        exit(-1)

    del sys.argv[0]
    json_consolidated_folder = sys.argv.pop()
    json_daily_folder = sys.argv.pop()   
    
    get_data_for_companies.get_todays_high_data(json_daily_folder)
    combine_jsons_in_one.combine_and_process_json(json_daily_folder, json_consolidated_folder)

if __name__ == '__main__':
    main()