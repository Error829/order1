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

models.Administrator.objects.create(username='TC', password=md5("359509tcw"), mobile="17798320257")
