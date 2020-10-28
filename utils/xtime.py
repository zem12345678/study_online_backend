from datetime import datetime


# 日期时间转换成时间字符串
def datetime2timestring(src_datetime, formatter=None, with_time=True):
    if formatter is None:
        formatter = '%Y-%m-%d'
        if with_time:
            formatter += ' %H:%M:%S'
    return datetime.strftime(src_datetime, formatter)
