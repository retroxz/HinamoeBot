import json


class defend_member:
    """
        配置项 要保护的成员
        :id: QQ号码
        :group_id: 群号码
    """
    qq = 0
    group_id = 0

    def __init__(self, qq, group_id):
        self.qq = str(qq)
        self.group_id = str(group_id)
