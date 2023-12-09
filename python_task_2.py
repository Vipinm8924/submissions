import pandas as pd
import networkx as nx

def calculate_distance_matrix(df):
    # Create a graph using NetworkX
    G = nx.Graph()

    # Add edges and their weights based on the dataset
    for index, row in df.iterrows():
        G.add_edge(row['from_id'], row['to_id'], weight=row['distance'])

    # Calculate shortest path lengths for all pairs of nodes
    distance_matrix = nx.floyd_warshall_numpy(G)

    # Replace infinite distances with 0 and round distances to 1 decimal place
    distance_matrix[distance_matrix == float('inf')] = 0
    distance_matrix = pd.DataFrame(distance_matrix, index=G.nodes(), columns=G.nodes())
    distance_matrix = distance_matrix.round(1)

    return distance_matrix

# Assuming 'dataset-3.csv' is the name of your CSV file
data = pd.read_csv('dataset-3.csv')

# Apply the function to calculate the distance matrix
result_distance_matrix = calculate_distance_matrix(data)

# Display the resulting distance matrix
print(result_distance_matrix)



import pandas as pd

def unroll_distance_matrix(distance_df):
    # Create an empty list to store unrolled data
    unrolled_data = []

    # Iterate through the DataFrame to create combinations and distances
    for id_start in distance_df.index:
        for id_end in distance_df.columns:
            if id_start != id_end:
                distance = distance_df.at[id_start, id_end]
                unrolled_data.append({'id_start': id_start, 'id_end': id_end, 'distance': distance})

    # Create a DataFrame from the unrolled data
    unrolled_df = pd.DataFrame(unrolled_data)

    return unrolled_df

# Assuming 'distance_df' is the DataFrame created in Question 1
# Replace it with your actual DataFrame containing distances
distance_df = ...  # Replace this line with your DataFrame

# Apply the function to unroll the distance matrix
unrolled_distance_df = unroll_distance_matrix(distance_df)

# Display the resulting unrolled DataFrame
print(unrolled_distance_df)



import pandas as pd

def find_ids_within_ten_percentage_threshold(df, reference_value):
    # Calculate the average distance for the reference value
    reference_avg_distance = df[df['id_start'] == reference_value]['distance'].mean()

    # Calculate the threshold range within 10% of the reference value's average
    threshold_min = reference_avg_distance - (reference_avg_distance * 0.1)
    threshold_max = reference_avg_distance + (reference_avg_distance * 0.1)

    # Filter and get the sorted list of values within the threshold range
    within_threshold_ids = (
        df.groupby('id_start')['distance'].mean()
        .loc[lambda x: (x >= threshold_min) & (x <= threshold_max)]
        .index.tolist()
    )

    # Sort the list of values
    within_threshold_ids.sort()

    return within_threshold_ids

# Assuming 'distance_df' is the DataFrame created in Question 2
# Replace it with your actual DataFrame containing distances
distance_df = ...  # Replace this line with your DataFrame

# Assuming 'reference_value' is the reference value as an integer
reference_value = 1001400  # Replace this with your reference value

# Apply the function to find IDs within the ten percentage threshold of the reference value
ids_within_threshold = find_ids_within_ten_percentage_threshold(distance_df, reference_value)

# Display the sorted list of IDs within the threshold range
print(ids_within_threshold)




import pandas as pd

def calculate_toll_rate(df):
    # Calculate toll rates for each vehicle type using their rate coefficients
    df['moto'] = df['distance'] * 0.8
    df['car'] = df['distance'] * 1.2
    df['rv'] = df['distance'] * 1.5
    df['bus'] = df['distance'] * 2.2
    df['truck'] = df['distance'] * 3.6

    # Round the calculated toll rates to 2 decimal places
    df = df.round({'moto': 2, 'car': 2, 'rv': 2, 'bus': 2, 'truck': 2})

    return df

# Assuming 'distance_df' is the DataFrame created in Question 2
# Replace it with your actual DataFrame containing distances
distance_df = ...  # Replace this line with your DataFrame

# Apply the function to calculate toll rates based on vehicle types
distance_with_toll_rates = calculate_toll_rate(distance_df)

# Display the DataFrame with added toll rate columns
print(distance_with_toll_rates)




import pandas as pd
from datetime import datetime, timedelta, time

def calculate_time_based_toll_rates(df):
    # Function to calculate the day of the week
    def get_day_of_week(day):
        return (datetime.strptime(day, '%Y-%m-%d') + timedelta(days=1)).strftime('%A')

    # Function to calculate the time intervals and corresponding discount factors
    def get_time_intervals(day, start_time, end_time):
        intervals = []
        weekday_intervals = [(time(0, 0, 0), time(10, 0, 0), 0.8),
                             (time(10, 0, 0), time(18, 0, 0), 1.2),
                             (time(18, 0, 0), time(23, 59, 59), 0.8)]
        weekend_factor = 0.7

        for interval in weekday_intervals:
            start, end, factor = interval
            intervals.append((day, start, day, end, factor))

        if get_day_of_week(day) in ['Saturday', 'Sunday']:
            intervals = [(day, time(0, 0, 0), day, time(23, 59, 59), weekend_factor)]

        return intervals

    # Calculate time-based toll rates for each day and time interval
    toll_rates = []
    for index, row in df.iterrows():
        intervals = get_time_intervals(row['startDay'], row['startTime'], row['endTime'])
        for interval in intervals:
            toll_row = row.copy()
            toll_row['startDay'], toll_row['start_time'], toll_row['endDay'], toll_row['end_time'], _ = interval
            toll_rates.append(toll_row)

    # Convert the calculated toll rates into a DataFrame
    toll_rates_df = pd.DataFrame(toll_rates)
    toll_rates_df = toll_rates_df.drop(columns=['startTime', 'endTime'])

    return toll_rates_df

# Assuming 'time_intervals_df' is the DataFrame created in Question 3
# Replace it with your actual DataFrame containing time intervals
time_intervals_df = ...  # Replace this line with your DataFrame

# Apply the function to calculate time-based toll rates
result_df = calculate_time_based_toll_rates(time_intervals_df)

# Display the resulting DataFrame with time-based toll rates
print(result_df)
