# pylint: disable=missing-module-docstring

from django.shortcuts import redirect


def redirect_to_home():
    """
    将错误访问跳转回主页
    """
    return redirect("/static/index.html")
