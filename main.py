#### Import Modules ####
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import dataCollection
import streamlit as st
import matplotlib.colors as mcolors



#### Global Objects ####
state_abbreviations = {
    "Alabama": "AL",
    "Alaska": "AK",
    "Arizona": "AZ",
    "Arkansas": "AR",
    "California": "CA",
    "Colorado": "CO",
    "Connecticut": "CT",
    "Delaware": "DE",
    "Florida": "FL",
    "Georgia": "GA",
    "Hawaii": "HI",
    "Idaho": "ID",
    "Illinois": "IL",
    "Indiana": "IN",
    "Iowa": "IA",
    "Kansas": "KS",
    "Kentucky": "KY",
    "Louisiana": "LA",
    "Maine": "ME",
    "Maryland": "MD",
    "Massachusetts": "MA",
    "Michigan": "MI",
    "Minnesota": "MN",
    "Mississippi": "MS",
    "Missouri": "MO",
    "Montana": "MT",
    "Nebraska": "NE",
    "Nevada": "NV",
    "New Hampshire": "NH",
    "New Jersey": "NJ",
    "New Mexico": "NM",
    "New York": "NY",
    "North Carolina": "NC",
    "North Dakota": "ND",
    "Ohio": "OH",
    "Oklahoma": "OK",
    "Oregon": "OR",
    "Pennsylvania": "PA",
    "Rhode Island": "RI",
    "South Carolina": "SC",
    "South Dakota": "SD",
    "Tennessee": "TN",
    "Texas": "TX",
    "Utah": "UT",
    "Vermont": "VT",
    "Virginia": "VA",
    "Washington": "WA",
    "West Virginia": "WV",
    "Wisconsin": "WI",
    "Wyoming": "WY"
}
full_candidate_list = {'Amy Klobuchar': 'DEM', 'Andrew Yang': 'OTH', 'Andy Beshear': 'DEM', 
                       'Andy Cohen': 'IND', 'Bernard Sanders': 'DEM', 'Charles Ballay': 'LIB', 
                       'Chase Oliver': 'LIB', 'Chris Christie': 'REP', 'Chris Sununu': 'REP', 
                       'Cornel West': 'IND', 'Cory A. Booker': 'DEM', 'Dean Phillips': 'IND', 
                       'Donald Trump': 'REP', 'Donald Trump Jr.': 'REP', 'Elizabeth Warren': 'DEM', 
                       'Elon Reeve Musk': 'UNK', 'Gavin Newsom': 'DEM', 'Glenn Youngkin': 'REP', 
                       'Gretchen Whitmer': 'DEM', 'Hillary Rodham Clinton': 'DEM', 'J.B. Pritzker': 'DEM', 
                       'Jerome Michael Segal': 'DEM', 'Jill Stein': 'GRE', 'Joe Biden': 'DEM', 
                       'Joe Manchin, III': 'IND', 'Josh Hawley': 'REP', 'Josh Shapiro': 'DEM', 
                       'Kamala Harris': 'DEM', 'Kanye West': 'REP', 'Kristi Noem': 'REP', 
                       'Larry Hogan': 'IND', 'Lars Mapstead': 'LIB', 'Liz Cheney': 'IND', 
                       'Marco Rubio': 'REP', 'Mark Cuban': 'UNK', 'Matthew David McConaughey': 'IND', 
                       'Michelle Obama': 'DEM', 'Mike Pence': 'REP', 'Mike Pompeo': 'REP', 
                       'Mitt Romney': 'REP', 'Nikki Haley': 'REP', 'Pete Buttigieg': 'DEM', 
                       'Philip Murphy': 'DEM', 'Randall A. Terry': 'CON', 'Rick Scott': 'REP', 
                       'Robert F. Kennedy': 'IND', 'Ron DeSantis': 'REP', 'Taylor Swift': 'DEM', 
                       'Ted Cruz': 'REP', 'Tim Scott': 'REP', 'Tom Cotton': 'REP', 
                       'Vivek G. Ramaswamy': 'REP', 'Al Gore': 'DEM'} 
full_party_list = {'CON': 'white', 'DEM': 'blue', 'GRE': 'green', 'IND': 'beige', 
                   'LIB': 'yellow', 'OTH': 'grey', 'REP': 'red', 'UNK': 'darkgray'}
timeframe_options = ["All polling this cycle", "All of 2024", "Latest polling results",
                     "Latest state polls", "Latest matchup polls", "Last 3 days",
                     "Last 7 days", "Last 14 days", "Last 30 days",
                     "Last 60 days", "Last 90 days", "Last 120 days",
                     "Last 180 days (6 mo)", "Last 270 days (9 mo)", "Last 365 days (1 yr)"]
pollster_options = []
population_options = ["Everyone", "Likely Voters", "Registered Voters", "All Respondents"]
weighting_options = ["Unweighted Average", "Pollster Rating", "Sample Size"]
map_type = "By State"



#### Define Functions ####
def update_opacity_slider():
    # Get values from widget
    '''widget_vals = st.session_state['opacity_slider']
    widget_min = int(widget_vals[0])
    widget_max = int(widget_vals[1])'''
    widget_val = st.session_state['opacity_slider']
    widget_min = st.session_state.opacity_min
    widget_max = widget_val

    # Calculate middle value
    widget_med = (2*widget_max + widget_min) / 3
    widget_med = int(widget_med)

    # Update system variables
    st.session_state.opacity_min = widget_min
    st.session_state.opacity_max = widget_max
    st.session_state.opacity_med = widget_med

    # Update map
    update_button_press()

    return

def weighting_method_change():
    if 'figure' in st.session_state:
        update_button_press()

    return

def set_maptype_national():
    st.session_state.map_type = "National"

    if st.session_state.button_text == "Update Map":
        update_button_press()

    return

def set_maptype_state():
    st.session_state.map_type = "By State"

    if st.session_state.button_text == "Update Map":
        update_button_press()

    return

def refine_candidate_names(candidate_list_list:list) -> list:
    refined_candidate_list = []
    for list_item in candidate_list_list:
        new_entry = ", ".join(list_item)
        refined_candidate_list.append(new_entry)

    return refined_candidate_list

def update_widget_display():
    # Change button appearance
    st.session_state.update_button_disabled = False

    # Get widget display information
    timeframe = st.session_state['timeframe_selectbox']
    pollsters = st.session_state['pollster_selectbox']
    rating = st.session_state['rating_slider']
    population = st.session_state['population_selectbox']
    candidates = st.session_state['matchup_selectbox']

    # Translate the timeframe to function params and date parse
    if timeframe == timeframe_options[0]:
        search_all = True
        search_current_year = False
        days_back = 2000
        starting_df = dataCollection.parse_data_by_date(preliminary_data, days_back, search_current_year, search_all)
    elif timeframe == timeframe_options[1]:
        search_all = False
        search_current_year = True
        days_back = 365
        starting_df = dataCollection.parse_data_by_date(preliminary_data, days_back, search_current_year, search_all)
    elif timeframe == timeframe_options[2]:
        search_all = False
        search_current_year = False
        days_back = 0
        starting_df = dataCollection.parse_data_by_date(preliminary_data, days_back, search_current_year, search_all)
    elif timeframe == timeframe_options[3]:
        starting_df = dataCollection.get_latest_state_polls(preliminary_data)
    elif timeframe == timeframe_options[4]:
        starting_df = dataCollection.get_latest_candidate_polls(preliminary_data)
    elif timeframe == timeframe_options[5]:
        search_all = False
        search_current_year = False
        days_back = 3
        starting_df = dataCollection.parse_data_by_date(preliminary_data, days_back, search_current_year, search_all)
    elif timeframe == timeframe_options[6]:
        search_all = False
        search_current_year = False
        days_back = 7
        starting_df = dataCollection.parse_data_by_date(preliminary_data, days_back, search_current_year, search_all)
    elif timeframe == timeframe_options[7]:
        search_all = False
        search_current_year = False
        days_back = 14
        starting_df = dataCollection.parse_data_by_date(preliminary_data, days_back, search_current_year, search_all)
    elif timeframe == timeframe_options[8]:
        search_all = False
        search_current_year = False
        days_back = 30
        starting_df = dataCollection.parse_data_by_date(preliminary_data, days_back, search_current_year, search_all)
    elif timeframe == timeframe_options[9]:
        search_all = False
        search_current_year = False
        days_back = 60
        starting_df = dataCollection.parse_data_by_date(preliminary_data, days_back, search_current_year, search_all)
    elif timeframe == timeframe_options[10]:
        search_all = False
        search_current_year = False
        days_back = 90
        starting_df = dataCollection.parse_data_by_date(preliminary_data, days_back, search_current_year, search_all)
    elif timeframe == timeframe_options[11]:
        search_all = False
        search_current_year = False
        days_back = 120
        starting_df = dataCollection.parse_data_by_date(preliminary_data, days_back, search_current_year, search_all)
    elif timeframe == timeframe_options[12]:
        search_all = False
        search_current_year = False
        days_back = 180
        starting_df = dataCollection.parse_data_by_date(preliminary_data, days_back, search_current_year, search_all)
    elif timeframe == timeframe_options[13]:
        search_all = False
        search_current_year = False
        days_back = 270
        starting_df = dataCollection.parse_data_by_date(preliminary_data, days_back, search_current_year, search_all)
    elif timeframe == timeframe_options[14]:
        search_all = False
        search_current_year = False
        days_back = 365
        starting_df = dataCollection.parse_data_by_date(preliminary_data, days_back, search_current_year, search_all)
    else:
        starting_df = dataCollection.get_latest_candidate_polls(preliminary_data)

    # Parse by pollster, rating, population, and candidate selections
    rating_df = dataCollection.parse_data_by_rating(starting_df, min=rating[0], max=rating[1])
    pollster_df = dataCollection.parse_data_by_pollster(rating_df, pollsters=pollsters)
    population_df = dataCollection.parse_by_population(pollster_df, pop_type=population)

    # Extract new lists from parsed data
    new_pollster_list = sorted(set(rating_df['pollster']))
    new_population_list = dataCollection.extract_population_types(pollster_df)
    rough_candidate_list = dataCollection.extract_candidate_groups(population_df)
    new_candidate_list = refine_candidate_names(rough_candidate_list)

    # Update widget dataset
    st.session_state.pollster_options = new_pollster_list
    st.session_state.population_options = new_population_list
    st.session_state.candidate_options = new_candidate_list

    return

def update_button_press():
    # Change button appearance
    st.session_state.update_button_disabled = True
    st.session_state.button_text = "Update Map"

    # Get widget display information
    timeframe = st.session_state['timeframe_selectbox']
    pollsters = st.session_state['pollster_selectbox']
    rating = st.session_state['rating_slider']
    population = st.session_state['population_selectbox']
    candidates = st.session_state['matchup_selectbox']

    if candidates:
        candidates = candidates.split(', ')
    else:
        return
    if "Joe Manchin" in candidates:
        candidates[candidates.index('Joe Manchin')] = 'Joe Manchin, III'
        candidates.remove('III')

    weight = st.session_state['weighting_selectbox']
    if weight == "Pollster Rating":
        weight = "pollster grade"
    elif weight == "Sample Size":
        weight = "sample size"
    else:
        weight = "unweighted average"

    # Validate that necessary data exists (timeframe, rating, population, and candidates)
    if not (timeframe and rating and population and candidates):
        st.subheader(":red[There is insufficient data to generate a map.  Please make sure all selections are made.]")
        return
    else:
        pass

    # Parse data by current selections
    if timeframe == timeframe_options[0]:
        search_all = True
        search_current_year = False
        days_back = 2000
        starting_df = dataCollection.parse_data_by_date(preliminary_data, days_back, search_current_year, search_all)
    elif timeframe == timeframe_options[1]:
        search_all = False
        search_current_year = True
        days_back = 365
        starting_df = dataCollection.parse_data_by_date(preliminary_data, days_back, search_current_year, search_all)
    elif timeframe == timeframe_options[2]:
        search_all = False
        search_current_year = False
        days_back = 0
        starting_df = dataCollection.parse_data_by_date(preliminary_data, days_back, search_current_year, search_all)
    elif timeframe == timeframe_options[3]:
        starting_df = dataCollection.get_latest_state_polls(preliminary_data)
    elif timeframe == timeframe_options[4]:
        starting_df = dataCollection.get_latest_candidate_polls(preliminary_data)
    elif timeframe == timeframe_options[5]:
        search_all = False
        search_current_year = False
        days_back = 3
        starting_df = dataCollection.parse_data_by_date(preliminary_data, days_back, search_current_year, search_all)
    elif timeframe == timeframe_options[6]:
        search_all = False
        search_current_year = False
        days_back = 7
        starting_df = dataCollection.parse_data_by_date(preliminary_data, days_back, search_current_year, search_all)
    elif timeframe == timeframe_options[7]:
        search_all = False
        search_current_year = False
        days_back = 14
        starting_df = dataCollection.parse_data_by_date(preliminary_data, days_back, search_current_year, search_all)
    elif timeframe == timeframe_options[8]:
        search_all = False
        search_current_year = False
        days_back = 30
        starting_df = dataCollection.parse_data_by_date(preliminary_data, days_back, search_current_year, search_all)
    elif timeframe == timeframe_options[9]:
        search_all = False
        search_current_year = False
        days_back = 60
        starting_df = dataCollection.parse_data_by_date(preliminary_data, days_back, search_current_year, search_all)
    elif timeframe == timeframe_options[10]:
        search_all = False
        search_current_year = False
        days_back = 90
        starting_df = dataCollection.parse_data_by_date(preliminary_data, days_back, search_current_year, search_all)
    elif timeframe == timeframe_options[11]:
        search_all = False
        search_current_year = False
        days_back = 120
        starting_df = dataCollection.parse_data_by_date(preliminary_data, days_back, search_current_year, search_all)
    elif timeframe == timeframe_options[12]:
        search_all = False
        search_current_year = False
        days_back = 180
        starting_df = dataCollection.parse_data_by_date(preliminary_data, days_back, search_current_year, search_all)
    elif timeframe == timeframe_options[13]:
        search_all = False
        search_current_year = False
        days_back = 270
        starting_df = dataCollection.parse_data_by_date(preliminary_data, days_back, search_current_year, search_all)
    elif timeframe == timeframe_options[14]:
        search_all = False
        search_current_year = False
        days_back = 365
        starting_df = dataCollection.parse_data_by_date(preliminary_data, days_back, search_current_year, search_all)
    else:
        starting_df = dataCollection.get_latest_candidate_polls(preliminary_data)

    # Parse by pollster, rating, population, and candidate selections
    rating_df = dataCollection.parse_data_by_rating(starting_df, min=rating[0], max=rating[1])
    pollster_df = dataCollection.parse_data_by_pollster(rating_df, pollsters=pollsters)
    population_df = dataCollection.parse_by_population(pollster_df, pop_type=population)
    parsed_df = dataCollection.parse_by_candidates(population_df, candidate_selection=candidates)

    # Use parsed data to get calculations
    poll_results_df = dataCollection.data_processing(parsed_df, candidate_list=candidates, weight_type=weight)
    electoral_vote_df, polled_state_list = dataCollection.calculate_electoral_votes(poll_results_df, candidate_list=candidates)

    make_map(poll_results_df, electoral_vote_df, polled_state_list, timeframe)

    return

def make_map(poll_scores:pd.DataFrame, electoral_votes:pd.DataFrame, state_list:list, title_str:str):
    # New color translator
    my_color_map = {x: full_party_list[full_candidate_list[x]] for x in full_candidate_list.keys()}
    my_color_map[None] = 'indigo'
    my_color_map['None'] = 'indigo'

    # Create data structure
    map_data_state = {}
    state_abbrev_list = []
    state_name_list = []
    winner_list = []
    score_list = []
    party_list = []
    candidate_list = []
    elector_list = []
    hovertext_list = []
    for state in state_abbreviations.keys():
        state_abbrev = state_abbreviations[state]
        state_abbrev_list.append(state_abbrev)

        if st.session_state.map_type == 'National':
            state_name_list.append('National')
        elif st.session_state.map_type == 'By State':
            state_name_list.append(state)

        if st.session_state.map_type == 'National':
            winner = poll_scores['National'].idxmax() if 'National' in poll_scores.columns else None
        elif st.session_state.map_type == 'By State':
            winner = poll_scores[state].idxmax() if state in poll_scores.columns else None
        winner_list.append(winner)
        
        candidates = [x for x in poll_scores.index]
        candidate_list.append(candidates)

        if st.session_state.map_type == 'National':
            score = poll_scores['National'] if 'National' in poll_scores.columns else None
        elif st.session_state.map_type == 'By State':
            score = poll_scores[state] if state in poll_scores.columns else None
        score_list.append(score)

        party = full_candidate_list[winner] if winner else None
        party_list.append(party)

        if st.session_state.map_type == 'National':
            electors = electoral_votes['Total'].sum() if 'Total' in electoral_votes.columns else None
        elif st.session_state.map_type == 'By State':
            electors = electoral_votes[state].max() if state in electoral_votes.columns else None
        elector_list.append(electors)

        if st.session_state.map_type == 'By State':
            if state in poll_scores.columns:
                hover_text = f"<b>{state}</b><br><br>"
                hover_text += f"{poll_scores[state].idxmax()} is currently leading in {state}<br><br>"
                state_electors = electoral_votes[state].max()
                for candidate in candidates:
                    hover_text += f"     {candidate}  -  {score[candidate]}%<br>"
                hover_text += f"<br>{state} has {state_electors} electors"
            else:
                hover_text = None
        elif st.session_state.map_type == 'National':
            if 'National' in poll_scores.columns:
                hover_text = f"<b>National</b><br><br>"
                hover_text += f"{poll_scores['National'].idxmax()} is currently leading nationally<br><br>"
                state_electors = electoral_votes['Total'].sum()
                for candidate in candidates:
                    hover_text += f"     {candidate}  -  {poll_scores['National'][candidate]}%<br>"
                hover_text += f"<br>This survey covers {state_electors} electors"
            else:
                hover_text = None
        hovertext_list.append(hover_text)

    map_data_state['States'] = state_abbrev_list
    map_data_state['State Names'] = state_name_list
    map_data_state['Score'] = score_list
    map_data_state['Party'] = party_list
    map_data_state['Winner'] = winner_list
    map_data_state['Candidates'] = candidate_list
    map_data_state['Electoral Count'] = elector_list
    map_data_state['Hover Text'] = hovertext_list

    electoral_dict = dict(electoral_votes['Total'])
    annotations = []
    shapes = []

    x_start = 0.80
    y_start = 0.325
    y_step = 0.05

    for i, (candidate, votes) in enumerate(electoral_dict.items()):
        candidate_party = full_candidate_list[candidate]
        percentage = poll_scores['National'][candidate] if 'National' in poll_scores.columns else 0

        shapes.append(go.layout.Shape(type='rect',
                                      x0=x_start + 0.01,
                                      y0=y_start - ((i) * y_step) + 0.0225,
                                      x1=x_start + 0.02,
                                      y1=y_start - ((i) * y_step) + 0.0025,
                                      xanchor='top',
                                      yanchor='left',
                                      xref='paper',
                                      yref='paper',
                                      fillcolor=my_color_map[candidate],
                                      line=dict(color='lightgray')))
        
        if st.session_state.map_type == 'By State':
            annotations.append(dict(x=x_start + 0.025,
                                    y=y_start - (i * y_step),
                                    xanchor='left',
                                    xref='paper',
                                    yref='paper',
                                    text=f"<b>{candidate} ({candidate_party})</b>  - {votes} EVs",
                                    showarrow=False,
                                    font={'size':12, 'color':'white'}))
            
        elif st.session_state.map_type == 'National':
            annotations.append(dict(x=x_start + 0.025,
                                    y=y_start - (i * y_step),
                                    xanchor='left',
                                    xref='paper',
                                    yref='paper',
                                    text=f"<b>{candidate} ({candidate_party})</b>  - {percentage}%",
                                    showarrow=False,
                                    font={'size':12, 'color':'white'}))

    fig = px.choropleth(map_data_state,
                        title=f"<b>{title_str.title()}  -  {st.session_state.map_type}</b>",
                        locations='States',
                        locationmode='USA-states',
                        color='Winner',
                        color_discrete_map=my_color_map,
                        hover_name='State Names',
                        hover_data={},
                        custom_data='Hover Text',
                        labels={'Winner':'Leading Candidate'},
                        scope='usa')
    
    z_list = []
    for trace in fig.data:
        # Get or set initial variables
        cand_name = trace.name
        cand_state_list = list(trace.hovertext)
        cand_state_list = [x for x in cand_state_list if x in poll_scores.columns]
        cand_score_list = []

        # Get candidate-specific scores
        for cand_state in cand_state_list:
            cand_score_list.append(poll_scores[cand_state][cand_name])
            z_list.append(poll_scores[cand_state][cand_name])

        # Get opacity settings
        opacity_min = round(st.session_state.opacity_min/100, 1)
        opacity_max = round(st.session_state.opacity_max/100, 1)
        opacity_med = round(st.session_state.opacity_med/100, 1)

        # Set colorscale by candidate's color
        color = my_color_map[cand_name]
        color_rgba = mcolors.to_rgba(color)
        r, g, b = color_rgba[0:3]

        # Make dark and light colors (alternative approach)
        dark_r, dark_g, dark_b = 255*max(r-0.5, 0), 255*max(g-0.5, 0), 255*max(b-0.5, 0)
        light_r, light_g, light_b = 255*min(r+0.85, 1), 255*min(g+0.85, 1), 255*min(b+0.85, 1)

        lowcolor = f"rgba({dark_r}, {dark_g}, {dark_b}, {opacity_max})"
        midcolor = f"rgba({r}, {g}, {b}, {opacity_max})"
        hicolor = f"rgba({light_r}, {light_g}, {light_b}, {opacity_max})"

        if st.session_state.map_type == 'By State':
            colorscale = [[0.0, hicolor], [0.5, midcolor], [1.0, lowcolor]]
        elif st.session_state.map_type == 'National':
            colorscale = [[0.0, midcolor], [1.0, midcolor]]

        # Set new parameters for the trace
        trace.z = cand_score_list if cand_score_list else trace.z
        #trace.zmin = 40
        #trace.zmax = 100
        #trace.zmid = 50
        trace.colorscale = colorscale

    if z_list:
        z_list.sort()
        z_min = z_list[0]
        z_max= z_list[-1]
        fig.update_traces(hovertemplate="%{customdata}",
                        zmin=z_min,
                        zmax=z_max)
    else:
        fig.update_traces(hovertemplate="%{customdata}")
    
    fig.update_geos(visible=False, 
                    resolution=50,
                    showcountries=False,
                    showsubunits=True,
                    subunitcolor="white")
    
    fig.update_layout(geo=dict(bgcolor= 'rgba(0,0,0,0)'),
                      plot_bgcolor='rgba(0,0,0,0)',
                      paper_bgcolor='rgba(0,0,0,0)',
                      margin=dict(l=0, r=0, t=0, b=0),
                      width=1800,
                      height=700,
                      title={'font':{'size':20, 'color':'white'}, 'x':0.5, 'y':0.975, 'xanchor': 'center'},
                      legend={'y': 0.75, 'yanchor': 'middle'},
                      showlegend=False,
                      annotations=annotations,
                      shapes=shapes,
                      dragmode=False)
    
    st.session_state.figure = fig

    return

@st.cache_data
def initial_data_load():
    global full_candidate_list

    preliminary_data = dataCollection.acquire_latest_data()
    preliminary_candidates = dataCollection.extract_candidate_groups(preliminary_data)
    preliminary_pollsters = sorted(set(preliminary_data['pollster']))

    all_candidates = sorted(set(preliminary_data['candidate_name']))
    full_candidate_list = {}
    
    for ind_candidate in all_candidates:
        cand_party = preliminary_data.loc[preliminary_data['candidate_name'] == ind_candidate, "party"].values[0]
        full_candidate_list[ind_candidate] = cand_party

    return preliminary_data, preliminary_candidates, preliminary_pollsters



#### Startup Actions ####
st.set_page_config(page_title="US Map", layout="wide")

preliminary_data, preliminary_candidates, preliminary_pollsters = initial_data_load()
candidate_options = refine_candidate_names(preliminary_candidates)
pollster_options = preliminary_pollsters

if 'disable_candidate_matchups' not in st.session_state:
    st.session_state['disable_candidate_matchups'] = False
if 'weighting_options' not in st.session_state:
    st.session_state['weighting_options'] = weighting_options
if 'timeframe_options' not in st.session_state:
    st.session_state['timeframe_options'] = timeframe_options
if 'pollster_options' not in st.session_state:
    st.session_state['pollster_options'] = pollster_options
if 'population_options' not in st.session_state:
    st.session_state['population_options'] = population_options
if 'candidate_options' not in st.session_state:
    st.session_state['candidate_options'] = candidate_options
if 'map_type' not in st.session_state:
    st.session_state['map_type'] = map_type
if 'update_button_disabled' not in st.session_state:
    st.session_state['update_button_disabled'] = False
if 'figure' not in st.session_state:
    st.session_state['figure'] = None
if 'button_text' not in st.session_state:
    st.session_state['button_text'] = "Generate Map"
if 'run_initial' not in st.session_state:
    st.session_state['run_initial'] = True
if 'opacity_min' not in st.session_state:
    st.session_state['opacity_min'] = 30
if 'opacity_med' not in st.session_state:
    st.session_state['opacity_med'] = 90
if 'opacity_max' not in st.session_state:
    st.session_state['opacity_max'] = 100



#### Page Layout ####
# Top Main Line
st.title("United States Election Polling Map",
         help="Data supplied by FiveThirtyEight.com aggregate presidential polls")

col1, col2, col3 = st.columns([1,1,3])
with col1:
    st.button(label="National",
              key="national_button",
              help="Displays national data on the map",
              use_container_width=True,
              on_click=set_maptype_national)
with col2:
    st.button(label="By State",
              key="bystate_button",
              help="Displays the statewide data on the map",
              use_container_width=True,
              on_click=set_maptype_state)

if st.session_state.figure:
    st.plotly_chart(st.session_state.figure)
    
# Sidebar options

st.sidebar.header("Weighting Method")
st.sidebar.selectbox("Method Selection",
                     options=st.session_state.weighting_options,
                     key="weighting_selectbox",
                     on_change=weighting_method_change)

st.sidebar.header("Filter Options")

st.sidebar.selectbox("Timeframe", 
                     options=st.session_state.timeframe_options,
                     key="timeframe_selectbox",
                     on_change=update_widget_display)
st.sidebar.multiselect("Pollsters",
                       options=st.session_state.pollster_options,
                       key="pollster_selectbox",
                       help="Leaving this blank includes all pollsters.",
                       on_change=update_widget_display)
st.sidebar.slider("Pollster Rating",
                  min_value=0.1,
                  max_value=3.0,
                  value=(0.1, 3.0),
                  step=0.1,
                  key="rating_slider",
                  on_change=update_widget_display)
st.sidebar.selectbox("Polling Population",
                     options=st.session_state.population_options,
                     key="population_selectbox",
                     help="For technical reasons, 'everyone' and 'all respondents' are not the same.  'Everyone' is broader.",
                     on_change=update_widget_display)

st.sidebar.selectbox("Candidate Matchups",
                     options=st.session_state.candidate_options,
                     key="matchup_selectbox",
                     on_change=update_widget_display)

st.sidebar.button(label=st.session_state.button_text,
                  key="update_button",
                  type="primary",
                  disabled=st.session_state.update_button_disabled,
                  on_click=update_button_press)

st.sidebar.header("")
st.sidebar.header("")
st.sidebar.slider("Opacity Setting",
                  min_value=5,
                  max_value=100,
                  value=(st.session_state.opacity_max),
                  step=1,
                  key="opacity_slider",
                  on_change=update_opacity_slider,
                  help="Sets the color range for the map.  A larger range shows a bigger difference between states.  The color for the national map is calculated based off these settings.")

if st.session_state.run_initial:
    update_widget_display()
    update_button_press()
    st.session_state.run_initial = False
    st.rerun()
