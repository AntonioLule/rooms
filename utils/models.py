from django.db import models


class BaseModel(models.Model):
    """
    Establecemos la base para los modelos con usuari y fechas
    """

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True, null=True, blank=True)

    class Meta:
        abstract = True