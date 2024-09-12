import json
from dataclasses import dataclass
from datetime import datetime
from getpass import getpass
from re import escape

import requests


@dataclass
class User:
    auth_token: str
    uuid: str
    password_update_required: bool


### API ###


def login(username: str, password: str):
    url = "https://backend.arca.dk/api/v2/login"
    data = {
        "password": password,
        "username": username,
    }
    response = requests.post(url, data=data)

    user = json.loads(response.text)
    return User(**user)


def get_participations_bookings(user: User):
    url = "https://backend.arca.dk/api/v2/participations/bookings"
    headers = {"Authorization": user.auth_token}
    response = requests.get(url, headers=headers)
    return json.loads(response.text)


def get_friend_requests_received(user: User):
    url = "https://backend.arca.dk/api/v2/friend_requests/received"
    headers = {"Authorization": user.auth_token}
    response = requests.get(url, headers=headers)
    return json.loads(response.text)


def get_announcement(user: User):
    url = "https://backend.arca.dk/api/v2/announcement"
    headers = {"Authorization": user.auth_token}
    response = requests.get(url, headers=headers)
    return json.loads(response.text)


def get_push_notifications(user: User):
    url = "https://backend.arca.dk/api/v2/push_notifications"
    headers = {"Authorization": user.auth_token}
    response = requests.get(url, headers=headers)
    return json.loads(response.text)


def get_friendships(user: User):
    url = "https://backend.arca.dk/api/v2/friendships"
    headers = {"Authorization": user.auth_token}
    response = requests.get(url, headers=headers)
    return json.loads(response.text)


def get_gyms(user: User):
    url = "https://backend.arca.dk/api/v2/gyms"
    headers = {"Authorization": user.auth_token}
    response = requests.get(url, headers=headers)
    return json.loads(response.text)


def get_feed(user: User):
    url = "https://backend.arca.dk/api/v2/activities/bookings"
    headers = {"Authorization": user.auth_token}
    response = requests.get(url, headers=headers)
    return json.loads(response.text)


def get_authorize_card(user: User):
    url = "https://backend.arca.dk/api/v2/authorize_card"
    headers = {"Authorization": user.auth_token}
    response = requests.get(url, headers=headers)
    return json.loads(response.text)


def get_settings(user: User):
    url = "https://backend.arca.dk/api/v2/settings"
    headers = {"Authorization": user.auth_token}
    response = requests.get(url, headers=headers)
    return json.loads(response.text)


def get_pay_debt(user: User):
    url = "https://backend.arca.dk/api/v2/pay_debt"
    headers = {"Authorization": user.auth_token}
    response = requests.get(url, headers=headers)
    return json.loads(response.text)


def get_user(user: User):
    url = "https://backend.arca.dk/api/v2/user"
    headers = {"Authorization": user.auth_token}
    response = requests.get(url, headers=headers)
    return json.loads(response.text)


def get_events(user: User, date: str, gym_id: int):
    url = f"https://backend.arca.dk/api/v2/events?date={date}&gym_id={gym_id}"
    headers = {"Authorization": user.auth_token}
    response = requests.get(url, headers=headers)
    return json.loads(response.text)


def book_event(user: User, event_id: int):
    url = f"https://backend.arca.dk/api/v2/events/{event_id}/book"
    headers = {"Authorization": user.auth_token}
    response = requests.post(url, headers=headers)
    if response.status_code != 200:
        print(f"Failed to book event {event_id}.")
        return
    print(f"Booked event {event_id}.")
    return json.loads(response.text)


### Display data ###


def show_bookings(get_participations_bookings, user):
    participations_bookings = get_participations_bookings(user)
    print(f"{len(participations_bookings["ss_participations"])} bookings found.")


def show_friend_requests(get_friend_requests_received, user):
    friend_requests_received = get_friend_requests_received(user)
    print(
        f"{len(friend_requests_received["friend_requests"])} friend requests received."
    )


def show_announcement(get_announcement, user):
    announcement = get_announcement(user)
    print("Announcement:")
    print(f"'{announcement["announcement"]["body"]}'")


def show_notifications(get_push_notifications, user):
    push_notifications = get_push_notifications(user)
    new_push_notifications = [
        notification
        for notification in push_notifications["push_notifications"]
        if not notification["read?"]
    ]
    print(f"{len(new_push_notifications)} new push notifications found.")


def show_friendships(get_friendships, user):
    friendships = get_friendships(user)
    print(f"{len(friendships["users"])} friendships found.")


def show_gyms(get_gyms, user):
    gyms = get_gyms(user)
    print(f"{len(gyms["gyms"])} gyms found:")
    gyms_with_names = {gym["id"]: gym["name"] for gym in gyms["gyms"]}
    for gym_id, gym_name in gyms_with_names.items():
        print(f"{gym_id}: {gym_name}")


def show_feed_titles(show_feed_titles, user):
    feed = show_feed_titles(user)
    print(f"Recent feed - {len(feed["activities"])} items:")
    titles = [activity["title"] for activity in feed["activities"]]
    for title in titles:
        print(title)


def show_user_information(get_user, user):
    user = get_user(user)
    user_info = user["user"]
    unread_invitations = user_info["unread_invitations"]
    print(f"{unread_invitations} unread invitations.")
    badges = user_info["badges"]
    print(f"{len(badges)} badges.")


def show_events(get_events, user, as_gym_id, date):
    events = get_events(user, date=date, gym_id=as_gym_id)
    event_data = events["ss_events"]
    bookable_events = [
        event for event in event_data if event["can_book"] and not event["is_canceled"]
    ]
    print(f"{len(bookable_events)} events:")
    for event in bookable_events:
        print(f"[{event["id"]}] '{event['title']}'")
        print(f"  Instructor: {event['instructor']}")
        start_local = (
            datetime.fromisoformat(event["start_date_time"])
            .astimezone(datetime.now().astimezone().tzinfo)
            .strftime("%H:%M")
        )
        end_local = (
            datetime.fromisoformat(event["end_date_time"])
            .astimezone(datetime.now().astimezone().tzinfo)
            .strftime("%H:%M")
        )
        print(f"  {start_local}-{end_local}")
        capacity = event["capacity"]
        free_space = event["free_space"]
        wait_list = abs(event["free_space"]) if event["free_space"] < 0 else 0
        print(f"  {capacity - free_space} signed up.")
        print(f"  {wait_list} on waitlist.")
        escaped = escape(event["description"])
        print(f"  '{escaped[:50] if len(escaped) > 50 else escaped}'")
        print()


### CLI ###

username = input("Enter your email: ")
password = getpass("Enter your password: ")
user = login(username=username, password=password)
if not user.auth_token:
    print("Login failed.")
    exit()
print(f"Logged in as user: '{user.uuid}'.")
print()

show_announcement(get_announcement, user)
print()
show_user_information(get_user, user)
show_notifications(get_push_notifications, user)
show_friend_requests(get_friend_requests_received, user)
show_friendships(get_friendships, user)
show_bookings(get_participations_bookings, user)
print()
show_feed_titles(get_feed, user)
print()
show_gyms(get_gyms, user)
print()

selected_gym = input("Which gym would you like to see events for? (ID): ")
if not selected_gym.isdigit():
    print("Invalid gym ID.")
    exit()
print()
as_gym_id = int(selected_gym)

date = input("Which date would you like to see events? (YYYY-MM-DD) or (MM-DD): ")
if not date:
    print("Invalid date.")
    exit()
if len(date) == 5:
    date = f"2024-{date}"
print()

show_events(get_events, user, as_gym_id, date)
print()

selected_event = input("Which event would you like to book? (ID): ")
if not selected_event.isdigit():
    print("Invalid event ID.")
    exit()
print()
event_id = int(selected_event)

book_event(user, event_id)
