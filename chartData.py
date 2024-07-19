#### Import Modules ####
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import plotly.graph_objects as go



#### Global Objects ####
URL_FAV = "https://projects.fivethirtyeight.com/polls/data/favorability_averages.csv"
URL_APP = "https://projects.fivethirtyeight.com/biden-approval-data/approval_topline.csv"
string_columns = ["politician", "subpopulation", "answer"]
date_columns = ["date"]
number_columns = ["pct_estimate", "lo", "hi"]



#### Define Functions ####
def acquire_data() -> pd.DataFrame:
    # Down CSV dataset
    full_df = pd.read_csv(URL_FAV)
    full_df = full_df.loc[full_df['subpopulation'].isna()]
    full_df.drop('subpopulation', axis=1, inplace=True)

    # Parse for specific candidates of interest
    candidate_list = ['Donald Trump', 'Joe Biden', 'Robert F. Kennedy']

    return_data = full_df.loc[full_df['politician'].isin(candidate_list)]

    return return_data
    
def build_plot(data=pd.DataFrame, favorability_type:str="Favorable"):
    # Validate input data
    try:
        full_df = pd.DataFrame(data)
        favorability = str(favorability_type).title()
        favorability = favorability if favorability in ["Favorable", "Unfavorable"] else "Favorable"
    except Exception as e:
        print("\n", f"Error Report:    {e}", "\n")

    # Filter DF by Favorability type
    full_df = full_df.loc[full_df['answer'] == favorability]

    # Acquire unique candidate list and sort by Favorability type
    candidate_list = full_df['politician'].unique()
        
    # Create figure and add traces to it
    fig = go.Figure()

    # Make traces for scatterplot
    color_dict = {"Donald Trump": "red", "Joe Biden": "blue", "Robert F. Kennedy": "beige"}
    for candidate in candidate_list:
        candidate_color = color_dict[candidate]
        trace = go.Line(x = full_df['date'],
                           y = full_df.loc[full_df['politician']==candidate, 'pct_estimate'],
                           mode = 'lines',
                           line_shape = 'spline',
                           connectgaps = True,
                           name = candidate,
                           line = dict(color = candidate_color))
        
        fig.add_trace(trace)

    # Update the figure layout
    fig.update_layout(title = "Favorability Ratings",
                      xaxis_title = "Date",
                      yaxis_title = "Favorability",
                      legend_title = "Candidates",
                      hovermode = "x unified",
                      plot_bgcolor='darkgrey',
                      yaxis_range = [10, 90])
    
    return fig



#### Main Actions ####
if __name__ == "__main__":
    a = acquire_data()
    print('\n', a, type(a), '\n')
    b = build_plot(a)
    b.show()