# Author: M.A.S.SILVA
#Date:12/09/2024
# Student ID: 20232554

import csv
import os

# Task A: Input Validation
def validate_date_input():
    """
    Prompts the user for a date in DD MM YYYY format, validates the input for:
    - Correct data type
    - Correct range for day, month, and year
    """
    # Day input    
    while True:
        try:
            day = int(input("Please enter the day of the survey in the format dd: "))
            if 1 <= day <= 31:
                break
            else:
                print("Out of range - day must be between 1 and 31.")
        except ValueError:
            print("Invalid input. Please enter a valid day (integer).")

    # Month input    
    while True:
        try:
            month = int(input("Please enter the month of the survey in the format MM: "))
            if 1 <= month <= 12:
                break
            else:
                print("Out of range - month must be between 1 and 12.")
        except ValueError:
            print("Invalid input. Please enter a valid month (integer).")

    # Year input
    while True:
        try:
            year = int(input("Please enter the year of the survey in the format YYYY: "))
            if 2000 <= year <= 2024:
                break
            else:
                print("Out of range - year must be between 2000 and 2024.")
        except ValueError:
            print("Invalid input. Please enter a valid year (integer).")

    return day, month, year

def validate_continue_input():
    """
    Prompts the user to decide whether to load another dataset:
    - Validates "Y" or "N" input
    """
    while True:
        choice = input("Do you want to select another data file for a different date? (Y/N): ").strip().upper()
        if choice == "Y":
            return True
        elif choice == "N":
            return False
        else:
            print("Invalid input. Please enter 'Y' for Yes or 'N' for No.")


# Task B: Process CSV Data
def process_csv_data(file_path):
    """
    Processes the CSV data for the selected date and extracts:
    - Total vehicles
    - Total trucks
    - Total electric vehicles
    - Two-wheeled vehicles, and other requested metrics
    """
    total_num_vehicles = 0
    total_num_trucks = 0
    total_num_electric_vehicles = 0
    total_num_two_wheeled = 0
    total_num_busses_north = 0
    total_num_straight_vehicles = 0
    total_num_bicycles = 0
    vehicles_over_speed_limit = 0
    elm_rabbit_avenue_vehicles = 0
    hanley_westway_highway_vehicles = 0
    elm_rabbit_avenue_scooters = 0
    rain_hours = 0
    rain_hours_set = set()
    busiest_hour_count = 0
    busiest_hour = None
    vehicle_counts_by_hour = {}
    
    hourly_traffic = [0] * 24 

    with open(file_path, mode='r', newline='') as file:
        csv_reader = csv.DictReader(file)

        for row in csv_reader:
            # Calculate total vehicles
            if row.get("VehicleType") in ["Motorcycle", "Bicycle", "Scooter", "Car", "Van", "Buss", "Truck"]:
                total_num_vehicles += 1
            
            # Get the hour for calculations
            hour = row.get('timeOfDay', '').split(':')[0]
            junction = row.get('JunctionName', '')
            
            # Total Trucks
            if row.get('VehicleType') == 'Truck':
                total_num_trucks += 1

            # Total Electric Vehicles    
            if row.get('elctricHybrid').upper() == 'TRUE':
                total_num_electric_vehicles += 1
                
            # Total Bicycle    
            if row.get('VehicleType') == 'Bicycle':
                total_num_bicycles += 1

            # Total of two-wheeled vehicles    
            if row.get('VehicleType') in ['Bicycle', 'Motorcycle', 'Scooter']:
                total_num_two_wheeled += 1
                
            # Buses that are headed North
            if (row.get('VehicleType') == 'Buss' and 
                row.get('travel_Direction_out') == 'N' and 
                row.get('JunctionName') == 'Elm Avenue/Rabbit Road'):
                total_num_busses_north += 1
                
            # Total vehicles passing through both junctions without turning
            if row.get('travel_Direction_in') == row.get('travel_Direction_out'):
                total_num_straight_vehicles += 1
                
            # Vehicles recorded as overspeeding
            if int(row.get('VehicleSpeed', 0)) > int(row.get('JunctionSpeedLimit', 0)):
                vehicles_over_speed_limit += 1
                
            # Vehicles recorded through Elm Avenue/Rabbit Road junction
            if row.get('JunctionName') == 'Elm Avenue/Rabbit Road':
                elm_rabbit_avenue_vehicles += 1

                # Total Scooters through Elm Avenue/Rabbit Road
                if row.get('VehicleType') == 'Scooter':
                    elm_rabbit_avenue_scooters += 1
            
            # Vehicles recorded through Hanley Highway/Westway junction
            if row.get('JunctionName') == 'Hanley Highway/Westway':
                hanley_westway_highway_vehicles += 1
                
                # Convert time to hour index (0-23)
                hour = int(row.get('timeOfDay', '').split(':')[0])
                hourly_traffic[hour] += 1
                
            # Rain hours (considering both Light Rain and Heavy Rain)
            if row.get ('Weather_Conditions') in ['Light Rain', 'Heavy Rain']:
                hour = int(row.get('timeOfDay', '').split(':')[0])
                rain_hours_set.add(hour)
                rain_hours = len(rain_hours_set)

        # Calculate averages and percentages
        if total_num_vehicles > 0:
            truck_percentage = round((total_num_trucks / total_num_vehicles) * 100)
        
        # Calculate bikes per hour using unique hours across both junctions
        if total_num_bicycles > 0:
            avg_bicycles_per_hour = round(total_num_bicycles / len(hourly_traffic))
        
        # Find busiest hour
        busiest_hour_count = max(hourly_traffic)  # Get the highest count
        busiest_hour = hourly_traffic.index(busiest_hour_count) 
        busiest_hour_range = f"{str(busiest_hour).zfill(2)}:00-{str(busiest_hour+1).zfill(2)}:00"

        # Calculate scooter percentage at Elm/Rabbit
        if elm_rabbit_avenue_vehicles > 0:
            elm_rabbit_avenue_scooter_percentage = round((elm_rabbit_avenue_scooters / elm_rabbit_avenue_vehicles) * 100)

    return {
        "The name of the selected CSV file": file_path,
        "The total number of vehicles passing through all junctions for the selected date": total_num_vehicles,
        "The total number of trucks passing through all junctions for the selected date": total_num_trucks,
        "The total number of electric vehicles passing through all junctions for the selected date": total_num_electric_vehicles,
        "The number of two-wheeled vehicles through all junctions for the date": total_num_two_wheeled,
        "The total number of busses leaving Elm Avenue/Rabbit Road junction heading north": total_num_busses_north,
        "The total number of vehicles passing through both junctions without turning left or right": total_num_straight_vehicles,
        "The percentage of all vehicles recorded that are Trucks for the selected date": f"{truck_percentage}%",
        "The average number Bicycles per hour for the selected date": avg_bicycles_per_hour,
        "The total number of vehicles recorded as over the speed limit for the selected date": vehicles_over_speed_limit,
        "The total number of vehicles recorded through only Elm Avenue/Rabbit Road junction for the selected date": elm_rabbit_avenue_vehicles,
        "The total number of vehicles recorded through only Hanley Highway/Westway junction for the selected date": hanley_westway_highway_vehicles,
        "The percentage of vehicles through Elm Avenue/Rabbit Road that are Scooters": f"{elm_rabbit_avenue_scooter_percentage}%",
        "The number of vehicles recorded in the peak (busiest) hour on Hanley Highway/Westway": busiest_hour_count,
        "The time or times of the peak traffic hour on Hanley Highway/Westway": busiest_hour_range,
        "The total number of hours of rain on the selected date": rain_hours
    }


def display_outcomes(outcomes):
    print("\n*********** Analysis Results ***********")
    for key, value in outcomes.items():
        print(f"{key}: {value}")

        
# Task C: Save Results to File
def save_results_to_file(outcomes, file_name="results.txt"):
    with open(file_name, "a") as file:
        file.write("\n*********** Analysis Results ***********\n")
        for key, value in outcomes.items():
            file.write(f"{key}: {value}\n")
    print(f"Results have been saved to '{file_name}'.")


while True:
    day, month, year = validate_date_input()
    file_name = f"traffic_data{day:02d}{month:02d}{year}.csv"

    if os.path.exists(file_name):
        outcomes = process_csv_data(file_name)
        display_outcomes(outcomes)
        save_results_to_file(outcomes)
    else:
        print(f"The file '{file_name}' was not found.")

    if not validate_continue_input():
        print("Exiting the program. Goodbye!")
        break

