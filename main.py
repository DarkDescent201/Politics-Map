#### Import Modules ####
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import dataCollection, chartData
import streamlit as st
import matplotlib.colors as mcolors
from datetime import datetime, timedelta



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
                       'Vivek G. Ramaswamy': 'REP', 'Al Gore': 'DEM', 'Claudia De La Cruz': 'PSL'} 
full_party_list = {'CON': 'white', 'DEM': 'blue', 'GRE': 'green', 'IND': 'beige', 
                   'LIB': 'yellow', 'OTH': 'grey', 'REP': 'red', 'UNK': 'darkgray',
                   'PSL': 'crimson'}
timeframe_options = ["All polling this cycle", "All of 2024", "Latest polling results",
                     "Latest state polls", "Latest matchup polls", "Last 3 days",
                     "Last 7 days", "Last 14 days", "Last 30 days",
                     "Last 60 days", "Last 90 days", "Last 120 days",
                     "Last 180 days (6 mo)", "Last 270 days (9 mo)", "Last 365 days (1 yr)"]
pollster_options = []
population_options = ["Everyone", "Likely Voters", "Registered Voters", "All Respondents"]
weighting_options = ["Unweighted Average", "Pollster Rating", "Sample Size", "Recency"]
map_type = "By State"
quantity_options = [25, 50, 100, 250, 500, 1000, 2000]
timeline_options = ["Earliest Common Date", "Entire Election Cycle", "Last 30 Days",
                    "Last 60 Days", "Last 90 Days", "Last 120 Days",
                    "Last 6 Months", "Last 9 Months", "Last Year"]



#### Define Functions ####
def set_poll_timeline():
    # Get values from widget
    widget_val = st.session_state["favor_time"]
    now = datetime.now()

    # Set response value conditionally
    if widget_val == "Entire Election Cycle":
        new_date = "2021-01-01"
    elif widget_val == "Last 30 Days":
        new_date = now - timedelta(days=30)
        new_date = new_date.date()
    elif widget_val == "Last 60 Days":
        new_date = now - timedelta(days=60)
        new_date = new_date.date()
    elif widget_val == "Last 90 Days":
        new_date = now - timedelta(days=90)
        new_date = new_date.date()
    elif widget_val == "Last 120 Days":
        new_date = now - timedelta(days=120)
        new_date = new_date.date()
    elif widget_val == "Last 6 Months":
        new_date = now - timedelta(days=180)
        new_date = new_date.date()
    elif widget_val == "Last 9 Months":
        new_date = now - timedelta(days=270)
        new_date = new_date.date()
    elif widget_val == "Last Year":
        new_date = now - timedelta(days=365)
        new_date = new_date.date()
    else:
        new_date = "common"

    # Update system variables
    st.session_state.chart_timeline = new_date

    # Update map
    update_button_press()

    return

def set_poll_quantity():
    # Get values from widget
    widget_val = st.session_state["quantity_selector"]

    # Update system variables
    st.session_state.poll_quantity = int(widget_val)

    # Update map
    update_button_press()

    return

def update_color_slider():
    # Get values from widget
    widget_val = st.session_state["color_selector"]

    # Update system variables
    st.session_state.color_state = widget_val

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

def set_favtype_favorable():
    st.session_state.favor_type = "Favorable"

    if st.session_state.button_text == "Update Map":
        update_button_press()

    return

def set_favtype_unfavorable():
    st.session_state.favor_type = "Unfavorable"

    if st.session_state.button_text == "Update Map":
        update_button_press()

    return

def set_favtype_approval():
    st.session_state.favor_type = "Approval"

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
    elif weight == "Recency":
        weight = "recency"
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

    get_poll_data(parsed_df)
    get_favorability_chart([st.session_state.show_dt, st.session_state.show_jb, st.session_state.show_rfk],
                           st.session_state.chart_timeline)
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
    margin_dict = {}

    # Fill data structure with all components
    for state in state_abbreviations.keys():
        state_abbrev = state_abbreviations[state]
        state_abbrev_list.append(state_abbrev)

        # Add state names
        if st.session_state.map_type == 'National':
            state_name_list.append('National')
        elif st.session_state.map_type == 'By State':
            state_name_list.append(state)

        # Find winners
        if st.session_state.map_type == 'National':
            winner = poll_scores['National'].idxmax() if 'National' in poll_scores.columns else None
        elif st.session_state.map_type == 'By State':
            winner = poll_scores[state].idxmax() if state in poll_scores.columns else None
        winner_list.append(winner)
        
        # Make list of all candidates
        candidates = [x for x in poll_scores.index]
        candidate_list.append(candidates)

        # Make dictionary of winning margins
        margin_list = []
        for candidate in candidates:
            index_name = state if st.session_state.map_type == "By State" else "National"
            top_score = poll_scores[index_name].max() if index_name in poll_scores.columns else 0
            candidate_score = poll_scores[index_name][candidate] if index_name in poll_scores.columns else 0
            winning_margin = top_score - candidate_score
            winning_margin = round(winning_margin, 1)
            margin_list.append(winning_margin)
        margin_list.sort()
        margin_dict[state if st.session_state.map_type=="By State" else "National"] = margin_list

        # Add pd.Series of candidate scores
        if st.session_state.map_type == 'National':
            score = poll_scores['National'] if 'National' in poll_scores.columns else None
        elif st.session_state.map_type == 'By State':
            score = poll_scores[state] if state in poll_scores.columns else None
        score_list.append(score)

        # Make party list of winner
        party = full_candidate_list[winner] if winner else None
        party_list.append(party)

        # Account for number of electoral votes
        if st.session_state.map_type == 'National':
            electors = electoral_votes['Total'].sum() if 'Total' in electoral_votes.columns else None
        elif st.session_state.map_type == 'By State':
            electors = electoral_votes[state].max() if state in electoral_votes.columns else None
        elector_list.append(electors)

        # Set the custom hover-text by state based on previous variables
        if st.session_state.map_type == 'By State':
            if state in poll_scores.columns:
                hover_text = f"<b>{state}</b><br><br>"
                hover_text += f"{poll_scores[state].idxmax()} is currently leading in {state}<br>"
                hover_text += f"by a margin of {margin_list[-1 if st.session_state.color_state=='Widest Margin' else 1]}%<br><br>"
                state_electors = electoral_votes[state].max()
                for candidate in candidates:
                    hover_text += f"     {candidate}  -  {score[candidate]}%<br>"
                hover_text += f"<br>{state} has {state_electors} electors"
            else:
                hover_text = None
        elif st.session_state.map_type == 'National':
            if 'National' in poll_scores.columns:
                hover_text = f"<b>National</b><br><br>"
                hover_text += f"{poll_scores['National'].idxmax()} is currently leading nationally<br>"
                hover_text += f"by a margin of {margin_list[-1 if st.session_state.color_state=='Widest Margin' else 1]}%<br><br>"
                state_electors = electoral_votes['Total'].sum()
                for candidate in candidates:
                    hover_text += f"     {candidate}  -  {poll_scores['National'][candidate]}%<br>"
                hover_text += f"<br>This survey covers {state_electors} electors"
            else:
                hover_text = None
        hovertext_list.append(hover_text)

    # Load data structure with variables
    map_data_state['States'] = state_abbrev_list
    map_data_state['State Names'] = state_name_list
    map_data_state['Score'] = score_list
    map_data_state['Party'] = party_list
    map_data_state['Winner'] = winner_list
    map_data_state['Candidates'] = candidate_list
    map_data_state['Electoral Count'] = elector_list
    map_data_state['Hover Text'] = hovertext_list

    map_data_state = pd.DataFrame(map_data_state)

    # Set preliminaries for map generation
    electoral_dict = dict(electoral_votes['Total'])

    # Generate the map after defining annotations
    fig = px.choropleth(map_data_state,
                        title=f"<b>{title_str.title()}  -  {st.session_state.map_type}</b>",
                        locations='States',
                        locationmode='USA-states',
                        color='Winner',
                        color_discrete_map=my_color_map,
                        hover_name='State Names',
                        hover_data={},
                        custom_data='Hover Text',
                        labels={'Winner':""},
                        scope='usa')
    
    # Customize traces, particularly for state coloring
    z_list = []
    for trace in fig.data:
        # Get or set initial variables
        cand_name = trace.name
        cand_state_list = list(trace.hovertext)
        cand_state_list = [x for x in cand_state_list if x in poll_scores.columns]
        cand_score_list = []
        cand_margin_list = []
        current_z_list = []
        if cand_name not in [None, 'None']:
            electoral_count = electoral_dict[cand_name]
            natl_percentage = poll_scores['National'][cand_name] if 'National' in poll_scores.columns else 0
            cand_party = full_candidate_list[cand_name][0]
        else:
            electoral_count = 0
            natl_percentage = 0
            cand_party = ""

        # Get candidate-specific scores and margins
        for cand_state in cand_state_list:
            # Get candidate scores
            cand_score = poll_scores[cand_state][cand_name]
            cand_score_list.append(cand_score)

            # Get candidate margins
            cand_margin_list = margin_dict[cand_state]
            cand_margin_list.sort()
            high_margin = cand_margin_list[-1]
            low_margin = cand_margin_list[1]

            # Conditionally append the scorelist
            if st.session_state.color_state == "Vote %":
                current_z_list.append(cand_score); z_list.append(cand_score)
            elif st.session_state.color_state == "Widest Margin":
                current_z_list.append(high_margin); z_list.append(high_margin)
            else:
                current_z_list.append(low_margin); z_list.append(low_margin)

        # Set colorscale by candidate's color
        color = my_color_map[cand_name]
        color_rgba = mcolors.to_rgba(color)
        r, g, b = color_rgba[0:3]

        # Make dark and light colors (alternative approach)
        dark_r, dark_g, dark_b = 255*max(r-0.5, 0), 255*max(g-0.5, 0), 255*max(b-0.5, 0)
        light_r, light_g, light_b = 255*min(r+0.85, 1), 255*min(g+0.85, 1), 255*min(b+0.85, 1)

        lowcolor = f"rgba({dark_r}, {dark_g}, {dark_b}, 255)"
        midcolor = f"rgba({r}, {g}, {b}, 255)"
        hicolor = f"rgba({light_r}, {light_g}, {light_b}, 255)"

        if st.session_state.map_type == 'By State':
            colorscale = [[0.0, hicolor], [0.5, midcolor], [1.0, lowcolor]]
        elif st.session_state.map_type == 'National':
            colorscale = [[0.0, midcolor], [1.0, midcolor]]

        # Set new parameters for the trace
        trace.z = current_z_list if current_z_list else trace.z
        trace.colorscale = colorscale
        if trace.name in [None, 'None']:
            trace.name = "<b>No polls for this range</b>"
        else:
            if st.session_state.map_type == "By State":
                trace.name = f"<b>{cand_name} ({cand_party})</b>   -   {electoral_count} EC votes"
            elif st.session_state.map_type == "National":
                trace.name = f"<b>{cand_name} ({cand_party})</b>   -   {natl_percentage}%"

    # Set the overall data comparison range
    if z_list:
        z_list.sort()
        z_min = z_list[0]
        z_max= z_list[-1]
        fig.update_traces(hovertemplate="%{customdata}",
                        zmin=z_min,
                        zmax=z_max)
    else:
        fig.update_traces(hovertemplate="%{customdata}")

    # Add dummy traces for missing candidates
    present_candidates = map_data_state['Winner'].unique()
    for candidate_item in candidates:
        candidate_party = full_candidate_list[candidate_item][0]
        if st.session_state.map_type == "National":
            natl_score = poll_scores['National'][candidate_item] if 'National' in poll_scores.columns else 0
            text_add = f"   -   {natl_score}%"
        elif st.session_state.map_type == "By State":
            elec_score = electoral_count = electoral_dict[candidate_item] if candidate_item in electoral_dict.keys() else 0
            text_add = f"   -   {elec_score} EC votes"
        else:
            text_add = ""
        if candidate_item not in present_candidates:
            dummy_trace = (go.Scatter(
                x=[None], y=[None],
                mode='markers',
                marker=dict(size=14, color=my_color_map[candidate_item]),
                showlegend=True,
                name=f"<b>{candidate_item} ({candidate_party})</b>"+text_add))

            # Add the trace
            fig.add_trace(dummy_trace)
    
    fig.update_geos(visible=False, 
                    resolution=50,
                    showcountries=False,
                    showsubunits=True,
                    subunitcolor="white")
    
    fig.update_layout(geo=dict(bgcolor= 'rgba(0,0,0,0)'),
                      plot_bgcolor='rgba(0,0,0,0)',
                      paper_bgcolor='rgba(0,0,0,0)',
                      margin=dict(l=0, r=0, t=0, b=0),
                      width=1400,
                      height=700,
                      title={'font':{'size':20, 'color':'white'}, 
                             'x':0.5, 'xanchor': 'center',
                             'y':1, 'yanchor':'top'},
                      legend={'y': 0, 'yanchor': 'top',
                              'x': 0.5, 'xanchor': 'center',
                              'orientation': 'h', 
                              'bordercolor': 'white', 'borderwidth': 0},
                      showlegend=True,
                      dragmode=False,
                      xaxis_visible=False,
                      yaxis_visible=False)
    
    st.session_state.figure = fig

    return

def get_poll_data(data:pd.DataFrame):
    # Sort DataFrame by date descending
    data = data.sort_values(by='end_date', ascending=False)

    # Get list of unique poll IDs
    pollID_list = data['poll_id'].unique()

    #Build the title row string
    lab1, lab2, lab3 = "Date:", "Range:", "Pollster:"
    lab4, lab5, lab6 = "Grade:","Sample:", "Population:"

    title_str = [lab1, lab2, lab3, lab4, lab5, lab6]

    st.session_state.poll_header = title_str

    # Get poll data by column
    working_list = []
    for pollID in pollID_list:
        working_df = data.loc[data['poll_id']==pollID]
        sample_size = working_df['sample_size'].values[0]
        pollster = working_df['pollster'].values[0]
        numeric_grade = working_df['numeric_grade'].values[0]
        methodology = working_df['methodology'].values[0]
        poll_state = working_df['state'].values[0]
        poll_date = working_df['end_date'].values[0]
        voter_population = working_df['population'].values[0]
        # Elaborate voter population
        if voter_population == 'rv':
            voter_population = "Registered Voters"
        elif voter_population == 'lv':
            voter_population = "Likely Voters"
        elif voter_population == 'v':
            voter_population = "Voters"
        else:
            voter_population = "All Respondents"
        # Elaborate on polled state
        if poll_state == " ":
            poll_state = "National"
        # Round numeric grade
        numeric_grade = round(numeric_grade, 1)

        # Build the main string
        item1, item2, item3 = str(poll_date), poll_state, pollster
        item4, item5, item6 = numeric_grade, int(sample_size), voter_population

        working_list.append([item1, item2, item3, item4, item5, item6])
    
    if len(working_list) > st.session_state.poll_quantity:
        st.session_state.poll_text = working_list[:st.session_state.poll_quantity]
    else:
        st.session_state.poll_text = working_list[:-1]

    return

def get_favorability_chart(showlist:list=[True,True,True], start_date:datetime.date="common"):
    display_date = start_date
    favorability_type = st.session_state.favor_type

    chart_data = chartData.acquire_data(showlist, favorability_type)

    if st.session_state.favor_type in ["Favorable", "Unfavorable"]:
        chart_figure = chartData.build_plot_fav(chart_data, display_date, favorability_type)
    elif st.session_state.favor_type == "Approval":
        chart_figure = chartData.build_plot_app(chart_data, display_date)

    st.session_state.favorability_chart = chart_figure

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

        if cand_party not in full_party_list.keys():
            full_party_list[cand_party] = 'lightgreen'
        else:
            pass

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
if 'color_state' not in st.session_state:
    st.session_state['color_state'] = "Vote %"
if 'poll_text' not in st.session_state:
    st.session_state['poll_text'] = None
if 'poll_header' not in st.session_state:
    st.session_state['poll_header'] = None
if 'poll_quantity' not in st.session_state:
    st.session_state['poll_quantity'] = 25
if 'favorability_chart' not in st.session_state:
    st.session_state['favorability_chart'] = None
if 'show_dt' not in st.session_state:
    st.session_state['show_dt'] = True
if 'show_jb' not in st.session_state:
    st.session_state['show_jb'] = True
if 'show_rfk' not in st.session_state:
    st.session_state['show_rfk'] = True
if 'favor_type' not in st.session_state:
    st.session_state['favor_type'] = "Approval"
if 'chart_timeline' not in st.session_state:
    st.session_state['chart_timeline'] = 'common'


#### Page Layout ####
# Page title
colu1, colu2, colu3 = st.columns([1,2,1])
with colu2:
    st.title("2024 Presidential Election Data")

# Top Main Line
st.subheader("Favorability Tracking",
             help="Data supplied by FiveThirtyEight.com favorability and approval polls.  Click on a candidate's name to toggle them on or off from the view.  Approval Rating always refers to the current administration.")

# Add favorability chart
if st.session_state.favorability_chart:
    col11, col22, col33, col44, col55 = st.columns([1,1,1,3,2])

    with col11:
        st.button(label="Favorability",
                key="favorable_button",
                help="Displays favorability data on the chart.",
                use_container_width=True,
                type="primary" if st.session_state.favor_type=="Favorable" else "secondary",
                on_click=set_favtype_favorable)
    with col22:
        st.button(label="Unfavorability",
                key="unfavorable_button",
                help="Displays unfavorability data on the chart.",
                use_container_width=True,
                type="primary" if st.session_state.favor_type=="Unfavorable" else "secondary",
                on_click=set_favtype_unfavorable)
    with col33:
        st.button(label="Approval",
                key="approval_button",
                help="UNDER CONSTRUCTION.  Displays approval data on the chart.  Only applies to the current president.",
                use_container_width=True,
                type="primary" if st.session_state.favor_type=="Approval" else "secondary",
                on_click=set_favtype_approval)
    with col55:
        st.selectbox("Timeline",
                     options=timeline_options,
                     key="favor_time",
                     on_change=set_poll_timeline)
        
    st.plotly_chart(st.session_state.favorability_chart,
                    use_container_width=True,
                    key="favor_chart")

# Add the map
st.write("")
st.subheader("United States Election Polling Map",
         help="Data supplied by FiveThirtyEight.com aggregate presidential polls.")

if st.session_state.figure:
    col1, col2, col3 = st.columns([1,1,3])

    with col1:
        st.button(label="National",
                key="national_button",
                help="Displays national data on the map.",
                use_container_width=True,
                type="primary" if st.session_state.map_type=="National" else "secondary",
                on_click=set_maptype_national)
    with col2:
        st.button(label="By State",
                key="bystate_button",
                help="Displays the statewide data on the map.",
                use_container_width=True,
                type="primary" if st.session_state.map_type=="By State" else "secondary",
                on_click=set_maptype_state)
        
    st.plotly_chart(st.session_state.figure,
                    key="map_figure")
    
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
st.sidebar.select_slider("Color Map By...",
                         options=["Lead Margin", "Widest Margin", "Vote %"],
                         value=st.session_state.color_state,
                         key="color_selector",
                         help="The lead margin is the difference between the leader and second place.  The widest margin is the difference between the leader and last place.  If there are only two candidates, the margins will be the same.  (When set to widest margin, the value in the hover text will change)",
                         on_change=update_color_slider)

st.write("")
co1, co2, c03 = st.columns([2,1,2])
with co1:
    st.subheader(f"Included Polls",
                    help="This poll list is for the state map and associated information.  Favorability and approval data is from a different dataset.")

if st.session_state.poll_text and st.session_state.poll_header:
    with co2:
        st.selectbox("Number of Polls Shown",
                        options=quantity_options,
                        on_change=set_poll_quantity,
                        key="quantity_selector")
    c_list = st.columns([2,2,5,2,2,2])
    for i, c in enumerate(c_list):
        with c:
            st.subheader(st.session_state.poll_header[i])
    
    for poll in st.session_state.poll_text:
        for j, c in enumerate(c_list):
            with c:
                st.write(poll[j])

if st.session_state.run_initial:
    update_widget_display()
    update_button_press()
    st.session_state.run_initial = False
    st.rerun()
