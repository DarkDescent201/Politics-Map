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
color_dict = {"Donald Trump": "red", "Joe Biden": "blue", "Robert F. Kennedy": "beige",
              "Approve": 'green', "Disapprove": 'orange'}



#### Define Functions ####
def acquire_data(show_list:list=[True,True,True], favorability_type:str="Favorable") -> pd.DataFrame:
    # Down CSV dataset
    if favorability_type == "Approval":
        full_df = pd.read_csv(URL_APP)
        full_df.drop(['subpopulation', 'polltype', 'subgroup', 'timestamp'], axis=1)

        return full_df

    else:
        full_df = pd.read_csv(URL_FAV)

        full_df = full_df.loc[full_df['subpopulation'].isna()]
        full_df.drop('subpopulation', axis=1, inplace=True)

        # Manually adding Trump data didn't work, so let's cheat by simply dropping the offending rows
        full_df = full_df[~full_df['date'].isin(['2023-10-07', '2023-10-08'])]

        # Parse for specific candidates of interest
        prelim_list = ['Donald Trump', 'Joe Biden', 'Robert F. Kennedy']
        candidate_list = []

        for i, truth in enumerate(show_list):
            if truth:
                candidate_list.append(prelim_list[i])

        return_data = full_df.loc[full_df['politician'].isin(candidate_list)]

        return return_data
    
def build_plot_fav(data=pd.DataFrame, poll_date:datetime.date="common", favorability_type:str="Favorable"):
    # Validate input data
    try:
        full_df = pd.DataFrame(data)
        favorability = str(favorability_type).title()
        favorability = favorability if favorability in ["Favorable", "Unfavorable"] else "Favorable"
    except Exception as e:
        print("\n", f"Error Report:    {e}", "\n")

    # Filter DF by Favorability type
    full_df = full_df.loc[full_df['answer'] == favorability]

    # Deal with the dates
    copy_df = full_df.copy()

    if poll_date == "common":
        earliest_dates = copy_df.groupby('politician')['date'].min()
        earliest_common_date = earliest_dates.max()
        full_df = full_df[full_df['date'] >= earliest_common_date]
    else:
        full_df = full_df[full_df['date'] >= str(poll_date)]

    # Acquire unique candidate list and sort by Favorability type
    candidate_list = full_df['politician'].unique()
        
    # Create figure and add traces to it
    fig = go.Figure()

    # Make traces for scatterplot
    for candidate in candidate_list[::-1]:
        candidate_color = color_dict[candidate]
        trace = go.Scatter(x = full_df['date'],
                           y = full_df.loc[full_df['politician']==candidate, 'pct_estimate'].round(2),
                           mode = 'lines',
                           line_shape = 'spline',
                           connectgaps = True,
                           name = candidate,
                           line = dict(color = candidate_color,
                                       width = 3))
        
        fig.add_trace(trace)

    # Update the figure layout
    fig.update_layout(title = "",
                      xaxis_title = "Date",
                      yaxis_title = "Score",
                      legend_title = "Candidates",
                      hovermode = "x",
                      plot_bgcolor = 'black',
                      paper_bgcolor = 'black',
                      xaxis = {'tickfont':{'color':'#6D8DAD'},
                               'titlefont':{'color':'#6D8DAD',
                                            'family': 'Arial Black'}},
                      yaxis = {'tickfont':{'color':'#6D8DAD'},
                               'titlefont':{'color':'#6D8DAD',
                                            'family': 'Arial Black'}},
                      yaxis_range = None, #[10, 70],# if favorability_type=="Unfavorable" else [20, 60],
                      legend = {'font':{'color':'#6D8DAD'},
                                'title_font': {'family': 'Arial Black'}})
    
    fig.update_xaxes(showgrid=False)
    fig.update_yaxes(showgrid=False)
    
    return fig

def build_plot_app(data:pd.DataFrame, poll_date:datetime.date="common"):
    # Validate inputs
    try:
        full_df = pd.DataFrame(data)
    except Exception as e:
        print("\n", f"Error Report:    {e}", "\n")

    # Deal with the dates
    copy_df = full_df.copy()

    if poll_date == "common":
        earliest_dates = copy_df.groupby('politician')['end_date'].min()
        earliest_common_date = earliest_dates.max()
        full_df = full_df[full_df['end_date'] >= earliest_common_date]
    else:
        full_df = full_df[full_df['end_date'] >= str(poll_date)]

    # Initialize chart
    fig = go.Figure()

    # Populate data
    trace1 = go.Scatter(x = full_df['end_date'],
                        y = full_df['approve_estimate'].round(2),
                        mode = 'lines',
                        line_shape = 'spline',
                        connectgaps = True,
                        name = "Approve",
                        line = dict(color = 'cyan',
                                    width = 3))
    
    trace2 = go.Scatter(x = full_df['end_date'],
                        y = full_df['disapprove_estimate'],
                        mode = 'lines',
                        line_shape = 'spline',
                        connectgaps = True,
                        name = "Disapprove",
                        line = dict(color = 'magenta',
                                    width = 3))
    
    fig.add_trace(trace2); fig.add_trace(trace1)

    # Update the figure layout
    fig.update_layout(title = "",
                      xaxis_title = "Date",
                      yaxis_title = "Score",
                      legend_title = "Sentiment",
                      hovermode = "x",
                      plot_bgcolor = 'black',
                      paper_bgcolor = 'black',
                      xaxis = {'tickfont':{'color':'#6D8DAD'},
                               'titlefont':{'color':'#6D8DAD',
                                            'family': 'Arial Black'}},
                      yaxis = {'tickfont':{'color':'#6D8DAD'},
                               'titlefont':{'color':'#6D8DAD',
                                            'family': 'Arial Black'}},
                      yaxis_range = None, #[10, 70],# if favorability_type=="Unfavorable" else [20, 60],
                      legend = {'font':{'color':'#6D8DAD'},
                                'title_font': {'family': 'Arial Black'}})
    
    fig.update_xaxes(showgrid=False)
    fig.update_yaxes(showgrid=False)
    
    return fig



#### Main Actions ####
if __name__ == "__main__":
    a = acquire_data(favorability_type="Approval")
    b = build_plot_app(a)
    b.show()