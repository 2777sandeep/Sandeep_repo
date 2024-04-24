import csv
from collections import defaultdict
from datetime import datetime

# Function to parse datetime string to datetime object
def parse_datetime(datetime_str):
    return datetime.strptime(datetime_str, '%m/%d/%Y %H:%M')

# Function to calculate trip duration in minutes
def calculate_trip_duration(pickup_time, dropoff_time):
    return (dropoff_time - pickup_time).total_seconds() / 60

# Function to process data and calculate various metrics
def process_data(data_file):
    total_trip_distance = 0
    total_amount_paid = 0
    amounts_by_airports = defaultdict(float)
    shortest_trip = None
    longest_trip = None

    with open(data_file, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            pickup_time = parse_datetime(row['tpep_pickup_datetime'])
            dropoff_time = parse_datetime(row['tpep_dropoff_datetime'])
            trip_distance = float(row['trip_distance'])
            rate_code_id = int(row['RatecodeID'])
            tip_amount = float(row['tip_amount'])
            tolls_amount = float(row['tolls_amount'])
            total_amount = float(row['total_amount'])
            airport_fee = float(row['Airport_fee'])

            # Calculate trip duration
            trip_duration = calculate_trip_duration(pickup_time, dropoff_time)

            # Update shortest trip
            if shortest_trip is None or trip_duration < shortest_trip['duration']:
                shortest_trip = {'pickup_time': pickup_time, 'dropoff_time': dropoff_time, 'duration': trip_duration, 'trip_distance': trip_distance}

            # Update longest trip
            if longest_trip is None or trip_duration > longest_trip['duration']:
                longest_trip = {'pickup_time': pickup_time, 'dropoff_time': dropoff_time, 'duration': trip_duration, 'trip_distance': trip_distance}

            # Update total trip distance and total amount paid
            total_trip_distance += trip_distance
            total_amount_paid += (tip_amount + tolls_amount + total_amount + airport_fee)

            # Update amounts paid by airports
            amounts_by_airports[rate_code_id] += (tip_amount + tolls_amount + total_amount + airport_fee)

    # Calculate average price per kilometer
    if total_trip_distance > 0:
        average_price_per_km = total_amount_paid / total_trip_distance
    else:
        average_price_per_km = 0

    return shortest_trip, longest_trip, amounts_by_airports, average_price_per_km

def main():
    data_file = 'C:\PY_SS\yellow_tripdata_2024-02.csv'
    output_file = 'output.csv'

    # Process data
    shortest_trip, longest_trip, amounts_by_airports, average_price_per_km = process_data(data_file)

    # Write results to CSV
    with open(output_file, 'w', newline='') as csvfile:
        fieldnames = ['Metric', 'Value']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        writer.writerow({'Metric': 'Shortest Trip Pickup Time', 'Value': shortest_trip['pickup_time']})
        writer.writerow({'Metric': 'Shortest Trip Dropoff Time', 'Value': shortest_trip['dropoff_time']})
        writer.writerow({'Metric': 'Shortest Trip Duration (minutes)', 'Value': shortest_trip['duration']})
        writer.writerow({'Metric': 'Shortest Trip Distance (miles)', 'Value': shortest_trip['trip_distance']})
        writer.writerow({'Metric': 'Longest Trip Pickup Time', 'Value': longest_trip['pickup_time']})
        writer.writerow({'Metric': 'Longest Trip Dropoff Time', 'Value': longest_trip['dropoff_time']})
        writer.writerow({'Metric': 'Longest Trip Duration (minutes)', 'Value': longest_trip['duration']})
        writer.writerow({'Metric': 'Longest Trip Distance (miles)', 'Value': longest_trip['trip_distance']})

        for rate_code_id, amount in amounts_by_airports.items():
            writer.writerow({'Metric': f'Total Amount Paid for Rate Code ID {rate_code_id}', 'Value': amount})

        writer.writerow({'Metric': 'Average Price per Kilometer', 'Value': average_price_per_km})

    print(f"Results written to {output_file}")

if __name__ == "__main__":
    main()
