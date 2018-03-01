from django.http import HttpResponse
from django.utils.encoding import escape_uri_path
from django.shortcuts import render
from bs4 import BeautifulSoup
from excel_response import ExcelResponse
import re


def index(request):
    return render(request, 'index.html')


def analyse(request):
    if request.method == 'GET':
        return HttpResponse('请从表单提交数据')
    elif request.method == 'POST':
        filename = request.POST['filename'] or '未命名'
        html = request.POST['html']
        if html:
            data = [
                ['时间', '阅读量', '类型', '标题']
            ]
            list = BeautifulSoup(html, 'lxml').find_all('div', attrs={'action-type': 'feed_list_item'})
            for tag in list:
                date = (tag.find(attrs={'node-type': 'feed_list_item_date'})['title'])
                haveRead = tag.find(attrs={'action-type': 'fl_pop'})
                read = ''
                if (haveRead):
                    read = re.search('\d+', haveRead.get_text()).group(0)
                else:
                    read = '没找到阅读量，登录没有？'
                title = ''
                type = ''
                if (tag.find(attrs={'action-type': 'widget_articleLayer'})):
                    title = str(
                        tag.find(attrs={'action-type': 'widget_articleLayer'}).get_text(strip=True))
                    type = '文章'
                else:
                    title = str(tag.find(attrs={'node-type': 'feed_list_content'}).get_text(strip=True))
                    type = '微博'
                data.append([
                    date, read, type, title
                ])
            response = HttpResponse(ExcelResponse(data), content_type='application/vnd.ms-excel')
            response["Content-Disposition"] = "attachment; filename={}.xlsx".format(escape_uri_path(filename))
            return response
        else:
            return HttpResponse('请填写完整ok？')
