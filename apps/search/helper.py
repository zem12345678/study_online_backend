from elasticsearch import Elasticsearch


# ESClient基类
class BaseESClient:
    es = None

    def __init__(self, index_name, doc_type='doc'):
        """指定索引名和文档类型，初始化es实例"""
        self.index_name = index_name
        self.doc_type = doc_type
        if self.es is None:
            self.es = Elasticsearch(['localhost:9200/'])

    def get_mapping_properties(self):
        """获取字段映射属性"""
        raise NotImplementedError

    def create_index(self):
        """创建索引"""
        self.es.indices.create(index=self.index_name, ignore=400, body={
            "mappings": {
                self.doc_type: {
                    "properties": self.get_mapping_properties()
                }
            }
        })

    def get_query_dicts(self, *args, **kwargs):
        """获取搜索条件，需要覆写该方法"""
        raise NotImplementedError

    def get_search_body(self, *args, **kwargs):
        """获取搜索条件体，统一使用bool查询，使用page和size指定分页"""
        search_body = {'query': {'bool': {'must': self.get_query_dicts(*args, **kwargs)}}}
        page = kwargs.get('page')
        size = kwargs.get('size')
        if page is not None and size:
            search_body['from'] = (page-1) * size
            search_body['size'] = size
        return search_body

    def get_search_result(self, res):
        """
        获取搜索结果
        :return:  {
            total: 结果总数，
            hits: 搜索结果列表
        }
        """
        total = res['hits']['total']
        result = {'total': total, 'hits': []}
        for hit in res['hits']['hits']:
            result['hits'].append(hit['_source'])
        return result

    def search(self, *args, **kwargs):
        """
        执行搜索，并返回搜索结果，搜索条件通过kwargs传入，支持page和size分页
        :return:  {
            total: 结果总数，
            hits: 搜索结果列表
        }
        """
        body = self.get_search_body(*args, **kwargs)
        res = self.es.search(index=self.index_name, body=body)
        return self.get_search_result(res)


# ESClient类
class ESClient(BaseESClient):
    def get_mapping_properties(self):
        """获取字段映射属性"""
        return {
            "charge": {"type": "keyword"},
            "description": {"analyzer": "ik_max_word", "search_analyzer": "ik_smart", "type": "text"},
            "end_time": {"format": "yyyy-MM-dd HH:mm:ss||yyyy-MM-dd'T'HH:mm:ss.SSSSSS", "type": "date"},
            "expires": {"format": "yyyy-MM-dd HH:mm:ss||yyyy-MM-dd'T'HH:mm:ss.SSSSSS", "type": "date"},
            "grade": {"type": "keyword"},
            "id": {"type": "keyword"},
            "mt": {"type": "keyword"},
            "name": {"analyzer": "ik_max_word", "search_analyzer": "ik_smart", "type": "text"},
            "pic": {"index": False, "type": "keyword"},
            "price": {"type": "float"},
            "price_old": {"type": "float"},
            "pub_time": {"format": "yyyy-MM-dd HH:mm:ss||yyyy-MM-dd'T'HH:mm:ss.SSSSSS", "type": "date"},
            "qq": {"index": False, "type": "keyword"},
            "st": {"type": "keyword"},
            "start_time": {"format": "yyyy-MM-dd HH:mm:ss||yyyy-MM-dd'T'HH:mm:ss.SSSSSS", "type": "date"},
            "status": {"type": "keyword"},
            "studymodel": {"type": "keyword"},
            "teachmode": {"type": "keyword"},
            "teachplan": {"analyzer": "ik_max_word", "search_analyzer": "ik_smart", "type": "text"},
            "users": {"index": False, "type": "text"},
            "valid": {"type": "keyword"}
        }

    def get_query_dicts(self, *args, **kwargs):
        """获取搜索条件，需要覆写该方法"""
        result = []
        query_string = kwargs.get('query_string')
        grade = kwargs.get('grade')
        mt = kwargs.get('mt')
        st = kwargs.get('st')
        course_id = kwargs.get('course_id')
        if course_id:
            result.append({'match': {'id': course_id}})
        if query_string:
            result.append({'query_string': {'query': 'name:{q} description:{q}'.format(**{'q': query_string})}})
        if grade:
            result.append({'match': {'grade': grade}})
        if mt:
            result.append({'match': {'mt': mt}})
        if st:
            result.append({'match': {'st': st}})
        return result


class MediaESClient(BaseESClient):
    def get_mapping_properties(self):
        """获取字段映射属性"""
        return {
            "courseid": {"type": "keyword"},
            "teachplan_id": {"type": "keyword"},
            "media_id": {"type": "keyword"},
            "media_url": {"index": False, "type": "text"},
            "media_fileoriginalname": {"index": False, "type": "text"}
        }

    def get_query_dicts(self, *args, **kwargs):
        """获取搜索条件，需要覆写该方法"""
        result = []
        teachplan_id = kwargs.get('teachplan_id')
        if teachplan_id:
            result.append({'match': {'teachplan_id': teachplan_id}})
        return result


if __name__ == '__main__':
    r = ESClient('cz_course').search(query_string='redis', page=1, size=2)
    print('total ', r['total'])
    for i in r['hits']:
        print(i)
