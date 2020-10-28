import jinja2
from cms.models import CmsPage, CmsTemplate
from common import response_code
from utils import xrequests


# 根据page_id获取数据模型
def get_model_by_page_id(page_id):
    # 获取cms_page数据
    cms_page = CmsPage.find_by_id(page_id)
    if cms_page is None:
        return 1, response_code.CMS_PAGE_NOTEXISTS
    # 根据data_url请求远端接口，获取数据模型
    data_url = cms_page.dataUrl
    if not data_url:
        return 1, response_code.CMS_GENERATEHTML_DATAISNULL
    return 0, xrequests.HTTPRequest(data_url).get()


# 根据page_id获取模板
def get_template_by_page_id(page_id):
    cms_page = CmsPage.find_by_id(page_id)
    if cms_page is None:
        return 1, response_code.CMS_PAGE_NOTEXISTS
    cms_template = cms_page.templateId
    if not cms_template:
        return 1, response_code.CMS_GENERATEHTML_TEMPLATEISNULL
    template_file = cms_template.templateFileId
    if not template_file:
        return 0, ''
    file_content = template_file.read()
    if file_content:
        file_content = file_content.decode()
    return 0, file_content


# 执行静态化
def generate_html(template, model):
    _template = jinja2.Template(template)
    html = _template.render(**model)
    return html


def get_page_html(page_id):
    # 获取数据模型
    status, model = get_model_by_page_id(page_id)
    if status == 0 and model.get('success'):
        model = model.get('data')
    else:
        return 1, response_code.CMS_GENERATEHTML_DATAISNULL
    # 获取模板
    status, template = get_template_by_page_id(page_id)
    if status != 0 or not template:
        return 1, response_code.CMS_GENERATEHTML_TEMPLATEISNULL
    # 执行静态化
    html = generate_html(template, model)
    return 0, html


def save_html(page_id, page_html):
    # 获取页面数据
    cms_page = CmsPage.find_by_id(page_id)
    if cms_page is None:
        return 1, response_code.INVALID_PARAM
    # 将page_html保存到cms_page的htmlFileId中
    cms_page.htmlFileId.new_file(encoding='utf8')
    cms_page.htmlFileId.write(page_html)
    cms_page.htmlFileId.close()
    cms_page.save()
    return 0, cms_page


if __name__ == '__main__':
    from cz_study.settings import connect
    status, html = get_page_html('5d7764e96f163a20e7ca0321')
    print(status)
    print(html)
