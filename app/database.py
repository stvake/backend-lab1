users = []
categories = []
records = []

def add_user(user):
    users.append(user)

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

def add_category(category):
    categories.append(category)

def get_all_categories():
    return categories

def delete_category(category_id):
    for category in categories:
        if category['id'] == category_id:
            categories.remove(category)
            return True
    return False