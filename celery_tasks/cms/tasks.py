import os
from celery_tasks.main import app
from cms.models import CmsPage


@app.task(bind=True, name='post_page')
def post_page(self, page_id):
    # 获取页面信息
    cms_page = CmsPage.find_by_id(page_id)
    # 读取页面html文件
    html_file = cms_page.htmlFileId
    input_stream = html_file.read()
    # 从页面对应站点中获取页面存储的根路径
    site_physical_path = cms_page.siteId.sitePhysicalPath
    # 拼接页面保存路径，将页面保存到指定的路径
    page_path = site_physical_path + cms_page.pagePhysicalPath+cms_page.pageName
    if not os.path.exists(os.path.dirname(page_path)):
        os.makedirs(os.path.dirname(page_path))
    with open(page_path, 'wb+') as file:
        file.write(input_stream)


