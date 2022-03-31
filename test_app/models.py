from django.db import models

# Create your models here.
class employees(models.Model):
    firstname=models.CharField(max_length=24)
    lastname=models.CharField(max_length=24)
    employee_id=models.AutoField(primary_key=True)

    def __str__(self):
        return self.firstname

class rooms(models.Model):
    room_id=models.AutoField(primary_key=True)
    room_number=models.CharField(max_length=20)

    def __str__(self):
        return self.room_number

class reservation(models.Model):
    meeting_id=models.AutoField(primary_key=True)
    room_id=models.ForeignKey(rooms, on_delete=models.DO_NOTHING)
    organizer=models.ForeignKey(employees, on_delete=models.DO_NOTHING)
    start_time=models.DateTimeField()
    end_time=models.DateTimeField()
    title=models.CharField(max_length=50)
    availability=models.BooleanField(default=True)

    def __str__(self):
        return self.title


class reservationInvitees(models.Model):
    reservation_id=models.ForeignKey(reservation, on_delete=models.CASCADE)
    invitees=models.ForeignKey(employees, on_delete=models.DO_NOTHING)
    confirmation=models.BooleanField(default=True)

    def __str__(self):
        return str(self.reservation_id)
    
    