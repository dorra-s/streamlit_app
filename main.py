#!/usr/bin/env python
# coding: utf-8

# In[6]:

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.ticker as mtick
import plotly.graph_objects as go
import dask.dataframe as dd
import plotly.express as px


# In[8]:

@st.cache_data
def read_data():
    df_InfoUser = pd.read_csv('/media/dorra/62207C0F207BE885/Users/ASUS/Desktop/archive/Info_UserData.csv')
    df_LogProblem = pd.read_csv('/media/dorra/62207C0F207BE885/Users/ASUS/Desktop/archive/Log_Problem.csv', nrows=500000)
    df_InfoContent = pd.read_csv('/media/dorra/62207C0F207BE885/Users/ASUS/Desktop/archive/Info_Content.csv')
    return df_InfoUser, df_LogProblem, df_InfoContent

df_InfoUser, df_LogProblem, df_InfoContent = read_data()


# In[9]:

title_style = """
    text-align: center;
    font-size: 32px;
    font-weight: bold;
    color: #007BFF; /* Blue color */
    padding: 20px 0;
    margin-bottom: 30px;
"""
st.markdown('<h2 style="text-align: center; background-color: orange; padding: 10px;">Data General Exploratory</h2>', unsafe_allow_html=True)
st.markdown("<h1 style='{}'>Data Visualisation</h1>".format(title_style), unsafe_allow_html=True)
st.write(f"The shape of df_InfoUser is: {df_InfoUser.shape}")
st.write(f"The shape of df_LogProblem is: {df_LogProblem.shape}")
st.write(f"The shape of df_InfoContent is: {df_InfoContent.shape}")


# # Data Cleaning

# In[14]:
markdown_style = """
    color: red;
    font-weight: bold;
"""
st.markdown("<p style='{}'>Shape of Files after Filtering Users:</p>".format(markdown_style), unsafe_allow_html=True)

uunique_uuids_in_logproblem = df_LogProblem['uuid'].unique()
df_InfoUser_filtered = df_InfoUser[df_InfoUser['uuid'].isin(uunique_uuids_in_logproblem)]
st.write(f"---> The shape of df_InfoUser_filtered is: {df_InfoUser_filtered.shape}")

unique_ucids_in_logproblem = df_LogProblem['ucid'].unique()
df_InfoContent_filtered = df_InfoContent[df_InfoContent['ucid'].isin(unique_ucids_in_logproblem)]
st.write(f"---> The shape of df_InfoContent_filtered is: {df_InfoContent_filtered.shape}")



# In[15]:
markdown_style = """
    color: lightblue;
    font-size: 36px;
"""
st.markdown("<p style='{}'>1_Check for missing values:</p>".format(markdown_style), unsafe_allow_html=True)

missing_values_InfoUser = df_InfoUser.isnull().sum()
missing_values_LogProblem = df_LogProblem.isnull().sum()
missing_values_InfoContent = df_InfoContent.isnull().sum()


total_rows_InfoUser = len(df_InfoUser)
total_rows_LogProblem = len(df_LogProblem)
total_rows_InfoContent = len(df_InfoContent)

percentage_missing_InfoUser = (missing_values_InfoUser / total_rows_InfoUser) * 100
percentage_missing_LogProblem = (missing_values_LogProblem / total_rows_LogProblem) * 100
percentage_missing_InfoContent = (missing_values_InfoContent / total_rows_InfoContent) * 100

filtered_missing_InfoUser = percentage_missing_InfoUser[percentage_missing_InfoUser > 1]
filtered_missing_LogProblem = percentage_missing_LogProblem[percentage_missing_LogProblem > 1]
filtered_missing_InfoContent = percentage_missing_InfoContent[percentage_missing_InfoContent > 1]

fig_missing_values = plt.figure(figsize=(12, 6))
plt.bar(filtered_missing_InfoUser.index, filtered_missing_InfoUser, label='Info_UserData.csv', color='blue', alpha=0.6)
plt.bar(filtered_missing_LogProblem.index, filtered_missing_LogProblem, label='Log_Problem.csv', color='orange', alpha=0.6)
plt.bar(filtered_missing_InfoContent.index, filtered_missing_InfoContent, label='Info_Content.csv', color='green', alpha=0.6)
plt.xlabel('Columns')
plt.ylabel('Percentage of Missing Values')
plt.xticks(rotation=90)

plt.gca().yaxis.set_major_formatter(mtick.PercentFormatter())

for i, v in enumerate(filtered_missing_InfoUser):
    plt.text(i, v, f"{v:.2f}%", ha='center', va='bottom', color='blue', fontweight='bold')

for i, v in enumerate(filtered_missing_LogProblem):
    plt.text(i + len(filtered_missing_InfoUser), v, f"{v:.2f}%", ha='center', va='bottom', color='orange', fontweight='bold')

for i, v in enumerate(filtered_missing_InfoContent):
    plt.text(i + len(filtered_missing_InfoUser) + len(filtered_missing_LogProblem), v, f"{v:.2f}%", ha='center', va='bottom', color='green', fontweight='bold')

plt.legend()
plt.tight_layout()
st.pyplot(fig_missing_values)


st.markdown("INSIGHTS: Impact on Recommendation Systems->remove Data [is_downgrade, is_upgrade]")


# In[23]:


#InfoUser

users_with_zero_teachers_and_students = df_InfoUser[(df_InfoUser['has_teacher_cnt'] == 0) & (df_InfoUser['has_student_cnt'] == 0)]

not_self_coach = users_with_zero_teachers_and_students[(users_with_zero_teachers_and_students['is_self_coach'] == False)]

num_not_self_coach = len(not_self_coach)

st.write("## Users with 0 students, 0 teachers, and not self-coach:", num_not_self_coach)

total_users = len(df_InfoUser)

num_not_self_coach = len(not_self_coach)

percentage_not_self_coach = (num_not_self_coach / total_users) * 100

percentage_other_users = 100 - percentage_not_self_coach

labels = ['0 students, 0 teachers, and not self-coach', 'Other users']
values = [percentage_not_self_coach, percentage_other_users]
layout = go.Layout(title="Percentage of Users with 0 students, 0 teachers, and not self-coach")

fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=0.3)], layout=layout)

st.plotly_chart(fig)

st.markdown("INSIGHTS:")
st.markdown("Users with grade or point > 0 are to be considered as Students or Self-Coach")
st.markdown("Propositions:")
st.markdown("1-Regression imputation")
st.markdown("2-Mean imputation")

# In[18]:

st.markdown("<p style='{}'> 2_Check for outliers:</p>".format(markdown_style), unsafe_allow_html=True)

#LogProblem
df_zero_sec_taken = df_LogProblem[df_LogProblem['total_sec_taken'] == 0]

num_users_with_zero_sec_taken = df_zero_sec_taken['uuid'].nunique()

st.write("## Number of users with 0 seconds taken:", num_users_with_zero_sec_taken)


import streamlit as st

# Write the insights as markdown text
st.write("INSIGHTS:")

st.write("Users with 0 'total_sec_taken':")
st.write("Users with a total_sec_taken of 0 likely indicate instances where the users did not spend any time attempting the problem. Insights from these cases might include:")
st.write("- Users who accessed the problem but did not engage in any interaction, possibly indicating a lack of interest or motivation.")
st.write("- Users who navigated to the problem but left the platform or session before attempting it.")
st.write("Possible actions or improvements could include:")
st.write("- Identifying potential usability issues or design flaws in the platform that might discourage users from attempting or interacting with problems.")
st.write("- Providing additional guidance or incentives to encourage users to actively attempt more problems and engage in learning activities.")

st.markdown("<p style='{}'> 3_The distribution of students across different learning stages :</p>".format(markdown_style), unsafe_allow_html=True)

#st.write("## The distribution of students across different learning stages:")

# In[24]:


learning_stages_count = df_InfoContent['learning_stage'].value_counts()
total_students = len(df_InfoContent)

percentage_per_stage = (learning_stages_count / total_students) * 100

fig = go.Figure(data=[go.Bar(x=learning_stages_count.index, y=learning_stages_count.values)])

for i in range(len(learning_stages_count)):
    value_count = learning_stages_count.values[i]
    percentage = percentage_per_stage.values[i]
    text = f"{value_count} ({percentage:.2f}%)"
    fig.add_annotation(
        x=learning_stages_count.index[i],
        y=learning_stages_count.values[i],
        text=text,
        showarrow=True,
        arrowhead=1
    )

fig.update_layout(
    title='Distribution of Students Across Learning Stages',
    xaxis_title='Learning Stage',
    yaxis_title='Number of Students',
    showlegend=False
)

st.plotly_chart(fig)


# In[25]:



image_path = '/home/dorra/Pictures/3.png'
image = open(image_path, 'rb').read()

st.image(image, caption='Diffrent Learning Stages Levels')
st.write("--> The data suggests that the majority of students who attended Junyi Academy Online Learning are in the younger age group, between 6 and 15 years old, comprising about 99% of the total student population")

st.markdown("<p style='{}'> 4_The Distribution of Difficulties of Exercises : </p>".format(markdown_style), unsafe_allow_html=True)

# In[26]:


import plotly.graph_objects as go

difficulty_distribution = df_InfoContent['difficulty'].value_counts()

colors = ['blue', 'green', 'orange', 'red']

fig = go.Figure(data=[go.Pie(labels=difficulty_distribution.index, values=difficulty_distribution.values, marker=dict(colors=colors))])

fig.update_layout(title='Distribution of Difficulties of Exercises')

st.plotly_chart(fig)


# # The number of students who have attempted to answer the problems in the exercises:

# In[28]:


unique_students_attempted = df_LogProblem['uuid'].nunique()
st.write("The number of students who have attempted to answer the problems in the exercises:",unique_students_attempted)


# #  The average number of problems in a single exercise:

# In[30]:


exercise_problem_counts = df_LogProblem.groupby('ucid')['problem_number'].nunique()

average_problems_per_exercise = int(exercise_problem_counts.mean())
st.markdown("## Summary of Exercise Data")

st.write("Average number of problems in a single exercise:", average_problems_per_exercise)

st.write("-Total Number of Exercises:", len(df_InfoContent['ucid']))
st.write("-Total Number of Problem attempts:", len(df_LogProblem['ucid']))
st.write("-Total Number of Exercise attempts:", df_LogProblem['ucid'].nunique())


# #  The average number of hints used per student per exercise:

# In[36]:


average_hints_per_student_per_exercise = int(df_LogProblem.groupby(['uuid', 'ucid'])['used_hint_cnt'].size().mean())

st.write("Average number of hints used per student per exercise:", average_hints_per_student_per_exercise)


# #  The average number of attempts per student per exercise:

# In[38]:


average_attempts_per_student = int(df_LogProblem.groupby(['uuid', 'ucid'])['total_attempt_cnt'].size().mean())
st.write("Average number of attempts per student per exercise: ",average_attempts_per_student)

