#!/usr/bin/env python
# coding: utf-8

# In[2]:


import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.ticker as mtick
import plotly.graph_objects as go
import dask.dataframe as dd
#from ydata_profiling import ProfileReport
#%matplotlib inline
#/home/dorra/.local/bin/streamlit run main.py


# In[4]:


df_InfoUser  = dd.read_csv(r'/media/dorra/62207C0F207BE885/Users/ASUS/Desktop/archive/Info_UserData.csv')
df_LogProblem = dd.read_csv(r'/media/dorra/62207C0F207BE885/Users/ASUS/Desktop/archive/Log_Problem.csv')
df_InfoContent = dd.read_csv(r'/media/dorra/62207C0F207BE885/Users/ASUS/Desktop/archive/Info_Content.csv')


# In[21]:


shape_df_LogProblem = df_LogProblem.shape
num_rows_df_LogProblem = shape_df_LogProblem[0].compute()
num_columns_df_LogProblem = shape_df_LogProblem[1]

shape_df_InfoUser= df_InfoUser.shape
num_rows_df_InfoUser = shape_df_InfoUser[0].compute()
num_columns_df_InfoUser = shape_df_InfoUser[1]

shape_df_InfoContent= df_InfoContent.shape
num_rows_df_InfoContent = shape_df_InfoContent[0].compute()
num_columns_df_InfoContent = shape_df_InfoContent[1]

print(f"the shape of df_InfoUser is: {num_rows_df_InfoUser}, {num_columns_df_InfoUser}")
print(f"the shape of df_LogProblem is: ({num_rows_df_LogProblem}, {num_columns_df_LogProblem})")
print(f"the shape of df_InfoContent is: {num_rows_df_InfoContent}, {num_columns_df_InfoContent}")


# # Data Cleaning

# ## 1_Check for missing values:

# In[15]:


missing_values_InfoUser = df_InfoUser.isnull().sum()
missing_values_LogProblem = df_LogProblem.isnull().sum()
missing_values_InfoContent = df_InfoContent.isnull().sum()


total_rows_InfoUser = len(df_InfoUser)
total_rows_LogProblem = len(df_LogProblem)
total_rows_InfoContent = len(df_InfoContent)

# Calculate the percentage of missing values for each column
percentage_missing_InfoUser = (missing_values_InfoUser / total_rows_InfoUser) * 100
percentage_missing_LogProblem = (missing_values_LogProblem / total_rows_LogProblem) * 100
percentage_missing_InfoContent = (missing_values_InfoContent / total_rows_InfoContent) * 100

# Filter columns with missing values percentage greater than 1%
filtered_missing_InfoUser = percentage_missing_InfoUser[percentage_missing_InfoUser > 1]
filtered_missing_LogProblem = percentage_missing_LogProblem[percentage_missing_LogProblem > 1]
filtered_missing_InfoContent = percentage_missing_InfoContent[percentage_missing_InfoContent > 1]

plt.figure(figsize=(12, 6))
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
plt.show()


# INSIGHTS:
# Impact on Recommendation Systems->remove Data?

# ## 2_Check for outliers:

# In[6]:


#InfoUser

users_with_zero_teachers_and_students = df_InfoUser[(df_InfoUser['has_teacher_cnt'] == 0) & (df_InfoUser['has_student_cnt'] == 0)]

not_self_coach =  users_with_zero_teachers_and_students[(users_with_zero_teachers_and_students['is_self_coach']== False)]

num_not_self_coach = len(not_self_coach)

print("has 0 students, 0 teachers and not self coach:",num_not_self_coach)


# In[7]:


outlier_columns = ['total_sec_taken', 'total_attempt_cnt', 'used_hint_cnt']

grouped_log_problem = df_LogProblem.groupby('uuid')

unique_uuids = df_InfoUser['uuid'].unique().compute()

plt.figure(figsize=(12, 6))

for i, col in enumerate(outlier_columns, 1):
    plt.subplot(1, 3, i)
    for uuid in unique_uuids:
        group = grouped_log_problem.get_group(uuid)
        sns.stripplot(x=[uuid] * len(group), y=col, data=group, jitter=True, color='green', alpha=0.7)
    plt.xlabel('uuid')
    plt.ylabel(col)
    plt.title(f'Strip Plot - {col}')
    plt.tight_layout()

plt.show()


# INSIGHTS:
# 
# 1_Users with 0 'total_sec_taken': Users with a total_sec_taken of 0 likely indicate instances where the users did not spend any time attempting the problem. Insights from these cases might include:
# 
#    .Users who accessed the problem but did not engage in any interaction, possibly indicating a lack of interest or motivation.
#    .Users who navigated to the problem but left the platform or session before attempting it.
# 2_Users with 0 'total_attempt_cnt': Users with a total_attempt_cnt of 0 likely indicate cases where the users did not make any attempts to solve the problem. Insights from these cases could include:
# 
#    .Users who accessed the problem but did not actively interact or attempt to solve it.
#    .Users who might have skipped or ignored the problem intentionally.
# 
# Possible actions or improvements could include:
# 
#   Identifying potential usability issues or design flaws in the platform that might discourage users from attempting or interacting with problems.
# 
#   Providing additional guidance or incentives to encourage users to actively attempt more problems and engage in learning activities.

# In[8]:


zero_sec_taken = df_LogProblem[df_LogProblem['total_sec_taken'] == 0]
zero_attempt_cnt = df_LogProblem[df_LogProblem['total_attempt_cnt'] == 0]

zero_sec_taken_hint_count = zero_sec_taken['used_hint_cnt'].value_counts()
zero_attempt_cnt_hint_count = zero_attempt_cnt['used_hint_cnt'].value_counts()

plt.figure(figsize=(10, 6))

plt.subplot(1, 2, 1)
plt.bar(zero_sec_taken_hint_count.index, zero_sec_taken_hint_count.values)
plt.xlabel('Number of Used Hints')
plt.ylabel('Number of Users')
plt.title('Number of Users with 0 Seconds Taken')

plt.subplot(1, 2, 2)
plt.bar(zero_attempt_cnt_hint_count.index, zero_attempt_cnt_hint_count.values)
plt.xlabel('Number of Used Hints')
plt.ylabel('Number of Users')
plt.title('Number of Users with 0 Attempt Count')

plt.tight_layout()
plt.show()


# # The distribution of students across different learning stages:

# In[121]:


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

fig.show()


# In[38]:


from IPython.display import Image

image_path = '/home/dorra/Pictures/3.png'

Image(filename=image_path)


# # The distribution of difficulties of the exercises:

# In[76]:


import plotly.graph_objects as go

difficulty_distribution = df_InfoContent['difficulty'].value_counts()

colors = ['blue', 'green', 'orange', 'red']

fig = go.Figure(data=[go.Pie(labels=difficulty_distribution.index, values=difficulty_distribution.values, marker=dict(colors=colors))])

fig.update_layout(title='Distribution of Difficulties of Exercises')

fig.show()


# # The number of students who have attempted to answer the problems in the exercises:

# In[20]:


unique_students_attempted = df_LogProblem['uuid'].nunique().compute()
print(unique_students_attempted)


# #  The average number of problems in a single exercise:

# In[24]:


exercise_problem_counts = df_LogProblem.groupby('ucid')['problem_number'].nunique().compute()

average_problems_per_exercise = exercise_problem_counts.mean()

print("Average number of problems in a single exercise:", average_problems_per_exercise)

print("Total Number of Exercises:", len(df_InfoContent['ucid']))
print("Total Number of Problem attempts:", len(df_LogProblem['ucid']))
print("Total Number of Exercise attempts:", df_LogProblem['ucid'].nunique().compute())


# #  The average number of hints used per student per exercise:

# In[26]:


average_hints_per_student_per_exercise = df_LogProblem.groupby(['uuid', 'ucid', 'upid'])['used_hint_cnt'].mean().mean().compute()

print("Average number of hints used per student per exercise:", average_hints_per_student_per_exercise)


# #  The average number of attempts per student per exercise:

# In[35]:


average_attempts_per_student = int(df_LogProblem.groupby(['uuid', 'ucid'])['total_attempt_cnt'].size().mean())
print(average_attempts_per_student)

