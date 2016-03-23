# coding:utf-8
# project/furniture/apis.py
from qiniu import Auth, put_data, BucketManager


class Page(object):
    def __init__(self, item_count, page_index=1, page_size=10):
        self.item_count = item_count
        self.page_size = page_size
        self.page_count = item_count // page_size + (1 if item_count % page_size > 0 else 0)
        if (item_count == 0) or (page_index > self.page_count):
            self.offset = 0
            self.limit = 0
            self.page_index = 1
        else:
            self.page_index = page_index
            self.offset = self.page_size * (page_index - 1)
            self.limit = self.page_size
        self.has_next = self.page_index < self.page_count
        self.has_previous = self.page_index > 1
        if self.page_count > 10:
            self.button_num = 10
        else:
            self.button_num = self.page_count

    def __str__(self):
        return 'item_count: %s, page_count: %s, page_index: %s, page_size: %s, offset: %s, limit: %s, has_next:\
         %s, has_previous: %s' \
               % (self.item_count, self.page_count, self.page_index, self.page_size, self.offset, self.limit,\
                  self.has_next, self.has_previous)

    __repr__ = __str__


def up_to_qiniu(filename, file_data, status):
    # 需要填写你的 Access Key 和 Secret Key
    access_key = 'iwCOmcdxdsqBLBaj1EsOQuYdJgNSj2Tn9kww8eW1'
    secret_key = 'zHmOMZ55R__8KfxeK1kv1_P1Or8i3j1z6p1nsIz6'
    # 构建鉴权对象
    q = Auth(access_key, secret_key)
    # 要上传的空间
    bucket_name = 'furniture'
    if status == 1:
        # 生成上传 Token，可以指定过期时间等
        token = q.upload_token(bucket_name, filename, 3600)
        ret, info = put_data(token, filename, file_data)
    if status == 0:
        # 初始化BucketManager
        bucket = BucketManager(q)

        # 删除bucket_name 中的文件 key
        ret, info = bucket.delete(bucket_name, filename)

    return ret, info

