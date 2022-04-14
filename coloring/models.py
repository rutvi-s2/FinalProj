from django.db import models

# todo: delete Author later
class Author(models.Model):
  name = models.CharField(max_length=50)
  
class User(models.Model):
  username = models.CharField(max_length=50)

class Posting(models.Model):
  QTY_CHOICES = [
    ('UN', 'Units'),
    ('LB', 'Pounds'),
    ('OZ', 'Ounces'),
    ('PT', 'Pints'),
    ('GL', 'Gallons'),
]
  item_name = models.CharField(max_length=70)
  listing_user = models.ForeignKey(User, on_delete=models.CASCADE, null = True)
  qty = models.IntegerField()
  qty_units = models.CharField(
        max_length=2,
        choices=QTY_CHOICES,
        default='UN'
    )
  best_by = models.DateField()
  private = models.BooleanField(default = False)
  description = models.CharField(max_length=300)
  active = models.BooleanField(default = True)
  # tags
  unopened = models.BooleanField(default = False)
  og_packaging = models.BooleanField(default = False)
  store_bought = models.BooleanField(default = False)
  homemade = models.BooleanField(default = False)
  

