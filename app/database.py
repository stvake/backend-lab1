users = []
categories = []
records = []


def get_all_users():
    return users


def get_user_by_id(user_id):
    for user in users:
        if user['id'] == user_id:
            return user


def delete_user_by_id(user_id):
    for user in users:
        if user['id'] == user_id:
            users.remove(user)
            return True
    return False