from django.db import models

class Database_Siemens(models.Model):
    time = models.DateTimeField()
    humidity = models.FloatField(default=0.0,null=True)
    temperature = models.FloatField(default=0.0,null=True)

def __str__(self):
        return f"{self.time} - {self.humidity} - {self.temperature} "  
'''
#This enable string representation of Database
 instance and make it human readiable

'''


