

# This project is a project from https://www.datacamp.com/projects/184 .
# Cookie Cats is a  popular mobile puzzle game.
# It's a  "connect three"-style puzzle game where the player must connect tiles of the same color to clear the board and win the level.
# Here is the promotional video:

# https://www.youtube.com/watch?v=0G-612U2vQY&t=6s

# As players progress through the levels of the game, they will occasionally encounter gates that force them to  make an in-app purchase to progress.
# But where should the gates be placed?
# Initially the first gate was placed at level 30. In this project, we're going to analyze an AB-test where we moved the first gate in Cookie Cats from level 30 to level 40.
# In particular, we will look at the impact on player retention.

#About the Dataset

#With head() we can observe the first 5 variables :

#The variables are:
#userid :  a unique number for each player.
#version : control group (gate_30 - a gate at level 30) or the test group (gate_40 - a gate at level 40).
#sum_gamerounds : the number of game rounds played by the player during the first week after installation
#retention_1: did the player come back and play 1 day after installing?
#retention_7 : did the player come back and play 7 days after installing?
#(player installed the game, he or she was randomly assigned to either gate_30 or gate_40.)

#Let's import the libraries :

import seaborn as sns
import pandas as pd
import  itertools
import matplotlib.pyplot as plt
import statsmodels.stats.api as sms
from scipy.stats import ttest_1samp, shapiro, levene, ttest_ind, mannwhitneyu,pearsonr, spearmanr, kendalltau, f_oneway, kruskal
from statsmodels.stats.proportion import  proportions_ztest

#Let's load the dataset :

pd.set_option('display.max_columns', None)
pd.set_option('display.width', 500)
pd.set_option('display.float_format', lambda x: '%3f' %x)

df= pd.read_csv('cookie_cats.csv')
df.head()

#You can access the row and column information in the dataset:

df.shape

#You can access the descriptive statistics of the numeric variables in the data set.
#Outlier values can be observed, and many analyzes such as average, max, min can be reached.

df.describe().T

#And you can see, there is an outier in 'sum_gamerounds'.
#While the mean value is 51 and the 75% value is 51, the maximum value is almost 50000. Because of this value, the evaluations may be wrong.

# We can see if there is a missing value in the data set, and we can take action accordingly.
#(Depending on the dataset story, missing values can be deleted or filled with other objects)

df.isnull().sum()

#Type examination of the variables in the data set can be done.

df.dtypes

# Apart from the type information of the variables, the observation unit and the number of variables also show whether they are null or not.

df.info()

#When a player installed the game, he or she was randomly assigned to either gate_30 or gate_40.
#We can observe the number of players in each version

df.groupby('version').count()




#Did you notice that users installed the game but 3994 users never played the game.

#OUTLIER THRESHOLD

#We need to threshold the outliers of the sum_gamerounds variable we caught above

df.groupby("sum_gamerounds").agg({'userid': 'count'})

#There is an unexpected value.While the sections are increasing in order, we see that it has increased from the 2961th section to the 49854th section.
#So it will suffice to seperate the maximum point.

df = df[df.sum_gamerounds < df.sum_gamerounds.max()]

#We can check now:

df.groupby("sum_gamerounds").agg({'userid': 'count'})
df.describe().T

#As we can see outliers have been edited.

#AB  TESTING

# Control group(A) : gate_30 - a gate at level 30
# Test group(B) : gate_40 - a gate at level 40

# Steps:
#1)Establish the hypothesis
#2)Assumption control:
#   Apply Shapiro Test for normality
#   Apply Levene Test for homogeneity of variances
#3)Implementation of the hypothesis:
#   If the distribution is Normal and the variances are homogeneous: apply the T-Test
#   If Distribution is Normal and the variances are not homogeneous: apply Welch Test ( with 'equal_var' argument )
#   If the distribution is not Normal: apply Mann Whitney U Test directly
#4)Result

#1)Establish the hypothesis :
#H0: A=B (There is no statistically significant difference between the experimental and control groups)
#H1: A!=B (There is statistically significant difference between the experimental and control groups)

#2)Assumption control:
#   2.1) Normality  Test:
#   H0: Distribution is Normal
#   H1: Distribution is not Normal

test_stat, pvalue= shapiro( df.loc[df['version']=='gate_30' , 'sum_gamerounds'])
print('Test Stat= %.4f,  p-value= %.4f ' %(test_stat, pvalue))

#  Test Stat= 0.0881,  p-value= 0.0000
# p-value < 0.05 : h0 is rejected , distribution is not normal.

#   2.2) Homogeneity  Test:
#   H0: Distribution is homogeneous
#   H1: Distribution is not homogeneous

test_stat, pvalue= levene( df.loc[df['version']=='gate_30' , 'sum_gamerounds'],
                           df.loc[df['version']=='gate_40' , 'sum_gamerounds'])
print('Test Stat= %.4f,  p-value= %.4f ' %(test_stat, pvalue))

#  Test Stat= 0.5292,  p-value= 0.4669
# p-value > 0.05 : h0 can't rejected , distribution is homogeneous.

#3)Implementation of the hypothesis:
# If the distribution is not Normal: apply Mann Whitney U Test directly

test_stat, pvalue= mannwhitneyu( df.loc[df['version']=='gate_30' , 'sum_gamerounds'],
                           df.loc[df['version']=='gate_40' , 'sum_gamerounds'])
print('Test Stat= %.4f,  p-value= %.4f ' %(test_stat, pvalue))

#  Test Stat= 1024331250.5000,  p-value= 0.0502
# p-value > 0.05 : h0 can't rejected.
#H0: A=B (There is no statistically significant difference between the experimental and control groups)


#Shapiro Testing rejected H0 for the Normality assumption. Therefore, we had to apply a Non-parametric test called Mann Whitney U to compare the two groups.
#As a result, Mann Whitney U Testing could not reject the H0 hypothesis and we learned that the A/B groups were not significantly different!
#In short, there is no statistically significant difference between the two groups in moving the first gate from level 30 to level 40 for game rounds.