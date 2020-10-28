import requests

base_url = 'http://localhost:8000'


def add_gridfs_file():
    url = base_url + '/test/gridfs'
    resp = requests.post(url)
    print(resp.text)


if __name__ == '__main__':
    add_gridfs_file()
