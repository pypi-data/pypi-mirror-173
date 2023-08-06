from django.db import models


class OtpData(models.Model):
    id = models.AutoField(primary_key=True)
    session_token = models.CharField(max_length=250)
    otp_no = models.IntegerField()
    to = models.CharField(max_length=255)
    time = models.DateTimeField(auto_now_add=True, blank=True)
    otp_count_today = models.IntegerField(blank=True, null=True)
