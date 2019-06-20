import base64
import os
from io import BytesIO
from django.shortcuts import render
from django.views import generic
from django.conf import settings as djangoSettings
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas

# Create your views here.
class Example1View(generic.TemplateView):
    template_name = 'polls/example1.html'
    context_object_name = 'results'

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        
        # generate some data (e.g. load your model)
        data = [
            ['', 'Question', 'Response', 'Votes'],
            [ 1, 'What is your favorite language?', 'Python', 22],
            [ 2, 'What is your favorite language?', 'R', 2],
            [ 3, 'What is your favorite language?', 'JAVA', 7],
            [ 4, 'What is your favorite language?', 'C/C++', 1],
            [ 5, 'What is your favorite language?', 'Other', 9],
        ]

        # crate a dataframe
        df = pd.DataFrame(data[1:], columns=data[0])
 
        # generate the plot
        df_fig = df[['Response', 'Votes']]
        df_fig = df_fig.set_index('Response')
        ax = df_fig.plot(kind='barh')
        ax.set_xlabel('Votes')
        plt.tight_layout()

        # save the file
        fig = ax.get_figure()
        fig_path = os.path.join(djangoSettings.BASE_DIR, 'polls/static/polls/images/figure1.jpg')
        fig.savefig(fig_path)  # this is the path on the server
        return self.render_to_response(context)


class Example2View(generic.TemplateView):
    template_name = 'polls/example2.html'
    context_object_name = 'results'

    def fig_to_tag(self, fig):
        buffer = BytesIO()
        canvas = FigureCanvas(fig)
        canvas.print_png(buffer)
        return base64.encodebytes(buffer.getvalue()).decode()

    
    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)

        # generate some data (e.g. load your model)
        data = [
            ['', 'Question', 'Response', 'Votes'],
            [ 1, 'How important is this class to your success?', 'Unimportant', 0],
            [ 2, 'How important is this class to your success?', 'Of little importance', 3],
            [ 3, 'How important is this class to your success?', 'Moderately important', 10],
            [ 4, 'How important is this class to your success?', 'Important', 15],
            [ 5, 'How important is this class to your success?', 'Very important', 22],
        ]

        # crate a dataframe
        df = pd.DataFrame(data[1:], columns=data[0])
 
        # generate the plot
        df_fig = df[['Response', 'Votes']]
        df_fig = df_fig.set_index('Response')
        ax = df_fig.plot(kind='barh')
        ax.set_xlabel('Votes')
        plt.tight_layout()

        # get the file
        fig = ax.get_figure()

        # convert the figure to a tag
        context['figure2'] = self.fig_to_tag(fig)

        return self.render_to_response(context)
