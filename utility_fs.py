# PROGRAMMER: JC Lopez  
# REVISED DATE: 04/22/2019
# PURPOSE: Utility functions for DS-Term-2 Project 1

# Import python libraries
import calendar
from collections import Counter
import numpy as np
import pandas as pd
import warnings

# Import visualization libraries
import matplotlib.dates as plotdates
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import seaborn as sns
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

# Import scikit-learn modules
from sklearn.compose import ColumnTransformer
from sklearn.exceptions import DataConversionWarning
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LinearRegression
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler, OneHotEncoder

# Import StatsModels modules
import statsmodels.api as sm


# Functions
def print_data(data, city, rows=3):
    """Provide high-level view of the content of the Airbnb data. 

    The information printed by the function is described below:
        1. Shape — total rows x total columns — of all 3 datasets for 
        the city.
        2. First n rows of `calendar.csv`.
        3. First n rows of `listings.csv`.
        4. First n rows of `reviews.csv`.  
    
    Args: 
        data (dict): Hierarchical dict with city as the first level and 
            dataset type — calendar, listings, reviews — as the second.
        city (str): 'Boston' or 'Seattle'.
        rows (int): Number of top rows to display.

    Returns: 
        None. Print statistics and display dataframes.
        
    """
    # Print shapes of dataframes 
    print('(1) Shape of datasets for {}:\n'.format(city))
    for name, df in data[city].items():
        print('{:>8s}.csv - {:>9,.0f} x {:>2.0f}'\
            .format(name, df.shape[0], df.shape[1]))
    
    # Display first n rows of all 3 dataframes
    k = 1
    for name, df in data[city].items():
        k += 1
        print('\n({}) First few rows of {}\'s {}.csv:'.format(k, city, name))
        display(df.head(n=rows))


def hist_miss_by_cols(data, data_name):
    """Build histograms to visualize the distribution of missing values 
    per column, measured as percentage of column-values missing. 
    
    Args: 
        data (dict): Hierarchical dict with city as the first level and 
            dataset type — calendar, listings, reviews — as the second.
        data_name (str): 'all', 'calendar', 'listings', or 'reviews'.
    
    Returns: 
        None. Displays the histograms.

    """
    # Set figure parameters      
    if data_name == 'all':
        fig, axes = plt.subplots(nrows=3, ncols=2, figsize=(11, 11), 
                                 sharey='row')
    else:
        fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(11, 5), 
                                 sharey='row')
    
    # City-specific colors
    city_props = {
        'Boston': [0, 'salmon'], 
        'Seattle': [1, 'plum']
        }
    # Dataset-specific colors
    data_props = {
        'calendar': [0, 'b'], 
        'listings': [1, 'r'], 
        'reviews': [2, 'g']
        }
    # Loop over cities    
    for city, values in data.items():   
        # Check input 'data_name'
        if data_name != 'all':
            values = {data_name: values[data_name]}
        # Loop over datasets 
        for name, df in values.items():
            # Select axis and adjust figure spacing 
            if data_name == 'all':
                ax = axes[data_props[name][0], city_props[city][0]]
                fig.subplots_adjust(top=0.95)
            else:
                ax = axes[city_props[city][0]]
                fig.subplots_adjust(top=0.90)
            # Calculate percentage of missing values per column
            pct_missing = df.isnull().sum() / df.shape[0] * 100
            
            # Plot histogram of percent missing by column   
            ax.hist(pct_missing, facecolor=data_props[name][1], 
                rwidth=0.9)
            # Text box with city and dataset names
            text_box = city + '\n' + name + '.csv'
            ax.text(0.80, 0.92, text_box, transform=ax.transAxes, 
                    fontsize=14, verticalalignment='top', 
                    horizontalalignment='center', 
                    bbox=dict(boxstyle='round', facecolor=city_props[city][1], 
                    alpha=0.3))
            # Properties of x-axis 
            ax.set_xlim(0, 100)
            ax.set_xticklabels(['{:,}%'.format(
                int(x)) for x in ax.get_xticks().tolist()])
            # Properties of y-axis paramenters
            if city_props[city][0] == 0:
                ax.set_ylabel('Count of columns')
            y_locator = ticker.MaxNLocator(5, integer=True)
            ax.yaxis.set_major_locator(y_locator)
    
    # Show figure
    fig.suptitle('HISTOGRAMS OF COLUMN COUNTS VS PERCENTAGE OF VALUES MISSING',
                fontweight='bold')
    plt.show()


def missing_by_column(data, data_name, n_features=None):
    """Print the percentage of missing values per column for a given 
    dataset type and both cities, in descending order of percentage 
    missing.  
    
    Args: 
        data (dict): Hierarchical dict with city as the first level and 
            dataset type — calendar, listings, reviews — as the second.
        data_name (str): 'all', 'calendar', 'listings', or 'reviews'.
        n_features (int): Number of features to print.
    
    Returns: 
        None. Print missing values per column statistics.

    """
    # Print title
    print('Percent missing values per column in {}.csv'.format(data_name))
    
    # Loop over cities
    for city, values in data.items():
        # Calculate percent missing values per column
        df = values[data_name]
        pc = df.isnull().sum() / df.shape[0] * 100
        if n_features == None:
            n_features = len(pc)
        
        # Sort, format, and print series of percentages
        sorted_pc = pc.sort_values(ascending=False)\
            .apply(lambda x: '{:2.1f}%'.format(x))   
        print('\n{:^25}'.format('— ' + city + ' —'))
        print(sorted_pc[0:n_features + 1])


def count_rows_missing(data, city, data_name):
    """Print the count of rows per number of features missing. That is, 
    iterate from zero to the total number of features and show count of 
    rows in the dataset associated with that number of missing features.

    Also, display a histogram to visualize the distribution of missing 
    features per row in the dataset.
    
    Args: 
        data (dict): Hierarchical dict with city as the first level and 
            dataset type — calendar, listings, reviews — as the second.
        city (str): 'Boston' or 'Seattle'.
        data_name (str): 'calendar', 'listings', or 'reviews'.
    
    Returns: 
        None. Print missing values per column statistics.

    """
    # Get dataframe
    df = data[city][data_name]

    # Calculate number of missing values per row
    missing_per_row = df.isnull().sum(axis=1)
    # Count instances of possible missing-values elements
    counter = Counter(missing_per_row)
    sorted_tuples = sorted(list(counter.items()), key=lambda tup: tup[0])
    
    # Print title
    print('Count of rows per number of missing features in {}.csv'\
        .format(data_name))
    print('\n{}:'.format(city))
    
    # Loop over sorted counter and print results
    for t in sorted_tuples:
        print('{:>2} of {:>2} missing: {:>3,} rows'\
            .format(t[0], df.shape[1], t[1]))
    
    # Plot the same statistics     
    if data_name == 'listings':
        _figsize = (11, 5)
    else:
        _figsize = (6, 4)
    fig, ax = plt.subplots(figsize=_figsize)
    sns.countplot(missing_per_row)
    ax.set_xlabel('# of missing features')
    ax.set_ylabel('# of rows')
    ax.set_yticklabels(['{:,}'\
        .format(int(x)) for x in ax.get_yticks().tolist()])
    ax.grid(True)
    plt.show()


def describe_columns(data, city, data_name):
    """Display dataframe including the output of the 'describe()' 
    method, plus the data type by columns and some additional 
    descriptive statistics; namely, the 0.90 and 0.99 quantiles. 
    
    Args: 
        data (dict): Hierarchical dict with city as the first level and 
            dataset type — calendar, listings, reviews — as the second.
        city (str): 'Boston' or 'Seattle'.
        data_name (str): 'calendar', 'listings', or 'reviews'.
    
    Returns: 
        None. Display dataframe of descriptive statistics.

    """
    # Get dataframe
    df = data[city][data_name]
    # Get data type of each column and store in dataframe
    dtypes = pd.DataFrame(df.dtypes.rename('dtype')).transpose()

    # Generate descriptive statistics of central tendency
    summary_stats = df.describe(include='all')
    # Return values at specific quantiles
    quantile_90 = pd.DataFrame(
                    df.quantile(.90).rename('90%', inplace=True)).transpose()
    quantile_99 = pd.DataFrame(
                    df.quantile(.99).rename('99%', inplace=True)).transpose()
    
    # Build and display complete dataframe
    df_desc = dtypes.append([
        summary_stats[0:-1], 
        quantile_90, 
        quantile_99,
        summary_stats[-1:]
        ], sort=False)
    
    display(df_desc)


def unique_listing_records(data):
    """Count the number of observations per 'listing_id' in 'calendar', 
    and tabulate the unique observation count by the total number of 
    listings associated with it. 
    
    Args: 
        data (dict): Hierarchical dict with city as the first level and 
            dataset type — calendar, listings, reviews — as the second.
    
    Returns: 
        None. Print the counts.

    """
    # Loop over cities
    for city in data.keys():
        # Print city name
        print(city + ':')
        # Count the number of observations per 'listing_id' 
        counts = data[city]['calendar']\
            .groupby(by=['listing_id'])['available_re'].count()
        # Loop over unique values in counts
        for count in counts.unique():
            # Print number of listings associated with count
            print('{} recorded nights: {:>5,} listings'\
                .format(count, sum(counts == count)))
        print('')


def countplot_availability(data, city):
    """Perform three tasks using data in 'calendar':

    1. Build a histogram of the distribution of total days in the 
       year-of-sample when listings were recorded as available.
    2. Print the total number of listings in the dataset for given city.
    3. Print the start and final dates of the year-of-sample by city.
    
    Args: 
        data (dict): Hierarchical dict with city as the first level and 
            dataset type — calendar, listings, reviews — as the second.
        city (str): 'Boston' or 'Seattle'.
    
    Returns: 
        None. Displays histogram and prints statistics.

    """
    # Get limit dates in calendar.csv
    start_date = data[city]['calendar']['date_re'].min().date()
    end_date = data[city]['calendar']['date_re'].max().date()

    # Generate series of availability flags, grouped by listing id
    per_listing = data[city]['calendar'].groupby(
        by=['listing_id'])['available_re']
    # Sum flags to get total available days per listing
    counter = per_listing.sum()
    
    # Create a figure and a set of subplots
    fig, ax = plt.subplots(figsize=(10, 6))
    col = {'Boston': 'salmon', 'Seattle': 'plum'}
    sns.distplot(counter, kde=False, bins=25, color=col[city])
    # Set figure properties
    ax.text(1.07, 0.95, city, transform=ax.transAxes, fontsize=16, 
            verticalalignment='top', horizontalalignment='center', 
            bbox=dict(boxstyle='round', facecolor=col[city], alpha=0.3))  
    ax.set_title('HISTOGRAM OF LISTING AVAILABILITY IN A YEAR', 
                 fontweight='bold')
    ax.set_xlabel('Available days in year')
    ax.set_ylabel('Total listings')
    ax.set_yticklabels(['{:,}'\
        .format(int(x)) for x in ax.get_yticks().tolist()])
    plt.show()
    
    # Print relevant statistics
    print('Total number of listings in {}: {:,}'.format(city, len(counter)))
    print('Year goes from {} to {}'.format(start_date, end_date))


def time_series_means(data, variable, city, time_ax):
    """Build plot to visualize the time-series dimension of 'calendar'
    for the proportion of available listings or the average price.
    
    Choose between three different time axes:
    1. datetime: calendar date; i.e., from 2016-01-04 to 2017-01-02
    2. day_of_year: from Jan 1st to Dec 31st
    3. day_of_sample: from 0 to 365 
    
    Args: 
        data (dict): Hierarchical dict with city as the first level and 
            dataset type — calendar, listings, reviews — as the second.
        variable (str): 'availability' or 'price'.
        city (str): 'Boston' or 'Seattle' or 'both'.
        time_ax (str): 'datetime' or 'day_of_year' or 'day_of_sample'.
    
    Returns: 
        None. Displays the plot.

    """   
    # Translate keywords to column names
    dictionary = {'availability': 'available_re', 'price': 'price_re'}
    variable = dictionary[variable]
    # Translate keywords to city names
    cities = {
        'both': ['Boston', 
        'Seattle']
        }.get(city, [city])
    # Color scheme
    colors = {
        'Boston': 'salmon', 
        'Seattle': 'darkviolet'
        }
    # Create figure and subplot  
    fig, ax = plt.subplots(figsize=(12, 6))
    
    # If time dimension is 'datetime' (calendar date)
    if time_ax == 'datetime':
        # Loop over cities
        for city in cities:
            # Create series grouped by chosen time dimension
            time_series = data[city]['calendar']\
                .groupby(by=['date_re'])[variable]
            # Line plot
            sns.lineplot(data = time_series.mean(), label=city, 
                         color=colors[city]) 
        # x-axis properties            
        ax.get_xticks()
        ax.xaxis.set_major_locator(plotdates.MonthLocator(interval=2))
        ax.set_xlabel('Date', fontsize=14)
    
    # If time dimension is 'day_of_year' (Jan-1 to Dec-31)
    elif time_ax == 'day_of_year':
        # Loop over cities
        for city in cities:
            # Create series grouped by chosen time dimension
            time_series = data[city]['calendar']\
                .groupby(by=['day_of_year'])[variable]
            # Line plot
            sns.lineplot(data = time_series.mean(), label=city,
                         color=colors[city])    

        # x-axis properties
        majors = [1, 32, 61, 92, 122, 153, 183, 214, 245, 275, 306, 336]
        labels = calendar.month_abbr[1:13]
        ax.xaxis.set_major_locator(ticker.FixedLocator(majors))
        ax.xaxis.set_major_formatter(ticker.FixedFormatter(labels))
        ax.set_xlabel('Day of year', fontsize=14)
    
    # If time dimension is 'day_of_sample' (0 to 364)
    elif time_ax == 'day_of_sample':
        # Loop over cities
        for city in cities:
            # Create series grouped by chosen time dimension
            time_series = data[city]['calendar']\
                .groupby(by=['day_of_sample'])[variable]
            # Line plot
            sns.lineplot(data = time_series.mean(), label=city,
                         color=colors[city])
        # x-axis properties    
        ax.set_xlabel('Day of sample per city', fontsize=14)
    
    # y-axis properties  
    # If outcome is availability 
    if variable == 'available_re':
        ax.yaxis.set_major_locator(ticker.MaxNLocator(5))
        ax.yaxis.set_major_formatter(ticker.PercentFormatter(xmax=1)) 
        ax.set_title('TIME SERIES OF AVAILABILITY', fontsize=16,
                     fontweight='bold')
        ax.set_ylabel('Percent listings available', fontsize=14)
    
    # If outcome is price     
    elif variable == 'price_re':
        ax.yaxis.set_major_formatter(ticker.FormatStrFormatter("$%d")) 
        ax.set_title('TIME SERIES OF PRICES', fontsize=16,
                     fontweight='bold')
        ax.set_ylabel('Price', fontsize=14)   
    
    # Display figure 
    plt.show()


def weekend_prices(data, city):
    """Use time_series_means() to explore the within-week variability 
    of prices by day-of-sample, separating the data into two subsets of 
    prices: 
    1. Friday and Saturday nights and 
    2. the rest of the week.  
    
    Args: 
        data (dict): Hierarchical dict with city as the first level and 
            dataset type — calendar, listings, reviews — as the second.
        city (str): 'Boston' or 'Seattle' or 'both'.

    Returns: 
        None. Displays the plots.

    """ 
    # Build time-series data for plot
    df = pd.DataFrame()
    df['price_re'] = data[city]['calendar']\
        .groupby(by=['day_of_sample'])['price_re'].mean()
    df['day_of_sample'] = data[city]['calendar']\
        .groupby(by=['day_of_sample'])['day_of_sample'].min()
    df['fri_sat'] = data[city]['calendar']\
        .groupby(by=['day_of_sample'])['fri_sat'].min()
    
    # Call time_series_means()
    time_series_means(data, variable='price', city = city, 
                      time_ax = 'day_of_sample')
    
    # Color scheme
    colors = {
        'Boston': ['salmon', 'firebrick'], 
        'Seattle': ['plum', 'darkviolet']
        }
    
    # Create figure and subplot  
    fig, ax = plt.subplots(figsize=(12, 6))
    
    # Build plot
    sns.lineplot(data = df, x = 'day_of_sample', y = 'price_re', 
                 hue='fri_sat', palette=colors[city])
    ax.text(0.89, 0.83, city, transform=ax.transAxes, fontsize=14, 
            verticalalignment='top', bbox=dict(boxstyle='round', 
            facecolor=colors[city][0], alpha=0.5))
    ax.legend(['Sun-Thu', 'Fri-Sat'])

    # Axes properties
    ax.set_xlabel('Day of sample', fontsize=14)
    ax.yaxis.set_major_formatter(ticker.FormatStrFormatter("$%d")) 
    ax.set_ylabel('Price', fontsize=14) 

    # Display figure 
    plt.show()


def countplot_reviews(data, city, cutoff=None):
    """Perform two tasks describing the distribution of reviews:
    1. Print descriptive statistics for reviews received. 
    2. Build a histogram of number of reviews by listing.    
    
    Args: 
        data (dict): Hierarchical dict with city as the first level and 
            dataset type — calendar, listings, reviews — as the second.
        city (str): 'Boston' or 'Seattle'.
        cutoff (int): Limit number of reviews (x-axis) in order to 
            zoom in.

    Returns: 
        None. Print statistics and display histogram.

    """
    # Review number by listing id
    review_counts = data[city]['calendar']\
        .groupby(by=['listing_id'])['total_reviews'].max()
    # Print total reviews for city
    print('Total number of reviews in {}: {:,}\n'\
        .format(city, review_counts.sum()))
    
    # Central tendency stats
    stats = review_counts.describe().apply(round)
    # Print central tendency stats
    for i in stats.index[1:-1]:
        print('{:6} {:>5,}'.format(i + ':', stats.loc[i]))
    print('{:6} {:>5,}'.format('90%:', round(review_counts.quantile(.90))))
    print('{:6} {:>5,}'.format('99%:', round(review_counts.quantile(.99))))
    print('{:6} {:>5,}'.format(stats.index[-1] + ':', stats.iloc[-1]))
    
    # Check for keyword 'cutoff'    
    if cutoff is None:
        data = review_counts
    else:
        data = review_counts[review_counts <= cutoff]
    
    # Color scheme
    colors = {
        'Boston': ['salmon', 'firebrick'], 
        'Seattle': ['plum', 'darkorchid']
        }
    
    # Create figure and subplot 
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.distplot(data, kde=False, bins=30, color=colors[city][1])
    ax.text(0.9, 0.95, city, transform=ax.transAxes, fontsize=14, 
            verticalalignment='top', bbox=dict(boxstyle='round', 
            facecolor=colors[city][0], alpha=0.5))
    
    # Figure properties
    ax.set_title('HISTOGRAM OF TOTAL REVIEWS RECEIVED', 
                 fontsize=14, fontweight='bold')
    ax.set_xlabel('Number of reviews')
    ax.set_ylabel('Total listings')
    ax.set_yticklabels(['{:,}'\
        .format(int(x)) for x in ax.get_yticks().tolist()])
    if cutoff is not None:
        ax.set_xlim(0, cutoff)
    
    # Display figure 
    plt.show()


def linear_model(data, outcome, ind_var='total_reviews',
                numeric_features=[], categorical_features=[]):
    """Instantiate and fit a scikit-learn linear regression model, 
    allowing for some flexibility in the choice of the price and 
    reviews measurements, as well as the choice of other numeric 
    and categorical covariates or features. 

    The main steps within the `linear_model()` function are:
    1. Instantiate a numeric transformer, to impute missing values 
       (when necessary) and to standardize the values. 
    2. Instantiate a categorical transformer, to impute missing values 
       (when necessary) and to perform one-hot encoding.
    3. Fit and transform the numeric and categorical features using 
       these transformers.
    4. Build the `X` matrix by appending the transformed covariates to 
       the independent variable of interest.
    5. Build the `y` vector, considering whether a log transformation 
       is required. 
    6. Fit the linear regression model.
    7. Print the main coefficient for the independent variable of 
        interest — either the number of reviews or a binary indicator 
        for having any number of reviews. 
    8. Return the fitted model, `X`, and `y`.
    
    Args: 
        data (dict): Hierarchical dict with city as the first level and 
            dataset type — calendar, listings, reviews — as the second.
        outcome (str): 'price' or 'log_price'.
        ind_var (str): 'total_reviews' or 'reviewed'.
        numeric_features (list): Column names for numeric covariates. 
        categorical_features (list): Column names for categorical 
            covariates.

    Returns: 
        lm (sklearn obj): fitted scikit-learn linear regression model.
        X (array): matrix of independent variable and covariates values.
        y (array): vector of outcome values.

    """
    # Instantiate numeric transformer: imputer + scaler
    numeric_transformer = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='constant', fill_value=0)),
        ('scaler', StandardScaler())
        ]) 
    # Instantiate categorical transformer: imputer + one-hot encoder
    categorical_transformer = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='constant', fill_value='missing')),
        ('onehot', OneHotEncoder(handle_unknown='ignore'))
        ]) 
    # Instantiate column transformer
    preprocessor = ColumnTransformer(transformers=[
        ('num', numeric_transformer, numeric_features),
        ('cat', categorical_transformer, categorical_features)
        ])  
    # Ignore Data Conversion Warning
    warnings.filterwarnings(action='ignore', category=DataConversionWarning)
    
    # Fit column transformer and transform data
    transformed_features = preprocessor\
        .fit_transform(data[numeric_features + categorical_features])
    # Transform data to numpy array if necessary
    try:
        array_features = transformed_features.toarray()
    except:
        array_features = transformed_features
    
    # Instantiate regressor - sklearn.linear_model
    lm = LinearRegression()
    # Build the `X` matrix 
    X = np.append(data[[ind_var]].values, array_features, axis=1)
    
    # If outcome is 'log_price'
    if outcome == 'log_price':
        # Build the `y` vector 
        y = np.log(data[['price_re']])
        # Fit the model
        lm.fit(X, y)
        # Print coefficient of independent variable
        print('Coefficient on "{}":   {:.2f}%'\
            .format(ind_var, 100 * lm.coef_[0][0]))
    
    # If outcome is 'price'
    elif outcome == 'price':
        # Build the `y` vector 
        y = data[['price_re']] 
        # Fit the model
        lm.fit(X, y)
        # Print coefficient of independent variable
        print('Coefficient on "{}":   $ {:.2f}'\
            .format(ind_var, lm.coef_[0][0]))
    
    #Return fitted model, 'X', and 'y'
    return lm, X, y
