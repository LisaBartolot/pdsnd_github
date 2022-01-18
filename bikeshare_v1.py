import time
import datetime
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }
months = ['january', 'february', 'march', 'april', 'may', 'june']
days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('\nHello! Let\'s explore some US bikeshare data!')

    #get user input for city (chicago, new york city, washington).
    no_valid_city = 1
    while no_valid_city:
        city = input("Please select a city: Chigaco, New York City or Washington.")
        if city.lower() in CITY_DATA:
            no_valid_city = 0
        elif city.lower().startswith('c'):
            confirmation = input("Do you want to see bikeshare data from Chicago? yes or no?")
            if confirmation.lower() == 'yes':
                city = 'chicago'
                no_valid_city = 0
            else:
                print('\nNo valid input!\n')
                continue
        elif city.lower().startswith('n'):
            confirmation = input("Do you want to see bikeshare data from New York City? yes or no?")
            if confirmation.lower() == 'yes':
                city = 'new york city'
                no_valid_city = 0
            else:
                print('\nNo valid input!\n')
                continue
        elif city.lower().startswith('w'):
            confirmation = input("Do you want to see bikeshare data from Washington? yes or no?")
            if confirmation.lower() == 'yes':
                city = 'washington'
                no_valid_city = 0
            else:
                print('\nNo valid input!\n')
                continue

    #get user input for month (all, january, february, ... , june)
    no_valid_month = 1
    while no_valid_month:
        month = input("Please select a month: january, february, march, april, may, june or all.")
        if month in months:
            no_valid_month = 0
            month = months.index(month) + 1
            break
        elif month == 'all':
            no_valid_month = 0
            break

    #get user input for day of week (all, monday, tuesday, ... sunday)
    no_valid_day = 1
    while no_valid_day:
        day = input("Please select a day: monday, tuesday, wednesday, thursday, friday, saturday, sunday or all.")
        if day in days:
            no_valid_day = 0
            day = days.index(day)
            break
        elif day == 'all':
            no_valid_day = 0
            break

    print('-'*40)
    if day != 'all' and month != 'all':
        print("Here you get some statistics on the bikeshare data on {} in {} 2017 in {}.\n".format((days[day] + 's').title(), (months[month-1]).title(), city.title()))
    elif day != 'all':
        print("Here you get some statistics on the bikeshare data on {} from January till June 2017 in {}.\n".format((days[day] + 's').title(), city.title()))
    elif month != 'all':
        print("Here you get some statistics on the bikeshare data in {} 2017 in {}.\n".format((months[month-1]).title(), city.title()))
    else:
        print("Here you get some statistics on the bikeshare data from January till June 2017 in {}.\n".format(city.title()))
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

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week and hour from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.dayofweek
    df['hour'] = df['Start Time'].dt.hour

    # filter by month if applicable
    if month != 'all':
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day]

    return df


def time_stats(df, city):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    #calculate the most common month
    popular_month = df['month'].mode()[0]
    popular_month = months[popular_month-1]

    #calculate the most common day of week
    popular_day = df['day_of_week'].mode()[0]
    popular_day = days[popular_day]+'s'

    #calculate the most common start hour
    popular_hour = df['hour'].mode()[0]
    popular_hour = datetime.time(popular_hour).strftime("%I %p")

    print('\nThe most frequent times of travel in {} is in {}, on {}, at {}.'.format(city.title(), popular_month.title(), popular_day.title(), popular_hour))
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    #calculate most commonly used start station
    popular_start_station = df['Start Station'].mode()[0]

    #calculate most commonly used end station
    popular_end_station = df['End Station'].mode()[0]

    #calculate most frequent combination of start station and end station trip
    df['trip'] = df['Start Station'] + ' --- ' + df['End Station']
    popular_trip = df['trip'].mode()[0]
    popular_trip_start_station = popular_trip.split(' --- ')[0]
    popular_trip_end_station = popular_trip.split(' --- ')[-1]

    print("\nThe most commonly used start station is {}, the end station is {}.". format(popular_start_station, popular_end_station))
    print("The most frequent combination of start station and end station trip is from {} to {}.".format(popular_trip_start_station, popular_trip_end_station))
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df, city):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    #calculate total travel time
    total_travel_time_s = df['Trip Duration'].sum().sum()
    total_travel_time_h = int(total_travel_time_s / 3600)
    total_travel_time_d = round(total_travel_time_h/24 , 1)

    #calculate mean travel time
    mean_travel_time_min = int(df['Trip Duration'].mean() / 60)

    print("The overall travel time in {} in this period is {} hours (about {} days).".format(city.title(), total_travel_time_h, total_travel_time_d))
    print("The mean travel time in {} in this period is {} min.".format(city.title(), mean_travel_time_min))
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df, city):
    """
    Displays statistics on bikeshare users.

    Get information on the users:
    - gender
    - min/max birth year
    - most frequent birth year

    No user data is available in Washington.  
    """

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    #calculate counts of user types
    user_type_counts = df['User Type'].value_counts()
    print(user_type_counts.to_string())
    print('\n')

    if city != 'washington':

        #calculate counts of gender
        gender_counts = df['Gender'].value_counts()
        gender_nans = df['Gender'].isnull().sum()
        print(gender_counts.to_string())
        print("{} users didn't provide information on their gender.".format(gender_nans))

        #calculate earliest, most recent, and most common year of birth
        earliest_birth_year = df['Birth Year'].min()
        recent_birth_year = df['Birth Year'].max()
        common_birth_year = df['Birth Year'].mode()[0]
        birth_year_nans = df['Birth Year'].isnull().sum()

        print('\nThe oldest user is born in {}, the youngest user is born in {}.'.format(int(earliest_birth_year), int(recent_birth_year)))
        print('Most users are born in {}.'.format(int(common_birth_year)))
        print("{} users didn't provide information on their birth year.".format(birth_year_nans))
        print("\nThis took %s seconds." % (time.time() - start_time))
    else:
        print("There is no detailed user data in Washington.")
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df, city)
        station_stats(df)
        trip_duration_stats(df, city)
        user_stats(df, city)

        print_data = input('\nWould you like to see some of the data? Enter yes or no.\n')
        i = 0
        pd.set_option('display.max_columns', None)
        while print_data.lower() == 'yes' and i < df.shape[0] :
            if i+5 < df.shape[0]:
                print(df.iloc[i:i+5, 0:df.shape[1]-4])
                i += 5
                print_data = input('\nWould you like to see more data? Enter yes or no.\n')
            else: #end of data
                print(df[i:])
                print("You have seen all of the data!")


        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break

if __name__ == "__main__":
	main()
