class AttributeAccessor:
    def __init__(self, src_dict):
        self.dict = src_dict

    def __getattr__(self, item):
        result = self.dict.get(item)
        if isinstance(result, dict):
            return AttributeAccessor(result)
        return result
