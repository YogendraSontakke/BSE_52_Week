#standard
import sys
#standard addon
import requests
from requests import Session

def get_html_data(i_url, params={},headers={}):
    try:        
        response = requests.request('GET', i_url, params=params, headers=headers)
    except requests.HTTPError as e:        
        print e
        return None
    except requests.ConnectionError as e:
        print e        
        return None
    except:
        print sys.exc_info()
        return None
    if response.ok == False:
        print response.content
        return None
    if len(response.content) == 0:
        return None
    html = response.content
    response.close()
    return html

def session_get(i_url, params={},headers={}):
    session = Session()
    try:        
        response = session.get(i_url, params=params, headers=headers)
    except requests.HTTPError as e:        
        print e
        return None
    except requests.ConnectionError as e:
        print e
        return None
    except:
        print sys.exc_info()
        return None
    if response.ok == False:
        print response.content
        return None
    if len(response.content) == 0:
        return None
    content = response.content
    response.close()
    return content

    
def post_request(i_url, data={}):
    try:   
        response = requests.post(i_url, data)   
    except requests.HTTPError as e:
        print e
        return None
    except requests.ConnectError as e:
        print e
        return None    
    if response.ok == False:
        print response.content
        return None
    if len(response.content) == 0:
        return None
    data = response.content
    response.close()    
    return data

    