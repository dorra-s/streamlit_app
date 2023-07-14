#!/usr/bin/env python
# coding: utf-8

# In[3]:

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
#from ydata_profiling import ProfileReport
#get_ipython().run_line_magic('matplotlib', 'inline')

# Set the title of the page
#st.title(":orange_book: Dataset General Configuration")
st.markdown('<h1 style="color: orange;">Dataset General Configuration</h1>', unsafe_allow_html=True)

# In[4]:


df_InfoUser  = pd.read_csv(r'C:\Users\ASUS\Desktop\archive\Info_UserData.csv')
df_LogProblem = pd.read_csv(r'C:\Users\ASUS\Desktop\archive\Log_Problem.csv',nrows=10000)
df_InfoContent = pd.read_csv(r'C:\Users\ASUS\Desktop\archive\Info_Content.csv')


# In[4]:


# Display the shape of the dataframes
st.write(f"The shape of df_InfoUser is: {df_InfoUser.shape}")
st.write(f"The shape of df_LogProblem is: {df_LogProblem.shape}")
st.write(f"The shape of df_InfoContent is: {df_InfoContent.shape}")

# # Data Cleaning

# ## 1_Check for missing values:

# In[26]:



# Check for missing values
missing_values_InfoUser = df_InfoUser.isnull().sum()
missing_values_LogProblem = df_LogProblem.isnull().sum()
missing_values_InfoContent = df_InfoContent.isnull().sum()

st.write("Missing values in Info_UserData.csv:")
st.write(missing_values_InfoUser)

st.write("Missing values in Log_Problem.csv:")
st.write(missing_values_LogProblem)

st.write("Missing values in Info_Content.csv:")
st.write(missing_values_InfoContent)


# ## 2_Check for outliers:

# In[24]:


# df_InfoUser:
# Create a figure with multiple subplots
fig1, axs = plt.subplots(2, 4, figsize=(15, 20))

axs = axs.flatten()

# Plot box plot for Info_UserData.csv
axs[0].boxplot(df_InfoUser['points'])
axs[0].set_title("Box plot of " + 'points')

axs[1].boxplot(df_InfoUser['badges_cnt'])
axs[1].set_title("Box plot of " + 'badges_cnt')

axs[2].boxplot(df_InfoUser['user_grade' ])
axs[2].set_title("Box plot of " + 'user_grade' )

axs[3].boxplot(df_InfoUser['has_student_cnt' ])
axs[3].set_title("Box plot of " + 'has_student_cnt' )

axs[4].boxplot(df_InfoUser['has_teacher_cnt' ])
axs[4].set_title("Box plot of " + 'has_teacher_cnt' )

#axs[5].boxplot(df_InfoUser['used_hint_cnt' ])
#axs[5].set_title("Box plot of " + 'used_hint_cnt' )

#axs[6].boxplot(df_InfoUser['has_class_cnt' ])
#axs[6].set_title("Box plot of " + 'has_class_cnt' )

# Adjust the spacing between subplots
plt.tight_layout()
st.pyplot(fig1)

# Display the figure with multiple box plots
#plt.show()


# In[30]:


#df_Log_Problem:
# Create a figure with multiple subplots
fig2, axs = plt.subplots(2, 3, figsize=(15, 20))

axs = axs.flatten()

# Plot box plot for Info_UserData.csv

axs[0].boxplot(df_LogProblem['used_hint_cnt'])
axs[0].set_title("Box plot of " + 'used_hint_cnt')

axs[1].boxplot(df_LogProblem['problem_number'])
axs[1].set_title("Box plot of " + 'problem_number')

axs[2].boxplot(df_LogProblem['exercise_problem_repeat_session' ])
axs[2].set_title("Box plot of " + 'exercise_problem_repeat_session' )

axs[3].boxplot(df_LogProblem['total_sec_taken' ])
axs[3].set_title("Box plot of " + 'total_sec_taken' )

axs[4].boxplot(df_LogProblem['total_attempt_cnt' ])
axs[4].set_title("Box plot of " + 'total_attempt_cnt' )

axs[5].boxplot(df_LogProblem['level' ])
axs[5].set_title("Box plot of " + 'level' )


# Adjust the spacing between subplots
plt.tight_layout()

# Display the figure with multiple box plots
st.pyplot(fig2)


# # The distribution of students across different learning stages:

# In[5]:


learning_stage_distribution =df_InfoContent['learning_stage'].value_counts()
st.write("Learning stage distribution:")
st.write(learning_stage_distribution)


# # The distribution of difficulties of the exercises:

# In[6]:


difficulty_distribution = df_InfoContent['difficulty'].value_counts()
st.write("Difficulty distribution:")
st.write(difficulty_distribution)

# # Total of exercises:

# In[7]:


total_exercises = len(df_InfoContent)
st.write("Total number of exercises:")
st.write(total_exercises)

# # The number of students who have attempted to answer the problems in the exercises:

# In[9]:


unique_students_attempted = df_LogProblem['uuid'].nunique()
st.write("unique_students_attempted:")
st.write(unique_students_attempted)


# #  The average number of problems in a single exercise:

# In[10]:


average_problems_per_exercise = len(df_InfoContent) / df_InfoContent['ucid'].nunique()
st.write("average_problems_per_exercise:")
st.write(average_problems_per_exercise)


# #  The average number of hints used per student per exercise:

# In[11]:


average_hints_per_student = df_LogProblem.groupby(['uuid', 'ucid'])['used_hint_cnt'].mean().mean()
st.write("average_hints_per_student:")
st.write(average_hints_per_student)

# #  The average number of attempts per student per exercise:

# In[12]:


average_attempts_per_student = df_LogProblem.groupby(['uuid', 'ucid'])['total_attempt_cnt'].mean().mean()
st.write("average_attempts_per_student:")
st.write(average_attempts_per_student)
