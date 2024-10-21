import base64
import pickle
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import gzip
import styles

from PIL import Image
from io import BytesIO
from dash import Dash, dcc, html, Input, Output, no_update
from concurrent.futures import ThreadPoolExecutor


def load_cluster_data(filename):
    with gzip.open(filename, "rb") as f:
        cluster_data = pickle.load(f)
    return cluster_data


def to_image(image):
    if image.dtype != np.uint8:
        image = (255 * (image - np.min(image)) / (np.max(image) - np.min(image))).astype(np.uint8)

    im = Image.fromarray(image, 'RGB')
    return np.array(im)


def extract_labels(cluster_data):
    labels = [data[1] for data in cluster_data]
    true_labels = [data[2] for data in cluster_data]
    reduced_features = np.array([data[3] for data in cluster_data])
    return labels, true_labels, reduced_features


def create_dataframe(cluster_data):
    # Use ThreadPoolExecutor to parallelize the label extraction
    with ThreadPoolExecutor() as executor:
        future = executor.submit(extract_labels, cluster_data)
        labels, true_labels, reduced_features = future.result()

    data_frame = pd.DataFrame({
        'x': reduced_features[:, 0],
        'y': reduced_features[:, 1],
        'image_index': range(len(cluster_data)),
        'label': labels,
        'true_label': true_labels
    })

    return data_frame


def image_to_base64(image):
    im = Image.fromarray(image, 'RGB')
    buffered = BytesIO()
    im.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode('utf-8')


def create_figure(df):
    fig = go.Figure(data=[
        go.Scatter(
            x=df["x"],
            y=df["y"],
            mode="markers",
            marker=dict(
                colorscale="turbo",
                color=df["label"],
                size=10,
                colorbar={"title": "Cluster<br>Label"},
                line={"color": "#fff"},
                reversescale=True,
                sizeref=45,
                sizemode="diameter",
                opacity=0.8,
            )
        )
    ])

    fig.update_traces(hoverinfo="none", hovertemplate=None)

    fig.update_layout(
        autosize=True,  # Ensure graph resizes automatically
        width='100%',  # Use full width of the container
        height=400,  # Adjust height for smaller screens
        margin=dict(l=0, r=0, t=0, b=0),  # Remove margins for mobile view
        xaxis=dict(showgrid=False, zeroline=False, visible=False),
        yaxis=dict(showgrid=False, zeroline=False, visible=False),
        plot_bgcolor='#121211',
    )

    return fig


app = Dash(__name__)
app.index_string = '''
<!DOCTYPE html>
<html>
    <head>
        <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
        <title>Map Cluster Graphs</title>
        <style>
            {media_queries}
        </style>
    </head>
    <body>
        <div id="react-entry-point">
            <script src="_dash-component-suites/dash/dash-renderer/build/dash_renderer.min.js"></script>
        </div>
    </body>
</html>
'''

# Default selected file
default_file = 'ground_truth.pkl'
clusters = None
df = None

# Layout with a dropdown for selecting which graph to load
app.layout = html.Div([
    html.H1("Age of Empires 2 Map Cluster Graphs", style=styles.text_style),
    dcc.Dropdown(
        id="graph-selection-dropdown",
        options=styles.dropdown_items,
        value=default_file,  # Set the default value to the first graph
        placeholder="Select a graph to load",
        style=styles.dropdown_style
    ),
    html.Div([
        dcc.Loading(  # Add a loading spinner
            id="loading-1",
            type="circle",
            color="#c2c2c2",
            children=dcc.Graph(id="graph-display", clear_on_unhover=True),
        ),
        dcc.Tooltip(id="graph-tooltip"),
    ], style=styles.container_style),
], style=styles.main_style)


@app.callback(
    Output("graph-display", "figure"),
    Input("graph-selection-dropdown", "value")
)
def update_graph(selected_file):
    if selected_file is None:
        return no_update

    global clusters
    global df
    clusters = load_cluster_data(f"./visualization/{selected_file}")
    df = create_dataframe(clusters)
    fig = create_figure(df)

    return fig


@app.callback(
    Output("graph-tooltip", "show"),
    Output("graph-tooltip", "bbox"),
    Output("graph-tooltip", "children"),
    Input("graph-display", "hoverData"),
    Input("graph-selection-dropdown", "value")
)
def display_hover(hover_data, selected_file):
    if hover_data is None or selected_file is None:
        return False, no_update, no_update

    pt = hover_data["points"][0]
    bbox = pt["bbox"]
    num = pt["pointNumber"]

    df_row = df.iloc[num]
    image_index = int(df_row['image_index'])
    label = df_row['label']
    true_label = df_row['true_label']

    image = to_image(clusters[image_index][0])
    img_src = f"data:image/png;base64,{image_to_base64(image)}"

    children = [
        html.Div([
            html.Img(src=img_src, style={"width": "100%"}),
            html.P(
                f"Cluster {label}",
                style=styles.text_style
            ),
            html.P(
                f"Image Label: {true_label}",
                style=styles.text_style
            ),
        ], style=styles.image_style)
    ]

    return True, bbox, children


if __name__ == "__main__":
    app.run_server(debug=True)
