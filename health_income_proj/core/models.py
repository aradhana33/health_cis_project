from django.db import models

class CISHealthData(models.Model):
    PERSONID = models.BigIntegerField(primary_key=True)
    Gender = models.IntegerField(null=True)
    income_after_tax = models.BigIntegerField(null=True)
    Province = models.IntegerField(null=True)
    Gen_health_state = models.IntegerField(null=True)
    Mental_health_state = models.IntegerField(null=True)
    Work_hours = models.IntegerField(null=True)
    CPP_QPP = models.BigIntegerField(null=True)
    Child_benefit = models.BigIntegerField(null=True)
    Guaranteed_income = models.BigIntegerField(null=True)
    Food_security = models.BigIntegerField(null=True)
    Highest_edu = models.IntegerField(null=True)

    class Meta:
        db_table = "cis_health_data"
        managed = False  # Django won't manage the table
