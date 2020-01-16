import time
import pandas as pd
import numpy as np
from collections import defaultdict

pd.set_option('display.max_columns', 30)

CITY_DATA = { 'Chicago': 'chicago.csv',
              'New York City': 'new_york_city.csv',
              'Washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')

    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = input('\nEnter the city to filter (options: chicago, new york city, washington): ').title()
    while city  not in ('Chicago', 'New York City', 'Washington'):
       city = input('\nIncorrect input, re-enter the city to filter (options: chicago, new york city, washington): ').title()

    # get user input for month (all, january, february, ... , june)
    month = input('\nEnter the month to filter from first 6 months (options: january, february, march e.t.c) or "all" to apply no month filter: ').title()
    while month  not in ('January', 'February', 'March', 'April', 'May', 'June', 'All'):
       month = input('\nIncorrect input, re-enter any of the month from first 6 months to filter (options: january, february, march e.t.c) or "all" to apply no month filter: ').title()

    # get user input for day of week (all, monday, tuesday, ... sunday)
    day = input('\nEnter the day of the week to filter (options: monday, tuesday, wednesday e.t.c) or "all" to apply no day filter: ').title()
    while day not in ('Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday', 'All'):
       day = input('\nIncorrect input, re-enter the day of the week to filter (options: monday, tuesday, wednesday e.t.c) or "all" to apply no day filter: ').title()
    print('-'*40)
    return city, month, day


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

     # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time & End Time columns to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['End Time'] = pd.to_datetime(df['End Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name

    # filter by month if applicable
    if month != 'All':
        # use the index of the months list to get the corresponding int
        months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'All':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    #popular_month = df['month'].mode()
    print('\nThe most common month(s) is/are ')
    most_common(df, 'month')

    # display the most common day of week
    #popular_day_of_week = df['day_of_week'].mode()
    print('\nThe most common day(s) of the week is/are ')
    most_common(df, 'day_of_week')

    # display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    #popular_hour = df['hour'].mode()
    print('\nThe most common hour(s) is/are ')
    most_common(df, 'hour')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    #popular_start_station = df['Start Station'].mode()[0]
    print('\nThe most commonly used start station(s) is/are ')
    most_common(df, 'Start Station')

    # display most commonly used end station
    #popular_end_station = df['End Station'].mode()[0]
    print('\nThe most commonly used end station(s) is/are ')
    most_common(df, 'End Station')

    # display most frequent combination of start station and end station trip
    df['trip'] = df['Start Station'] + ' - ' + df['End Station']
    #popular_trip = df['trip'].mode()[0]
    print('\nThe most common trip(s) (combination of Start Station - End Station) is/are ')
    most_common(df, 'trip')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    print('\nTotal travel duration: {} mins'.format(df['Trip Duration'].sum()/60))

    # display mean travel time
    print('\nAverage travel time: {} mins'.format(df['Trip Duration'].mean()/60))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df, city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print('\nCounts of user type: \n', df['User Type'].value_counts())

    # Display counts of gender
    if city != 'Washington':
        print('\nCounts of gender: \n', df['Gender'].value_counts())


        # Display earliest, most recent, and most common year of birth
        print('\nEarliest year of birth: ', int(df['Birth Year'].min()))
        print('\nMost recent year of birth: ', int(df['Birth Year'].max()))
        print('\nMost common year of birth: ')
        most_common(df, 'Birth Year')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def most_common(df, col):
    """Calculate the most common values."""

    dict_counter = defaultdict(int)
    for d in df[col]:
        dict_counter[d] += 1
    #Sort the key, value tuples
    sorted_tuples = sorted(dict_counter.items(), key = lambda x:x[1], reverse = True)

    #Print the first value
    print(sorted_tuples[0][0])

    #Print the second value - in case of a tie between the most common instances (Which mode function cannot do)
    for i in range(0, len(sorted_tuples)-1):
        if sorted_tuples[i][1] == sorted_tuples[i+1][1]:
            print ('\n', sorted_tuples[i+1][0])
        else:
            break

def snapshot_of_data(df):
    """Displays 5 rows of the data."""

    print('\nShowing the 5 rows...\n')
    print(df.head(5))


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city)

        view_data = input('\nWould you like to view 5 rows of data? Enter yes or no(or something else). ').title()
        if view_data == 'Yes':
            snapshot_of_data(df)

        restart = input('\nWould you like to restart? Enter yes or no(or something else).\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
