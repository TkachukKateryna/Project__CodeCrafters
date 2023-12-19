from record_manager import MiscChecks, RecordManager
from datetime import datetime
#from collections import UserDict

class bcolors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    DEFAULT = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class ContactBook(): #UserDict
    def __init__(self):
        self.data = {}
        self.priority_ids = []
        self.language = None
        self.record_cnt = 0
        self.generated_ids = 0
        self.file = "storage.bin"
        self.update_file("load",0)

        self.opnng = f"{bcolors.CYAN}Введіть, будь ласка, "
        self.non_obligatory = f"{bcolors.CYAN}( або '{bcolors.RED}N{bcolors.CYAN}', якщо бажаєте додати пізніше)"
        self.opnng_en = f"{bcolors.CYAN}Please, enter the "
        self.non_obligatory_en = f"{bcolors.CYAN}( or '{bcolors.RED}N{bcolors.CYAN}', if you want to add it later)"
        self.method_table = {'__localization_insert':{
                                'name':{
                                    'en':"of the contact manager", 
                                    'ua':"менеджера контактів"},
                                'description':{
                                    'en':"contact manager", 
                                    'ua':"менеджер контактів та записів"}},
                            'create':{
                                'description':{
                                    'en':"Adds a new record to the contact book. You can add a name, a phone, a birthday, an address, an an email - either when creating a record, or later.",
                                    'ua':"Додає новий запис до книги контактів. Можна додати ім'я, телефони, день народження, адресу та email одразу, а можна й пізніше."}, 
                                'methods':{
                                    self.add_name:{
                                        'name':{
                                            'en':f"{self.opnng_en}name{self.non_obligatory_en}",
                                            'ua':f"{self.opnng}ім'я{self.non_obligatory}"}},
                                    self.add_phone:{
                                        'phone':{
                                            'en':f"{self.opnng_en}phone number{self.non_obligatory_en}",
                                            'ua':f"{self.opnng}номер телефону{self.non_obligatory}"}},
                                    self.add_birthday:{
                                        'birthday':{
                                            'en':f"{self.opnng_en}birthday{self.non_obligatory_en}",
                                            'ua':f"{self.opnng}день народження контакта{self.non_obligatory}"}},
                                    self.add_email:{
                                        'email':{
                                            'en':f"{self.opnng_en}email{self.non_obligatory_en}",
                                            'ua':f"{self.opnng}електронну пошту контакта{self.non_obligatory}"}},
                                    self.add_address:{
                                        'address':{
                                            'en':f"{self.opnng_en}address{self.non_obligatory_en}",
                                            'ua':f"{self.opnng}адресу контакта{self.non_obligatory}"}}}},
                            'check_birthdays':{
                                'description':{
                                    'en':"Displays a list of contacts, who have a birthday in the specified perioud.",
                                    'ua':"Виводить список іменинників на обраний користувачем період."}, 
                                'methods':{
                                    self.contacts_upcoming_birthday:{
                                        'attr_id':{
                                            'en':f"{self.opnng_en}number of days",
                                            'ua':f"{self.opnng}кількість днів"}}}}}
  
        
    def contacts_upcoming_birthday(self, numb):
        while True:
            try:
                days_ahead = int(numb)
                break
            except ValueError:
                if numb.lower() == 'n':
                    return
                print("Неправильний формат кількості днів. Спробуйте ще раз.")
                numb = input()
        today = datetime.now()
        upcoming_birthdays = []
        for record_id, record in self.data.items():
            if record.birthday is not None:
                dob = datetime.strptime(record.birthday, '%m-%d-%Y')
                current_year_birthday = datetime(today.year, dob.month, dob.day)
                if current_year_birthday >= today:
                    days_until_birthday = (current_year_birthday - today).days
                    if days_until_birthday <= days_ahead:
                        upcoming_birthdays.append((record.name, record.birthday))
                else:
                    next_birthday = datetime(today.year + 1, dob.month, dob.day)
                    days_until_birthday = (next_birthday - today).days
                    if days_until_birthday <= days_ahead:
                        upcoming_birthdays.append((record.name, record.birthday))
        if upcoming_birthdays:
            print(f"Контакти у яких день народження протягом наступних {days_ahead} днів від сьогоднішньої дати:")
            for name, birthday in upcoming_birthdays:
                print(f"{name} - {birthday}")
        else:
            print(f"Немає контактів у яких день народження протягом наступних {days_ahead} днів від сьогоднішньої дати.")

    # Prepares self.data[id] to be saved.
    # Explanation: operates in one mode: 'add' (requires record id). returns prepared dict with record variables. 
    # Used to add new lines to the file.bin
    def prepare_data(self,mode:str,record_id=None):
        if mode == "add":
            for rid,record in self.data.items():
                if rid == record_id:
                    return {'Name':record.name,'Phones':record.phones,'Birthday':record.birthday,'Email':record.email,'Address':record.address}
            raise ValueError('Record Id not found!')
    
    # Dynamicly adds new records, deletes records, creates file.bin, etc.
    # If mode == add, adding record to file (with correct persistent id). If mode == 'del', removes the record by id, overwrites saved data with the new parsed self.data. 
    # With "ed", overwrites saved data with the new parsed self.data
    def update_file(self,mode:str,r_id=None):
        import pickle
        from pathlib import Path
        file = Path(self.file)
        if not file.exists():
            with open(file, 'wb') as storage:
                print("No data to load! Creating new file!")
                return

        if mode == "add":
            with open(file, 'ab') as storage:
                pickle.dump(self.prepare_data(mode="add",record_id=r_id),storage)
                self.generated_ids += 1
        elif mode == "del":
            with open(file, 'wb') as storage:
                if r_id in self.data:
                    del self.data[r_id]

                if len(self.data) > 0:
                    id_generator = 0
                    for id,record in self.data.items():
                        pickle.dump({'Name':record.name,'Phones':record.phones,'Birthday':record.birthday,'Email':record.email,'Address':record.address},storage)
                        id_generator += 1
                    self.generated_ids = id_generator
                else:
                    print("ERROR!\nNo such record exists!")
        elif mode == "ed":
            with open(file, 'wb') as storage:
                if len(self.data) > 0:
                    id_generator = 0
                    for id,record in self.data.items():
                        pickle.dump({'Name':record.name,'Phones':record.phones,'Birthday':record.birthday,'Email':record.email,'Address':record.address},storage)
                        id_generator += 1
                    self.generated_ids = id_generator
        elif mode == "load":
            with open(file, 'rb') as storage:
                if file.stat().st_size != 0:
                    id_generator = 0
                    try:
                        while True:  
                            record = pickle.load(storage)
                            self.data[id_generator] = RecordManager()
                            self.data[id_generator].load_data(name=record['Name'],phones=record['Phones'],birthday=record['Birthday'],email=record['Email'],address=record['Address'])
                            id_generator += 1
                    except EOFError:
                        self.generated_ids = id_generator
                        self.record_cnt = id_generator
                        print('Reached the end of file!')
            #print(self.data)


    #Saves self.data and some technical variables. Can be used, although everything should be saved automatically. may be used to ensure, that nothing will be lost.
    #def save_changes(self):
        #self.update_file("ed")

    def add_name(self,name):
        new_record = RecordManager()
        new_record.language = self.language
        if self.dialogue_check(name):
            try:
                new_record.add_name(name)
            except ValueError as error_text:
                return str(error_text)
            
            self.id_assign(mode="add",record=new_record)
            return True

        

    def add_phone(self,phone):
        record = self.data[self.ongoing]
        if self.dialogue_check(phone):
            try:
                record.add_phone(phone)
            except ValueError as error_text:
                return str(error_text)

        return True

    def add_birthday(self,birthday):
        record = self.data[self.ongoing]
        if self.dialogue_check(birthday):
            try:
                record.add_birthday(birthday)
            except ValueError as error_text:
                return str(error_text)

            return True

    def add_email(self,email):
        record = self.data[self.ongoing]
        if self.dialogue_check(email):
            try:
                record.add_email(email)
            except ValueError as error_text:
                return str(error_text)

            return True

    def add_address(self,address):
        record = self.data[self.ongoing]
        if self.dialogue_check(address):
            try:
                record.add_address(address)
            except ValueError as error_text:
                return str(error_text)

            local = {'part_1':{'en':"Contact created with name",'ua':"Контакт створено з ім'ям"},
                    'part_2':{'en':"phone numbers",'ua':"номерами телефону"},
                    'part_3':{'en':"birthday",'ua':"днем народження"},
                    'part_4':{'en':"email",'ua':"електронною поштою"},
                    'part_5':{'en':"address",'ua':"адресою"}}
            string = f"{bcolors.GREEN}{local['part_1'][self.language]}: {record.name}; {local['part_2'][self.language]}: {record.phones}; {local['part_3'][self.language]}: {record.birthday}; {local['part_4'][self.language]}: {record.email}; {local['part_5'][self.language]}: {record.address}"
            print(string)
            self.update_file(mode="add",r_id=self.generated_ids)
            self.ongoing = None
            return True

    def dialogue_check(self,variable):
        if variable.lower() != 'n':
            return True
        return False

    def id_assign(self,mode:str,record:RecordManager):
        if mode == "add":
            if len(self.priority_ids) > 0:
                self.data[self.priority_ids[0]] = record
                self.ongoing = self.priority_ids[0]
                del self.priority_ids[0]
            else:
                self.data[self.record_cnt] = record
                self.ongoing = self.record_cnt
                self.record_cnt += 1
        elif mode == "del":
            for k,v in self.data.items():
                if v == record:
                    self.priority_ids.append(k)
