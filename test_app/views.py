from sys import api_version
from django.shortcuts import render
from django.http import Http404
from django.http import HttpResponse
from django.shortcuts import get_list_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics
import json
from .models import employees, rooms, reservationInvitees, reservation
from .serializers import employeesSerializer, roomsSerializer, reservationSerializer, reservationInviteesSerializer, UserSerializer, RegisterSerializer
import logging
from test_app import models
from knox.models import AuthToken
from rest_framework.authtoken.serializers import AuthTokenSerializer
from knox.views import LoginView as KnoxLoginView
from django.contrib.auth import login
from rest_framework import permissions

# Create your views here.

logger = logging.getLogger(__name__)


class employeeList(APIView):
    def get(self,request):
        logger.info("Get all employees new")
        employees1=employees.objects.all()
        serializer=employeesSerializer(employees1, many=True)
        return Response (serializer.data)

    def post(self, request):
        serializer=  employeesSerializer(data=request.data)
        if serializer.is_valid():
            logger.info("New Employee added")
            serializer.save()
        return Response(serializer.data)

class roomList(APIView):

    def get(self,request):
        logger.info("Get all rooms")
        rooms1=rooms.objects.all()
        serializer=roomsSerializer(rooms1, many=True)
        return Response (serializer.data)

    def post(self, request):
        serializer=  roomsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            logger.info("New Room added")
        return Response(serializer.data)


class reservationList(APIView):

    def get(self,request):
        logger.info("Get all Reservations")
        reservation1=reservation.objects.all()
        serializer=reservationSerializer(reservation1, many=True)
        data =[]
        for x in serializer.data:
            x = json.loads(json.dumps(x))
            query = employees.objects.get(employee_id=x['organizer'])
            employee = employeesSerializer(query)
            x.update({"organizer_name":query.firstname+" "+query.lastname })
            data.append(x)
        return Response(data)

    def post(self, request):
        room_Ocupied = reservation.objects.filter(end_time__gt=request.data['start_time'], room_id=request.data['room_id'])
        if room_Ocupied:
            logger.warning("Room is already booked on given time")
            return Response({"Msg":"The room is reserved on provided time...please choose another time slot for this room.."}, status=status.HTTP_400_BAD_REQUEST)
        emp_Ocupied = reservation.objects.filter(end_time__gt=request.data['start_time'], organizer=request.data['organizer'])
        if emp_Ocupied:
            logger.warning("Employee is already reserved for given time..")
            return Response({"Msg":"The given emp is already scheduled for this time..please choose another time slot.."}, status=status.HTTP_400_BAD_REQUEST)
        serializer=  reservationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            logger.info("New meeting reservation added")
        return Response(serializer.data)

class reservationDetail(APIView): 
    
    def get_object(self, id):
        try:
            return reservation.objects.get(meeting_id=id)
        except reservation.DoesNotExist:
            raise Http404
    
    def get(self, request, meeting_id, format=None):
        query = self.get_object(meeting_id)
        serializer = reservationSerializer(query)
        return Response(serializer.data)
    
    def delete(self, request, meeting_id, format=None):
        query = self.get_object(meeting_id)
        query.delete()
        logger.info("Reservation is deleted")
        return Response(status=status.HTTP_204_NO_CONTENT)

class getReservationByEmployee(APIView):
     def get(self, request):
        logger.info("Get room reservations by room id or by employee id")
        data =[]
        emp_id = request.query_params.get('emp_id')
        rooms_reserv = reservation.objects.filter(room_id = request.query_params.get('roomid'))
        for x in rooms_reserv.values():
            reserved_employees = reservationInvitees.objects.filter(reservation_id = x['meeting_id'])
            data.append({"reservation":x,"invitees":reserved_employees.values()})
        data_by_employee = []
        if emp_id:
            for x in data:
                if x['reservation']['organizer_id']==int(emp_id):
                    data_by_employee.append(x)
                for z in x['invitees']:
                    if z['invitees_id'] ==int(emp_id):
                        data_by_employee.append(x)
                        break
            return Response(data_by_employee)
        return Response(data)

class reservationInviteesList(APIView):

    def get(self,request):
        reservationInvitees1=reservationInvitees.objects.all()
        serializer=reservationInviteesSerializer(reservationInvitees1, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer=  reservationInviteesSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            logger.info("New invitees has been added for meeting..")
        return Response(serializer.data)

class reservationInviteeDetail(APIView):

    def get_object(self, res_id, emp_id):
        try:
            return reservationInvitees.objects.get(reservation_id=res_id, invitees=emp_id)
        except reservation.DoesNotExist:
            raise Http404
    
    def get(self, request, format=None):
        query = self.get_object(request.query_params.get('res_id'), request.query_params.get('emp_id'))
        serializer = reservationInviteesSerializer(query)
        return Response(serializer.data)

    def put(self, request):
        
        record = self.get_object(request.query_params.get('res_id'), request.query_params.get('emp_id'))

        serializer = reservationInviteesSerializer(record, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Register API
class RegisterAPI(generics.GenericAPIView):
    logger.info("Register new user")
    serializer_class = RegisterSerializer
    permission_classes = (permissions.AllowAny,)
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
        "user": UserSerializer(user, context=self.get_serializer_context()).data,
        "token": AuthToken.objects.create(user)[1]
        })


class LoginAPI(KnoxLoginView):
    permission_classes = (permissions.AllowAny,)
    logger.info("User logged in..")
    def post(self, request, format=None):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        return super(LoginAPI, self).post(request, format=None)