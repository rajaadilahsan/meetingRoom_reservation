
# Meeting Room reservation 




## Run server

To deploy this project run

```bash
  python manage.py makemigrations
  python manage.py migrate
  python manage.py runserver
```
visit the url http://localhost:8000


## API Reference

#### Register new user

```
  POST api/register/
```


#### Login to system to get authenticate

```
  Post /api/login
```

Get token form response and add token to request headers to authenticate the apis.\
e.g Authorization: Token 8c7fa6fcfdd2fec4ff92e4b61dda4934e7f7367092324bd87576250dc59cfc74 

#### Employee

```
  Post /api/employees
```

```
  GET /api/employees
```

#### Rooms

```
  Post /api/rooms
```
```
  GET /api/rooms
```
#### Reservation

```
  Post /api/reservations
```
If the room or employee is already reserved on given time the response will be 400 says choose another time.

Request Body
```
{
    "meeting_id": 1,
    "start_time": "2022-03-25T11:08:59Z",
    "end_time": "2022-03-25T11:09:01Z",
    "title": "Test",
    "availability": true,
    "room_id": 1,
    "organizer": 1
        
}
```

```
  GET /api/reservations
```
Get or delete Reservation by sepecific room
```
  GET /api/delete_reservation/:meetingid
```

```
  DELETE /api/delete_reservation/:meetingid
```

#### Get room Reservation by roomid or emp id

Get all room reservation of given room id
```
  GET /api/getRoomReservation/?roomid=1
```
Get all room reservattion and also filter by employee 
```
  GET /api/getRoomReservation/?roomid=1&emp_id=1
```

#### Meeting Invitee cancel invitation

```
  Get /api/invitee_cancel_reservation/?res_id=1&emp_id=1
```

```
  PUT /api/invitee_cancel_reservation/?res_id=1&emp_id=1
```
Request Body
```
{
"confirmation": false,  #meeting invitee can also cancel his invitation by setting confirmation false
"reservation_id": 1,  #meeting_id from reservation table
"invitees": 1         #employee_id from employees table
}
```

#### Add invitees to meeting 

```
  Post /api/invitees
```
Request Body

```
{
"confirmation": true,
"reservation_id": 1,  #meeting_id from reservation table
"invitees": 1         #employee_id from employees table
}
```

```
  GET /api/invitees
```

#### Logout 

```
  Post /api/logout
```
"# meetingRoom_reservation" 
