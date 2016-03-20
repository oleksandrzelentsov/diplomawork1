from abc import abstractmethod
from statistics import mean

import plotly
import plotly.graph_objs as go
from plotly.offline import plot

from terms.models import Category, Term


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

        return plotly.offline.plot({
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


class TermsChart(Chart):
    @abstractmethod
    def get_plot(self):
        pass

    def __init__(self, terms):
        self.terms = terms


class TermsCountByCategoryChart(TermsChart):
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
        plot_ = plotly.offline.plot({
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
        # def get_plot(self):
        #     return ''


class TermsPopularityChart(TermsChart):
    def get_plot(self):
        popularity = [x.popularity for x in self.terms]
        trace1 = go.Bar(
            x=list(range(len(self.terms))),
            y=popularity,
            name='terms',
            marker=dict(
                showscale=True,
                colorscale=[[0, 'rgb(200,200,200)'], [0.95, 'rgb(100,100,150)'], [1, 'rgb(200, 0, 0)']],
                cmax=1,
                cmin=0,
                color=[1 if x.public else float(x.popularity) / Term.average_popularity() for x in self.terms],
            ),
            text=[x.name + ', ' + ('public' if x.public else '{}% not enough to be public'.format(
                round(100 - float(x.popularity) / Term.average_popularity() * 100, 2))) for x in self.terms]
        )
        trace2 = go.Scatter(
            x=[-1, len(self.terms)],
            y=[Term.average_popularity()] * 2,
            name='average',
        )
        data = [trace1, trace2]
        layout = go.Layout(
            title='Popularity',
            xaxis=dict(title='Terms'),
            yaxis=dict(title='Popularity'),
            showlegend=False,
        )
        fig = go.Figure(data=data, layout=layout)
        plot_ = plot(fig, **Chart.default_args)
        return plot_
