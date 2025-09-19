import re


def get_file_name(path):
    '''
    str -> str
    '''
    return re.search('[a-z]+_\d+\-\w+\d*[rv]*', path).group(0)


def get_page_name(path):
    '''
    str -> str
    '''
    return re.sub('[_-]', ' ', path)