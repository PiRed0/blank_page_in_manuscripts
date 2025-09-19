import re
import requests
import urllib.request as urlrq



def page_number_to_str(i):
    '''
    int -> str
    Require: i < 1000
    Returns the string which corresponds to i with three digits
    '''
    if i < 10:
        return '00' + str(i)
    elif i < 100:
        return '0' + str(i)
    return str(i)
    

def download_file(url, path_dst):
    '''
    str * str -> None
    Downloads the image file at the url in the path_dst directory
    '''
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }
    with requests.get(url, headers=headers, stream=True) as response:
        response.raise_for_status()
        with open(path_dst, 'wb') as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)
            file.close()


def get_number_pages(url):
    '''
    str -> int
    Returns the number of pages of a manuscript given its Gallica url
    If this number of pages couldn't be found returns -1
    '''
    page = urlrq.urlopen(url)

    view = re.search('vue 1/\d+', str(page.read()))
    if view:
        split_view = re.split('/', view.group(0))
        if len(split_view) == 2:
            return int(split_view[1])
    return -1