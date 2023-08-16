import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.ticker as mtick
import plotly.express as px
import plotly.graph_objects as go
import dask.dataframe as dd
from PIL import Image




def set_styles():
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Open+Sans&display=swap');
        .title-text {
            color: #FF5733;
            font-family: 'Open Sans', sans-serif;
            font-size: 36px;
            font-weight: bold;
            margin-bottom: 1rem;
        }
        .subheader-text {
            color: #3399FF;
            font-family: 'Open Sans', sans-serif;
            font-size: 24px;
            margin-bottom: 0.5rem;
        }
        .emoji {
            font-size: 24px;
            margin-right: 0.5rem;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

set_styles()

# Sidebar Widgets
st.sidebar.header("Select An Option")
selected_option = st.sidebar.radio("( Data Exploratory on 5000 Users )", ("Data Aberration", "Data Inquiry"))

# Initialize sub_option_a
sub_option_a = None

# Main Content
image_path = '/home/dorra/Downloads/1.png'
photo = Image.open(image_path)
st.image(photo, use_column_width=True)

# Display the selected option and the image in the middle
col1, col2, col3 = st.columns([1, 3, 1])  # Create columns to center content

# Display the "Data Exploratory" title in blue color in the middle
data_exploratory_title = """
<div style="text-align: center; font-family: 'Tangerine', serif; font-size: 48px;">
     Data Exploratory
</div>
"""

tangerine_title_style = """
<style>
    .tangerine-title {
        font-family: 'Tangerine', serif;
        font-size: 36px;
    }
</style>
"""

st.markdown(data_exploratory_title, unsafe_allow_html=True)

# Load data
df_InfoUser = pd.read_csv(r'/home/dorra/InfoUserP.csv')
df_LogProblem = pd.read_csv(r'/home/dorra/LogProblemP.csv')
df_InfoContent = pd.read_csv(r'/home/dorra/InfoContentP.csv')

def main_content(selected_option, sub_option_a): 

 if selected_option == "Data Aberration":

    # Missing Values
    st.subheader("1. Gender and Student Progession Missing Values :")
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

    fig, ax = plt.subplots(figsize=(12, 6))
    ax.bar(filtered_missing_InfoUser.index, filtered_missing_InfoUser, label='Info_UserData.csv', color='blue', alpha=0.6)
    ax.bar(filtered_missing_LogProblem.index, filtered_missing_LogProblem, label='Log_Problem.csv', color='orange', alpha=0.6)
    ax.bar(filtered_missing_InfoContent.index, filtered_missing_InfoContent, label='Info_Content.csv', color='green', alpha=0.6)
    plt.xlabel('Columns')
    plt.ylabel('Percentage of Missing Values')
    plt.xticks(rotation=90)

    ax.yaxis.set_major_formatter(mtick.PercentFormatter())

    for i, v in enumerate(filtered_missing_InfoUser):
       ax.text(i, v, f"{v:.2f}%", ha='center', va='bottom', color='blue', fontweight='bold')

    for i, v in enumerate(filtered_missing_LogProblem):
       ax.text(i + len(filtered_missing_InfoUser), v, f"{v:.2f}%", ha='center', va='bottom', color='orange', fontweight='bold')

    for i, v in enumerate(filtered_missing_InfoContent):
       ax.text(i + len(filtered_missing_InfoUser) + len(filtered_missing_LogProblem), v, f"{v:.2f}%", ha='center', va='bottom', color='green', fontweight='bold')

    plt.legend()
    st.pyplot(fig)

    st.subheader("Insights:")
    st.write("Impact on Recommendation Systems -> Remove Data")
 
    ###

    st.subheader("2. Users Classification undeclared :")

    users_with_zero_teachers_and_students = df_InfoUser[(df_InfoUser['has_teacher_cnt'] == 0) & (df_InfoUser['has_student_cnt'] == 0)]
    not_self_coach =  users_with_zero_teachers_and_students[(users_with_zero_teachers_and_students['is_self_coach'] == False)]

    num_not_self_coach = len(not_self_coach)
    total_users = len(df_InfoUser)

    percentage_not_self_coach = (num_not_self_coach / total_users) * 100
    percentage_other_users = 100 - percentage_not_self_coach

    labels = ['0 students, 0 teachers, and not self-coach', 'Other users']
    values = [percentage_not_self_coach, percentage_other_users]

    layout = go.Layout(title="Percentage of Users with 0 students, 0 teachers, and not self-coach")
    fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=0.3)], layout=layout)

    st.plotly_chart(fig)



    #LogProblem
    st.subheader("3. Time Aberration :")

    df_zero_sec_taken = df_LogProblem[df_LogProblem['total_sec_taken'] == 0]
    num_users_with_zero_sec_taken = df_zero_sec_taken['uuid'].nunique()

    st.write("We Have Users with 0 Sec Taken For About : " ,num_users_with_zero_sec_taken)

    st.subheader("Insights:")

    st.write("""
    Users with 0 'total_sec_taken are likely to indicate instances where the users did not spend any time attempting the problem. Insights from these cases might include:
   """)
    st.write("""
   .Users who accessed the problem but did not engage in any interaction, possibly indicating a lack of interest or motivation.
   """)
    st.write("""
   .Users who navigated to the problem but left the platform or session before attempting it.
   """)
    st.write("""
   ---> Possible actions or improvements could include:
   """)
    st.write("""
   1-Identifying potential usability issues or design flaws in the platform that might discourage users from attempting or interacting with problems.
   """)
    st.write("""
   2-Providing additional guidance or incentives to encourage users to actively attempt more problems and engage in learning activities.
   """)

 elif selected_option == "Data Inquiry":
   
   sub_option_a = st.sidebar.selectbox("Sub Option", ("Data Discovery", "Data Visualisation"))

    
   if sub_option_a == "Data Discovery":
 
     # The distribution of students across different learning stages
     st.subheader("1. The distribution of students across different learning stages :")
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
      xaxis_title='Learning Stage',
      yaxis_title='Number of Students',
      showlegend=False
     )
     st.plotly_chart(fig)

     image_path = '/home/dorra/Pictures/3.png'
     st.subheader("Diffrent Learning Stages in Taiwan:")
     image = Image.open(image_path)
     st.image(image)



     # The distribution of difficulties of the exercises
     st.subheader("2. The distribution of difficulties of the exercises :")
     difficulty_distribution = df_InfoContent['difficulty'].value_counts()

     colors = ['blue', 'green', 'orange', 'red']

     fig = go.Figure(data=[go.Pie(labels=difficulty_distribution.index, values=difficulty_distribution.values, marker=dict(colors=colors))])

     fig.update_layout()

     st.plotly_chart(fig)


     ###


     # The average number of problems in a single exercise
     st.subheader("3. Exercises Exploratory :")
     exercise_problem_counts = df_LogProblem.groupby('ucid')['problem_number'].nunique()
     average_problems_per_exercise = int(exercise_problem_counts.mean())
     st.write("The average number of problems in a single exercise :",average_problems_per_exercise)
     st.write("Total Number of Exercises: ", len(df_InfoContent['ucid']))
     st.write("Total Number of Problem attempts: ", len(df_LogProblem['ucid']))
     st.write("Total Number of Exercise attempts: ", df_LogProblem['ucid'].nunique())

     # The average number of hints used per student per exercise
     average_hints_per_student_per_exercise = int(df_LogProblem.groupby(['uuid', 'ucid'])['used_hint_cnt'].size().mean())
     st.write("The average number of hints used per student per exercise: ",average_hints_per_student_per_exercise)

     # The average number of attempts per student per exercise
     average_attempts_per_student = int(df_LogProblem.groupby(['uuid', 'ucid'])['total_attempt_cnt'].size().mean())
     st.write("The average number of attempts per student per exercise: ",average_attempts_per_student)
    

     ###


     st.subheader("4. Distribution of Answer Correctness Across All Exercises :")
     correctness_counts = df_LogProblem['is_correct'].value_counts()

     fig = go.Figure(data=[go.Bar(x=correctness_counts.index, y=correctness_counts.values, marker=dict(color='orange'))])
     fig.update_layout(
                  xaxis_title='Is Correct',
                  yaxis_title='Count')

     st.plotly_chart(fig)

     st.write("68% of answers are correct --> Good performance")


     ###


     st.subheader("5. Distribution of Proficiency Levels Across All Exercises :")
     level_counts = df_LogProblem['level'].value_counts()

     fig = go.Figure(data=[go.Bar(x=level_counts.index, y=level_counts.values)])
     fig.update_layout(title='',
                  xaxis_title='Proficiency Level',
                  yaxis_title='Count')

     st.plotly_chart(fig)

     st.write("76% of exercises are at 0 level proficiency.")


     ###


     st.subheader("6. Points Distribution by User Grade :")
     energy_points_stats = df_InfoUser.groupby('user_grade')['points'].agg(['mean', 'max', 'min']).reset_index()

     fig = px.bar(energy_points_stats, x='user_grade', y=['mean', 'max', 'min'],
             labels={'user_grade': 'User Grade', 'value': 'Points'},
             color_discrete_map={'mean': 'red', 'max': 'orange', 'min': 'black'},
             opacity=0.7)

     fig.update_layout(xaxis_tickangle=-45)
     st.plotly_chart(fig)

     st.write("Grades between 4 and 7 are the most performant students (Elementary).")


     ###


     st.subheader("7. Time Distribution of Attempts on Exercises :")

     df_LogProblem['timestamp_TW'] = pd.to_datetime(df_LogProblem['timestamp_TW'])
     time_intervals = df_LogProblem.set_index('timestamp_TW').resample('D').size().reset_index()
     time_intervals.columns = ['Date', 'Number of Attempts']

     fig = px.line(time_intervals, x='Date', y='Number of Attempts',
              labels={'Date': 'Date', 'Number of Attempts': 'Number of Attempts'},
              markers=True)

     st.plotly_chart(fig)
     
     st.write("The bulk of user activity is concentrated in the second semester of the school year, spanning from late February to June.")
 
   elif sub_option_a == "Data Visualisation" :
         
         df_LogProblem['hint_used'] = df_LogProblem['used_hint_cnt'] > 0
         hint_users = df_LogProblem[df_LogProblem['hint_used'] == True]
         no_hint_users = df_LogProblem[df_LogProblem['hint_used'] == False]

         total_users = df_LogProblem['uuid'].nunique()

         hint_correct_count = hint_users['is_correct'].sum()
         no_hint_correct_count = no_hint_users['is_correct'].sum()
   
         hint_avg_time_taken = hint_users['total_sec_taken'].mean()
         no_hint_avg_time_taken = no_hint_users['total_sec_taken'].mean()

         st.subheader("1. Effect of Using Hints on Correct Answers :")

         fig1 = go.Figure(data=[go.Bar(x=['With Hint', 'Without Hint'], y=[hint_correct_count, no_hint_correct_count])])
         fig1.update_layout(
                   xaxis_title='Hint Usage',
                   yaxis_title='Correct Answers')
         

         fig2 = go.Figure(data=[go.Bar(x=['With Hint', 'Without Hint'], y=[hint_avg_time_taken, no_hint_avg_time_taken])])
         fig2.update_layout(title='',
                   xaxis_title='Hint Usage',
                   yaxis_title='Average Time Taken (seconds)')

         st.plotly_chart(fig1)
         st.subheader("2. Effect of Using Hints on Average Time Taken :")
         st.plotly_chart(fig2)
         st.write("The provision of hints did not yield improvements in student performance as evidenced by their unaltered accuracy and problem-solving speed. It also shows that the hints might not be as helpful as intended")


         ###


         df_merged = df_LogProblem.merge(df_InfoContent[['ucid', 'difficulty']], on='ucid', how='left')

         grouped = df_merged.groupby(['difficulty', 'level']).size().reset_index(name='count')

         st.subheader("3. Levels Attended by Users for Each Category of Exercises :")
         fig = px.bar(grouped, x='difficulty', y='count', color='level',
             labels={'difficulty': 'Difficulty', 'count': 'Number of Exercises'},
             category_orders={'level': ['0', '1', '2', '3', '4']},
             barmode='stack')

         st.plotly_chart(fig)

         
         ###

         
         st.subheader("4. User's Proficiency, Exercise's Proficiency:")

         max_levels = df_LogProblem.groupby('uuid')['level'].max()
         exercise_counts = df_LogProblem.groupby(['uuid', 'level'])['ucid'].nunique()
         level_counts = max_levels.value_counts().sort_index()

         # number of users with maximum level
         fig, axes = plt.subplots(1, 2, figsize=(12, 6))

         bars1 = axes[0].bar(level_counts.index, level_counts.values, color='purple')  # Change bar color to purple
         axes[0].set_xlabel('Maximum Level')
         axes[0].set_ylabel('Number of Users')
         axes[0].set_title('Number of Users with Maximum Level')
         axes[0].set_xticks(range(5)) 

         for bar in bars1:
             yval = bar.get_height()
             axes[0].text(bar.get_x() + bar.get_width()/2, yval + 30, round(yval), ha='center', color='black', fontsize=10)

         # number of exercises attended at maximum level
         bars2 = axes[1].bar(exercise_counts.index.get_level_values('level'), exercise_counts.values, color='green')
         axes[1].set_xlabel('Maximum Level')
         axes[1].set_ylabel('Number of Exercises Attended')
         axes[1].set_title('Number of Exercises Attended at Maximum Level')
         axes[1].set_xticks(range(5))  
       
         plt.tight_layout()
         st.pyplot(fig)


         ###


         st.subheader("5. Correlation Between Number of Attempts and Overall Performance:")

         df_LogProblem['correct_attempts'] = df_LogProblem['is_correct']
         df_LogProblem['total_attempts'] = df_LogProblem['total_attempt_cnt']
         df_LogProblem['overall_performance'] = (df_LogProblem['correct_attempts'] / df_LogProblem['total_attempts']) * 100

         correlation = df_LogProblem['total_attempts'].corr(df_LogProblem['overall_performance'])

         fig = px.scatter(df_LogProblem, x='total_attempts', y='overall_performance')
         fig.update_layout(
             xaxis_title="Number of Attempts",
             yaxis_title="Overall Performance (%)",
             title=f"Correlation: {correlation:.2f}"
         )       

         st.plotly_chart(fig) 

         st.write("""
              A correlation of -0.33 suggests a weak negative correlation between the number of attempts made by a student and their overall performance. This means that, on average, as the number of attempts increases, the overall performance tends to slightly decrease.
         """)

         ###


         st.subheader("6. Average Absolute Accuracy :")
         num_correct_attempts = df_LogProblem['is_correct'].sum()
         total_attempts = len(df_LogProblem)
         AAA = num_correct_attempts / total_attempts

         st.write("AAA :", AAA)
     
         ###

         st.subheader("7. Proficiency Level Distribution :")
         df_merged = df_LogProblem.merge(df_InfoContent[['ucid', 'difficulty']], on='ucid', how='left')

         user_proficiency = df_merged.groupby('uuid')['difficulty'].max().reset_index()

         proficiency_counts = user_proficiency['difficulty'].value_counts()

         fig = px.bar(x=proficiency_counts.index, y=proficiency_counts.values,
             labels={'x': 'Proficiency Level', 'y': 'Number of Users'}
             )

         st.plotly_chart(fig)

         ###

         st.subheader("8. Distribution of Number of Interactions :")
         interaction_count = df_LogProblem['uuid'].value_counts().reset_index()
         interaction_count.columns = ['uuid', 'interaction_count']

         fig = px.histogram(interaction_count, x='interaction_count', nbins=20,
                   labels={'interaction_count': 'Number of Interactions'}
                   )

         st.plotly_chart(fig)

         ###

         level_4_attempts = df_LogProblem[df_LogProblem['level'] == 4]
         user_level4_encounters = level_4_attempts['uuid'].value_counts().reset_index()
         user_level4_encounters.columns = ['uuid', 'level4_encounter_count']

         def determine_proficiency(encounter_count):
             if encounter_count == 0:
                 return 'Low'
             elif encounter_count < 5:
                 return 'Medium'
             else:
                 return 'High'

         user_level4_encounters['proficiency_level'] = user_level4_encounters['level4_encounter_count'].apply(determine_proficiency)
         user_profiles = user_level4_encounters.merge(df_InfoUser[['uuid', 'user_grade', 'has_teacher_cnt']], on='uuid', how='left')
 
         fig = px.bar(user_profiles, 
             x='proficiency_level', 
             y='level4_encounter_count', 
             color='has_teacher_cnt', 
             barmode='group',
             labels={
                 'proficiency_level': "Proficiency Level",
                 'level4_encounter_count': "Number of Level 4 Encounters",
                 'has_teacher_cnt': "Has Teacher Count"
             },
             title="User's Proficiency Level vs. Number of Level 4 Encounters",
             height=600)

         st.plotly_chart(fig)

         st.subheader("Feature that affect student;s performance:")
         st.write("1-Grade. (Elemntary students are the most performant)")
         st.write("2-Has Teacher. (Having teachers help improve performance)")
         st.write("3-Hint Usage. (Self reliance leads to better solving the problems)")




main_content(selected_option, sub_option_a)




