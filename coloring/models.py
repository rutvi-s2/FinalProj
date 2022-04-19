from django.db import models

# todo: delete Author later
class Author(models.Model):
  name = models.CharField(max_length=50)
  
class User(models.Model):
  username = models.CharField(max_length=50)
  friends = models.JSONField(null=True)
  saved = models.JSONField(null=True)
  claimed = models.JSONField(null=True)
  rating = models.IntegerField(null=True)
  total = models.IntegerField(null=True)
  verified = models.BooleanField(default = False)

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
  # claimed_by = models.ForeignKey(User, on_delete=models.CASCADE, null = True)
  qty = models.IntegerField(null=True)
  qty_units = models.CharField(
        max_length=2,
        choices=QTY_CHOICES,
        default='UN'
    )
  best_by = models.DateField(null=True)
  private = models.BooleanField(default = False)
  description = models.CharField(max_length=300)
  active = models.BooleanField(default = True)
  claimed = models.BooleanField(default = False)
  rating_lister = models.IntegerField(null=True)
  # rating_taker = models.IntegerField(null=True)
  # tags
  unopened = models.BooleanField(default = False)
  og_packaging = models.BooleanField(default = False)
  store_bought = models.BooleanField(default = False)
  homemade = models.BooleanField(default = False)
  
  