# 启动django
import os
import sys
import django

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(base_dir)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Order1.settings')
django.setup()  # 伪造让django启动

from web import models
from utils.encrypt import md5

# 创建级别
# level_object = models.Level.objects.create(title="VIP", percent=90)
#
# models.Customer.objects.create(
#     username='alex',
#     password=md5("alex"),
#     mobile='1999999998',
#     level_id=1,
#     creator_id=1
# )

# for i in range(1, 30):
#     models.Customer.objects.create(
#         username='alex-{}'.format(i),
#         password=md5("alex-{}".format(i)),
#         mobile='1999999998',
#         level_id=1,
#         creator_id=1
#     )
