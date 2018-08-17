from database_setup import Category, CategoryItem, User

def create_user(session, login_session):
    """Create user and return user id from login session"""
    new_user = User(
        name=login_session['username'],
        email=login_session['email'],
        picture=login_session['picture']
    )
    session.add(new_user)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one_or_none()
    return user.id


def get_user_info(session, user_id):
    """Returns user by user id"""
    user = session.query(User).filter_by(id=user_id).one_or_none()
    return user


def get_user_id(session, email):
    """Returns user id by email"""
    try:
        user = session.query(User).filter_by(email=email).one_or_none()
        return user.id
    except Exception:
        return None