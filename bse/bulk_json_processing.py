#standard
import subprocess
import sys
from multiprocessing import Pool as ProcessPool

def get_data(file):    
    subprocess.call(["D:/Python27/python.exe ./mc.py", file])    
    print file

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print "Usage: bulk_json_processing.py <dir>"
        exit(-1)
    files = subprocess.check_output(["ls", sys.argv[1] + "*.json"])
    for file in files:
        subprocess.call(["D:/Python27/python.exe ./mc.py", file])    
