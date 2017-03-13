from __future__ import unicode_literals

from django.db import models
from django.db.models import Count
from django.utils import timezone

# Create your models here.


class Location(models.Model): # List of Sheds/Warehouse pay points
    LOCATION = (
        ('IMP', 'Import'),
        ('EXP', 'Export'),
        ('COU', 'Courier'),
        ('COA', 'COA')
    )
    location = models.CharField(max_length=3, choices=LOCATION, default='IMP')

    def __unicode__(self):
        return self.location


class Software(models.Model): # List the software in use
    software = models.CharField(max_length=6)

    def __unicode__(self):
        return self.software


class Bank(models.Model):
    BANKS = (
        ('Access', 'Access Bank'),
        ('GTBank', 'Guaranty Trust Bank'),
        ('FBN', 'First Bank Nigeria'),
        ('Skye', 'Skye Bank'),
        ('ZBN', 'Zenith Bank Nigeria'),
        ('UBA', 'United Bank for Africa'),
        ('Fidelity', 'Fidelity Bank'),
        ('Stanbic', 'Stanbic IBTC')
    )
    banks = models.CharField(max_length=10, choices=BANKS, default='Access')

    def __unicode__(self):
        return self.banks


class AgencyDetail(models.Model):
    AGENCY_TYPE = (
        ('CR','Credit'),
        ('CA','Cash')
    )
    agency_name = models.CharField(max_length=50)
    agency_type = models.CharField(max_length=2, choices=AGENCY_TYPE)
    agency_minimum_balance = models.FloatField(default=1000000.00)
    agency_current_balance = models.FloatField(default=0.00)

    def __unicode__(self):
        return self.agency_name


class Staff(models.Model):
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    staff_no = models.CharField(max_length=4)
    # set designation for access control

    def __unicode__(self):
        return self.staff_no


class AgentAWBList(models.Model):
    agency = models.ForeignKey(AgencyDetail)
    airwaybill = models.CharField(max_length=11)
    awb_pieces = models.IntegerField()
    rcvd_pieces = models.IntegerField()
    awb_weight = models.FloatField(default=0.00)
    rcvd_weight = models.FloatField(default=0.00)
    flight_date = models.DateTimeField()
    input_date = models.DateTimeField()
    exit_date = models.DateTimeField()
    authorized_by = models.ForeignKey(Staff)

    def __unicode__(self):
        return self.airwaybill


class PaymentUtilizations(models.Model):
    awb_on_list = models.ForeignKey(AgentAWBList)
    invoice_amount = models.FloatField(default=0.00)
    authorized_by = models.ForeignKey(Staff)


class Payments(models.Model):
    PAYMENTMODE = (
        ('CA', 'Cash'),
        ('CQ', 'Cheque'),
        ('DR', 'Bank Draft'),
        ('TR', 'Transfer')
    )
    agency = models.ForeignKey(AgencyDetail)
    payment = models.FloatField(default=0.00)
    payment_date = models.DateTimeField()
    payment_mode = models.CharField(max_length=2, choices=PAYMENTMODE)
    teller_no = models.CharField(max_length=10)
    authorized_by = models.ForeignKey(Staff)


class TellerData(models.Model):
    location = models.ForeignKey(Location)
    software = models.ForeignKey(Software, default='Galaxy')
    teller_date = models.DateTimeField()
    bank = models.ForeignKey(Bank)
    agency = models.ForeignKey(AgencyDetail)  # used specially for MOU/credit agents
    teller_no = models.CharField(max_length=10)
    teller_amount = models.FloatField(default=0.00)
    authorized_by = models.ForeignKey(Staff)


class DailySales(models.Model):
    SALESTYPE = (
        ('CR', 'Credit'),
        ('CA', 'Cash')
    )
    Location = models.ForeignKey(Location)
    sales_date = models.DateTimeField()
    sales_type = models.CharField(max_length=2,choices=SALESTYPE)
    net_sales = models.FloatField(default=0.00)
    vat = models.FloatField(default=0.00)
    total_stamp = models.FloatField(default=0.00)

class EventActions(models.Model):
    event_code = models.CharField(max_length=3)
    event_actions = models.CharField(max_length=30)


class EventTrail(models.Model): # Create an events audit trail
    event_action = models.ForeignKey(EventActions)
    event_action_success = models.BooleanField(default=1)
    event_time = models.DateTimeField()
    event_by = models.ForeignKey(Staff)
