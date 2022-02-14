import os
import sys
import django


# 获取项目的根目录
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(base_dir)  # 添加到系统环境变量
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "saas.settings")  # 加载项目的配置文件，demos是项目
django.setup()  # 启动django
