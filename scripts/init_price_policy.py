from scripts import base
from web import models


def run():
    exist = models.PricePolicy.objects.filter(category=1, title='个人免费版').exists()
    if not exist:
        models.PricePolicy.objects.create(
            category=1,
            title='个人免费版',
            price=0,
            project_num=3,
            project_member=5,
            project_size=20,
            pre_file_size=5,
        )


if __name__ == '__main__':
    run()
