import requests
base_url = 'http://localhost:8000'


def add_cms_page():
    url = base_url + '/cms/page/add'
    resp = requests.post(url, json={
      "dataUrl": "string",
      "pageAlias": "string",
      "pageName": "测试页面111",
      "pagePhysicalPath": "string",
      "pageStatus": "string",
      "pageType": "string",
      "pageWebPath": "string",
      "siteId": "5a751fab6abb5044e0d19ea1",
      "templateId": "5a925be7b00ffc4b3c1578b5"
    })
    print(resp.json())


def update_cms_page():
    url = base_url + '/cms/page/edit/5d7764e96f163a20e7ca031f'
    resp = requests.put(url, json={
        "siteId": "5a751fab6abb5044e0d19ea1",
        "pageAlias": "修改后的页面别名",
        "pageName": "修改后的页面名称",
        "pageWebPath": "string",
        "pagePhysicalPath": "string",
        "pageType": "1",
        "pageStatus": "string",
        "templateId": "5a962bf8b00ffc514038fafa",
        "dataUrl": "string"
    })
    print(resp.json())


def delete_cms_page():
    url = base_url + '/cms/page/del/5d7764e96f163a20e7ca031f'
    resp = requests.delete(url)
    print(resp.json())


if __name__ == '__main__':
    # add_cms_page()
    # update_cms_page()
    delete_cms_page()
