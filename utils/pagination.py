import copy
from django.utils.safestring import mark_safe
from web import models


class Pagination(object):
    def __init__(self, request, querylist):
        self.request = request
        self.start = None
        self.end = None
        self.page = None
        self.start_page = None
        self.end_page = None
        self.page_total = None
        self.querylist = querylist

        per_page = 10
        total_count = self.querylist.count()
        self.page_total, rest = divmod(total_count, per_page)
        if rest:
            self.page_total = self.page_total + 1
        self.page = self.request.GET.get('page')
        if not self.page:
            self.page = 1
        else:
            if self.page.isdecimal():
                self.page = int(self.page)
                if (self.page - 1) < 0:
                    self.page = 1
                else:
                    if self.page > total_count:
                        self.page = self.page_total
            else:
                self.page = 1
        self.start = (self.page - 1) * per_page
        self.end = self.page * per_page
        self.start_page = self.page - 5
        self.end_page = self.page + 5
        if self.start_page < 1:
            self.start_page = 1
        if self.end_page > self.page_total:
            self.end_page = self.page_total

    def get_paramstring(self):
        self.request.GET._mutable = True

        # <li class="page-item"><a class="page-link" href="#">1</a></li>
        str_list = []
        querydict = copy.deepcopy(self.request.GET)
        if (self.page - 1) > 0:
            querydict.setlist('page', [1])
            str_list.append(
                '<li class="page-item"><a class="page-link" href="?{}">{}</a></li>'.format(querydict.urlencode(),
                                                                                           '首页'))
            querydict.setlist('page', [self.page - 1])
            str_list.append(
                '<li class="page-item"><a class="page-link" href="?{}">{}</a></li>'.format(querydict.urlencode(),
                                                                                           '上一页'))
        for i in range(self.start_page, self.end_page + 1):
            querydict.setlist('page', [i])
            if self.page == i:
                str_list.append('<li class="page-item active"><a class="page-link" href="?{}">{}</a></li>'.format(
                    querydict.urlencode(), i))
            else:
                str_list.append(
                    '<li class="page-item"><a class="page-link" href="?{}">{}</a></li>'.format(querydict.urlencode(),
                                                                                               i))
            # paramstring = '<li class="page-item"><a class="page-link" href="#">1</a></li>'
        if self.page < self.page_total:
            querydict.setlist('page', [self.page + 1])
            str_list.append(
                '<li class="page-item"><a class="page-link" href="?{}">{}</a></li>'.format(querydict.urlencode(),
                                                                                           '下一页'))
            querydict.setlist('page', [self.page_total])
            str_list.append(
                '<li class="page-item"><a class="page-link" href="?{}">{}</a></li>'.format(querydict.urlencode(),
                                                                                           '末页'))
        paramstring = mark_safe(''.join(str_list))
        return paramstring
