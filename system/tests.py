from django.test import TestCase

# Create your tests here.


class SystemSmokeTest(TestCase):
    """基础冒烟测试：确认 system 应用可正常加载。"""

    def test_import(self):
        from system import views  # noqa: F401
        self.assertTrue(True)
