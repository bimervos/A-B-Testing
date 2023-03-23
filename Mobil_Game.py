# This project is a project from https://www.datacamp.com/projects/184 .
# Cookie Cats is a  popular mobile puzzle game.
# It's a  "connect three"-style puzzle game where the player must connect tiles of the same color to clear the board and win the level.
# Here is the promotional video:

# https://www.youtube.com/watch?v=0G-612U2vQY&t=6s

# As players progress through the levels of the game, they will occasionally encounter gates that force them to  make an in-app purchase to progress.
# But where should the gates be placed?
# Initially the first gate was placed at level 30. In this project, we're going to analyze an AB-test where we moved the first gate in Cookie Cats from level 30 to level 40.
# In particular, we will look at the impact on player retention.

#With head() we can observe the first 5 variables :

#The variables are:
#userid :  a unique number for each player.
#version : control group (gate_30 - a gate at level 30) or the test group (gate_40 - a gate at level 40).
#sum_gamerounds : the number of game rounds played by the player during the first week after installation
#retention_1: did the player come back and play 1 day after installing?
#retention_7 : did the player come back and play 7 days after installing?
#(player installed the game, he or she was randomly assigned to either gate_30 or gate_40.)

# AB Testing Process:

# Understanding data
# Detect and resolve problems in the data (Missing Value, Outliers, Unexpected Value)
# Check summary stats and plots
# Apply hypothesis testing and check assumptions
# Check Normality & Homogeneity
# Apply tests (Shapiro, Levene Test, T-Test, Welch Test, Mann Whitney U Test)
# Evaluate the results
# Make inferences
# Recommend business decision to your customer/director/ceo etc.


#First, let's load the dataset and save it as df :

import seaborn as sns
import pandas as pd
import  itertools
import matplotlib.pyplot as plt
import statsmodels.stats.api as sms
from scipy.stats import ttest_1samp, shapiro, levene, ttest_ind, mannwhitneyu,pearsonr, spearmanr, kendalltau, f_oneway, kruskal
from statsmodels.stats.proportion import  proportions_ztest

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
pd.set_option('display.width', 500)
pd.set_option('display.float_format', lambda x: '%3f' %x)

df= pd.read_csv('cookie_cats.csv')
df.head()

#You can access the row and column information in the dataset:

df.shape

#You can access the descriptive statistics of the numeric variables in the data set.
#Outlier values can be observed, and many analyzes such as average, max, min can be reached.

df.describe().T

# We can see if there is an empty value in the data set, and we can take action accordingly.
#(Depending on the dataset story, empty values can be deleted or filled with other objects)

df.isnull().sum()

#Type examination of the variables in the data set can be done.

df.dtypes

# Apart from the type information of the variables, the observation unit and the number of variables also show whether they are null or not.

df.info()

df.groupby('version').count()