from datetime import datetime

categories = []
records = []

# categories
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

# records
def add_record(record):
    record["creation_time"] = datetime.today()
    records.append(record)

def get_record_by_id(record_id):
    for record in records:
        if record['id'] == record_id:
            return record

def delete_record(record_id):
    for record in records:
        if record['id'] == record_id:
            records.remove(record)
            return True
    return False

def get_records_by_user_and_category(user_id=None, category_id=None):
    result = []
    for record in records:
        if ((user_id is None or record['user_id'] == user_id) and
                (category_id is None or record['category_id'] == category_id)):
            result.append(record)
    return result
