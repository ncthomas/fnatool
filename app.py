from flask import Flask, request, render_template
import numpy
import matplotlib
import matplotlib.pyplot
import seaborn
import io
import base64

seaborn.set(style='white')
app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')


@app.route('/cxcr6')
def marker1home():
    return render_template('marker1home.html')


@app.route('/cxcr6', methods=['POST'])
def marker1results():

    marker1 = request.form.get('cxcr6', type=float)
    p = get_marker1_probability(marker1)
    graph = get_bar_graph(p)

    return render_template("marker1result.html", probability=str(p), graph=graph)


@app.route('/cd8trm')
def marker2home():
    return render_template('marker2home.html')


@app.route('/cd8trm', methods=['POST'])
def marker2results():

    marker2 = request.form.get('cd8trm', type=float)
    p = get_marker2_probability(marker2)
    graph = get_bar_graph(p)

    return render_template("marker2result.html", probability=str(p), graph=graph)


def get_marker1_probability(cxcr6):

    p = 1 / (1 + numpy.exp(2.518-0.149*cxcr6))
    p = numpy.round(100*p, 1)

    return p


def get_marker2_probability(cd8trm):

    p = 1 / (1 + numpy.exp(2.323-0.728*cd8trm))
    p = numpy.round(100*p, 1)

    return p


def get_bar_graph(p):

    cmap = matplotlib.cm.get_cmap('coolwarm')
    c = cmap(p/100)

    img = io.BytesIO()
    fig, ax = matplotlib.pyplot.subplots(figsize=(6, 1))
    ax.barh([0], [p], color=c)
    ax.set_xlim(0, 100)
    ax.set_yticks([])
    matplotlib.pyplot.tight_layout()
    matplotlib.pyplot.savefig(img, format='png')
    img.seek(0)
    graph_url = base64.b64encode(img.getvalue()).decode()
    matplotlib.pyplot.close()
    graph = "data:image/png;base64,{}".format(graph_url)

    return graph


if __name__ == '__main__':
    app.run()
