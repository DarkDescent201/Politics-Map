#### Import Modules ####
import pandas as pd
import numpy as np
import pyinputplus as pyip
from datetime import datetime, timedelta
from collections import defaultdict



#### Global Objects ####
us_states_lower = [
    "alabama", "alaska", "arizona", "arkansas", "california",
    "colorado", "connecticut", "delaware", "florida", "georgia",
    "hawaii", "idaho", "illinois", "indiana", "iowa",
    "kansas", "kentucky", "louisiana", "maine", "maryland",
    "massachusetts", "michigan", "minnesota", "mississippi", "missouri",
    "montana", "nebraska", "nevada", "new-hampshire", "new-jersey",
    "new-mexico", "new-york", "north-carolina", "north-dakota", "ohio",
    "oklahoma", "oregon", "pennsylvania", "rhode-island", "south-carolina",
    "south-dakota", "tennessee", "texas", "utah", "vermont",
    "virginia", "washington", "west-virginia", "wisconsin", "wyoming"
]
us_states_cap = [x.replace('-', ' ').title() for x in us_states_lower]
percent_encoding = {
    ' ': '%20',
    '!': '%21',
    '"': '%22',
    '#': '%23',
    '$': '%24',
    '%': '%25',
    '&': '%26',
    "'": '%27',
    '(': '%28',
    ')': '%29',
    '*': '%2A',
    '+': '%2B',
    ',': '%2C',
    '/': '%2F',
    ':': '%3A',
    ';': '%3B',
    '<': '%3C',
    '=': '%3D',
    '>': '%3E',
    '?': '%3F',
    '@': '%40',
    '[': '%5B',
    '\\': '%5C',
    ']': '%5D',
    '^': '%5E',
    '_': '%5F',
    '`': '%60',
    '{': '%7B',
    '|': '%7C',
    '}': '%7D',
    '~': '%7E',
    '\x7F': '%7F',  # Delete (ASCII 127)
    # Latin-1 supplement characters
    '\x80': '%80',
    '\x81': '%81',
    '\x82': '%82',
    '\x83': '%83',
    '\x84': '%84',
    '\x85': '%85',
    '\x86': '%86',
    '\x87': '%87',
    '\x88': '%88',
    '\x89': '%89',
    '\x8A': '%8A',
    '\x8B': '%8B',
    '\x8C': '%8C',
    '\x8D': '%8D',
    '\x8E': '%8E',
    '\x8F': '%8F',
    '\x90': '%90',
    '\x91': '%91',
    '\x92': '%92',
    '\x93': '%93',
    '\x94': '%94',
    '\x95': '%95',
    '\x96': '%96',
    '\x97': '%97',
    '\x98': '%98',
    '\x99': '%99',
    '\x9A': '%9A',
    '\x9B': '%9B',
    '\x9C': '%9C',
    '\x9D': '%9D',
    '\x9E': '%9E',
    '\x9F': '%9F',
}
electoral_votes = {
    'alabama': 9,
    'alaska': 3,
    'arizona': 11,
    'arkansas': 6,
    'california': 54,
    'colorado': 10,
    'connecticut': 7,
    'delaware': 3,
    'district of columbia': 3,
    'florida': 30,
    'georgia': 16,
    'hawaii': 4,
    'idaho': 4,
    'illinois': 19,
    'indiana': 11,
    'iowa': 6,
    'kansas': 6,
    'kentucky': 8,
    'louisiana': 8,
    'maine': 2,
    'maryland': 10,
    'massachusetts': 11,
    'michigan': 15,
    'minnesota': 10,
    'mississippi': 6,
    'missouri': 10,
    'montana': 4,
    'nebraska': 4,
    'nevada': 6,
    'new hampshire': 4,
    'new jersey': 14,
    'new mexico': 5,
    'new york': 28,
    'north carolina': 16,
    'north dakota': 3,
    'ohio': 17,
    'oklahoma': 7,
    'oregon': 8,
    'pennsylvania': 19,
    'rhode island': 4,
    'south carolina': 9,
    'south dakota': 3,
    'tennessee': 11,
    'texas': 40,
    'utah': 6,
    'vermont': 3,
    'virginia': 13,
    'washington': 12,
    'west virginia': 4,
    'wisconsin': 10,
    'wyoming': 3
}
columns_to_keep = ['poll_id', 'pollster_id', 'pollster', 'numeric_grade', 'pollscore',
                   'methodology', 'state', 'start_date', 'end_date', 'question_id',
                   'sample_size', 'population', 'party', 'candidate_id', 'candidate_name',
                   'pct']
string_columns = ['pollster', 'methodology', 'state', 'population', 'party', 'candidate_name']
number_columns = ['poll_id', 'pollster_id', 'pollscore', 'question_id', 'candidate_id', 'pct']
URL = "https://projects.fivethirtyeight.com/polls/data/president_polls.csv"



#### Functions ####
def acquire_latest_data() -> pd.DataFrame:
    full_df = pd.read_csv(URL)
    full_df = full_df[columns_to_keep]
    full_df[string_columns] = full_df[string_columns].fillna(' ')
    full_df[number_columns] = full_df[number_columns].fillna(0)
    full_df['numeric_grade'] = full_df['numeric_grade'].fillna(0.1)
    full_df['sample_size'] = full_df['sample_size'].fillna(100)

    return full_df

def parse_data_by_date(data:pd.DataFrame, days_ago:int=0, search_current_year:bool=False, 
                       search_all:bool=False) -> pd.DataFrame:
    # Input parameter verification and variable setting
    try:
        full_df = data
        days_back = int(days_ago) if days_ago > 0 else 0
        year_search_true = bool(search_current_year)
        search_all_true = bool(search_all)
    except Exception as e:
        print('\n', "There has been an error parsing data by date.", "The error is likely due to missing or incorrect data.", f"Error Report:  {e}", '\n', sep='\n',)

    # Setting the target date based on parameters
    if search_all_true:
        target_date = "1/1/01"
        target_date = datetime.strptime(target_date, r"%m/%d/%y")
    elif year_search_true:
        target_date = "1/1/24"
        target_date = datetime.strptime(target_date, r"%m/%d/%y")
    elif days_back == 0:
        target_date = full_df["end_date"][0]
        target_date = datetime.strptime(target_date, r"%m/%d/%y")
    else:
        now = datetime.now()
        target_date = now - timedelta(days=days_back)

    # Getting the data subset
    full_df.loc[:, 'end_date'] = pd.to_datetime(full_df["end_date"], format=r"%m/%d/%y", errors='coerce').dt.date
    dated_df = full_df.loc[full_df["end_date"] >= target_date.date()]
    
    return dated_df

def get_latest_state_polls(data:pd.DataFrame) -> pd.DataFrame:
    # Set and get preliminary data
    full_df = data
    state_list = sorted(set(full_df['state']))

    # Make DFs for each state
    DF_list = []
    for state in state_list:
        state_df = full_df.loc[full_df['state'] == state]
        state_df.loc[:, "end_date"] = pd.to_datetime(state_df["end_date"], format=r"%m/%d/%y", errors='coerce').dt.date
        max_date = state_df["end_date"].max()
        state_df = state_df.loc[state_df["end_date"] == max_date]
        DF_list.append(state_df)

    state_date_df = pd.concat(DF_list, axis=0)

    return state_date_df

def get_latest_candidate_polls(data:pd.DataFrame, candidate_list:list=['Donald Trump', 'Joe Biden']) -> pd.DataFrame:
    # Parse by candidate options
    candidate_df = parse_by_candidates(data)

    # Get most recent polls for each state
    candidate_state_df = get_latest_state_polls(candidate_df)

    return candidate_state_df

def parse_data_by_pollster(data:pd.DataFrame, pollsters:list=[""]) -> pd.DataFrame:
    # Input parameter verification and variable setting
    try:
        full_df = data
        pollsters = list(pollsters)
    except Exception as e:
        print('\n', "There has been an error parsing data by pollster.", "The error is likely due to missing or incorrect data.", f"Error Report:  {e}", '\n', sep='\n',)

    # Return the full list in case of a blank entry as a default
    if pollsters in [[""], []]:
        return full_df
    else:
        pass

    # Getting the data subset
    pollster_df = full_df.loc[full_df["pollster"].isin(pollsters)]

    return pollster_df

def parse_data_by_rating(data:pd.DataFrame, min:float=0, max:float=3.0) -> pd.DataFrame:
    # Input parameter verification and variable setting
    try:
        full_df = data
        minimum = float(min)
        maximum = float(max)
    except Exception as e:
        print('\n', "There has been an error parsing data by rating.", "The error is likely due to missing or incorrect data.", f"Error Report:  {e}", '\n', sep='\n',)

    # Getting the data subset
    ratings_df = full_df.loc[(minimum <= full_df["numeric_grade"]) & (full_df["numeric_grade"] <= maximum)]

    return ratings_df

def parse_by_population(data:pd.DataFrame, pop_type:str='everyone') -> pd.DataFrame:
    # Input parameter verification and variable setting
    try:
        full_df = data
        population_type = pop_type.title() if pop_type.lower() in ["everyone", "likely voters", "registered voters", "all respondents"] else "Everyone"
    except Exception as e:
        print('\n', "There has been an error parsing data by population type.", "The error is likely due to missing or incorrect data.", f"Error Report:  {e}", '\n', sep='\n',)

    # If 'everyone' send back whole DF and end function
    if population_type == "Everyone":
        return full_df
    else:
        pass

    # Set the sortation key conditionally
    if population_type == "Likely Voters":
        key = ["lv"]
    elif population_type == "Registered Voters":
        key = ['rv', 'v']
    elif population_type == "All Respondents":
        key = ['a']
    else:
        return None
    
    # Sort DataFrame by population key
    population_df = full_df.loc[full_df["population"].isin(key)]

    return population_df

def parse_by_candidates(data:pd.DataFrame, candidate_selection:list=['Donald Trump', 'Joe Biden']) -> pd.DataFrame:
    # Validate inputs
    try:
        data = pd.DataFrame(data)
        chosen_candidate_list = list(candidate_selection)
    except Exception as e:
        print('\n', "There has been an error parsing data by candidates.", "The error is likely due to missing or incorrect data.", f"Error Report:  {e}", '\n', sep='\n',)
    
    # Sort into polls and questions
    polls = sort_into_polls(data)
    data = sort_polls_into_questions(polls)

    # Parse questions by chosen candidate list
    parsed_question_dict = {}
    for question in data.keys():
        question_data = data[question]
        candidates = sorted(question_data['candidate_name'])
        if candidates == chosen_candidate_list:
            parsed_question_dict[question] = question_data
        else:
            pass

    # Concatenate to a DataFrame
    DF_list = []
    for item in parsed_question_dict.keys():
        target = parsed_question_dict[item]
        DF_list.append(target)

    candidate_df = pd.concat(DF_list, axis=0)

    return candidate_df

def sort_into_polls(data:pd.DataFrame) -> dict: # Do any non-candidate parsing first
    # Create a grouped DataFrame
    full_df = data
    grouped_dfs = full_df.groupby("poll_id")

    # Separate the group into individual DFs stored in a dictionary
    df_data = {poll_id: poll_data for poll_id, poll_data in grouped_dfs}

    return df_data

def sort_polls_into_questions(data:dict={}) -> dict: # Must be sorted into polls first
    # Separate polls by question
    poll_question_dict = {}
    for key in data.keys():
        poll = data[key]
        question_list = sorted(set(poll['question_id']))
        for question in question_list:
            question_df = poll.loc[poll["question_id"] == question]
            poll_question_dict[question] = question_df

    return poll_question_dict

def data_processing(data:pd.DataFrame, candidate_list:list, weight_type:str="unweighted average") -> pd.DataFrame:
    # Defining terms
    weighting_methods = ["unweighted average", "pollster grade", "sample size"]
    if weight_type in weighting_methods:
        pass
    else:
        weight_type = "unweighted average"

    # Get individual questions
    polls = sort_into_polls(data)
    poll_question_dict = sort_polls_into_questions(polls)

    # Extract data from each question
    denominator = 0
    score_list = []
    state_list = []
    for question in poll_question_dict.keys():
        question_data = poll_question_dict[question]
        numeric_grade = question_data['numeric_grade'].iloc[0]
        sample_size = question_data['sample_size'].iloc[0]
        state_polled = question_data['state'].iloc[0]

        if state_polled == " ":
            state_polled = "National"
        else:
            pass
        state_list.append(state_polled)

        if weight_type == "pollster grade":
            denominator = numeric_grade
            denominator = round(denominator, 1)
        elif weight_type == "sample size":
            denominator = sample_size
            denominator = int(denominator)
        else:
            denominator = 1

        candidate_scores = {state_polled: {}}
        for candidate in candidate_list:
            current_score = question_data.loc[question_data["candidate_name"]==candidate, "pct"].values[0]
            if weight_type == "pollster grade":
                current_score = current_score * numeric_grade
                current_score = round(current_score, 1)
            elif weight_type == "sample size":
                current_score = current_score * sample_size
                current_score = int(current_score)
            else:
                pass
            
            candidate_scores[state_polled][candidate] = current_score
            candidate_scores[state_polled]["denominator"] = denominator
            
        score_list.append(candidate_scores)

    # Get the sums from the datasets
    final_scores = defaultdict(lambda: {key: 0 for key in candidate_list + ['denominator']})

    for item in score_list:
        for outer_key, inner_dict in item.items():
            for thing in candidate_list + ['denominator']:
                final_scores[outer_key][thing] += inner_dict.get(thing, 0)
                final_scores[outer_key][thing] = round(final_scores[outer_key][thing], 1)

    returned_data = {}
    for state in final_scores.keys():
        returned_data[state] = {}

        active_dict = final_scores[state]
        divisor = active_dict['denominator']
        for target in active_dict.keys():
            if target == 'denominator':
                pass
            else:
                current_num = active_dict[target]
                new_num = current_num / divisor
                new_num = round(new_num, 1)
                returned_data[state][target] = new_num
    
    returned_data = {x: returned_data[x] for x in sorted(returned_data)}
    returned_data = pd.DataFrame(returned_data)

    return returned_data

def calculate_electoral_votes(data:pd.DataFrame, candidate_list:list) -> tuple:
    # Input validation
    try:
        total_state_list = list(us_states_cap)
        scores_df = pd.DataFrame(data)
        candidate_list = list(candidate_list)
        polled_state_list = list(scores_df.columns)
        vote_count = dict(electoral_votes)
    except Exception as e:
        print('\n', "There has been an error calculating the electoral college score.", "The error is likely due to missing or incorrect data.", f"Error Report:  {e}", '\n', sep='\n',)
    
    # Access state-by-state data
    electoral_count = {}
    for state in total_state_list + ['National']:
        electoral_count[state] = {candidate:0 for candidate in candidate_list}

    for state in polled_state_list:
        winner = scores_df[state].idxmax()

        if state in ['Maine CD-1', 'Maine CD-2']:
            state = 'Maine'
            electoral_value = 1
        elif state in ['Nebraska CD-1', 'Nebraska CD-2', 'Nebraska CD-3']:
            state = 'Nebraska'
            electoral_value = 1
        elif state == 'National':
            electoral_value = 0
        else:
            electoral_value = vote_count[state.lower()]

        electoral_count[state][winner] += electoral_value

    electoral_count = pd.DataFrame(electoral_count)
    electoral_count['Total'] = electoral_count.sum(axis=1)

    return electoral_count, polled_state_list

def get_political_parties(data:pd.DataFrame) -> dict:
    all_candidates = sorted(set(data['candidate_name']))
    political_party_dict = {}

    for candidate in all_candidates:
        party = data.loc[data['candidate_name'] == candidate, 'party'].values[0]
        political_party_dict[candidate] = party

    return political_party_dict

def extract_candidate_groups(data:pd.DataFrame) -> list:
    # Validate inputs
    try:
        full_df = pd.DataFrame(data)
    except Exception as e:
        print('\n', "There has been an error extracting the candidate groups.", "The error is likely due to missing or incorrect data.", f"Error Report:  {e}", '\n', sep='\n',)

    # Sort into polls and questions
    polls = sort_into_polls(full_df)
    questions = sort_polls_into_questions(polls)

    # Get candidate lists from data
    candidate_list = []
    for question in questions.keys():
        question_data = questions[question]
        candidates = sorted(question_data['candidate_name'])
        candidate_list.append(candidates)

    unique_candidate_list = [list(x) for x in set(tuple(x) for x in candidate_list)]
    unique_candidate_list.sort()
    unique_candidate_list.sort(key=len)
    if ["Donald Trump", "Joe Biden"] in unique_candidate_list:
        unique_candidate_list.remove(["Donald Trump", "Joe Biden"])
        unique_candidate_list = [["Donald Trump", "Joe Biden"]] + unique_candidate_list

    return unique_candidate_list

def extract_population_types(data:pd.DataFrame) -> list:
    # Validate inputs
    try:
        full_df = pd.DataFrame(data)
    except Exception as e:
        print('\n', "There has been an error extracting the population types.", "The error is likely due to missing or incorrect data.", f"Error Report:  {e}", '\n', sep='\n',)

    # Extract list of population types
    population_list = sorted(set(full_df['population']))

    translated_population_list = []
    for item in population_list:
        if item.lower() == "a":
            translated_population_list.append("All Respondents")
        elif item.lower() == "lv":
            translated_population_list.append("Likely Voters")
        elif item.lower() in ["rv", "v"]:
            translated_population_list.append("Registered Voters")
        else:
            translated_population_list.append("All Respondents")

    sorted_list = sorted(set(translated_population_list))
    return_list = ["Everyone"] + sorted_list
    
    return return_list



#### Main Actions ####
# Proper sequence of actions as follows:
    # 1) acquire the latest data, functions don't auto-pull
    # 2a) perform parsing by date, pollster, rating, and/or population ... OR
    # 2b) directly pull Latest State Polls or Latest Candidate Polls
    # 3a) sort into polls, sort into questions, parse by candidates IN THAT ORDER... OR
    # 3b) if using Latest Candidate Polls, don't need to parse by candidates again
    # 4) Process the data; candidate list and DF will be provided from candidate parse
if __name__ == '__main__':
    df1 = acquire_latest_data()
    df2 = parse_data_by_date(df1, 90)
    df3 = get_latest_state_polls(df1)
    df4 = get_latest_candidate_polls(df1)
    print('\n', df1, df2, df3, df4, '\n', sep='\n\n')
    df5 = extract_candidate_groups(df2)
    print('\n', df5, '\n')