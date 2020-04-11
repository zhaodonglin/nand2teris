import base64

fp= open("/Users/zhaodonglin/Repositories/elasticbox/keys/google_key.p12", 'r+b')
str1 = fp.read()
print base64.b64encode(str1)
# print base64.b64decode(base64.b64encode(str1))
fp.close()