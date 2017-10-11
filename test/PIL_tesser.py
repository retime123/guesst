# coding=utf-8
# import os,sys,re,time
# reload(sys)
# sys.setdefaultencoding('utf-8')

# import Image
import PIL

import random
from pytesser import *

'''
识别简单的验证码
程序需要PIL库(图像处理)和pytesser支持
'''

'''
安装：pytesser
下载后得到 “pytesser_v0.0.1.zip”，是一个压缩文件，使用方法： 
1、在 “D:\python_2\Lib\site-packages” 路径下新建一个文件夹，命名 “pytesser” 。把 “pytesser_v0.0.1.zip” 里的文件解压到该目录下
2、将 “pytesser.py” 改名为 “__init__.py”。

3、打开 “__init__.py” 文件，将 “tesseract_exe_name” 变量的值改为
“‘D:\python_2\Lib\site-packages/pytesser /tesseract’”(原值为 “‘tesseract’”)。

4、pytesser 模块依赖于 PIL 模块，如果是按照上面的方法安装 PIL 的话，需要把 “__init__.py” 文件里的 “import Image” 改成 “from PIL import Image” 
'''

im = Image.open('fonts_test.png')
img = Image.open('test.jpg')
text = image_to_string(img)
print "Using image_to_string(): "
print text
text = image_file_to_string('fonts_test.png', graceful_errors=True)
print "Using image_file_to_string():"
print text

