import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        try:
            city = str(input("Please enter a city (chicago, new york city, or washington): ")).lower()
            if city in ['chicago', 'new york city', 'washington']:
                print("City input successful")
                break
            else:
                print("City input failed. Please enter 'chicago', 'new york city', or 'washington'")
        except ValueError:
            print("Not a valid string")
        except KeyboardInterrupt:
            print("No input taken")
            break                         

    # TO DO: get user input for month (all, january, february, ... , june)
    while True:
        try:
            month = str(input("Please enter a month (all, january, february, ... , june): ")).lower()
            if month in ['all', 'january', 'february', 'march', 'april', 'may', 'june']:
                print("Month input successful")
                break
            else:
                print("Month input failed. Please enter 'all', 'january', 'february', ... , or 'june'")
        except ValueError:
            print("Not a valid string")
        except KeyboardInterrupt:
            print("No input taken")
            break

    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        try:
            day = str(input("Please enter a day of the week (all, monday, tuesday, ... sunday): ")).lower()
            if day in ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']:
                print("Day of week input successful")
                break
            else:
                print("City input failed. Please enter 'all', 'monday', 'tuesday', ... or 'sunday'")
        except ValueError:
            print("Not a valid string")
        except KeyboardInterrupt:
            print("No input taken")
            break

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

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
    
        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month
    popular_month = df['month'].mode()[0]
    months = ['january', 'february', 'march', 'april', 'may', 'june']
    popular_month = months[popular_month - 1].title()
    print("Most popular month: {}".format(popular_month))

    # TO DO: display the most common day of week
    popular_day = df['day_of_week'].mode()[0]
    print("Most popular day: {}".format(popular_day))

    # TO DO: display the most common start hour
    # create new hour column
    df['hour'] = df['Start Time'].dt.hour
    popular_hour = df['hour'].mode()[0]
    print("Most popular hour: {}".format(popular_hour))
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    popular_start = df['Start Station'].mode()[0]
    print("Most popular start station: {}".format(popular_start))

    # TO DO: display most commonly used end station
    popular_end = df['End Station'].mode()[0]
    print("Most popular end station: {}".format(popular_end))    

    # TO DO: display most frequent combination of start station and end station trip
    popular_comb = df.groupby(['Start Station', 'End Station']).size().idxmax()
    print("Most popular combination of start and end station: {}".format(popular_comb))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    # cast Start and End Times as timestamps
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['End Time'] = pd.to_datetime(df['End Time'])
    df['Trip Time'] = df['End Time'] - df['Start Time']
    total_trav_time = df['Trip Time'].sum()
    print("Total travel time: {}".format(total_trav_time))

    # TO DO: display mean travel time
    avg_trav_time = df['Trip Time'].mean()
    print("Average travel time: {}".format(avg_trav_time))      
          
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    user_types = df.groupby(['User Type']).size()
    print("User Type Counts: {}".format(user_types.to_string()))

    # TO DO: Display counts of gender
    if 'Gender' in df.columns:
        gender_type_groups = df.groupby(['Gender']).size()
        print("Gender Counts: {}".format(gender_type_groups.to_string()))
    else:
        print("Sorry, but this city does not have Gender data available.")

    # TO DO: Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        earliest_year = df['Birth Year'].min()
        most_recent_year = df['Birth Year'].max()
        common_year = df['Birth Year'].mode()[0]
        print("Earliest Birth Year: {} \nMost Recent Birth Year: {} \nMost Common Birth Year: {}"\
        .format(int(earliest_year), int(most_recent_year), int(common_year)))
    else:
        print("This city does not have Birth Year data available.") 

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def show_raw_data(df):
    """Displays raw data from the dataset, if requested."""
    
    i = 0
    while True:
        try:
            data_req = str(input("Would you like to see 5 (more) rows of raw data? Please enter 'yes' or 'no': ")).lower()
            if data_req == 'yes':
                print(df[i:i+5])
                i += 5
            if data_req == 'no':
                print("Thank you.")          
                break
            else:
                print("Input failed. Please enter 'yes' or 'no'.")
        except ValueError:
            print("Not a valid string")
        except KeyboardInterrupt:
            print("No input taken")
            break
    
def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        
        show_raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
