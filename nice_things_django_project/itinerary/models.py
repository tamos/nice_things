from django.db import models
from django_pandas.managers import DataFrameManager


class Food(models.Model):
    """
    This is a model for food inspections data.
    See README.md for details on the data and its fields.
    """
    inspection_id = models.PositiveIntegerField(primary_key=True)
    dba_name = models.CharField(max_length=200)
    aka_name = models.CharField(max_length=200)  # informal name
    license_num = models.PositiveIntegerField() 
    facility_type = models.CharField(max_length=200)  # type of eatery
    risk = models.CharField(max_length=200, default=None)  # assessed risk
    address = models.CharField(max_length=200, default=None)
    city = models.CharField(max_length=200, default=None)
    state = models.CharField(max_length=2, default=None)
    zip_code = models.IntegerField(default=None)
    inspection_date = models.DateTimeField(default=None)
    inspection_type = models.CharField(max_length=200, default=None)
    results = models.CharField(max_length=200, default=None)  # pass/fail, etc.
    violations = models.TextField(default=None)  # details of issues
    longitude = models.FloatField(default=None)
    latitude = models.FloatField(default=None)
    # We need our results as a DataFrame in order to use record_linkage.
    objects = DataFrameManager() 


class Wages(models.Model):
    """
    This is a model for Wage and Hour Compliance Data.
    See README.md for details on the data fields. 
    """
    case_id = models.PositiveIntegerField(primary_key=True)
    trade_nm = models.CharField(max_length=200)  # informal business name
    legal_name = models.CharField(max_length=200)  # legal name
    street_addr_1_txt = models.CharField(max_length=200)   # address
    cty_nm = models.CharField(max_length=200)  # city
    st_cd = models.CharField(max_length=2)  # state
    zip_code = models.IntegerField(default=None)  
    case_violtn_cnt = models.PositiveIntegerField()  # No. infractions
    longitude = models.FloatField(default=None)
    latitude = models.FloatField(default=None)
    objects = DataFrameManager()


class Env_Complaints(models.Model):
    '''
    This model is data on environmental records from CDPH.
    It does not contain information on the individual violations,
    only that a violation exists. But the URL links to the details.
    '''
    longitude = models.FloatField(default=None)
    latitude = models.FloatField(default=None)
    objects = DataFrameManager()
    address = models.CharField(max_length=200) 
    complaints = models.BooleanField(default = None)  # Environmental Complaints
    complaints_url = models.URLField(default = None)  # link to the complaint
    enviro_enforcement = models.BooleanField(default = None)  # Enforcement
    enviro_enforcement_url = models.URLField(default = None)  # link


class Divvy(models.Model):
    """
    This is a model for Divvy bike-share station location data.
    See README.md for details.
    """
    station_id = models.PositiveIntegerField(primary_key=True)
    name = models.CharField(max_length=200)
    city = models.CharField(max_length=200)
    longitude = models.FloatField(default=None)
    latitude = models.FloatField(default=None)
    capacity = models.PositiveIntegerField()  # number of bikes available
    objects = DataFrameManager()









