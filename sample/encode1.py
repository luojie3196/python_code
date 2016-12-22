#!/usr/bin/env python
# -*- codeing:utf-8 -*-

import sys
print(sys.getdefaultencoding())

# name为Python3默认编码 Unicode编码
name='罗杰'
# Unicode 编码成 GBK输出
print(name.encode('GBK'))
# Unicode编码成 utf-8输出
print(name.encode('utf-8'))
# Unicode 先编码再解码
print(str(name.encode('utf-8'), encoding='utf-8'))
print(str(name.encode('GBK').decode('GBK')))