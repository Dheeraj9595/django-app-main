from django.db import models


class LocalBrand(models.Model):
    id = models.AutoField(primary_key=True, db_column="local_brand_id")
    local_brand_name = models.CharField(max_length=200)

    def __str__(self) -> str:
        return self.local_brand_name


class Division(models.Model):
    id = models.AutoField(primary_key=True, db_column="division_id")
    division = models.CharField(max_length=200)

    def __str__(self) -> str:
        return self.division


class Brand(models.Model):
    brand_code = models.CharField(max_length=100, primary_key=True, db_column="brand_code")
    division = models.OneToOneField(Division, on_delete=models.CASCADE, null=True, blank=True)
    local_brand = models.OneToOneField(LocalBrand, on_delete=models.CASCADE)
    global_brand_name = models.CharField(max_length=200, null=True, blank=True)
    upc_ean_gtin = models.CharField(max_length=200, null=True, blank=True)
    # brand_name = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self) -> str:
        return self.brand_code
