from urllib.parse import urlparse
def character(original_url):
    # print("char收到了prigurl",original_url)
    res = urlparse(original_url)
    # print(res)
    # print("执行了character", res.netloc)
    if len(res.netloc)>0:
        return res.netloc

    else:
        return 1
