class PagerHelper():
    def __init__(self, request, total_count, base_url, show_num):
        self.request = request
        self.total_count = total_count
        self.base_url = base_url
        self.show_num = show_num

        self.v, a = divmod(self.total_count, self.show_num)
        self.v = [self.v, self.v+1][a!=0]

        try:
            self.current_page = int(self.request.GET.get('page', 1))
        except ValueError:
            self.current_page = 1
        else:
            if self.current_page <= 0:
                self.current_page = 1
            elif self.current_page > self.v:
                self.current_page = self.v

    @property
    def db_start(self):
        return (self.current_page - 1) * self.show_num

    @property
    def db_end(self):
        return self.current_page * self.show_num

    def pager_str(self):

        # 确定分页的区间
        if self.v <= 11:
            start_page = 1
            end_page = self.v
        else:
            if self.current_page < 6:
                start_page = 1
                end_page = 11
            elif self.current_page > self.v - 5:
                start_page = self.v - 10
                end_page = self.v
            else:
                start_page = self.current_page - 5
                end_page = self.current_page + 5
        # 生成页码字符串(15个a标签)
        pager_list = []
        if self.v == 1:
            pager_list.append('<a href="javascript:void(0)">首页</a>')
        else:
            pager_list.append('<a href="{}?page={}">首页</a>'.format(self.base_url, 1))
        if self.current_page == 1:
            pager_list.append('<a href="javascript:void(0)">上一页</a>')
        else:
            pager_list.append('<a href="{}?page={}">上一页</a>'.format(self.base_url, self.current_page-1))
        for i in range(start_page, end_page+1):
            if i == self.current_page:
                pager_list.append('<a class="active" href="{}?page={}">{}</a>'.format(self.base_url, i, i))
            else:
                pager_list.append('<a href="{}?page={}">{}</a>'.format(self.base_url, i, i))
        if self.current_page == self.v:
            pager_list.append('<a href="javascript:void(0)">下一页</a>'.format(self.current_page))
        else:
            pager_list.append('<a href="{}?page={}">下一页</a>'.format(self.base_url, self.current_page+1))
        if self.v == 1:
            pager_list.append('<a href="javascript:void(0)">首页</a>')
        else:
            pager_list.append('<a href="{}?page={}">尾页</a>'.format(self.base_url, self.v))
        pager = ''.join(pager_list)
        return pager
