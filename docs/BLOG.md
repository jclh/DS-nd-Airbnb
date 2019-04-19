# 
This post is a synopsis of a quantitative-research project using public Airbnb data for the cities of [Boston](https://www.kaggle.com/airbnb/boston) and [Seattle](https://www.kaggle.com/airbnb/seattle/data). The analysis relies on six datasets — that is, three analogous data sources for each city:
* **Listings**:  home-level information about Airbnb listings.
* **Reviews**:  review-level information, including comments. 
* **Calendar**:  daily price and availability data per listing. 

I used my own background knowledge and intuitions concerning Airbnb and the hospitality industry to come up with three main questions that could be investigated using these public datasets:
1. How does average availability of Airbnb homes vary over time in each city? How does it compare between cities?
2. Is there a clear seasonal pattern for the average nightly rate on Airbnb in Boston and Seattle? Is there a clear weekly pattern?
3. Is there a strong association between a listing’s nightly rate and the number of guest reviews the home has received?
---
## Question 1
## How does average availability of homes vary over time?
Our `calendar` datasets include a variable for *availability* per night, per home, over the sample timeframe of 365 days. That is, for a given date an Airbnb home can be listed as either available or unavailable. 

With this variable, we can build a sample distribution for **available nights per year** for each city.

### Distribution of availability in a year
[image:FCF5BD8D-1046-465F-819E-363AB2E361D7-353-000046672A66F6B5/download.png]
[image:52704A04-F55B-4E8E-92D0-DD37921382DD-353-000046715E9B4203/download-1.png]

Excluding both *tails* of the histograms — near 0 nights and 365 nights of availability — the distribution of *available nights per year** looks similar in Boston and Seattle; that is, below approximately 300 nights per year the distribution is fairly uniform, and it seems to increase non-linearly after that. In other words, a plurality of Airbnb homes are recorded as available on at least 300 nights of the year for both Boston (~34%) and Seattle (~52%) .

Despite the similarities in the middle of the histograms, there are significant differences between the cities if we look at the extremes. For Boston, we clearly see a dominant spike in the distribution near 0 nights of availability; whereas for Seattle, the dominant spike is near 365 nights.

My best guess is that the differences in the tails are a product of different approaches of sampling the Airbnb data — home listings and dates — between the two cities (i.e., selection bias). In other words, I have a difficult time coming up with a hypothesis which would explain why these differences are a true characteristic of the underlying population of Airbnb listings in these two cities.

A plausible scenario consistent with selection bias is that all the Seattle listings were active on Airbnb during the year of sample (such that hosts were actually managing the availability of their homes on the platform), while a large plurality of Boston listings only became active hosts in the platform after the end of the year of sample for Boston.

### Average availability of homes over time

The histograms above provide a snapshot of a year of availability per home in their respective city. But in order to understand the dynamic, temporal behavior of availability in a city we can aggregate the daily snapshots of the data (i.e., cross-sections) and analyze these statistics over time.

The first figure in this section contains plots for the proportion of available Airbnb homes per night. The statistics are calculated separately for each city and plotted against the calendar date. For Boston, the timeframe covers from 2016-09-06 to 2017-09-05; and for Seattle the timeframe covers from 2016-01-04 to 2017-01-02.

[image:96866360-EADE-41D5-9FBA-097E22839F64-353-00004A4028D2BDBC/download-2.png]

In the first three months of their corresponding samples, Boston and Seattle show a similar *ramp up* pattern in the proportion of available homes per night. After that, the proportions are mostly stable with some small variation.  

This can be seen even more clearly if we plot the proportions of available homes against the **day-of-sample**; that is, from 0 to 365:
[image:B39DA02C-8800-4A57-AD01-4C033D92555F-353-00004BC2020E6797/download-3.png]

Even though the trends look very similar between the two cities, the plots stabilize at very different magnitudes for the proportion; with Seattle’s being significantly higher. This is consistent with what I noted in the previous section. My guess is that this gap between the proportions is a product of different approaches of sampling the Airbnb data between the two cities ; as opposed to Seattle and Boston inherently having such different levels of Airbnb availability in the long run.

Moreover, I would suppose that the datasets were backfilled with *observations* of homes before these homes were actually on Airbnb; this would make sense if the objective were to have tidy panel data, with the same dates dimension recorded for all homes. Since the yet-to-become Airbnb homes would be recorded as unavailable, this approach would produce an artificially low proportion of available homes,  which would ramp up over time.

Finally, the same proportion statistic can be plotted against **day-of-year** (January 1 to December 31), which is a better visualization to investigate whether there is a clear seasonal pattern.
[image:D869C77C-CF57-424C-BA9C-D58A68958B47-353-00004C0F5860B314/download-4.png]

The proportions of available homes do not seem to follow a clear seasonal behavior in these samples. It is plausible that some of the small dips in availability are associated with high-demand times-of-year, such as Spring Break and the start of Summer.

On the other hand, I prefer the explanation that these plots show non-seasonal and odd behavior, which is consistent with my argument in previous sections regarding the low availability being an artifice of sample selection and dataset construction.
---
## Question 2
## What are the seasonal and weekly patterns of average nightly rates?
The `calendar` datasets also include a variable for *price* per night, per home, over the sample timeframe of 365 days. For a given date, if the home is listed as unavailable then no price is posted; if the home is listed as available, a nightly rate is recorded. With this variable, we can build a variety of time-series plots for **average Airbnb rates** in Boston and Seattle.

As we did in the previous section, we’ll start by plotting our statistic of interest against  the calendar date: 2016-09-06 to 2017-09-05 for Boston; and 2016-01-04 to 2017-01-02 for Seattle.
[image:2833DC01-DE49-4899-82E4-B6335DA60A70-353-00004D6A47C7C634/download-5.png]

The plots show that the average nightly rate is a pretty noisy statistic, showing significant within-week variation. Since the Seattle time-series coincides with a calendar year, it’s easier to identify a seasonal pattern of higher prices in the Summer. This should become even clearer when we look at rates by time-of-year.
[image:9DED5DE4-BC0A-4704-A910-C983CBEC809D-353-00004DD0E2D0E687/download-6.png]

By looking at and comparing the last two figures, I propose the following plausible insights concerning the average nightly rates:
1. Average rates seem to be increasing *independently of the seasonal pattern*. Thus, I would guess that if the sample covered a longer timeframe, we would see that the average rates in these two cities were increasing year-over-year.
2. The seasonal pattern of the average rate is analogous in Boston and Seattle; that is, peaking in the early Summer months and bottoming out in late Winter.
3. The spike in the Boston average rate that happens in September is not a product of real conditions in the city. This high and noisy portion of the time-series occurs at the beginning of the sample, when few homes were available (as seen in the previous section)  and prices were not posted. Thus the spike and erratic pattern are probably due to the small sample size.
4. The other highly noticeable spike in the Boston average rate happens in April of 2017.  This spike is not a product of a smaller sample of available homes, and it is not present in the time-series for Seattle; so the pattern is likely a consequence of some real event that affected the lodging-market conditions in the city.

### Price spike in Boston — April of 2017

For a few days in April of 2017, the average nightly rate spiked in Boston, approximately, from $190/night to $235/night. This spike is significant and there is no analogous pattern in Seattle. In the following figure, we *zoom in* to visualize the average rate in Boston within the timeframe corresponding to the spike.  
[image:C485E280-B760-4916-B195-CB97D42AA32F-353-0000501E00C3416F/download-7.png]

The plot shows that the average rate in Boston spiked approximately from 2017-04-10 to 2017-04-18. Since the**2017 Boston Marathon**took place on Monday April 17, I think it is safe to say that this was the event that caused a substantial increase in demand and average rates for Airbnb’ homes in Boston.

### Within-week variation in nightly rates

In this section I will investigate whether there is a pattern of within-week variation in the average nightly rate.  Based on the time-series plots presented in the previous section (especially the issue concerning the small sample of available homes in Boston for a portion of time) I decided to look into the within-week rate pattern in Seattle. 

A simple way to assess whether the nightly rates are consistent with my own intuitions about the lodging industry — that is, rates are substantially higher on weekends — is to calculate the **average rate per day-of-week** for the Airbnb homes in Seattle:

	Monday  	$135.68
	Tuesday  	$135.41
	Wednesday  	$135.45
	Thursday  	$136.48
	Friday 		$143.04
	Saturday 	$143.20
	Sunday  		$136.46

Based on these simple averages, we can arrive at the following plausible conclusions about the association between Airbnb rates and day-of-week in Seattle:
1. Rates peak for weekend evenings: Fridays and Saturdays. The average nightly rate on weekends is about 6% higher than the average between Mondays and Wednesdays. 
2. The lowest rates are posted for Monday, Tuesday, and Wednesday.
3. Slightly higher rates are posted for Thursdays and Sundays.

In the final two figures of this section, we will take a second look at the time-series of average rates in Seattle. But this time we will see the effect of separating the weekend rates  (Friday-Saturday) from the weekday rates (Sunday-Thursday).
[image:6747E9B5-1EAF-403A-AFAC-68FF8C25900E-353-00005DEBE2F2CC09/download-8.png]
[image:849F71E0-7634-4A74-BA7C-6E5D33AA3D8F-353-00005DE4F74B3B77/download-9.png]
These two figures clearly show how the *noisy* average rate in Seattle can be smoothed out significantly by separating the data and making one plot for Friday-Saturday nights and another plot for the rest of the weeknights. 

As noted above the average weekend rate remains approximately 6% higher than the average weeknight rate during the entire sample. 
---
## Question 3
## Is there a strong association between the nightly rate and the number of guest reviews received?
In the final section of this project I look into the association between the nightly rate and the quantity of reviews a host has received on Airbnb. 

My preexisting intuitions about reviews on Airbnb were the following:
1. *Neutral* guest experiences are less likely to end in a review.
2. *Bad* guest experiences are likely to end in a negative review, but hosts that receive too many of those have a hard time renting their places and end up leaving Airbnb. 
3. *Good* guest experiences are likely to end in a positive review, and hosts with many positive reviews are successful and stay on Airbnb. Thus, more reviews tend to be a sign of quality hosting

Given these preexisting ideas about reviews on Airbnb, my working hypothesis about the association between rates and reviews was that *the more reviews a host has the higher the rate they are able to charge*.

### Distribution of reviews amongst listings on Airbnb

Before jumping into the analysis of nightly rates, let’s look at the histograms of reviews-per-listing in the sample. These provide a useful visualization of how reviews are distributed amongst Airbnb listings. 

[image:8488F9B1-A6AE-4935-B752-70154B3EB163-353-000061F478D2C6C2/download-10.png]
[image:EC80B7A6-37F2-4163-8240-831257C12865-353-000061F47917CD61/download-11.png]

The sample distribution of reviews-per-listing is highly skewed in both cities, with most listings having none or very few reviews, but a “long tail” of small numbers of listings having very many reviews. In fact, to have a better visualization of the majority of the listings, I cut off the x-axes in the figure above to only show 90% of the listings. The remaining 10% of listings were spread out approximately between 60 and 400+ reviews. 

### Observed association between nightly rates and number of reviews

In order to quantify the association between the nightly rate and the number of reviews corresponding to a particular listing, I had to impose some sort of conceptual structure on the underlying or latent relationship between rates and number of reviews received. This conceptual structure is typically referred to as the *model*.

Many assumptions or premises go into building a model, but some are extremely important to note explicitly. For instance, I should stress the fact that my analysis does not incorporate the *content* of reviews. In other words, there is no distinction between positive, neutral, and negative reviews; all reviews are treated equally. A more complete analysis of the relationship between prices and guest reviews ought to look into the content of the reviews in order to assess how different types of reviews are associated with the nightly rates that Airbnb hosts are able to charge.

Another extremely important conceptual assumption of the model is known as the *functional form*. For this analysis, I rely on the commonly used **general linear model** or **multivariate regression model** in order to quantify the relationship between rates and number of reviews. Roughly speaking, this family of statistical models can be used to estimate the factor by which the average nightly rate varies as a function of the number of reviews, while holding constant other variables that are relevant but not of primary interest. 

### **Nightly rate vs. Number of reviews**

The first estimate for the simple association between rates and number of reviews comes from a *naive* model. I call this first version of the model “naive” because it does not account for characteristics of a home — size, location, etc. — which in my opinion would obviously be associated with the nightly rate on Airbnb. 

This naive estimate indicates that, on average, every additional guest review is associated with a decrease in listing price of 0.17%. This would imply that, for instance, if an average listing starts with no reviews and a nightly rate of $100, after its first review the host would post a new rate of $99.83. 

To me this finding is counterintuitive, given my preconception that reviews tend to be positive and associated with good quality of Airbnb homes.

### **Nightly rate vs. [Number of reviews + Home Size + Neighborhood]**

Building on the naive model, I used the available data concerning home size/capacity and neighborhood to obtain an estimate (that is, of the association between rates and number of reviews) that accounts for how homes of different sizes and locations likely post different average nightly rates, independently of their number of reviews. 

Adding the data for home size and location produces an estimate that is about half of that of the naive model: on average, every additional guest review is associated with a decrease in listing price of 0.09%.

### **Nightly rate vs. [Number of reviews + Home Size + Neighborhood + Time of year]**

The final version of the model builds on the previous one — which used home size and location data — by attempting to capture some of the variation in nightly rates which is seasonal or dependent on the day of week. 

But adding a time dimension to the model only slightly changes the previous estimate; that is, on average, every additional guest review is associated with a decrease in listing price of 0.08%. So it looks like my simple addition of time-trends is mostly irrelevant.

The tiny change in the estimate after adding time-trends to the model seems counterintuitive, especially after what we saw in the discussion of Question 2 above: that average nightly rates follow clear within-week and seasonal trends. However, given the Airbnb data we have there is a statistical explanation of why adding these time-trends did not make a huge difference in our model.

In the data we have, the number of reviews is a constant number for each home, which means that we do not observe how each host modifies its own nightly rate as they receive more reviews. This implies that, roughly speaking, the estimate of 0.08% is completely driven by the average differences in rates between many homes with different numbers of reviews — as opposed to being driven by differences in nightly rates that would occur as each home receives reviews on different days of week and times of year. 

##  Synthesis
The empirical or statistical findings in this project were interesting to me, especially as they relate to my preconceived intuitions about Airbnb and, more generally, the lodging sector. Some of my preconceptions were not consistent with the statistical observations — I wrongly presumed listings with more reviews would post higher nightly rates — while some others were consistent — for instance, average nightly rates follow seasonal patterns and are highest on Fridays and Saturdays. 

An extremely important takeaway of this project should be that *the data **does not** speak for itself,* since in each step of the analysis we had to establish very important conceptual constraints (that is, both domain-specific and statistical) that allowed us to draw business and engineering insights from the datasets. For instance, consider the figure below which includes the two plots of average nightly rates in Boston and Seattle.

[image:99336103-E088-44A0-BE6C-C7849CF7A811-353-00007E3F8DA5CEB7/download-6.png]

The average nightly rate in Seattle follows a pattern that makes business sense, with consistent within-week behavior and a broad, slight peak in the Summer. On the other hand, the average rate in Boston only partially follows a similar pattern; the within-week behavior is basically the same as Seattle, but there are very dominant spikes in the nightly rate — one in April and one in September — which muddy up a broader seasonal pattern.

In my analysis I argued that the peak in April was due to a real-world event, the 2017 Boston Marathon, which caused a significant increase in demand of Airbnb homes. In contrast, I argued that the peak in September does not represent a real spike in demand and rates, but it is a result of the average rate being calculated with a small sample of available homes in Boston during the first few months of the sample. 

Finally, we saw that in our sample having more guest reviews is associated with slightly lower nightly rates. I am highly skeptical about this *finding* being a real causal link between rates and reviews on Airbnb. In other words, the simple associations I was able to quantify should be tested further using more robust business research strategies like prospective experimentation or richer analyses of existing data. 



























