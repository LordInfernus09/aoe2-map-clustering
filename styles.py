from dash import html

main_style = {
    "background-color": "white",
    "color": "#f5f5f5",
    "font-family": "Tahoma",
    "text-transform": "capitalize",
    "width": "100%",
    'padding': '10px',
    'margin': '0 auto',
    'max-width': '100%',  # Make the layout responsive
    'box-sizing': 'border-box',
}

text_style = {
    "color": "#121211",
    "font-family": "Tahoma",
    "text-transform": "capitalize",
    "margin": "8px",
}

container_style = {
    'display': 'flex',
    'justify-content': 'center',
    'align-items': 'center',
    'flex-direction': 'column',  # Column layout for better mobile adaptation
    'width': '100%',
    'padding': '10px'
}

dropdown_style = {
    "color": "#121211",
    "font-family": "Tahoma",
    "text-transform": "capitalize",
    "margin": "8px",
    "width": "50%",
}

dropdown_item_style = {
    "background-color": "#f5f5f5",
    "color": "#121211",
    "font-family": "Tahoma",
    "text-transform": "capitalize",
    "padding": "8px",
    'width': '90%',  # Ensure dropdown width adapts to mobile screen size
    'margin': '10px auto',
    'font-size': '16px',  # Adjust font size for readability
    'box-sizing': 'border-box'
}

dropdown_items = [
    {
        "label": html.Span(["Ground Truth"], style=dropdown_item_style),
        'value': 'ground_truth.pkl'
    },
    {
        "label": html.Span(["Kmeans Model (k = 8)"], style=dropdown_item_style),
        'value': 'kmeans_clusters_8.pkl'
    },
    {
        "label": html.Span(["Kmeans Model (k = 16)"], style=dropdown_item_style),
        'value': 'kmeans_clusters_16.pkl'
    },
    {
        "label": html.Span(["Kmeans Model (k = 30)"], style=dropdown_item_style),
        'value': 'kmeans_clusters_30.pkl'
    },
    {
        "label": html.Span(["Contrastive STL-10 Trained Model"], style=dropdown_item_style),
        'value': 'cc_STL_10_clusters.pkl'
    },
    {
        "label": html.Span(["Contrastive CIFAR-10 Trained Model"], style=dropdown_item_style),
        'value': 'cc_CIFAR_10_clusters.pkl'
    },
    {
        "label": html.Span(["Contrastive CIFAR-100 Trained Model"], style=dropdown_item_style),
        'value': 'cc_CIFAR_100_clusters.pkl'
    },
    {
        "label": html.Span(["Contrastive AOE2-Maps Trained Model 440"], style=dropdown_item_style),
        'value': 'cc_aoe2_maps_clusters.pkl'
    },
    {
        "label": html.Span(["Contrastive AOE2-Maps Trained Model 560"], style=dropdown_item_style),
        'value': 'cc_aoe2_maps_560_clusters.pkl'
    },
    {
        "label": html.Span(["Contrastive Small AOE2-Maps Trained Model 560"], style=dropdown_item_style),
        'value': 'cc_small_aoe2_maps_560_clusters.pkl'
    }
]

image_style = {
    "background-color": "#f5f5f5",
    "color": "#121211",
    "font-family": "Tahoma",
    "font-size": "14px",
    "text-transform": "capitalize",
    'width': '100%',  # Make image responsive
    'height': 'auto',
    'max-width': '300px',  # Limit maximum width for small screens
    'margin': '10px auto',
}

# Add media queries for mobile view
media_queries = """
@media only screen and (max-width: 600px) {
    .container {
        flex-direction: column;
        padding: 5px;
    }
    .dropdown {
        width: 95%;
    }
    .graph {
        width: 100%;
        height: 400px;
    }
}
"""
