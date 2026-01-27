from django.db import models, transaction
from django.conf import settings
from django.core.exceptions import ValidationError

class Wallet(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='wallet')
    balance = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    currency = models.CharField(max_length=3, default='BRL')
    version = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if self.pk:
            with transaction.atomic():
                current_version = Wallet.objects.select_for_update().get(pk=self.pk).version
                if current_version != self.version:
                    raise ValueError("Conflito de Concorrência: A carteira foi modificada por outra transação.")
                self.version += 1
        else:
            self.version = 0
        super().save(*args, **kwargs)

        def __str__(self):
            return f"Carteira de {self.user.username} ({self.currency})"

# repensar valores nulos desse objeto.
class Transaction(models.Model):
    TRANSACTION_TYPES = (('DEPOSIT', 'Deposit'), ('TRANSFER', 'Transfer'))

    idempotency_id = models.UUIDField(unique=True, null=True, blank=True)
    
    type = models.CharField(choices=TRANSACTION_TYPES, max_length=10)
    value = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3, default='BRL')

    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='sent_transactions')
    receiver = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='received_transactions')

    created_at = models.DateTimeField(auto_now_add=True)

    # temporário rs
    def clean(self):
        if self.value <= 0:
            raise ValidationError("O valor da transação deve ser positivo.")

        if self.sender and self.receiver and self.sender == self.receiver:
            raise ValidationError("O remetente e o destinatário não podem ser a mesma pessoa.")
        
        if self.sender and self.sender.wallet.currency != self.currency:
            # [TO DO]: implementar uma conversão de moeda aqui
            raise ValidationError("A moeda do remetente não corresponde à moeda da transação.")

        if self.type == 'TRANSFER' and self.sender.wallet.balance < self.value:
            raise ValidationError("Saldo insuficiente para completar a transação.")
