# Зберігає в собі методи перевірки значень класу RecordManager. Окремо не використовується.
class MiscChecks:
    def month_check(self,month:str):
        if len(month) > 2:
            raise ValueError("Wrong month format. Should only contain two symbols.")
        if month[:1] == "0":
            month = month[:1]
        if int(month) <= 12:
            return True
        else:
            raise ValueError("Wrong month format. There can't be more than 12 of them. Correct format: MM-DD-YYYY")

    def p_check(self,phone:str):
        from re import search
        map = {' ':''}
        phone.translate(map)
        if len(phone) == 10 and search(r'\d{10}', phone) != None:
            return phone
        else:
            raise ValueError("Incorrect phone number. Must be exactly 10 characters, digits only.")

    def birthday_check(self,birthday):
        from re import search
        # Format: MM-DD-YYYY
        if birthday == None:
            return None
        elif (search(r'\d{2}\D\d{2}\D\d{4}', birthday) != None and len(birthday) == 10):
            tmp = birthday[0:2]
            if self.month_check(tmp):
                return birthday
        elif search(r'\d{8}', birthday) != None and len(birthday) == 8:
            tmp = birthday[0:2]
            if self.month_check(tmp):
                tmp = birthday[0:2] + "-" + birthday[2:4] + "-" + birthday[4:6] + birthday[6:8]
                return tmp
        else:
            raise ValueError("Wrong birthday format. The correct format would be: MM-DD-YYYY")
        
    def has_phone(self,phone:str):
        for i in self.phones:
            if i.value == phone:
                return True
           
        return False 

# Екземпляр класу. Відповідає за зберігання усіх змінних запису. Створюється у ContactBook. Необов'язкові поля можуть бути пропущені символами "n"/"N".
# У самому класі зберігається лише функціонал запису/зміни/видалення. Все інше наслідується від MiscChecks.
class RecordManager(MiscChecks):
    def __init__(self, name):
        self.method_table = {}
        self.phones = []
        self.name = name
        self.birthday = None

    def __str__(self):
        return f"Record name: {self.name}, Birthday: {self.birthday}, phones: {'; '.join(p for p in self.phones)}"

    def add_phone(self,phone):
        if type(self.p_check(phone)) == str:
            phone = self.p_check(phone)
            self.phones.append(phone)
            print(f"Added number {phone} to the record (named '{self.name}')!")

    def add_birthday(self,birthday):
        if self.birthday_check(birthday):
            self.birthday = self.birthday_check(birthday)
            print(f"Added birthday {birthday} to the record (named '{self.name}')!")

    def edit_phone(self,phone:str,new_phone:str):
        if self.has_phone(phone):
            if type(self.p_check(new_phone)) == str:
                self.phones.remove(phone)
                self.phones.append(new_phone)
                return
        
        raise ValueError("Phone not found!")
    
    def edit_birthday(self,new_birthday:str):
        if self.birthday != None:
            if type(self.birthday_check(new_birthday)) == str:
                self.birthday = self.birthday_check(new_birthday)
                return
        
        raise ValueError("Birthday not set yet!")
        
    def edit_name(self,name:str):
        self.name = name

    def remove_phone(self,phone:str):
        if self.has_phone(phone):
            self.phones.remove(phone)
            return
        
        raise ValueError("Phone not found!")
    
    def remove_birthday(self):
        self.birthday = None
    
    def remove_name(self):
        self.name = "Unnamed contact"

    def load_data(self,name,phones,birthday): # To avoid reoccurring checks when loading from storage.bin
        self.phones = phones
        self.name = name
        self.birthday = birthday