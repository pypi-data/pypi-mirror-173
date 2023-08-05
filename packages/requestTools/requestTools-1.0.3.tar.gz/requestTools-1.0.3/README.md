## Example Package
This is a simple example package. You can use

[联系作者](https://mp.weixin.qq.com/s/9FQ-Tun5FbpBepBAsdY62w)

to write your content.

```python

    from com.http.HttpRequestProcessor import NormalHttpRequestProcessor
    from com.http.HttpRequestUtils import MethodEnum
    
    class XXXNormalHttpRequestProcessor(NormalHttpRequestProcessor):
        """一个基本的http请求处理实现类
        该类重新实现了setCookieFileName,setUrl,setMethod,setFormValues5个抽象方法
        """
        # 设置cookie文件名称
        def setCookieFileName(self):
            return "xxx.txt"
    
        # 设置Url
        def setUrl(self, dynamicParams=None):
            return "xxxxx"
    
        # 设置方法
        def setMethod(self):
            return MethodEnum.POST
    
        # 设置表单信息
        def setFormValues(self, dynamicParams=None):
            # 固定不变的请求参数
            formValues = {
              
            }
    
            # 合并动态的请求参数
            if dynamicParams is not None:
                formValues = {**formValues, **dynamicParams}
    
            return formValues
    
    
    if __name__ == '__main__':
        xxxNormalHttpRequestProcessor = XXXNormalHttpRequestProcessor()
        xxxNormalHttpRequestProcessor.getResponse()

```
