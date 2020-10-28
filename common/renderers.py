from rest_framework.renderers import JSONRenderer
from common.response_code import SUCCESS


class StandardJSONRender(JSONRenderer):

    def render(self, data, accepted_media_type=None, renderer_context=None):
        data = {} if data is None else data
        if isinstance(data, dict) and data.get('success') is not None:
            standard_data = data
        else:
            standard_data = {'success': SUCCESS[0], 'code': SUCCESS[1], 'message': SUCCESS[2], 'data': data}

        return super().render(standard_data, accepted_media_type=accepted_media_type, renderer_context=renderer_context)
