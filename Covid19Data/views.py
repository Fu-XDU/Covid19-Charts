from django.shortcuts import render


# 返回templates中的login.html文件
def index(request):
    return render(request, 'index.html')
