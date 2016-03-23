from abc import abstractmethod

import plotly
import plotly.graph_objs as go
from plotly.offline import plot

from terms.models import Category, Term


class Chart:
    default_args = {'auto_open': False, 'output_type': 'div', 'show_link': False}

    def __init__(self):
        pass

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


class TermsChart(Chart, object):
    @abstractmethod
    def get_plot(self):
        pass

    def __init__(self, terms):
        super(TermsChart, self).__init__()
        self.terms = terms


class TermsCountByCategoryChart(TermsChart):
    def get_plot(self):
        all_categories = Category.objects.all()
        data = [(cat, len(self.terms.filter(category__exact=cat))) for cat in all_categories]
        data.sort(key=lambda x: str(x[0]))
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
        return plot_


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
