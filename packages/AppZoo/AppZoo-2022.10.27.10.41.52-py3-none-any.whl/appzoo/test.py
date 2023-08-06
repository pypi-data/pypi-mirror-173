#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AppZoo.
# @File         : test
# @Time         : 2022/3/25 下午4:36
# @Author       : yuanjie
# @WeChat       : 313303303
# @Software     : PyCharm
# @Description  :


from meutils.pipe import *


# rename
BASE_DIR = Path(__file__).resolve().parent.parent


print(BASE_DIR)
DIR = Path(__file__).absolute().parent
package_name = DIR.name
version = time.strftime("%Y.%m.%d.%H.%M.%S", time.localtime())
Path(DIR / '/data/VERSION').write_text(version)