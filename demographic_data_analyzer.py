import pandas as pd

def calculate_demographic_data(df):
    # Race count - sort by index for consistency
    race_count = df['race'].value_counts().sort_index()

    # Average age of men
    average_age_men = round(df[df['sex'] == 'Male']['age'].mean(), 1)

    # Percentage with Bachelors degree
    total = len(df)
    percentage_bachelors = round((df['education'] == 'Bachelors').sum() / total * 100, 1)

    # Advanced education
    higher_education = df['education'].isin(['Bachelors', 'Masters', 'Doctorate'])
    lower_education = ~higher_education

    # Percentage with advanced education earning >50K
    higher_education_rich = round((df[higher_education]['salary'] == '>50K').sum() / higher_education.sum() * 100, 1)
    # Percentage without advanced education earning >50K
    lower_education_rich = round((df[lower_education]['salary'] == '>50K').sum() / lower_education.sum() * 100, 1)

    # Minimum hours worked per week
    min_work_hours = df['hours-per-week'].min()

    # Percentage of minimum hour workers earning >50K
    num_min_workers = df[df['hours-per-week'] == min_work_hours].shape[0]
    rich_min_workers = df[(df['hours-per-week'] == min_work_hours) & (df['salary'] == '>50K')].shape[0]
    rich_percentage = round(rich_min_workers / num_min_workers * 100, 1) if num_min_workers > 0 else 0

    # Country with highest percentage earning >50K
    country_counts = df['native-country'].value_counts()
    country_rich = df[df['salary'] == '>50K']['native-country'].value_counts()
    percentages = (country_rich / country_counts * 100).dropna()
    highest_earning_country = percentages.idxmax()
    highest_earning_country_percentage = round(percentages.max(), 1)

    # Most popular occupation for >50K earners in India
    india_high_earners = df[(df['native-country'] == 'India') & (df['salary'] == '>50K')]
    top_IN_occupation = india_high_earners['occupation'].mode()[0] if not india_high_earners.empty else None

    return {
        'race_count': race_count,
        'average_age_men': average_age_men,
        'percentage_bachelors': percentage_bachelors,
        'higher_education_rich': higher_education_rich,
        'lower_education_rich': lower_education_rich,
        'min_work_hours': min_work_hours,
        'rich_percentage': rich_percentage,
        'highest_earning_country': highest_earning_country,
        'highest_earning_country_percentage': highest_earning_country_percentage,
        'top_IN_occupation': top_IN_occupation
    }
