from .db import get_data_as_dict, insert_data

def register_user(data):

    query = f"""
        INSERT INTO public.users (fname, lname, email, username, password)
        VALUES (%s, %s, %s, %s, crypt(%s, gen_salt('bf'))) RETURNING username, user_uuid
    """
    fname = data['fname']
    lname = data['lname']
    email = data['email']
    username = data['username']
    password = data['password']

    count, result = insert_data(query, fname, lname, email, username, password)

    return count, result

def login_user(data):
    query = f"""
        SELECT user_id, user_uuid, username
        FROM public.users
        WHERE username=%s AND password=crypt(%s, password)
        LIMIT 1
    """
    username = data['username']
    password = data['password']

    count, result = get_data_as_dict(query, username, password)

    return count, result
