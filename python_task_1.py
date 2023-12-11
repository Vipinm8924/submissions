import pandas as pd

# Function to generate the desired matrix
def generate_car_matrix(df):
    # Pivot the DataFrame to create the desired matrix
    result_df = df.pivot(index='id_1', columns='id_2', values='car').fillna(0)
    
    # Set diagonal values to 0
    for i in range(min(result_df.shape)):
        result_df.iloc[i, i] = 0.0
    
    return result_df

# Read the dataset-1.csv file into a DataFrame
data = pd.read_csv('dataset-1.csv')

# Generate the matrix using the function
result_matrix = generate_car_matrix(data)

# Display the resulting DataFrame
print(result_matrix)





def get_type_count(df):
    # Add a new categorical column 'car_type'
    df['car_type'] = pd.cut(df['car'], bins=[-float('inf'), 15, 25, float('inf')],
                            labels=['low', 'medium', 'high'], right=False)
    
    # Calculate the count of occurrences for each 'car_type' category
    count_by_type = df['car_type'].value_counts().to_dict()
    
    # Sort the dictionary alphabetically based on keys
    sorted_count = {key: count_by_type[key] for key in sorted(count_by_type)}
    
    return sorted_count

# Assuming 'dataset-1.csv' is the name of your CSV file
data = pd.read_csv('dataset-1.csv')

# Get the count of car_type occurrences using the function
type_count = get_type_count(data)

# Display the result as a dictionary sorted alphabetically by keys
print(type_count)






def get_bus_indexes(df):
    # Calculate the mean value of the 'bus' column
    bus_mean = df['bus'].mean()
    
    # Identify indices where 'bus' values are greater than twice the mean
    bus_indexes = df[df['bus'] > 2 * bus_mean].index.tolist()
    
    # Sort the indices in ascending order
    bus_indexes.sort()
    
    return bus_indexes

# Assuming 'dataset-1.csv' is the name of your CSV file
data = pd.read_csv('dataset-1.csv')

# Get the indices where 'bus' values are greater than twice the mean
bus_indices = get_bus_indexes(data)

# Display the sorted list of indices
print(bus_indices)






def filter_routes(df):
    # Group by 'route' column and calculate the average of 'truck' column
    route_avg_truck = df.groupby('route')['truck'].mean()
    
    # Filter routes where the average of 'truck' column is greater than 7
    filtered_routes = route_avg_truck[route_avg_truck > 7].index.tolist()
    
    # Sort the list of routes in ascending order
    filtered_routes.sort()
    
    return filtered_routes

# Assuming 'dataset-1.csv' is the name of your CSV file
data = pd.read_csv('dataset-1.csv')

# Get the sorted list of routes where the average of 'truck' values is greater than 7
filtered_route_list = filter_routes(data)

# Display the sorted list of routes
print(filtered_route_list)




def multiply_matrix(input_df):
    # Create a copy of the input DataFrame to avoid modifying the original
    modified_df = input_df.copy()

    # Apply the multiplication logic based on conditions provided
    for idx in modified_df.index:
        for col in modified_df.columns:
            value = modified_df.at[idx, col]
            if value > 20:
                modified_df.at[idx, col] = round(value * 0.75, 1)
            else:
                modified_df.at[idx, col] = round(value * 1.25, 1)

    return modified_df

# Sample result DataFrame from the question
sample_result_df = pd.DataFrame({
    'id_2': [0.0, 5.5, 6.9, 15.4, 23.5, 26.8],
    '802': [5.5, 0.0, 6.9, 10.3, 18.4, 21.7],
    '803': [12.0, 6.9, 0.0, 3.9, 12.0, 15.3],
    '804': [15.4, 10.3, 3.9, 0.0, 8.8, 12.2],
    '805': [23.5, 18.4, 12.0, 8.8, 0.0, 4.0],
    '806': [26.8, 21.7, 15.3, 12.2, 4.0, 0.0]
}, index=['801', '802', '803', '804', '805', '806'])

# Apply the multiplication logic to the sample result DataFrame
modified_sample_result_df = multiply_matrix(sample_result_df)

# Display the modified DataFrame
print(modified_sample_result_df)







def verify_time_completeness(df):
    # Combine 'startDay' and 'startTime' to create a single start timestamp
    df['start_timestamp'] = pd.to_datetime(df['startDay'] + ' ' + df['startTime'])

    # Combine 'endDay' and 'endTime' to create a single end timestamp
    df['end_timestamp'] = pd.to_datetime(df['endDay'] + ' ' + df['endTime'])

    # Calculate the duration of each record
    df['duration'] = df['end_timestamp'] - df['start_timestamp']

    # Group by 'id' and 'id_2'
    grouped = df.groupby(['id', 'id_2'])

    # Check if each group covers a full 24-hour period for all 7 days of the week
    completeness_check = grouped.apply(
        lambda group: (
            group['duration'].min() >= pd.Timedelta(days=1)  # Check for 24-hour coverage
            and group['start_timestamp'].dt.dayofweek.nunique() == 7  # Check for all 7 days of the week
        )
    )

    return completeness_check

# Load dataset-2.csv into a DataFrame
data = pd.read_csv('dataset-2.csv')

# Apply the function to verify time completeness
verification_result = verify_time_completeness(data)

# Display the boolean series indicating incorrect timestamps for each (id, id_2) pair
print(verification_result)
