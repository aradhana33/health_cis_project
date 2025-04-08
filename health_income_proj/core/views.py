from .models import CISHealthData
from django_pandas.io import read_frame  # you may need to pip install django-pandas
import matplotlib.pyplot as plt       # for plotting
import seaborn as sns                 # for prettier plots
import base64                         # for image encoding
from io import BytesIO                # for in-memory image buffer
from django.shortcuts import render
from django.http import JsonResponse
from django.db.models import Avg

def fig_to_base64(fig):
    buf = BytesIO()
    fig.tight_layout()
    fig.savefig(buf, format='png')
    buf.seek(0)
    image_png = base64.b64encode(buf.getvalue()).decode('utf-8')
    buf.close()
    return image_png
    
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
    
def gender_pay_gap_chart(request):
    return render(request, "core/gender_chart.html")
    
def api_gender_pay_gap(request):
    data = (
        CISHealthData.objects
        .filter(Gender__in=[1, 2])
        .values('Gender')
        .annotate(avg_income=Avg('income_after_tax'))
    )
    return JsonResponse(list(data), safe=False)
    # return render(request, "core/gender_chart.html")

def api_province_income_health(request):
    data = (
        CISHealthData.objects
        .values('Province')
        .annotate(
            avg_income=Avg('income_after_tax'),
            avg_health=Avg('Gen_health_state'),
            avg_mental=Avg('Mental_health_state'),
        )
    )
    return JsonResponse(list(data), safe=False)

from django.db.models import FloatField
from django.db.models.functions import Cast

def api_work_vs_mental(request):
    records = CISHealthData.objects.exclude(Work_hours=None, Mental_health_state=None)
    result = records.annotate(
        Work_hours_f=Cast('Work_hours', FloatField()),
        Mental_health_state_f=Cast('Mental_health_state', FloatField())
    ).values('Work_hours_f', 'Mental_health_state_f')
    return JsonResponse(list(result), safe=False)

def api_assistance_vs_food(request):
    all_data = CISHealthData.objects.all().values(
        'CPP_QPP', 'Child_benefit', 'Guaranteed_income', 'Food_security'
    )
    counts = {}

    for record in all_data:
        programs_received = sum(
            int(record.get(field, 0)) > 0
            for field in ['CPP_QPP', 'Child_benefit', 'Guaranteed_income']
        )
        food_insecure = 1 if record.get('Food_security', 0) > 0 else 0

        if programs_received not in counts:
            counts[programs_received] = {'insecure': 0, 'total': 0}

        counts[programs_received]['total'] += 1
        counts[programs_received]['insecure'] += food_insecure

    result = [
        {
            'programs_received': k,
            'food_insecurity_probability': v['insecure'] / v['total']
        } for k, v in counts.items()
    ]
    return JsonResponse(result, safe=False)


