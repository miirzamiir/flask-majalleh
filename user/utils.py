import re
from .models import User
from persiantools.jdatetime import JalaliDate

def validate_user(username, email, password=None, fname=None, lname=None, phone=None, 
                  bdate=None, curr_username=None, curr_email=None, curr_phone=None):
    errors = []

    if not re.match(r'^(?=.{4,})[a-z][a-z0-9_]*\d*$', username):
        errors.append('نام کاربری باید حداقل ۴ کاراکتر شامل کاراکترها و اعداد انگلیسی و آندرلاین باشد')
    elif username != curr_username and User.query.filter(User.username == username).first():
        errors.append('این نام کاربری از قبل ثبت شده است')

    if not re.match(r'^[A-Za-z0-9\._]+@[A-Za-z0-9]+\.[A-Za-z]{2,4}$', email):
        errors.append('ایمیل درست وارد کنید')
    elif email != curr_email and User.query.filter(User.email == email).first():
        errors.append('این ایمیل قبلا ثبت شده است')
    
    if password is not None:
        if re.match(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.{8,20}$)[^\s]*$', password):
            errors.append('پسورد باید حداقل شامل ۸ کاراکتر و حداکثر ۲۰ کاراکتر باشد. حداقل یک حرف کوچک و یک عدد را شامل شود و فاقد فاصله باشد')
    if fname is not None:
        if len(fname) < 3:
            errors.append('نام باید حداقل شامل ۳ کاراکتر باشد')
    if lname is not None:
        if len(lname) < 3:
            errors.append('نام خانوادگی باید حداقل شامل ۳ کارکتر باشد')

    if phone:
        if not re.match(r'^09\d{9}$', phone):
            errors.append('شماره تلفن رو به این شکل وارد کنید (۰۹۱۲۳۴۵۶۷۸۹)')
        elif phone != curr_phone and User.query.filter(User.phonenumber == phone).first():
            errors.append('این شماره تلفن قبلا ثبت شده')

    date = ''
    if bdate:
        bd = bdate.split('-')
        try:
            date = JalaliDate(int(bd[0]), int(bd[1]), int(bd[2]))
            if date > JalaliDate.today():
                errors.append('تاریخ تولد نمیتواند از تاریخ امروز بیشتر باشد')
            else:
                date = date.strftime('%Y-%m-%d')
        except:
            errors.append('تاریخ را به شکل درست وارد کنید')

    return errors, date