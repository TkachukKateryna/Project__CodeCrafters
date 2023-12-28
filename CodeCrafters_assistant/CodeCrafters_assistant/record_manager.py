from re import search
from datetime import date,datetime

# Зберігає в собі методи перевірки значень класу RecordManager. Окремо не використовується.
class MiscChecks:
    def month_check(self,month:str):
        if len(month) > 2:
            raise ValueError(self.parent.translate_string('wrong_month_format_char_num','yellow','green'))
        check_month = month
        if month[:1] == "0":
            check_month = month[:1]
        if int(check_month) <= 12:
            return True
        else:
            raise ValueError(self.parent.translate_string('wrong_month_format_out_bound','yellow','green'))

    def day_check(self,day:str):
        if len(day) > 2:
            raise ValueError(self.parent.translate_string('wrong_day_format_char_num','yellow','green'))
        check_day = day
        if day[:1] == "0":
            check_day = day[:1]
        if int(check_day) <= 31:
            return True
        else:
            raise ValueError(self.parent.translate_string('wrong_day_format_out_bound','yellow','green'))

    def year_check(self,year:str):
        if len(year) > 4:
            raise ValueError(self.parent.translate_string('wrong_year_format_char_num','yellow','green'))
        if int(year) <= date.today().year:
            return True
        else:
           raise ValueError(self.parent.translate_string('wrong_year_format_out_bound','yellow','green'))

    def calendar_check(self,year:str,month:str,day:str):
        try:
            if datetime(int(year),int(month),int(day)).date():
                return True
            raise ValueError(self.parent.translate_string('wrong_year_format_days_num','yellow','green'))
        except ValueError:
            raise ValueError(self.parent.translate_string('wrong_year_format_days_num','yellow','green'))

    def p_check(self,phone:str):
        map = {' ':''}
        phone.translate(map)
        if len(phone) == 10 and search(r'\d{10}', phone) != None:
            return phone
        else:
            raise ValueError(self.parent.translate_string('incorrect_phone','yellow','green'))

    def birthday_check(self,birthday):
        # Format: MM-DD-YYYY
        if (search(r'\d{2}\D\d{2}\D\d{4}', birthday) != None and len(birthday) == 10):
            month = birthday[0:2]
            day = birthday[3:5]
            year = birthday[6:10]
            if self.month_check(month) and self.day_check(day) and self.year_check(year) and self.calendar_check(year,month,day):
                return birthday
        elif search(r'\d{8}', birthday) != None and len(birthday) == 8:
            month = birthday[0:2]
            day = birthday[2:4]
            year = birthday[4:8]
            if self.month_check(month) and self.day_check(day) and self.year_check(year) and self.calendar_check(year,month,day):
                birthday = birthday[0:2] + "-" + birthday[2:4] + "-" + birthday[4:6] + birthday[6:8]
                return birthday
        else:
            raise ValueError(self.parent.translate_string('wrong_birthday_format','yellow','green'))
        
    def days_to_birthday(self,mode=None):
        if self.birthday != "None":
            TODAY = date.today()
            tmp = self.birthday
            BD_DAY = datetime(int(tmp[6:]), int(tmp[0:2]), int(tmp[3:5])).date()
            if (BD_DAY.month < TODAY.month) or ((BD_DAY.month == TODAY.month) and (BD_DAY.day < TODAY.day)):
                BD_DAY = BD_DAY.replace(year = TODAY.year + 1)
            else:
                BD_DAY = BD_DAY.replace(year = TODAY.year)
            if mode == 'no_math':
                return (BD_DAY)
            else:
                return (BD_DAY - TODAY)
        return "None"

    def email_check(self,email:str):
        # Format: text@text.text
        if (search(r'\S{3,}@[a-zA-Z]{2,}.[a-zA-Z]{2,}', email) != None):
            email = f"{email[:email.rfind('@')]}{email[email.rfind('@'):].lower()}"
            return email
        else:
            raise ValueError(self.parent.translate_string('wrong_email_format','yellow','green'))
        
    def has_phone(self,phone:str):
        for i in self.phones.values():
            if i == phone:
                return True
           
        return False 

    def find_in_name(self, text):
        text = fr"{text.lower()}"
        if self.name.lower().find(text) != -1:
            return search(text,self.name.lower()).span()
        else:
            return False

    def find_in_birthday(self, text):
        text = fr"{text.lower()}"
        if self.birthday.lower().find(text) != -1:
            return search(text,self.birthday.lower()).span()
        else:
            return False

    def find_in_email(self, text):
        text = fr"{text.lower()}"
        if self.email.lower().find(text) != -1:
            return search(text,self.email.lower()).span()
        else:
            return False

    def find_in_address(self, text):
        text = fr"{text.lower()}"
        if self.address.lower().find(text) != -1:
            return search(text,self.address.lower()).span()
        else:
            return False

    def find_in_phones(self, text):
        text = fr"{text.lower()}"
        phones = "; ".join(f"{phone}" for phone in self.phones.values())
        if phones.lower().find(text) != -1:
            return search(text,phones.lower()).span()
        else:
            return False

# Екземпляр класу. Відповідає за зберігання усіх змінних запису. Створюється у ContactBook. Необов'язкові поля можуть бути пропущені символами "n"/"N".
# У самому класі зберігається лише функціонал запису/зміни/видалення. Все інше наслідується від MiscChecks.
class RecordManager(MiscChecks):
    def __init__(self, parent_class):
        self.parent = parent_class
        self.phones = {}
        if self.parent:
            self.name = self.parent.translate_string('unnamed_contact')
            self.birthday = self.parent.translate_string('none')
            self.email = self.parent.translate_string('none')
            self.address = self.parent.translate_string('none')
        else:
            self.name = "Unnamed contact"
            self.birthday = "None"
            self.email = "None"
            self.address = "None"

    def __str__(self):
        return f"{self.parent.translate_string('record_name','red','green')}: {self.name}, {self.parent.translate_string('contact_attr_p2','red','green')}: {self.birthday}, {self.parent.translate_string('contact_attr_p3','red','green')}: {self.email}, {self.parent.translate_string('contact_attr_p4','red','green')}: {self.address}, {self.parent.translate_string('contact_attr_p5','red','green')}: {'; '.join(phone for phone in self.phones.values())}"

    def record_error(func):
        #print(func.__name__)
        def true_handler(self,arg):
            try:
                result = func(self,arg)
            except ValueError as error_text:
                raise ValueError(error_text)
        return true_handler

    @record_error
    def add_birthday(self,birthday):
        self.birthday = self.birthday_check(birthday)

    @record_error
    def add_name(self,name:str):
        self.name = name

    @record_error
    def add_email(self,email:str):
        self.email = self.email_check(email)

    @record_error
    def add_address(self,address:str):
        self.address = address

    @record_error
    def edit_birthday(self,new_birthday:str):
        if self.birthday != "None":
            self.birthday = self.birthday_check(new_birthday)
        
        raise ValueError(self.parent.translate_string('no_birthday','yellow','green'))

    @record_error
    def edit_email(self,new_email:str):
        if self.email != "None":
                self.email = self.email_check(new_email)

        raise ValueError(self.parent.translate_string('no_email','yellow','green'))

    @record_error
    def edit_name(self,name:str):
        self.name = name

    @record_error
    def edit_address(self,address:str):
        self.address = address

    def phone_check_and_set(self,mode,phone,new_phone=None):
        try:
            if mode == 'add':
                if phone.lower() == "stop":
                    return True
                phone = self.p_check(phone)
                self.phones[len(self.phones)] = phone
                raise ValueError(f"{self.parent.translate_string('phone_added_p0','yellow','red')}{self.parent.translate_string('phone_added_p1')}{self.parent.translate_string('phone_added_p2','yellow','green')}")
            elif mode == 'ed':
                if self.has_phone(phone):
                    if type(self.p_check(new_phone)) == str:
                        for phone_id,phone_number in self.phones.items():
                            if phone_number == phone:
                                self.phones[phone_id] = new_phone
                                return
                    
                raise ValueError(self.parent.translate_string('phone_not_found','yellow','green'))
            elif mode == 'del':
                if self.has_phone(phone):
                    for phone_id,phone_number in self.phones.items():
                        if phone_number == phone:
                            del self.phones[phone_id]
                            print(self.parent.translate_string('phone_removed','yellow','green'))
                            return
                
                raise ValueError(self.parent.translate_string('phone_not_found','yellow','green'))
        except ValueError as error_text:
            raise ValueError(error_text)
            
    def remove_name(self):
        self.name = self.parent.translate_string('unnamed_contact')
        print(self.parent.translate_string('name_removed','yellow','green'))

    def remove_birthday(self):
        self.birthday = self.parent.translate_string('none')
        print(self.parent.translate_string('birthday_removed','yellow','green'))
    
    def remove_email(self):
        self.email = self.parent.translate_string('none')
        print(self.parent.translate_string('email_removed','yellow','green'))

    def remove_address(self):
        self.address = self.parent.translate_string('none')
        print(self.parent.translate_string('address_removed','yellow','green'))
        
    def load_data(self,name,phones,birthday,email,address): # To avoid reoccurring checks when loading from storage.bin
        id_generator = 0
        for do_not_use,phone in phones.items(): #rearranging phone ids, just like with contactbook records.
            self.phones[id_generator] = phone
            id_generator += 1

        self.name = name
        self.birthday = birthday
        self.email = email
        self.address = address