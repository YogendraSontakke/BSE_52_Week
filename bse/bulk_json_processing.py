#standard
import subprocess
import sys
from multiprocessing import Pool as ProcessPool
#locals
import mc

def get_data(file):    
    subprocess.call(["D:/Python27/python.exe ./mc.py", file])    
    print file

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print "Usage: bulk_json_processing.py <dir>"
        exit(-1)
    folder_path = sys.argv[1].replace('\\','/')
    files = subprocess.check_output(["ls", folder_path + '/' + "*.json"])
    for file in files.split('\r\n'):
        if len(file) > 0:
            mc.read_json(file)
