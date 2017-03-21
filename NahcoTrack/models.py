from __future__ import unicode_literals

from django.db import models
from django.db.models import Count
from django.utils import timezone
from django.urls import reverse

# Create your models here.


class Location(models.Model): # List of Sheds/Warehouse pay points
    LOCATION = (
        ('IMP', 'Import'),
        ('EXP', 'Export'),
        ('COU', 'Courier'),
        ('COA', 'COA')
    )
    location = models.CharField(max_length=3, choices=LOCATION, default='IMP')

    # Metadata
    class Meta:
        ordering = ["-location"]

    # Methods
    def get_absolute_url(self):
        """
        Returns the url to access a particular instance of Location.
        """
        return reverse('location-detail', args=[str(self.id)])

    # def __str__(self):
    #     return self.location

    def __unicode__(self):
        return self.location


class Software(models.Model): # List the software in use
    software = models.CharField(max_length=6)

    # Metadata
    class Meta:
        ordering = ["-software"]

    # Methods
    def get_absolute_url(self):
        """
        Returns the url to access a particular instance of Model.
        """
        return reverse('software-detail', args=[str(self.id)])

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
    banks = models.CharField(max_length=10, choices=BANKS, default='Skye')

    # Metadata
    class Meta:
        ordering = ["-banks"]

    # Methods
    def get_absolute_url(self):
        """
        Returns the url to access a particular instance of Location.
        """
        return reverse('bank-detail', args=[str(self.id)])

    def __unicode__(self):
        return self.banks


class AgencyDetail(models.Model):
    AGENCY_TYPE = (
        ('CR','Credit'),
        ('CA','Cash')
    )
    agency_name = models.CharField(max_length=50)
    agency_type = models.CharField(max_length=2, choices=AGENCY_TYPE)
    agency_minimum_balance = models.DecimalField(decimal_places=2,max_digits=10, null=True)
    agency_current_balance = models.DecimalField(decimal_places=2,max_digits=10, null=True)

    # Metadata
    class Meta:
        ordering = ["-agency_name"]

    # Methods
    def get_absolute_url(self):
        """
        Returns the url to access a particular instance of Model.
        """
        return reverse('AgencyDetail-detail', args=[str(self.id)])

    def __unicode__(self):
        return self.agency_name


# class Staff(models.Model):
#     first_name = models.CharField(max_length=20)
#     last_name = models.CharField(max_length=20)
#     staff_no = models.CharField(max_length=4)
#     # set designation for access control
#
#     def __unicode__(self):
#         return self.staff_no


class AgentAWBList(models.Model):
    agency = models.ForeignKey(AgencyDetail, on_delete=models.SET_NULL, null=True)
    airwaybill = models.CharField(max_length=11)
    awb_pieces = models.IntegerField()
    rcvd_pieces = models.IntegerField()
    awb_weight = models.FloatField(default=0.00)
    rcvd_weight = models.FloatField(default=0.00)
    flight_date = models.DateField()
    input_date = models.DateField()
    exit_date = models.DateField()
    awb_cleared = models.BooleanField(default=False)
    #authorized_by = models.ForeignKey(Staff)

    # Metadata
    class Meta:
        ordering = ["-exit_date"]

    # Methods
    def get_absolute_url(self):
        """
        Returns the url to access a particular instance of Model.
        """
        return reverse('AgentAWBList-detail', args=[str(self.id)])

    def __unicode__(self):
        return self.airwaybill


class Payments(models.Model):
    PAYMENTMODE = (
        ('CA', 'Cash'),
        ('CQ', 'Cheque'),
        ('DR', 'Bank Draft'),
        ('TR', 'Transfer')
    )
    bank = models.ForeignKey(Bank, on_delete=models.SET_NULL, null=True)
    agency = models.ForeignKey(AgencyDetail, on_delete=models.SET_NULL, null=True)
    payment_amount = models.DecimalField(decimal_places=2,max_digits=10)
    payment_date = models.DateField()
    payment_mode = models.CharField(max_length=2, choices=PAYMENTMODE, default='Cash')
    teller_no = models.CharField(max_length=11)
    #authorized_by = models.ForeignKey(Staff)

    def __unicode__(self):
        return self.teller_no

    # Metadata
    class Meta:
        ordering = ["bank", "payment_date", "-teller_no"]

    # Methods
    def get_absolute_url(self):
        """
        Returns the url to access a particular instance of Model.
        """
        return reverse('Payments-detail', args=[str(self.id)])

    def __get_full_Lodgementdetail(self):
        ":returns teller no, Amount, bank and payment/lodgement date"
        return '%s (%s) %s, %s' % (self.teller_no,self.payment,self.bank,self.payment_date)
    lodgement_detail = property(__get_full_Lodgementdetail)


class PaymentUtilizations(models.Model):
    payment = models.ForeignKey(Payments, on_delete=models.SET_NULL, null=True)
    awb_on_list = models.ForeignKey(AgentAWBList, on_delete=models.SET_NULL, null=True)
    invoice_amount = models.DecimalField(decimal_places=2, max_digits=10)
    utilization_date = models.DateField(null=True)
    #authorized_by = models.ForeignKey(Staff)

    # Metadata
    class Meta:
        ordering = ["payment", "-utilization_date"]

    # Methods
    def get_absolute_url(self):
        """
        Returns the url to access a particular instance of Model.
        """
        return reverse('PaymentUtilizations-detail', args=[str(self.id)])

    def __unicode__(self):
        return '%s (%s)' % (self.utilization_date, self.payment__payments__teller_no)


class TellerData(models.Model):
    PAYMENTMODE = (
        ('PO', 'POS'),
        ('BA', 'Bank'),
        ('TR', 'Transfer')
    )
    location = models.ForeignKey(Location)
    software = models.ForeignKey(Software, on_delete=models.SET_NULL, null=True, default='Galaxy')
    teller_date = models.DateField()
    bank = models.ForeignKey(Bank, on_delete=models.SET_NULL, null=True)
    agency = models.ForeignKey(AgencyDetail, on_delete=models.SET_NULL, null=True)  # used specially for MOU/credit agents
    teller_no = models.CharField(max_length=10)
    teller_amount = models.DecimalField(decimal_places=2,max_digits=10)
    payment_mode = models.CharField(max_length=2, choices=PAYMENTMODE, default='BA')
    #authorized_by = models.ForeignKey(Staff)

    # Metadata
    class Meta:
        ordering = ["software", "-bank", "teller_no", "teller_amount"]

    # Methods
    def get_absolute_url(self):
        """
        Returns the url to access a particular instance of Model.
        """
        return reverse('TellerData-detail', args=[str(self.id)])

    def __unicode__(self):
        return '(%s) %s %s %s %s' % (self.software, self.teller_date, self.bank, self.teller_amount, self.teller_no)


class DailySales(models.Model): # Summary of a point daily sale
    SALESTYPE = (
        ('CR', 'Credit'),
        ('CA', 'Cash')
    )
    Location = models.ForeignKey(Location)
    sales_date = models.DateField()
    sales_type = models.CharField(max_length=2,choices=SALESTYPE)
    net_sales = models.DecimalField(decimal_places=2,max_digits=10)
    vat = models.DecimalField(decimal_places=2,max_digits=10)
    total_stamp = models.DecimalField(decimal_places=2,max_digits=10)

    # Metadata
    class Meta:
        ordering = ["-sales_date", "Location"]

    # Methods
    def get_absolute_url(self):
        """
        Returns the url to access a particular instance of Model.
        """
        return reverse('DailySales-detail', args=[str(self.id)])

    def __unicode__(self):
        return '(%s) %s %s %s %s' % (self.sales_date, self.sales_type, self.net_sales, self.vat, self.total_stamp)

# class EventActions(models.Model):
#     event_code = models.CharField(max_length=3)
#     event_actions = models.CharField(max_length=30)
#
#
# class EventTrail(models.Model): # Create an events audit trail
#     event_action = models.ForeignKey(EventActions)
#     event_action_success = models.BooleanField(default=1)
#     event_time = models.DateTimeField()
#     #event_by = models.ForeignKey(Staff)
