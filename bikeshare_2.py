import time
import pandas as pd
import numpy as np

CITY_DATA = {'chicago': 'chicago.csv',
             'new york city': 'new_york_city.csv',
             'washington': 'washington.csv'}


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.
    """
    print("Hello! Let's explore some US bikeshare data!")
    
    prompts = {
        'city': {
            'choices': CITY_DATA.keys(),
            'message': "Please select either Chicago, New York City, or Washington. Remember to double check your spelling!"
        },
        'month': {
            'choices': ['january', 'february', 'march', 'april', 'may', 'june', 'all'],
            'message': "What month would you like to filter by? Please enter a month from January to June or enter 'all' if you would like to view all six months in the data. Please make sure you are using the full month name with no abbreviations."
        },
        'day': {
            'choices': ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'all'],
            'message': "What day of the week would you like to filter by? Please enter a day of the week or enter 'all' if you would like to view all days in the data. Please make sure you are using the full day name with no abbreviations."
        }
    }
    
    responses = {}
    for key, value in prompts.items():
        user_input = ''
        while user_input not in value['choices']:
            print(value['message'])
            user_input = input().lower()
        responses[key] = user_input

    print('-' * 40)
    return responses['city'], responses['month'], responses['day']


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    df = pd.read_csv(CITY_DATA[city])

    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()

    if month != 'all':
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
        df = df[df['month'] == month]

    if day != 'all':
        df = df[df['day_of_week'] == day.title()]

    return df


def display_raw_data(df):
    """
    Displays 5 lines of raw data at a time and asks user if they'd like to see more.
    If yes, it will show the next 5 lines of data.
    This will continue until the user inputs 'no' or there is no more data to display.
    """

    i = 0
    raw = input("\nWould you like to see first 5 rows of raw data; type 'yes' or 'no'?\n").lower()
    pd.set_option('display.max_columns', 200)

    while True:
        if raw == 'no':
            break
        print(df[i:i + 5])
        raw = input("\nWould you like to see next 5 rows of raw data; type 'yes' or 'no'?\n").lower()
        i += 5


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    common_month = df['month'].mode()[0]
    print(f"Most common month: {common_month}")

    # display the most common day of week
    common_day_of_week = df['day_of_week'].mode()[0]
    print(f"Most common day: {common_day_of_week}")

    # display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    common_hour = df['hour'].mode()[0]
    print(f"Most common hour: {common_hour}")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    common_start_station = df['Start Station'].mode()[0]
    print(f"Most commonly used start station: {common_start_station}")

    # display most commonly used end station
    common_end_station = df['End Station'].mode()[0]
    print(f"Most commonly used end station: {common_end_station}")

    # display most frequent combination of start station and end station trip
    common_station_combination = df['Start Station'] + " to " + df['End Station']
    most_common_station_combination = common_station_combination.mode()[0]
    print(f"Most Frequent Combination of start station and end station trip: {most_common_station_combination}")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = df['Trip Duration'].sum()
    print(f"Total travel time: {total_travel_time}")

    # display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    print(f"Mean travel time: {mean_travel_time}")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print(f"User Types:\n{user_types}")

    # Display counts of gender
    if 'Gender' in df:
        gender = df['Gender'].value_counts()
        print(f"\nGender:\n{gender}")

    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df:
        earliest_year = df['Birth Year'].min()
        print(f"\nEarliest Year: {earliest_year}")
        most_recent_year = df['Birth Year'].max()
        print(f"Most Recent Year: {most_recent_year}")
        most_common_year = df['Birth Year'].mode()[0]
        print(f"Most Common Year: {most_common_year}")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        display_raw_data(df)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()
