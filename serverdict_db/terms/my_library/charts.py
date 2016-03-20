from abc import abstractmethod
from plotly.offline import offline
from terms.models import Category


class Chart:
    default_args = {'auto_open': False, 'output_type': 'div', 'show_link': False}

    @abstractmethod
    def get_plot(self):
        pass


class CubicParabolaPlot(Chart):
    def get_plot(self):
        def my_range(first, last=None, step=1.0):
            if last is None:
                last = first
                first = 0
            i = first
            while i < last:
                yield i
                i += step

        x = list(my_range(-10, 10, 1e-3))

        return offline.plot({
            "data": [
                {
                    'x': x,
                    'y': list(map(lambda arg: arg ** 3, x))
                }
            ],
            "layout": {
                'title': "hello world"
            }
        }, **Chart.default_args)


class TermsCountByCategoryChart(Chart):
    def __init__(self, terms):
        self.terms = terms

    def get_plot(self):
        import time
        all_cats_query_time_begin = time.time()
        all_categories = Category.objects.all()
        all_cats_query_time_end = time.time()
        print("all cats query time:", all_cats_query_time_end - all_cats_query_time_begin)
        data_creation_begin = time.time()
        data = [(cat, len(self.terms.filter(category__exact=cat))) for cat in all_categories]
        data_creation_end = time.time()
        print('data creation time:', data_creation_end - data_creation_begin)
        data_sorting_begin = time.time()
        data.sort(key=lambda x: str(x[0]))
        data_sorting_end = time.time()
        print('data sorting time:', data_sorting_end - data_sorting_begin)
        plot_begin = time.time()
        plot_ = offline.plot({
            "data": [
                {
                    'labels': [str(a[0]) for a in data],
                    'values': [a[1] for a in data],
                    'type': 'pie'
                }
            ],
            "layout": {
                'title': "Terms count by category"
            }
        }, **Chart.default_args)
        plot_end = time.time()
        print('plot time:', plot_end - plot_begin)
        return plot_
