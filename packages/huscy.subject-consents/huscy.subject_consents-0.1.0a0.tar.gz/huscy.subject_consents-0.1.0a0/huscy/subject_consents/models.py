from django.db import models

from huscy.consents.models import ConsentFile
from huscy.subjects.models import Subject


class SubjectConsentFile(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    consent_file = models.ForeignKey(ConsentFile, on_delete=models.PROTECT)
