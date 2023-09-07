import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.ticker as mtick
import plotly.express as px
import plotly.graph_objects as go
import dask.dataframe as dd
from PIL import Image


st.set_page_config(page_title="Junyi Academy", page_icon="📊", layout="wide")


style = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Prompt&family=Montserrat:wght@300&display=swap');

.header {
    font-family: 'Prompt', cursive;
    font-size: 48px;
    color: #0077B5;
}
.subheader {
    font-family: 'Prompt', cursive;
    font-size: 24px;
    color: #0077B5;
    text-align: center;
}
.callout-box {
    background-color: #FFA500;
    color: #00008B;
    padding: 10px;
    border-radius: 10px;
}
.callout-box.note {
    background-color: #a3cbf5;
    color: #000000;
    padding: 10px;
    border-radius: 10px;
}
"""

st.markdown(style, unsafe_allow_html=True)

selected_option = st.sidebar.radio("( Data Exploratory on 5000 Users )", ("Data Aberration", "Data Inquiry"))

sub_option_a = None

# Main Content
image_path = '/home/dorra/Downloads/13.png'
photo = Image.open(image_path)

col1, col2 = st.columns((0.1,0.2))

with col2:
    st.markdown('<div class="header">Data Exploratory</div>', unsafe_allow_html=True)

with col1:
    st.image(photo, width=200)

st.write("---")


# Load data
df_InfoUser = pd.read_csv(r'/home/dorra/InfoUserP.csv')
df_LogProblem = pd.read_csv(r'/home/dorra/LogProblemP.csv')
df_InfoContent = pd.read_csv(r'/home/dorra/InfoContentP.csv')


student_grouped = df_LogProblem.groupby('uuid').agg({'is_correct': 'sum', 'total_attempt_cnt': 'sum'})

# Calculate AAA for each student and add it as a new column
student_grouped['AAA'] = student_grouped['is_correct'] / student_grouped['total_attempt_cnt']

student_grouped.reset_index(inplace=True)

df_LogProblem = df_LogProblem.merge(student_grouped[['uuid', 'AAA']], on='uuid', how='left')

#@st.cache_data

def main_content(selected_option, sub_option_a): 

 if selected_option == "Data Aberration":
    a,b = st.columns((0.1,0.1))
    ###

    #LogProblem
    a.markdown('<div class="subheader">Time Aberration</div>',unsafe_allow_html=True)

    df_zero_sec_taken = df_LogProblem[df_LogProblem['total_sec_taken'] == 0]
    #num_users_with_zero_sec_taken = df_zero_sec_taken['uuid'].nunique()
    a.markdown("")
    a.markdown("")
    a.markdown("")

    a.markdown("We Have Users with 0 Sec Taken For About : 1517" )

    a.subheader("Insights:")

    a.markdown("""
    Users with 0 'total_sec_taken are likely to indicate instances where the users did not spend any time attempting the problem. Insights from these cases might include:
   """)
    a.markdown("""
   .Users who accessed the problem but did not engage in any interaction, possibly indicating a lack of interest or motivation.
   """)
    a.markdown("""
   .Users who navigated to the problem but left the platform or session before attempting it.
   """)
    a.markdown("""
   ---> Possible actions or improvements could include:
   """)
    a.markdown("""
   1-Identifying potential usability issues or design flaws in the platform that might discourage users from attempting or interacting with problems.
   """)
    a.markdown("""
   2-Providing additional guidance or incentives to encourage users to actively attempt more problems and engage in learning activities.
   """)
    
    ###


    # Missing Values
    b.markdown('<div class="subheader">Gender and Student Progession Missing Values</div>', unsafe_allow_html=True)
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
    b.pyplot(fig)

    b.subheader("Insights:")
    b.write("Impact on Recommendation Systems -> Remove Data")
 
    
    
    ###

    
    st.markdown('<div class="subheader">Users Classification undeclared</div>',unsafe_allow_html=True)

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

    st.plotly_chart(fig,use_container_width=True)


 elif selected_option == "Data Inquiry":
   
   sub_option_a = st.sidebar.selectbox("Select an Option", ("Data Discovery", "Data Visualisation"))

    
   if sub_option_a == "Data Discovery":
     
     c,d = st.columns((0.1,0.06))

     c.markdown('<div class="subheader">The distribution of students across different learning stages</div>',unsafe_allow_html=True)
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
     c.plotly_chart(fig,use_container_width=True)

     image_path = '/home/dorra/Pictures/3.png'
     d.markdown('<div class="callout-box">Diffrent Learning Stages in Taiwan:</div>',unsafe_allow_html=True)
     image = Image.open(image_path)
     d.image(image)


     e,f = st.columns((0.1,0.06))
     # The distribution of difficulties of the exercises
     e.markdown('<div class="subheader">The distribution of difficulties of the exercises</div>',unsafe_allow_html=True)
     difficulty_distribution = df_InfoContent['difficulty'].value_counts()

     colors = ['blue', 'green', 'orange', 'red']

     fig = go.Figure(data=[go.Pie(labels=difficulty_distribution.index, values=difficulty_distribution.values, marker=dict(colors=colors))])

     fig.update_layout()

     e.plotly_chart(fig,use_container_width=True)


     ###


     # The average number of problems in a single exercise
     f.markdown("")
     f.markdown("")
     f.markdown("")
     f.markdown("")

     f.markdown('<div class="callout-box">Exercises Exploratory :</div>',unsafe_allow_html=True)
     exercise_problem_counts = df_LogProblem.groupby('ucid')['problem_number'].nunique()
     average_problems_per_exercise = int(exercise_problem_counts.mean())
     f.markdown("The average number of problems in a single exercise : 47")
     f.markdown("Total Number of Exercises: 1326", )
     f.markdown("Total Number of Problem attempts: 998040")
     f.markdown("Total Number of Exercise attempts: 1317")

     # The average number of hints used per student per exercise
     #average_hints_per_student_per_exercise = int(df_LogProblem.groupby(['uuid', 'ucid'])['used_hint_cnt'].size().mean())
     f.markdown("The average number of hints used per student per exercise: 9")

     # The average number of attempts per student per exercise
     #average_attempts_per_student = int(df_LogProblem.groupby(['uuid', 'ucid'])['total_attempt_cnt'].size().mean())
     f.markdown("The average number of attempts per student per exercise: 9")
    

     ###

     g,h = st.columns((0.1,0.1))
     g.markdown('<div class="subheader">Distribution of Answer Correctness Across All Exercises<div/>',unsafe_allow_html=True)
     correctness_counts = df_LogProblem['is_correct'].value_counts()

     fig = go.Figure(data=[go.Bar(x=correctness_counts.index, y=correctness_counts.values, marker=dict(color='orange'))])
     fig.update_layout(
                  xaxis_title='Is Correct',
                  yaxis_title='Count')

     g.plotly_chart(fig,use_container_width=True)

     g.markdown("68% of answers are correct --> Good performance")


     ###


     h.markdown('<div class="subheader">Distribution of Proficiency Levels Across All Exercises</div>',unsafe_allow_html=True)
     level_counts = df_LogProblem['level'].value_counts()

     fig = go.Figure(data=[go.Bar(x=level_counts.index, y=level_counts.values)])
     fig.update_layout(title='',
                  xaxis_title='Proficiency Level',
                  yaxis_title='Count')

     h.plotly_chart(fig,use_container_width=True)

     h.markdown("76% of exercises are at 0 level proficiency.")


     ###


     st.markdown('<div class="subheader">Points Distribution by User Grade</div>',unsafe_allow_html=True)
     energy_points_stats = df_InfoUser.groupby('user_grade')['points'].agg(['mean', 'max', 'min']).reset_index()

     fig = px.bar(energy_points_stats, x='user_grade', y=['mean', 'max', 'min'],
             labels={'user_grade': 'User Grade', 'value': 'Points'},
             color_discrete_map={'mean': 'red', 'max': 'orange', 'min': 'black'},
             opacity=0.7)

     fig.update_layout(xaxis_tickangle=-45)
     st.plotly_chart(fig)

     st.markdown("Grades between 4 and 7 are the most performant students (Elementary).")


     ###


     st.markdown('<div class="subheader">Time Distribution of Attempts on Exercises</div>',unsafe_allow_html=True)

     #df_LogProblem['timestamp_TW'] = pd.to_datetime(df_LogProblem['timestamp_TW'])
     #time_intervals = df_LogProblem.set_index('timestamp_TW').resample('D').size().reset_index()
     #time_intervals.columns = ['Date', 'Number of Attempts']

     #fig = px.line(time_intervals, x='Date', y='Number of Attempts',
              #labels={'Date': 'Date', 'Number of Attempts': 'Number of Attempts'},
              #markers=True)

     #st.plotly_chart(fig)
     st.markdown("")
     st.markdown("")
     st.markdown("")

     image_Time_path = '/home/dorra/Downloads/14.png'
     imageTime = Image.open(image_Time_path)
     st.image(imageTime)
     
     st.markdown("The bulk of user activity is concentrated in the second semester of the school year, spanning from late February to June.")
 
   elif sub_option_a == "Data Visualisation" :
         
         g,h = st.columns((0.1,0.1))
         df_LogProblem['hint_used'] = df_LogProblem['used_hint_cnt'] > 0
         hint_users = df_LogProblem[df_LogProblem['hint_used'] == True]
         no_hint_users = df_LogProblem[df_LogProblem['hint_used'] == False]

         total_users = df_LogProblem['uuid'].nunique()

         hint_correct_count = hint_users['is_correct'].sum()
         no_hint_correct_count = no_hint_users['is_correct'].sum()
   
         hint_avg_time_taken = hint_users['total_sec_taken'].mean()
         no_hint_avg_time_taken = no_hint_users['total_sec_taken'].mean()

         g.markdown('<div class="subheader">Effect of Using Hints on Correct Answers<div/>',unsafe_allow_html=True)

         fig1 = go.Figure(data=[go.Bar(x=['With Hint', 'Without Hint'], y=[hint_correct_count, no_hint_correct_count])])
         fig1.update_layout(
                   xaxis_title='Hint Usage',
                   yaxis_title='Correct Answers')
         

         fig2 = go.Figure(data=[go.Bar(x=['With Hint', 'Without Hint'], y=[hint_avg_time_taken, no_hint_avg_time_taken])])
         fig2.update_layout(title='',
                   xaxis_title='Hint Usage',
                   yaxis_title='Average Time Taken (seconds)')

         g.plotly_chart(fig1,use_container_width=True)
         h.markdown('<div class="subheader">Effect of Using Hints on Average Time Taken<div/>',unsafe_allow_html=True)
         h.plotly_chart(fig2,use_container_width=True)
         st.write("The provision of hints did not yield improvements in student performance as evidenced by their unaltered accuracy and problem-solving speed. It also shows that the hints might not be as helpful as intended")


         ###


         df_merged = df_LogProblem.merge(df_InfoContent[['ucid', 'difficulty']], on='ucid', how='left')

         grouped = df_merged.groupby(['difficulty', 'level']).size().reset_index(name='count')

         st.markdown('<div class="subheader">Levels Attended by Users for Each Category of Exercises<div/>',unsafe_allow_html=True)
         fig = px.bar(grouped, x='difficulty', y='count', color='level',
             labels={'difficulty': 'Difficulty', 'count': 'Number of Exercises'},
             category_orders={'level': ['0', '1', '2', '3', '4']},
             barmode='stack')

         st.plotly_chart(fig)

         
         ###

         
         st.markdown('<div class="subheader">Users Proficiency, Exercises Proficiency<div/>',unsafe_allow_html=True)
         st.markdown("")
         st.markdown("")
         st.markdown("")

         image_Time_path = '/home/dorra/Downloads/15.png'
         imageTime = Image.open(image_Time_path)
         st.image(imageTime)

         #max_levels = df_LogProblem.groupby('uuid')['level'].max()
         #exercise_counts = df_LogProblem.groupby(['uuid', 'level'])['ucid'].nunique()
         #level_counts = max_levels.value_counts().sort_index()

         # number of users with maximum level
         #fig, axes = plt.subplots(1, 2, figsize=(12, 6))

         #bars1 = axes[0].bar(level_counts.index, level_counts.values, color='purple')  # Change bar color to purple
         #axes[0].set_xlabel('Maximum Level')
         #axes[0].set_ylabel('Number of Users')
         #axes[0].set_title('Number of Users with Maximum Level')
         #axes[0].set_xticks(range(5)) 

         #for bar in bars1:
             #yval = bar.get_height()
             #axes[0].text(bar.get_x() + bar.get_width()/2, yval + 30, round(yval), ha='center', color='black', fontsize=10)

         # number of exercises attended at maximum level
         #bars2 = axes[1].bar(exercise_counts.index.get_level_values('level'), exercise_counts.values, color='green')
         #axes[1].set_xlabel('Maximum Level')
         #axes[1].set_ylabel('Number of Exercises Attended')
         #axes[1].set_title('Number of Exercises Attended at Maximum Level')
         #axes[1].set_xticks(range(5))  
       
         #plt.tight_layout()
         #st.pyplot(fig)


         ###

         
         i,j = st.columns((0.1,0.06))
         i.markdown('<div class="subheader">Correlation Between Number of Attempts and Overall Performance<div/>',unsafe_allow_html=True)

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

         i.plotly_chart(fig,use_container_width=True) 

         j.markdown("")
         j.markdown("")
         j.markdown("")
         j.markdown("")
         j.markdown("")
         j.markdown("")
         j.markdown('<div class="callout-box">A correlation of -0.33 suggests a weak negative correlation between the number of attempts made by a student and their overall performance. This means that, on average, as the number of attempts increases, the overall performance tends to slightly decrease.</div>',unsafe_allow_html=True)
      

         ###

         
         st.markdown("Average Absolute Accuracy :")
         num_correct_attempts = df_LogProblem['is_correct'].sum()
         total_attempts = len(df_LogProblem)
         AAA = num_correct_attempts / total_attempts

         st.write("AAA :", AAA)
         #student_grouped = df_LogProblem.groupby('uuid').agg({'is_correct': 'sum', 'total_attempt_cnt': 'sum'})
         #student_grouped['AAA'] = student_grouped['is_correct'] / student_grouped['total_attempt_cnt']
         #df_LogProblem = df_LogProblem.merge(student_grouped[['uuid', 'AAA']], on='uuid', how='left')

         #student_grouped.reset_index(inplace=True)

         #st.markdown('AAA Analysis for Each Student')
  
         #fig = px.line(student_grouped, x='uuid', y='AAA', labels={'uuid': 'Student Identifier (UUID)', 'AAA': 'Average Absolute Accuracy (AAA)'})
         #fig.update_xaxes(tickangle=-45)  # Rotate x-axis labels for better readability

         #st.plotly_chart(fig)
     
         ###
         o,p = st.columns((0.1,0.1))

         o.markdown('<div class="subheader">Proficiency Level Distribution<div/>',unsafe_allow_html=True)
         df_merged = df_LogProblem.merge(df_InfoContent[['ucid', 'difficulty']], on='ucid', how='left')

         user_proficiency = df_merged.groupby('uuid')['difficulty'].max().reset_index()

         proficiency_counts = user_proficiency['difficulty'].value_counts()

         fig = px.bar(x=proficiency_counts.index, y=proficiency_counts.values,
             labels={'x': 'Proficiency Level', 'y': 'Number of Users'}
             )

         o.plotly_chart(fig,use_container_width=True)

         ###


         p.markdown('<div class="subheader">Distribution of Number of Interactions<div/>',unsafe_allow_html=True)
         interaction_count = df_LogProblem['uuid'].value_counts().reset_index()
         interaction_count.columns = ['uuid', 'interaction_count']

         fig = px.histogram(interaction_count, x='interaction_count', nbins=20,
                   labels={'interaction_count': 'Number of Interactions'}
                   )

         p.plotly_chart(fig,use_container_width=True)

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
             height=600)

         st.markdown('<div class="subheader">Users Proficiency Level vs Number of Level 4 Encounters<div/>',unsafe_allow_html=True)
         st.plotly_chart(fig)

         st.markdown('<div class="subheader">Features that affect students performance<div/>',unsafe_allow_html=True)
         #st.markdown("1-Grade. (Elemntary students are the most performant)")
         #st.markdown("2-Has Teacher. (Having teachers help improve performance)")
         #st.markdown("3-Hint Usage. (Self reliance leads to better solving the problems)")
         col1, col2, col3, col4, col5 = st.columns((0.1,0.1,0.1,0.1,0.1))
         col1.metric("1","Grade")
         col2.metric("2","Has Teacher")
         col3.metric("3","Hint Usage")
         col4.metric("4","AAA")
         col5.metric("4","Total Sec Taken")



main_content(selected_option, sub_option_a)




