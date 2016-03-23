from math import ceil


class Pager:
    def __init__(self, objects, split_number=7, page_number=0):
        self.page_number = page_number
        self.split_number = split_number
        self.objects = objects

    def __len__(self):
        return ceil(len(self.objects) / self.split_number)

    def current_page(self):
        return self[self.page_number]

    def __getitem__(self, index):
        if len(self) >= index >= 0:
            if index != len(self) - 1:
                return self.objects[(index * self.split_number):((index + 1) * self.split_number)]
            else:
                return self.objects[(index * self.split_number):]
        else:
            return self[(len(self) + index) % len(self)]


class TermsPagePager(Pager, object):
    def __init__(self, objects, split_number=7, page_number=0, previous_url=None, next_url=None, current_url=None):
        super(TermsPagePager, self).__init__(objects, split_number=split_number, page_number=page_number)
        if not previous_url:
            previous_url = '/terms/?page=%i' % (page_number - 1)
        if not next_url:
            next_url = '/terms/?page=%i' % (page_number + 1)
        if not current_url:
            current_url = '/terms/?page=%i' % page_number
        self.urls = {'previous': previous_url, 'next': next_url, 'current': current_url}
