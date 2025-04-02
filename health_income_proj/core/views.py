from .models import CISHealthData
from django_pandas.io import read_frame  # you may need to pip install django-pandas
import matplotlib.pyplot as plt       # for plotting
import seaborn as sns                 # for prettier plots
import base64                         # for image encoding
from io import BytesIO                # for in-memory image buffer

def dashboard_from_excel(request):
    # Load data from DB
    queryset = CISHealthData.objects.all()
    df = read_frame(queryset)

    charts = {}

    # Gender Pay Gap
    gender_income = df.groupby('Gender')['income_after_tax'].mean().reset_index()
    fig1 = plt.figure(figsize=(6, 4))
    sns.barplot(x='Gender', y='income_after_tax', data=gender_income)
    plt.title('Average Income by Gender')
    plt.xlabel('Gender')
    plt.ylabel('Income After Tax')
    charts['gender_income'] = fig_to_base64(fig1)

    # Province-Wise Average Income
    prov_group = df.groupby('Province').agg({
        'income_after_tax': 'mean',
        'Gen_health_state': 'mean',
        'Mental_health_state': 'mean'
    }).reset_index()

    fig2 = plt.figure(figsize=(7, 4))
    sns.barplot(x='Province', y='income_after_tax', data=prov_group)
    charts['income_by_province'] = fig_to_base64(fig2)

    fig3 = plt.figure(figsize=(7, 4))
    sns.barplot(x='Province', y='Gen_health_state', data=prov_group)
    charts['health_by_province'] = fig_to_base64(fig3)

    fig4 = plt.figure(figsize=(6, 4))
    sns.regplot(x='Work_hours', y='Mental_health_state', data=df)
    charts['work_vs_mental'] = fig_to_base64(fig4)

    # Assistance vs Food Security
    df['programs_received'] = ((df[['CPP_QPP', 'Child_benefit', 'Guaranteed_income']] > 0).sum(axis=1))
    df['Food_insecure'] = df['Food_security'].apply(lambda x: 1 if x > 0 else 0)
    food_insecure_prob = df.groupby('programs_received')['Food_insecure'].mean().reset_index()

    fig5 = plt.figure(figsize=(6, 4))
    sns.barplot(x='programs_received', y='Food_insecure', data=food_insecure_prob)
    charts['assistance_vs_food'] = fig_to_base64(fig5)

    return render(request, 'core/dashboard.html', charts)
