from django.contrib import admin
from .models import employees, rooms, reservation, reservationInvitees
# from .models import rooms
# from .models import reservation
# from .models import reservationInvitees
# Register your models here.
admin.site.register(employees)
admin.site.register(rooms)
admin.site.register(reservation)
admin.site.register(reservationInvitees)