# Write A Data Science Blog Post
## Project #1 of Data Scientist Nanodegree Program - Term 2

## Motivation 

The goal of this project is to begin building a data science portfolio by creating a blog post and Github repository.

The high-level instructions are enumerated below:
1. Come up with three questions you are interested in answering.
2. Extract the necessary data to answer these questions.
3. Perform necessary cleaning, analysis, and modeling.
4. Evaluate your results.
5. Create a Github repository to share your code and data wrangling/modeling techniques, with a technical audience in mind.
6. Create a blog post to share your questions and insights with a non-technical audience.

## Summary 

This project is an exercise in quantitative business research using public Airbnb data for the cities of [Boston](https://www.kaggle.com/airbnb/boston) and [Seattle](https://www.kaggle.com/airbnb/seattle/data).  The project uses 3 analogous datasets for each city.

The main analysis in the project is an investigation of the following 3 questions:
1. What is the temporal behavior of the average availability of Airbnb homes in each city, and how do they compare to each other?
2. What is the seasonal behavior of average rates for Airbnb homes in these cities? Are average rates consistently higher on weekends?
3. What is the association between the average price/rate and the quantity of guest reviews received by a home on Airbnb?

## Data for Boston and Seattle
* **Listings**, including full descriptions and average review score 
* **Reviews**, including unique id for each reviewer and detailed comments 
* **Calendar**, including listing id and the price and availability for that day

Six (6) csv files in total.

## Python version
3.7.1 (default, Oct 23 2018, 14:07:42) 

## Files in the repository
- `ds_blog_post_airbnb.ipynb`:  Jupyter notebook including main code for data cleaning, analysis, and modeling; as well as comments and discussion of results. 
- `utility_fs.py`:  Python file including the custom-built functions required for the main analysis in the Jupyter notebook. 

## Python libraries
The Jupyter Notebook file, `ds_blog_post_airbnb.ipynb`,  requires the following Python libraries:
- sys
- numpy
- pandas
- matplotlib
- seaborn
- statsmodels.api
- utility_fs.py

The utility functions in `utility_fs.py` require the following Python libraries:
- numpy
- pandas
- calendar
- collections
- warnings
- matplotlib
- seaborn
- sklearn
- statsmodel.api

## Summary of results
Below is a brief synopsis of the results of the analysis, addressing each of the business questions described at the beginning of this document.

### 1)  Temporal behavior of average availability 

Average availability does not seem to show a systematic, seasonal behavior. In fact, the average availabilities per city follow very similar (or parallel) patterns only when plotted against the **day-of-sample** — from day 1 to day 365 of each sample — as opposed to the actual date of day-of-year. Since the two samples correspond to two different spans of calendar dates, I can’t think of a good reason why the trends would match in this way, unless the behavior is entirely a product of sample selection and panel-dataset construction.

### 2)  Weekly and seasonal behavior of average Airbnb rates 

Following a noisy segment of data for Boston (first 120 days of sample), the time-series of Boston’s average rate follows the same weekly cycle as Seattle’s average rate. The association between average rate and day-of-week seems to be analogous across the two cities:
1. The lowest rates are posted for Monday, Tuesday, and Wednesday.
2. Slightly higher rates are posted for Thursdays and Sundays.
3. Rates increase and peak for the weekend evenings, Fridays and Saturdays.

The visualizations that show average rates in a calendar year suggest the following working hypotheses: 
1. Average rates seem to be increasing independently of season. I would guess that average rates in this two cities were increasing year over year.
2. The seasonal behavior of rates is analogous in Boston and Seattle, with average price peaking in the early Summer months and bottoming out in late Winter.
3. The spike in the Boston average rate that happens in September of 2016 is not a product of real conditions in the city. The high and noisy trend in rates is due to a smaller sample of available listings.
4. The highly noticeable spike in the Boston average rate that happens in April of 2017 is most likely a product of some real event that affected the market conditions in the city: the 2017 Boston Marathon.

### 3)  Association between rates and quantity of guest reviews 

The association between rates and the quantity of reviews is difficult to investigate exclusively through visualizations. Thus, the analysis relies on a comparison of means using simple linear regressions.

Estimating a naive-pooled-model without covariates/controls suggests that, on average, every additional guest review is associated with a decrease in rates of 0.17%. This is counterintuitive if one believes that reviews tend to be positive and associated with good AirBnB hosting; which in turn should provide leverage for host to post higher prices for their homes.

Another specification of the model, with controls for home size, location, and time trends, produces an estimate of -0.0008: on average, every additional guest review is associated with a decrease in rates of 0.08%.

The estimate coming from the last specification of the model indicates that if we control for home size, location, and time trends, having 1 or more guest reviews is associated with an average decrease in rates of 6%.
Once again, this is a counterintuitive finding if one believes that being a reviewed home provides the host leverage to increase its price. On the other hand, if the saliency of bad experiences on AirBnB drive guests to disproportionately post bad reviews, then our measurement would be consistent with that underlying series of events.

Finally, an alternative explanation would be that there are selection bias problems in the sample with respect to guest reviews. If there is some underlying mechanism by which the reviewed listings are systematically different from the listings with zero reviews, then the average difference in price would be impossible to predict without a conceptual understanding of said systematic differences.

## Acknowledgements
* [Josh Bernhard](https://medium.com/@josh_2774), [Robert Chang](https://medium.com/@rchang) for inspiration and examples.
* [Airbnb Open Data](https://www.kaggle.com/airbnb)




