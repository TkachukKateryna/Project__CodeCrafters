from re import search

class bcolors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD_RED = '\033[1m\033[91m'
    DEFAULT = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

# Зберігає в собі методи перевірки значень класу RecordManager. Окремо не використовується.
class MiscChecks:
    def month_check(self,month:str):
        if len(month) > 2:
            error_text = {'en':"Wrong month format. Should be exactly two characters.",'ua':"Некоректний формат місяця: має складатись рівно з двох символів."}
            raise ValueError(error_text[self.language])
        if month[:1] == "0":
            month = month[:1]
        if int(month) <= 12:
            return True
        else:
            error_text = {'en':"Wrong month format: there can't be more than 12 of them. Correct format: MM-DD-YYYY, or MMDDYYYY.",'ua':"Некоректний формат місяця: їх не може бути більше дванадцяти. Правильний формат: ММ-ДД-РРРР, або ММДДРРРР."}
            raise ValueError(error_text[self.language])

    def day_check(self,day:str):
        if len(day) > 2:
            error_text = {'en':"Wrong day format. Should be exactly two characters.",'ua':"Некоректний формат дня: має складатись рівно з двох символів."}
            raise ValueError(error_text[self.language])
        if day[:1] == "0":
            day = day[:1]
        if int(day) <= 31:
            return True
        else:
            error_text = {'en':"Wrong day format: there can't be more than 31 of them. Correct format: MM-DD-YYYY, or MMDDYYYY.",'ua':"Некоректний формат дня: їх не може бути більше тридцяти одного. Правильний формат: ММ-ДД-РРРР, або ММДДРРРР."}
            raise ValueError(error_text[self.language])

    def year_check(self,year:str):
        from datetime import date
        if len(year) > 4:
            error_text = {'en':"Wrong year format. Should be exactly four characters.",'ua':"Некоректний формат року: має складатись рівно з чотирьох символів."}
            raise ValueError(error_text[self.language])
        if int(year) <= date.today().year:
            return True
        else:
            error_text = {'en':"Wrong year format: birthday cannot be in the future. Correct format: MM-DD-YYYY, or MMDDYYYY.",'ua':"Некоректний формат року: день народження не може бути у майбутньому. Правильний формат: ММ-ДД-РРРР, або ММДДРРРР."}
            raise ValueError(error_text[self.language])

    def p_check(self,phone:str):
        map = {' ':''}
        phone.translate(map)
        if len(phone) == 10 and search(r'\d{10}', phone) != None:
            return phone
        else:
            error_text = {'en':"Incorrect phone number. Must be exactly 10 characters, digits only.",'ua':"Некорректний номер телефону. Має складатись виключно з цифр, і цифр має бути 10. Не більше і не менше."}
            raise ValueError(error_text[self.language])

    def birthday_check(self,birthday):
        # Format: MM-DD-YYYY
        if (search(r'\d{2}\D\d{2}\D\d{4}', birthday) != None and len(birthday) == 10):
            month = birthday[0:2]
            day = birthday[3:5]
            year = birthday[6:10]
            if self.month_check(month) and self.day_check(day) and self.year_check(year):
                return birthday
        elif search(r'\d{8}', birthday) != None and len(birthday) == 8:
            month = birthday[0:2]
            day = birthday[2:4]
            year = birthday[4:8]
            if self.month_check(month) and self.day_check(day) and self.year_check(year):
                month = birthday[0:2] + "-" + birthday[2:4] + "-" + birthday[4:6] + birthday[6:8]
                return month
        else:
            error_text = {'en':"Wrong birthday format. The correct format would be: MM-DD-YYYY, or MMDDYYYY",'ua':"Некоректний формат дня народження. Правильний формат: ММ-ДД-РРРР, або ММДДРРРР."}
            raise ValueError(error_text[self.language])
        
    def days_to_birthday(self,mode=None):
        if self.birthday != "None":
            from datetime import date,datetime
            TODAY = date.today()
            tmp = self.birthday
            print(tmp)
            print((int(tmp[6:]), int(tmp[0:2]), int(tmp[3:5])))
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
            error_text = {'en':"Wrong email format. The correct format would be: text@text.text",'ua':"Некоректний формат електронної пошти. Правильний формат: текст@текст.текст"}
            raise ValueError(error_text[self.language])
        
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
    def __init__(self):
        self.language = None
        self.phones = {}
        self.name = "Unnamed contact"
        self.birthday = "None"
        self.email = "None"
        self.address = "None"

    def __str__(self):
        return f"Record name: {self.name}, Birthday: {self.birthday}, phones: {'; '.join(p for p in self.phones)}"

    def add_birthday(self,birthday):
        try:
            self.birthday = self.birthday_check(birthday)
        except ValueError as error_text:
            raise ValueError(error_text)
            
    def add_name(self,name:str):
        self.name = name

    def add_email(self,email:str):
        try:
            self.email = self.email_check(email)
        except ValueError as error_text:
            raise ValueError(error_text)

    def add_address(self,address:str):
        self.address = address

    def edit_birthday(self,new_birthday:str):
        if self.birthday != "None":
            try:
                self.birthday = self.birthday_check(new_birthday)
                return
            except ValueError as error_text:
                raise ValueError(error_text)
        
        error_text = {'en':"Birthday is not set in this record. Please, use the function for adding birthday instead.",'ua':"День народження у записі відсутній. Будь ласка, скористайтеся функцією додавання дня народження!"}
        raise ValueError(error_text[self.language])
            
    def edit_email(self,new_email:str):
        if self.email != "None":
            try:
                self.email = self.email_check(new_email)
                return
            except ValueError as error_text:
                raise ValueError(error_text)

        error_text = {'en':"Email is not set in this record. Please, use the function for adding email instead.",'ua':"Електронна пошта у записі відсутня. Будь ласка, скористайтеся функцією додавання дня електронної пошти!"}
        raise ValueError(error_text[self.language])
        
    def edit_name(self,name:str):
        self.name = name

    def edit_address(self,address:str):
        self.address = address
    
    def phone_check_and_set(self,mode,phone,new_phone=None):
        if mode == 'add':
            if phone.lower() == "stop":
                return True
            try:
                phone = self.p_check(phone)
                self.phones[len(self.phones)] = phone
                error_text = {'en':f"{bcolors.YELLOW}Phone added. if you want to add another one, enter it in the console. When you are done, just enter 'stop' in the console.{bcolors.GREEN}",'ua':f"{bcolors.YELLOW}Телефон додано. Якщо бажаєте додати ще один, введіть його у консоль. Коли додасте всі, що хотіли, просто пропишіть 'stop' у консоль.{bcolors.GREEN}"}
                raise ValueError(error_text[self.language])
            except ValueError as error_text:
                raise ValueError(error_text)
        elif mode == 'ed':
            if self.has_phone(phone):
                try:
                    if type(self.p_check(new_phone)) == str:
                        for phone_id,phone_number in self.phones.items():
                            if phone_number == phone:
                                self.phones[phone_id] = new_phone
                                #error_text = {'en':"Phone changed.",'ua':"Телефон відредаговано."}
                                #print(error_text[self.language])
                                return
                except ValueError as error_text_2:
                    raise ValueError(error_text_2)
                
            error_text = {'en':"Haven't found this phone number in the chosen contact!",'ua':"Цей телефон у обраному контакті не знайдено!"}
            raise ValueError(error_text[self.language])
        elif mode == 'del':
            if self.has_phone(phone):
                for phone_id,phone_number in self.phones.items():
                    if phone_number == phone:
                        del self.phones[phone_id]
                        error_text = {'en':"Phone removed.",'ua':"Телефон видалено."}
                        print(error_text[self.language])
                        return
            
            error_text = {'en':"Haven't found this phone number in the chosen contact!",'ua':"Цей телефон у обраному контакті не знайдено!"}
            raise ValueError(error_text[self.language])
            
    def remove_birthday(self):
        self.birthday = "None"
    
    def remove_name(self):
        self.name = "Unnamed contact"

    def remove_email(self):
        self.email = "None"

    def remove_address(self):
        self.address = "None"
        
    def load_data(self,name,phones,birthday,email,address): # To avoid reoccurring checks when loading from storage.bin
        id_generator = 0
        for do_not_use,phone in phones.items(): #rearranging phone ids, just like with contactbook records.
            self.phones[id_generator] = phone
            id_generator += 1

        self.name = name
        self.birthday = birthday
        self.email = email
        self.address = address