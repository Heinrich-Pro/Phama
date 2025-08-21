from django.db import models
from products.models import Product
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail

class InventoryLog(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    change = models.IntegerField()  # + pour ajout, - pour retrait
    date = models.DateTimeField(auto_now_add=True)
    reason = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.product} - {self.change}"

@receiver(post_save, sender=Product)
def check_low_stock(sender, instance, **kwargs):
    if instance.stock < 10:  # Seuil pour notification
        send_mail(
            'Stock bas',
            f'Le stock de {instance.name} est bas : {instance.stock} unités restantes.',
            'admin@pharmacy.com',
            ['admin@email.com'],  # Remplace par email admin
        )