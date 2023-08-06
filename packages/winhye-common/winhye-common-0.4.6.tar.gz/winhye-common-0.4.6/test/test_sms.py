import json
import os
import sys

from winhye_common.utils.sms import Sample

PATH = os.path.join(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))
sys.path.append(PATH)
print(PATH)


def test_oss_a(phone_numbers, sign_name, template_code, template_param):
    # 再发送
    aa = Sample(
        'LTAI5tG9WoZ4CQpdfEHhfVCb',
        'FuOX7YpIG3sqPVENmb6ryYdhFubVJl'
    )
    res = aa.send_sms(phone_numbers, sign_name, template_code, template_param)
    print()

if __name__ == '__main__':
    # loop = asyncio.get_event_loop()
    test_oss_a(
        '13032643571',
        "北京云汉通航科技有限公司",
        "SMS_223060267",
        {"code": "666666"}
    )
    # asyncio.run(main('17737263251',
    #                  "北京云汉通航科技有限公司",
    #                  "SMS_223060267",
    #                  '{"code":"55"}'))
