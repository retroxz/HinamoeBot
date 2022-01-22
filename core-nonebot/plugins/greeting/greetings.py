# !/usr/bin/env python3
# coding=utf-8

from string import Template
import inspect


class Greeting:
    morning_early = Template('天还没亮呢，再睡一会吧！')
    morning = Template('''
        现在是${date} 星期${weekdays}
        你是群里第【${rank}】位起床的哦！
    ''')
    morning_late = Template('现在才起来，真的是比taffy还懒呢！！')
