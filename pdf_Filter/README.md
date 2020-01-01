# pdf_Filter

![PyPI - Python Version](https://img.shields.io/pypi/pyversions/Pillow)
![GitHub last commit](https://img.shields.io/github/last-commit/QidiLiu/pdf_Filter)

pdf滤镜。改变pdf文件的背景、文字颜色，使其适合阅读。

## 使用

- 主程序为pdf_filter.py (依赖库：Pillow, PyMuPDF)
- 尽量使用python3.5及以上版本，python2.7虽然也支持Pillow和PyMuPDF，但我没测试过

## 参考

- [Python 图片与pdf相互转换](https://blog.csdn.net/XnCSD/article/details/80849996)
- [python 判断目录和文件是否存在，若不存在即创建](https://blog.csdn.net/u013247765/article/details/79050947)
- [Python round() too slow, faster way to reduce precision?](https://stackoverflow.com/questions/44920655/python-round-too-slow-faster-way-to-reduce-precision)
- [python的tkinter进度条的实现](https://blog.csdn.net/qq_41149269/article/details/83043605)
- [tkinter实现下载进度条（python）](https://blog.csdn.net/asdfg6541/article/details/93918703)
- [Python图像处理库PIL的ImageOps模块介绍](https://blog.csdn.net/icamera0/article/details/50785776)
- [Docs » 数字图像处理 » Python-PIL-ImageOps](http://accu.cc/content/pil/pil_imageops/)
- [Docs » 参考文献 » ImageOps 模块](https://www.osgeo.cn/pillow/reference/ImageOps.html)
- [色调分离](https://zh.wikipedia.org/wiki/%E8%89%B2%E8%AA%BF%E5%88%86%E9%9B%A2)
- [python json.dumps 中文编码](https://blog.csdn.net/u014431852/article/details/53058951)
- [如何将 Python 程序打包成 .exe 文件？](https://zhuanlan.zhihu.com/p/45288707)
- [用Python为PDF添加目录](https://zhuanlan.zhihu.com/p/88618967)

## 功能实现进度

- [x] 基本功能
- [x] 窗口化
- [x] 处理进度计算效率过低问题
- [x] 清晰度设置
- [ ] 语言设置
- [x] 滤镜设置
- [x] 用settings.json记住设置
- [x] 保存时自定义文件名
- [x] 生成windows平台.exe程序
- [x] 还原输入pdf文件的目录

（语言设置太麻烦了，暂时不做了）
