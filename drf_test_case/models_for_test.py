from django.db import models

class PrefixModel(models.Model):
    name = models.CharField(max_length=100, unique=True)
    class Meta:
        app_label = 'drf_test_case'
    def __str__(self):
        return self.name

class MyModel(models.Model):
    name = models.CharField(max_length=100)
    prefix_fk = models.ForeignKey(PrefixModel, on_delete=models.CASCADE, null=True, blank=True)
    class Meta:
        unique_together = [("prefix_fk", "name")]
        app_label = 'drf_test_case'
    def __str__(self):
        return f"{self.prefix_fk_id}__{self.name}"
