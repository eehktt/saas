class BoostrapForm(object):
    def __init__(self, *args, **kwargs):
        super().__init__( *args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            # 特例，自定义placeholder
            if name == 'confirm_password':
                pass
            else:
                # 格式化不能被用户控制 否则会信息泄漏甚至rce
                field.widget.attrs['placeholder'] = '请输入%s' % (field.label,)
