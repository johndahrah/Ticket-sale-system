# users
username = 'user_name'
password = 'password'
level = 'privilege_level'
change_data_type = 'change'
userID = 'userid'

# tickets
opened = 'openedforselling'
event_name = 'eventname'
date = 'eventdate'
time = 'eventtime'
place = 'eventplace'
organizer = 'EventOrganizerName'
price = 'sellprice'
comment = 'comment'
organizerid = 'organizerid'
serial = 'serialnumber'
id = 'id'
all_ticket_properties = (
    id, event_name, opened, date, time, place,
    organizer, price, comment, organizerid, serial
    )
sell_tickets_id = 'selling'

# organizers
organizer_name = 'name'
organizer_address = 'address'
organizer_id = 'id'
all_organizer_properties = (
    organizer_id, organizer_name, organizer_address
)

# coupons
coupon = 'coupon'


json_change_value_error = 'nothing has been changed: %s is not a valid json value'
