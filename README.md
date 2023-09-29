# streamlit_app
Junyi Academy Dataset general configuration
# Project Readme: "Utilizing Python for Educational Data Analysis and Dynamic Visualization through Streamlit"

## Overview

The project aims to harness the power of Python for in-depth analysis of educational data, providing actionable insights, and presenting the findings through an interactive Streamlit application. In the modern educational landscape, data-driven decision-making is pivotal for educators, administrators, and policymakers. This project serves as a comprehensive solution to address this need.
## Project Structure

The project is structured as follows:

- **Data Files**:
  - `Info_UserData.csv`: Contains information about users, including user IDs, demographics, and engagement metrics.
  - `Log_Problem.csv`: Records interactions between users and educational content, including timestamps, problem details, and user performance.
  - `Info_Content.csv`: Provides details about the educational content, such as content IDs, difficulty levels, and subjects.

- **Streamlit App**: The core of the project is a Streamlit web application (`app.py`) that  presents the insights in an interactive and user-friendly manner.

- **Analysis Scripts**: Python scripts (`data_analysis.py`) are used to load and analyze the data files and perform data preprocessing, feature engineering, and generate insights from the raw data.

- **Machine Learning Model**: The ML.py script includes the machine learning component, where a linear regression model is trained on the data to predict student outcomes.

- **Requirements**: A `requirements.txt` file lists the necessary Python libraries and dependencies to run the project.

## Running the Streamlit App

To run the Streamlit app, follow these steps:

1. Clone the project repository to your local machine.
2. Navigate to the project directory.
3. Install the required dependencies using `pip install -r requirements.txt`.
4. Run the Streamlit app with the command `streamlit run app.py`.
5. The app will open in your default web browser, allowing you to interact with the data and view the analyses.

## Features of the Streamlit App

The Streamlit app provides the following features:

1. **Data Exploration**: Users can load and explore the three CSV data files, selecting specific columns and filtering options.

2. **Data Cleaning**: The app allows users to perform data cleaning tasks, such as handling missing values, filtering data based on criteria, and identifying outliers.

3. **Descriptive Statistics**: Users can view summary statistics, distributions, and visualizations related to the data, including histograms, pie charts, and scatter plots.

4. **Insights and Conclusions**: The app presents key insights and conclusions drawn from the data analysis, highlighting trends, patterns, and potential areas for further investigation.

5. **User Profiling**: Users can explore user profiles, including demographics, interaction history, and performance metrics.

6. **Educational Content Analysis**: The app provides insights into the educational content, including difficulty levels, subjects, and learning stages.

7. **Predictive Modeling**: If applicable, the app may include predictive models or machine learning algorithms to make predictions or recommendations based on the data.

8. **Data Export**: Users can export selected data or visualizations for further analysis or reporting.

## Data Sources

The data for this project comes from three CSV files:

- `Info_UserData.csv`: Contains user-related information.
- `Log_Problem.csv`: Records user interactions with educational content.
- `Info_Content.csv`: Provides details about the educational content.

These datasets are fictional and created for the purpose of this project. They do not contain any real or personally identifiable information.

## Contributors

- Dorra Saadallah : (https://www.linkedin.com/in/dorra-saadallah)

## Feedback and Issues

If you encounter any issues, have suggestions for improvements, or would like to contribute to this project, please feel free to open an issue or pull request on the project's GitHub repository.

Happy exploring and analyzing educational data with Streamlit!
