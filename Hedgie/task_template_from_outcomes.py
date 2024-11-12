pip install pandas
import pandas as pd

# Replace 'your_data.csv' with the path to your CSV file
df = pd.read_csv('skills_book_pts.csv')

def select_ptids(df, outcome_codes, max_ptids=20):
    # Filter PTs that match the outcome codes
    df_filtered = df[df['OUTCOMES'].isin(outcome_codes)].copy()
    
    # Identify outcome codes without matching PTs
    unmatched_outcomes = set(outcome_codes) - set(df_filtered['OUTCOMES'].unique())
    
    if df_filtered.empty:
        return [], unmatched_outcomes, 0.0
    
    # Criteria 2: Prefer 'Gold', 'Gold - Auto', or 'Unassigned' quality
    preferred_qualities = ['Gold', 'Gold - Auto', 'Unassigned']
    df_filtered['quality_preference'] = df_filtered['PROBLEM_TEMPLATE_QUALITY'].apply(
        lambda x: 0 if x in preferred_qualities else 1
    )
    
    # Criteria 3: Prefer PTs with 2 or fewer max subproblems
    df_filtered['subproblem_preference'] = df_filtered['MAX_SUBPROBLEM_NUMBER'].apply(
        lambda x: 0 if x <= 2 else 1
    )
    
    # Combine preferences into a total rank
    df_filtered['total_preference'] = df_filtered['quality_preference'] + df_filtered['subproblem_preference']
    
    # Criteria 1: Approximately equal distribution among outcome codes
    ptids = []
    per_outcome_quota = max_ptids // len(outcome_codes)
    
    for outcome in outcome_codes:
        df_outcome = df_filtered[df_filtered['OUTCOMES'] == outcome]
        if df_outcome.empty:
            continue
        
        # Criteria 4: Vary subproblem types
        df_outcome = df_outcome.drop_duplicates(subset=['SUBPROBLEM_TYPE'])
        
        # Sort by total preference
        df_outcome = df_outcome.sort_values('total_preference')
        
        # Select up to per_outcome_quota PTIDs
        selected_ptids = df_outcome['PROBLEM_TEMPLATE_ID'].unique()[:per_outcome_quota]
        ptids.extend(selected_ptids)
    
    # Fill up remaining slots if less than max_ptids
    if len(ptids) < max_ptids:
        remaining_ptids = df_filtered[~df_filtered['PROBLEM_TEMPLATE_ID'].isin(ptids)]
        remaining_ptids = remaining_ptids.sort_values('total_preference')
        extra_ptids = remaining_ptids['PROBLEM_TEMPLATE_ID'].unique()[:(max_ptids - len(ptids))]
        ptids.extend(extra_ptids)
    
    # Remove duplicates and limit to max_ptids
    ptids = list(pd.unique(ptids))[:max_ptids]
    
    # Prepare DataFrame for arranging difficulty
    df_ptids = df_filtered[df_filtered['PROBLEM_TEMPLATE_ID'].isin(ptids)].drop_duplicates('PROBLEM_TEMPLATE_ID')
    
    # Criteria 5: Arrange the list so that the most difficult questions are in the middle
    df_ptids = df_ptids.sort_values('AVERAGE_COMPLETION_TIME')
    n = len(df_ptids)
    arranged_ptids = []
    for i in range(n):
        if i % 2 == 0:
            arranged_ptids.append(df_ptids.iloc[i]['PROBLEM_TEMPLATE_ID'])
        else:
            arranged_ptids.insert(n - i, df_ptids.iloc[i]['PROBLEM_TEMPLATE_ID'])
    
    # Compute the sum of average completion times
    total_completion_time = df_ptids['AVERAGE_COMPLETION_TIME'].sum()
    
    return arranged_ptids, unmatched_outcomes, total_completion_time

# Example usage:
# Assume 'df' is your DataFrame loaded from your data source
# outcome_codes = ['6.NS.1a', '6.NS.2b']  # Replace with your actual outcome codes
# selected_ptids, unmatched_outcomes, total_time = select_ptids(df, outcome_codes)
# print("Selected PTIDs:", ', '.join(map(str, selected_ptids)))
# print("Unmatched Outcome Codes:", unmatched_outcomes)
# print("Total Average Completion Time:", total_time)
