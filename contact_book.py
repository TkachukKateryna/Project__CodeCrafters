from record_manager import MiscChecks, RecordManager
from datetime import date,datetime,timedelta

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

class ContactBook():
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
                                    'en':"contact manager", 
                                    'ua':"менеджера контактів"},
                                'description':{
                                    'en':"contact manager", 
                                    'ua':"менеджер контактів та записів"}},
                            'create':{
                                'description':{
                                    'en':"Adds a new record to the contact book. You can add a name, a phone, a birthday, an address, an email - either when creating a record, or later.",
                                    'ua':"Додає новий запис до книги контактів. Можна додати ім'я, телефони, день народження, адресу та email одразу, а можна й пізніше."}, 
                                'methods':{
                                    self.contact_create:{},
                                    self.add_name:{
                                        'name':{
                                            'en':f"{self.opnng_en}name{self.non_obligatory_en}",
                                            'ua':f"{self.opnng}ім'я{self.non_obligatory}"}},
                                    self.add_phone:{
                                        'phone':{
                                            'en':f"{self.opnng_en}phone number (10 digits){self.non_obligatory_en}",
                                            'ua':f"{self.opnng}номер телефону (10 цифр){self.non_obligatory}"}},
                                    self.add_birthday:{
                                        'birthday':{
                                            'en':f"{self.opnng_en}birthday (MM-DD-YYYY){self.non_obligatory_en}",
                                            'ua':f"{self.opnng}день народження контакта (MM-DD-YYYY){self.non_obligatory}"}},
                                    self.add_email:{
                                        'email':{
                                            'en':f"{self.opnng_en}email(text@text.text){self.non_obligatory_en}",
                                            'ua':f"{self.opnng}електронну пошту контакта(text@text.text){self.non_obligatory}"}},
                                    self.add_address:{
                                        'address':{
                                            'en':f"{self.opnng_en}address{self.non_obligatory_en}",
                                            'ua':f"{self.opnng}адресу контакта{self.non_obligatory}"}},
                                    self.add_contact_finish:{}}},
                            'check_birthdays':{
                                'description':{
                                    'en':"Displays a list of contacts, who have a birthday in the specified perioud.",
                                    'ua':"Виводить список іменинників на обраний користувачем період."}, 
                                'methods':{
                                    self.show_upcoming_birthdays:{
                                        'attr_id':{
                                            'en':f"{self.opnng_en}number of days",
                                            'ua':f"{self.opnng}кількість днів"}}}},
                            'edit':{
                                'description':{
                                    'en':"Edits the name/birthday/email/address of a contact.",
                                    'ua':"Редагує ім'я/день народження/електронну пошту/адресу контакта."}, 
                                'methods':{
                                    self.print_contacts:{},
                                    self.choose_contact_from_the_list:{
                                        'note_id':{
                                            'en':f"{self.opnng_en}number of a contact you want to edit",
                                            'ua':f"{self.opnng}номер контакта, який ви хочете відредагувати"}},
                                    self.print_contact_attributes:{},
                                    self.choose_contact_attribute:{
                                        'attr_id':{
                                            'en':f"{self.opnng_en}what you are going to edit",
                                            'ua':f"{self.opnng}що ви збираєтесь редагувати"}},
                                    self.edit_contact:{
                                        'new_text':{
                                            'en':f"{self.opnng_en}new text",
                                            'ua':f"{self.opnng}новий текст"}},
                                    }},
                            'edit_phone':{
                                'description':{
                                    'en':"Edits the phone number of a contact.",
                                    'ua':"Редагує номер телефона контакта."}, 
                                'methods':{
                                    self.print_contacts:{},
                                    self.choose_contact_from_the_list:{
                                        'note_id':{
                                            'en':f"{self.opnng_en}number of a contact, which has the phone you want to edit",
                                            'ua':f"{self.opnng}номер контакту, номери телефону якого ви хочете відредагувати"}},
                                    self.print_contact_phones:{},
                                    self.choose_contact_phone:{
                                        'attr_id':{
                                            'en':f"{self.opnng_en}phone number, which you are going to edit",
                                            'ua':f"{self.opnng}номер телефону, який ви збираєтесь редагувати"}},
                                    self.edit_phones:{
                                        'new_text':{
                                            'en':f"{self.opnng_en}new phone number",
                                            'ua':f"{self.opnng}новий номер телефону"}},
                                    }},
                            'add_phone':{
                                'description':{
                                    'en':"Adds a new phone number to the contact.",
                                    'ua':"Додає новий номер телефону до контакта."}, 
                                'methods':{
                                    self.print_contacts:{},
                                    self.choose_contact_from_the_list:{
                                        'attr_id':{
                                            'en':f"{self.opnng_en}number of the contact, which you are going to edit",
                                            'ua':f"{self.opnng}номер контаку, який ви збираєтесь редагувати"}},
                                    self.add_phone:{
                                        'attr_id':{
                                            'en':f"{self.opnng_en}phone number, which you are going to add",
                                            'ua':f"{self.opnng}номер телефону, який ви хочете додати"}},
                                    self.add_phone_finish:{},
                                    }},
                            'find':{
                                'description':{
                                    'en':"Looks for a specified text in the contacts.",
                                    'ua':"Шукає введений текст у контактах."}, 
                                'methods':{
                                    self.print_find_modes:{},
                                    self.choose_find_mode:{
                                        'attr_id':{
                                            'en':f"{self.opnng_en}search mode number",
                                            'ua':f"{self.opnng}номер режиму пошуку"}},
                                    self.find_hub:{
                                        'attr_id':{
                                            'en':f"{self.opnng_en}text you want to find",
                                            'ua':f"{self.opnng}текст, який ви бажаєте знайти"}}}},
                            'remove':{
                                'description':{
                                    'en':"Deletes the contact.",
                                    'ua':"Видаляє контакт."}, 
                                'methods':{
                                    self.print_contacts:{},
                                    self.choose_contact_from_the_list:{
                                        'attr_id':{
                                            'en':f"{self.opnng_en}contact you are going to delete",
                                            'ua':f"{self.opnng}контакт, який збираєтесь видалити"}},
                                    self.remove_contact_finish:{}}},
                            'remove_phone':{
                                'description':{
                                    'en':"Deletes one of the phone numbers of the chosen contact.",
                                    'ua':"Видаляє один з номерів телефону обраного контакту."}, 
                                'methods':{
                                    self.print_contacts:{},
                                    self.choose_contact_from_the_list:{
                                        'attr_id':{
                                            'en':f"{self.opnng_en}contact, where the phone number is",
                                            'ua':f"{self.opnng}контакт, у якому знаходиться номер телефону"}},
                                    self.print_contact_phones:{},
                                    self.choose_contact_phone:{
                                        'attr_id':{
                                            'en':f"{self.opnng_en}the phone number you are going to delete",
                                            'ua':f"{self.opnng}номер телефону, який ви збираєтеся видалити"}},
                                    self.remove_contact_phone_finish:{}}},
                            'show_all':{
                                'description':{
                                    'en':"Displays the contents of the contact book.",
                                    'ua':"Виводить всі контакти, які є в книзі."}, 
                                'methods':{
                                    self.show_contacts:{}}}}
  
        
    def show_upcoming_birthdays(self, number):
        days_ahead = 0
        if self.dialogue_check(number):
            try:
                days_ahead = int(number)
                days_ahead = (datetime(date.today().year,date.today().month,date.today().day) + timedelta(days=int(number))).date()
            except ValueError:
                error_text = {'en':f"{bcolors.YELLOW}Error! Number of days must be a valid number{bcolors.GREEN}",'ua':f"{bcolors.YELLOW}Помилка! Кількість днів має бути числом!{bcolors.GREEN}"}
                return error_text[self.language] 
        
        upcoming_birthdays = []
        for record_id, record in self.data.items():
            result = record.days_to_birthday(mode='no_math')
            if result != "None" and result <= days_ahead:
                    upcoming_birthdays.append(record_id)
        if upcoming_birthdays != []:
            error_text = {'en':f"{bcolors.GREEN}Contacts, which have a birthday in the next {bcolors.RED}{number}{bcolors.GREEN} days:",'ua':f"{bcolors.GREEN}Контакти у яких день народження протягом наступних {bcolors.RED}{number}{bcolors.GREEN} днів від сьогоднішньої дати:"}
            print(error_text[self.language])
            for i in upcoming_birthdays:
                print(f"{self.data[i]}")
        else:
            error_text = {'en':f"{bcolors.YELLOW}No contacts found, with a birthday in the next {bcolors.RED}{number}{bcolors.YELLOW} days:",'ua':f"{bcolors.YELLOW}Немає контактів у яких день народження протягом наступних {bcolors.RED}{number}{bcolors.YELLOW}  днів від сьогоднішньої дати."}
            print(error_text[self.language])

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
    # If mode == add, adding record to file. If mode == 'del', removes the record by id, overwrites saved data with the new parsed self.data. 
    # With "ed", overwrites saved data with the new parsed self.data
    def update_file(self,mode:str,r_id=None):
        import pickle
        from pathlib import Path
        file = Path(self.file)
        if not file.exists():
            with open(file, 'wb') as storage:
                #print("No data to load! Creating new file!")
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
                    error_text = {'en':f"{bcolors.YELLOW}Contact list is empty!{bcolors.GREEN}",'ua':f"{bcolors.YELLOW}Список контактів порожній!{bcolors.GREEN}"}
                    print(error_text[self.language])
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
                        #print('Reached the end of file!')

    def contact_create(self):
        new_record = RecordManager()
        new_record.language = self.language
        self.id_assign(mode="add",record=new_record)

    def add_name(self,name):
        record = self.data[self.ongoing]
        record.language = self.language
        if self.dialogue_check(name):
            try:
                record.add_name(name)
            except ValueError as error_text:
                return str(error_text)
            
            return True

    def add_phone(self,phone):
        record = self.data[self.ongoing]
        record.language = self.language
        if self.dialogue_check(phone):
            try:
                record.phone_check_and_set(mode='add', phone=phone)
            except ValueError as error_text:
                return str(error_text)

        return True

    def add_birthday(self,birthday):
        record = self.data[self.ongoing]
        record.language = self.language
        if self.dialogue_check(birthday):
            try:
                record.add_birthday(birthday)
            except ValueError as error_text:
                return str(error_text)

            return True

    def add_email(self,email):
        record = self.data[self.ongoing]
        record.language = self.language
        if self.dialogue_check(email):
            try:
                record.add_email(email)
            except ValueError as error_text:
                return str(error_text)

            return True

    def add_address(self,address):
        record = self.data[self.ongoing]
        record.language = self.language
        if self.dialogue_check(address):
            try:
                record.add_address(address)
            except ValueError as error_text:
                return str(error_text)

            return True

    def print_contacts(self):
        if len(self.data) > 0:
            local = {'part_0':{'en':"Saved contacts list", 'ua':"Наразі збережені такі контакти"},
                    'part_1':{'en':"Contact name", 'ua':"Ім'я контакту"},
                    'part_2':{'en':"phone numbers",'ua':"номера телефонів"},
                    'part_3':{'en':"birthday",'ua':"день народження"},
                    'part_4':{'en':"email",'ua':"електронна пошта"},
                    'part_5':{'en':"address",'ua':"адреса"},
                    'part_6':{'en':"To choose the contact, enter it's respective number in a console", 'ua':"Щоб обрати контакт, введіть у консоль його номер у списку"},}
            string = f"{bcolors.GREEN}{local['part_0'][self.language]}:\n"
            string += '\n'.join(f"{bcolors.RED}{key}{bcolors.GREEN}. {local['part_1'][self.language]}: {record.name}; {local['part_2'][self.language]}: {'; '.join(f'{phone}' for phone in record.phones.values())}; {local['part_3'][self.language]}: {record.birthday}; {local['part_4'][self.language]}: {record.email}; {local['part_5'][self.language]}: {record.address};" for key, record in self.data.items())
            print(string)
        else:
            error_text = {'en':f"{bcolors.YELLOW}Contact list is empty!{bcolors.GREEN}",'ua':f"{bcolors.YELLOW}Список контактів порожній!{bcolors.GREEN}"}
            print(error_text[self.language])
            return 'abort'

    def show_contacts(self):
        if len(self.data) > 0:
            local = {'part_0':{'en':"Saved contacts list", 'ua':"Наразі збережені такі контакти"},
                    'part_1':{'en':"Contact name", 'ua':"Ім'я контакту"},
                    'part_2':{'en':"phone numbers",'ua':"номера телефонів"},
                    'part_3':{'en':"birthday",'ua':"день народження"},
                    'part_4':{'en':"email",'ua':"електронна пошта"},
                    'part_5':{'en':"address",'ua':"адреса"},
                    'part_6':{'en':"To choose the contact, enter it's respective number in a console", 'ua':"Щоб обрати контакт, введіть у консоль його номер у списку"},}
            string = f"{bcolors.GREEN}{local['part_0'][self.language]}:\n"
            string += '\n'.join(f"{bcolors.RED}{key}{bcolors.GREEN}. {local['part_1'][self.language]}: {record.name}; {local['part_2'][self.language]}: {'; '.join(f'{phone}' for phone in record.phones.values())}; {local['part_3'][self.language]}: {record.birthday}; {local['part_4'][self.language]}: {record.email}; {local['part_5'][self.language]}: {record.address};" for key, record in self.data.items())
            print(string)
        else:
            error_text = {'en':f"{bcolors.YELLOW}Contact list is empty!{bcolors.GREEN}",'ua':f"{bcolors.YELLOW}Список контактів порожній!{bcolors.GREEN}"}
            print(error_text[self.language])

    def print_contact_attributes(self):
        local = {'part_0':{'en':"Choose, what you are going to edit",'ua':"Оберіть, що ви хочете редагувати"},
                'part_1':{'en':"Contact name", 'ua':"Ім'я контакту"},
                'part_2':{'en':"Birthday",'ua':"День народження"},
                'part_3':{'en':"Email",'ua':"Електронну пошту"},
                'part_4':{'en':"Address",'ua':"Адресу"},
                'part_5':{'en':"Phone numbers",'ua':"Номера телефонів"}}
        string = f"{bcolors.GREEN}{local['part_0'][self.language]}:\n"
        string += f"{bcolors.RED}0{bcolors.GREEN}. {local['part_1'][self.language]}: {self.data[self.ongoing].name}\n"
        string += f"{bcolors.RED}1{bcolors.GREEN}. {local['part_2'][self.language]}: {self.data[self.ongoing].birthday}\n"
        string += f"{bcolors.RED}2{bcolors.GREEN}. {local['part_3'][self.language]}: {self.data[self.ongoing].email}\n"
        string += f"{bcolors.RED}3{bcolors.GREEN}. {local['part_4'][self.language]}: {self.data[self.ongoing].address}\n"
        #string += f"{bcolors.RED}5{bcolors.GREEN}. {local['part_5'][self.language]}: {self.data[self.ongoing].phones}\n"
        print(string)

    def choose_contact_from_the_list(self, contact_id):
        if len(self.data) > 0:
            try:
                contact_id = self.input_to_id(contact_id)
                if (type(contact_id) == int) and (contact_id in self.data.keys()):
                    self.ongoing = contact_id
                elif type(contact_id) == str:
                    return contact_id
                else:
                    raise ValueError
            except ValueError:
                error_text = {'en':f"{bcolors.YELLOW}There is no contact with this id, try again!{bcolors.GREEN}",'ua':f"{bcolors.YELLOW}Контакту з таким id немає, спробуйте ще раз!{bcolors.GREEN}"}
                return error_text[self.language]
        else:
            error_text = {'en':f"{bcolors.YELLOW}Contact list is empty!{bcolors.GREEN}",'ua':f"{bcolors.YELLOW}Список контактів порожній!{bcolors.GREEN}"}
            print(error_text[self.language])

    def choose_contact_attribute(self, field_id):
        try:
            field_id = self.input_to_id(field_id)
            if type(field_id) == int and field_id < 4:
                self.field_id = field_id
            elif type(field_id) == str:
                return field_id
            else:
                raise ValueError
        except:
                error_text = {'en':f"{bcolors.YELLOW}Wrong id, try again!{bcolors.GREEN}",'ua':f"{bcolors.YELLOW}Некоректний id, спробуйте ще раз!{bcolors.GREEN}"}
                return error_text[self.language]
           
    def edit_contact(self, new_text):
        self.data[self.ongoing].language = self.language
        local = [{'en':"Name", 'ua':"Iм'я"}, {'en':"Birthday", 'ua':"День народження"}, {'en':"Email", 'ua':"Електронну пошту"}, {'en':"Address", 'ua':"Адресу"}, {'en':"Phone", 'ua':"Телефон"}]
        done_text = {'en':f"{bcolors.GREEN}{local[self.field_id][self.language]} edited.",'ua':f"{bcolors.YELLOW}{local[self.field_id][self.language]} відредаговано.{bcolors.GREEN}"}
        if self.field_id == 0:
            try:
                self.data[self.ongoing].add_name(new_text)
            except ValueError as error_text:
                return str(error_text)
        elif self.field_id == 1:
            try:
                self.data[self.ongoing].add_birthday(new_text)
            except ValueError as error_text:
                return str(error_text)
        elif self.field_id == 2:
            try:
                self.data[self.ongoing].add_email(new_text)
            except ValueError as error_text:
                return str(error_text)
        elif self.field_id == 3:
            try:
                self.data[self.ongoing].add_address(new_text)
            except ValueError as error_text:
                return str(error_text)
        
        self.update_file(mode="ed")
        self.field_id = None
        self.ongoing = None
        print(done_text[self.language])

    def print_contact_phones(self):
        if len(self.data[self.ongoing].phones) > 0:
            local = {'en':"Choose the phone number you need", 'ua':"Оберіть потрібний номер телефону"}
            contact = self.data[self.ongoing]
            string = f"{bcolors.GREEN}{local[self.language]}:\n"
            string += "".join(f'{bcolors.RED}{phone_id}{bcolors.GREEN}. {phone_number};\n' for phone_id, phone_number in contact.phones.items())
            print(string)
        else:
            error_text = {'en':f"{bcolors.YELLOW}The contact has no saved phone numbers!{bcolors.GREEN}",'ua':f"{bcolors.YELLOW}Контакт не має збережених номерів телефону!{bcolors.GREEN}"}
            print(error_text[self.language])
            return 'abort'

    def input_to_id(self, text):
        map = {' ':'','\n':'','\t':'','\r':''}
        new_line = text.translate(map)
        try:
            if int(new_line) >= 0:
                return int(new_line)
            else:
                error_text = {'en':f"{bcolors.YELLOW}An id cannot be a negative number!{bcolors.GREEN}",'ua':f"{bcolors.YELLOW}Id не може бути від'ємним числом!{bcolors.GREEN}"}
                return error_text[self.language]
        except ValueError:
            error_text = {'en':f"{bcolors.YELLOW}Wrong id, try again!{bcolors.GREEN}",'ua':f"{bcolors.YELLOW}Некоректний id, спробуйте ще раз!{bcolors.GREEN}"}
            return error_text[self.language]

    def choose_contact_phone(self, field_id):
        contact = self.data[self.ongoing]
        try:
            field_id = self.input_to_id(field_id)
            if type(field_id) == int and field_id < len(contact.phones):
                self.field_id = field_id
            elif type(field_id) == str:
                return field_id
            else:
                raise ValueError
        except:
                error_text = {'en':f"{bcolors.YELLOW}Wrong id, try again!{bcolors.GREEN}",'ua':f"{bcolors.YELLOW}Некоректний id, спробуйте ще раз!{bcolors.GREEN}"}
                return error_text[self.language]
        
    def edit_phones(self, new_text):
        note = self.data[self.ongoing]
        note.language = self.language
        local = {'en':"Phone", 'ua':"Телефон"}
        done_text = {'en':f"{bcolors.YELLOW}{local[self.language]} edited.{bcolors.GREEN}",'ua':f"{bcolors.YELLOW}{local[self.language]} відредагований.{bcolors.GREEN}"}
        try:
            note.phone_check_and_set(mode='ed', phone=note.phones[self.field_id], new_phone=new_text)
        except ValueError as error_text:
            return str(error_text)
        
        self.update_file(mode="ed")
        self.field_id = None
        self.ongoing = None
        print(done_text[self.language])

    def add_contact_finish(self):
        record = self.data[self.ongoing]
        local = {'part_1':{'en':"Contact created with name",'ua':"Контакт створено з ім'ям"},
                'part_2':{'en':"phone numbers",'ua':"номерами телефону"},
                'part_3':{'en':"birthday",'ua':"днем народження"},
                'part_4':{'en':"email",'ua':"електронною поштою"},
                'part_5':{'en':"address",'ua':"адресою"}}
        string = f"{bcolors.YELLOW}{local['part_1'][self.language]}: {record.name}; {local['part_2'][self.language]}: {'; '.join(f'{v}' for k,v in record.phones.items())}; {local['part_3'][self.language]}: {record.birthday}; {local['part_4'][self.language]}: {record.email}; {local['part_5'][self.language]}: {record.address}"
        print(string)
            
        self.update_file(mode="add",r_id=self.generated_ids)
        self.ongoing = None

    def remove_contact_finish(self):
        done_text = {'en':f"{bcolors.YELLOW}Contact removed.{bcolors.GREEN}",'ua':f"{bcolors.YELLOW}Контакт видалений.{bcolors.GREEN}"}
        print(done_text[self.language])
        self.update_file(mode="del", r_id=self.ongoing)
        self.ongoing = None

    def remove_contact_phone_finish(self):
        del self.data[self.ongoing].phones[self.field_id]
        done_text = {'en':f"{bcolors.YELLOW}Phone removed.{bcolors.GREEN}",'ua':f"{bcolors.YELLOW}Телефон видалений.{bcolors.GREEN}"}
        print(done_text[self.language])
        self.update_file(mode="ed", r_id=self.ongoing)
        self.ongoing = None
        self.field_id = None

    def add_phone_finish(self):
        self.update_file(mode="ed")
        self.field_id = None
        self.ongoing = None
  
    def remove_phone_finish(self):
        note = self.data[self.ongoing]
        note.language = self.language
        try:
            note.phone_check_and_set(mode='del', phone=self.field_id)
        except ValueError as error_text:
            return str(error_text)
        
        self.update_file(mode="ed")
        self.field_id = None
        self.ongoing = None
        
    def print_find_modes(self):
        local = {'part_0':{
                    'en':"Choose, where you want to look for the text",
                    'ua':"Оберіть, де ви хочете шукати текст"},
                'part_1':{
                    'en':"In the names.",
                    'ua':"У іменах."},
                'part_2':{
                    'en':"In the birthdays.",
                    'ua':"У днях народження."},
                'part_3':{
                    'en':"In the emails.",
                    'ua':"У електронних поштах."},
                'part_4':{
                    'en':"In the addresses.",
                    'ua':"У адресах."},
                'part_5':{
                    'en':"In the phones.",
                    'ua':"У телефонах."},
                'part_6':{
                    'en':"Everywhere.",
                    'ua':"Всюди."}}
        
        string = f"{bcolors.GREEN}{local['part_0'][self.language]}:\n"
        string += f"{bcolors.RED}0{bcolors.GREEN}. {local['part_1'][self.language]}\n{bcolors.RED}1{bcolors.GREEN}. {local['part_2'][self.language]}\n{bcolors.RED}2{bcolors.GREEN}. {local['part_3'][self.language]}\n{bcolors.RED}3{bcolors.GREEN}. {local['part_4'][self.language]}\n{bcolors.RED}4{bcolors.GREEN}. {local['part_5'][self.language]}\n{bcolors.RED}5{bcolors.GREEN}. {local['part_6'][self.language]}\n"
        print(string)

    def choose_find_mode(self, field_id):
        try:
            field_id = self.input_to_id(field_id)
            if type(field_id) == int and field_id <= 5:
                self.field_id = field_id
            elif type(field_id) == str:
                 return field_id
            else:
                raise ValueError
        except:
                error_text = {'en':f"{bcolors.YELLOW}Wrong id, try again!{bcolors.GREEN}",'ua':f"{bcolors.YELLOW}Некоректний id, спробуйте ще раз!{bcolors.GREEN}"}
                return error_text[self.language]
        
    def find_hub(self, text):
        checker = False
        string = ""
        local = {'Failure':{'en':f"Specified text not found",'ua':f"Вказаний текст не знайдено"},'Intro':{'en':f"Specified text found in the next contacts",'ua':f"Вказаний текст знайдено у наступних контактах"},'Name':{'en':f"name",'ua':f"Ім'я"},'Birthday':{'en':f"birthday",'ua':f"день народження"},'Email':{'en':f"email",'ua':f"електронна пошта"},'Address':{'en':f"address",'ua':f"електронна пошта"},'Phones':{'en':f"phones",'ua':f"номери телефону"}}
        success = f"{bcolors.YELLOW}{local['Intro'][self.language]}:{bcolors.GREEN}\n"
        failure = f"{bcolors.YELLOW}{local['Failure'][self.language]}!{bcolors.GREEN}"
        highlighted_name = ''
        highlighted_birthday = ''
        highlighted_email = ''
        highlighted_address = ''
        highlighted_phones = ''
        if self.field_id == 0:
            for contact_id,class_instance in self.data.items():
                if class_instance.find_in_name(text):
                    checker = True
                    highlighted_name = f"{bcolors.GREEN}{class_instance.name[:class_instance.find_in_name(text)[0]]}{bcolors.YELLOW}{class_instance.name[class_instance.find_in_name(text)[0]:class_instance.find_in_name(text)[1]]}{bcolors.GREEN}{class_instance.name[class_instance.find_in_name(text)[1]:]}"
                    string += f"{bcolors.RED}{contact_id}{bcolors.GREEN}. {local['Name'][self.language]}: {highlighted_name}; {local['Phones'][self.language]}: {class_instance.phones}; {local['Birthday'][self.language]}: {class_instance.birthday}; {local['Email'][self.language]}: {class_instance.email}; {local['Address'][self.language]}: {class_instance.address};\n"
        elif self.field_id == 1:
            for contact_id,class_instance in self.data.items():
                if class_instance.find_in_birthday(text):
                    checker = True
                    highlighted_birthday = f"{bcolors.GREEN}{class_instance.birthday[:class_instance.find_in_birthday(text)[0]]}{bcolors.YELLOW}{class_instance.birthday[class_instance.find_in_birthday(text)[0]:class_instance.find_in_birthday(text)[1]]}{bcolors.GREEN}{class_instance.birthday[class_instance.find_in_birthday(text)[1]:]}"
                    string += f"{bcolors.RED}{contact_id}{bcolors.GREEN}. {local['Name'][self.language]}: {class_instance.name}; {local['Phones'][self.language]}: {class_instance.phones}; {local['Birthday'][self.language]}: {highlighted_birthday}; {local['Email'][self.language]}: {class_instance.email}; {local['Address'][self.language]}: {class_instance.address};\n"
        elif self.field_id == 2:
            for contact_id,class_instance in self.data.items():
                if class_instance.find_in_email(text):
                    checker = True
                    highlighted_email = f"{bcolors.GREEN}{class_instance.email[:class_instance.find_in_email(text)[0]]}{bcolors.YELLOW}{class_instance.email[class_instance.find_in_email(text)[0]:class_instance.find_in_email(text)[1]]}{bcolors.GREEN}{class_instance.email[class_instance.find_in_email(text)[1]:]}"
                    string += f"{bcolors.RED}{contact_id}{bcolors.GREEN}. {local['Name'][self.language]}: {class_instance.name}; {local['Phones'][self.language]}: {class_instance.phones}; {local['Birthday'][self.language]}: {class_instance.birthday}; {local['Email'][self.language]}: {highlighted_email}; {local['Address'][self.language]}: {class_instance.address};\n"
        elif self.field_id == 3:
            for contact_id,class_instance in self.data.items():
                if class_instance.find_in_address(text):
                    checker = True
                    highlighted_address = f"{bcolors.GREEN}{class_instance.address[:class_instance.find_in_address(text)[0]]}{bcolors.YELLOW}{class_instance.address[class_instance.find_in_address(text)[0]:class_instance.find_in_address(text)[1]]}{bcolors.GREEN}{class_instance.address[class_instance.find_in_address(text)[1]:]}"
                    string += f"{bcolors.RED}{contact_id}{bcolors.GREEN}. {local['Name'][self.language]}: {class_instance.name}; {local['Phones'][self.language]}: {class_instance.phones}; {local['Birthday'][self.language]}: {class_instance.birthday}; {local['Email'][self.language]}: {class_instance.email}; {local['Address'][self.language]}: {highlighted_address};\n"
        elif self.field_id == 4:
            for contact_id,class_instance in self.data.items():
                if class_instance.find_in_phones(text):
                    checker = True
                    phones = "; ".join(f"{phone_number}" for phone_id,phone_number in class_instance.phones.items())
                    highlighted_phones = f"{bcolors.GREEN}{phones[:class_instance.find_in_phones(text)[0]]}{bcolors.YELLOW}{phones[class_instance.find_in_phones(text)[0]:class_instance.find_in_phones(text)[1]]}{bcolors.GREEN}{phones[class_instance.find_in_phones(text)[1]:]}"
                    string += f"{bcolors.RED}{contact_id}{bcolors.GREEN}. {local['Name'][self.language]}: {class_instance.name}; {local['Phones'][self.language]}: {highlighted_phones}; {local['Birthday'][self.language]}: {class_instance.birthday}; {local['Email'][self.language]}: {class_instance.email}; {local['Address'][self.language]}: {class_instance.address};\n"
        elif self.field_id == 5:
            for contact_id,class_instance in self.data.items():
                if class_instance.find_in_name(text):
                    checker = True
                    highlighted_name = f"{bcolors.GREEN}{class_instance.name[:class_instance.find_in_name(text)[0]]}{bcolors.YELLOW}{class_instance.name[class_instance.find_in_name(text)[0]:class_instance.find_in_name(text)[1]]}{bcolors.GREEN}{class_instance.name[class_instance.find_in_name(text)[1]:]}"
                    string += f"{bcolors.RED}{contact_id}{bcolors.GREEN}. {local['Name'][self.language]}: {highlighted_name}; {local['Phones'][self.language]}: {class_instance.phones}; {local['Birthday'][self.language]}: {class_instance.birthday}; {local['Email'][self.language]}: {class_instance.email}; {local['Address'][self.language]}: {class_instance.address};\n"
                elif class_instance.find_in_birthday(text):
                    checker = True
                    highlighted_birthday = f"{bcolors.GREEN}{class_instance.birthday[:class_instance.find_in_birthday(text)[0]]}{bcolors.YELLOW}{class_instance.birthday[class_instance.find_in_birthday(text)[0]:class_instance.find_in_birthday(text)[1]]}{bcolors.GREEN}{class_instance.birthday[class_instance.find_in_birthday(text)[1]:]}"
                    string += f"{bcolors.RED}{contact_id}{bcolors.GREEN}. {local['Name'][self.language]}: {class_instance.name}; {local['Phones'][self.language]}: {class_instance.phones}; {local['Birthday'][self.language]}: {highlighted_birthday}; {local['Email'][self.language]}: {class_instance.email}; {local['Address'][self.language]}: {class_instance.address};\n"
            for contact_id,class_instance in self.data.items():
                if class_instance.find_in_email(text):
                    checker = True
                    highlighted_email = f"{bcolors.GREEN}{class_instance.email[:class_instance.find_in_email(text)[0]]}{bcolors.YELLOW}{class_instance.email[class_instance.find_in_email(text)[0]:class_instance.find_in_email(text)[1]]}{bcolors.GREEN}{class_instance.email[class_instance.find_in_email(text)[1]:]}"
                    string += f"{bcolors.RED}{contact_id}{bcolors.GREEN}. {local['Name'][self.language]}: {class_instance.name}; {local['Phones'][self.language]}: {class_instance.phones}; {local['Birthday'][self.language]}: {class_instance.birthday}; {local['Email'][self.language]}: {highlighted_email}; {local['Address'][self.language]}: {class_instance.address};\n"
            for contact_id,class_instance in self.data.items():
                if class_instance.find_in_address(text):
                    checker = True
                    highlighted_address = f"{bcolors.GREEN}{class_instance.address[:class_instance.find_in_address(text)[0]]}{bcolors.YELLOW}{class_instance.address[class_instance.find_in_address(text)[0]:class_instance.find_in_address(text)[1]]}{bcolors.GREEN}{class_instance.address[class_instance.find_in_address(text)[1]:]}"
                    string += f"{bcolors.RED}{contact_id}{bcolors.GREEN}. {local['Name'][self.language]}: {class_instance.name}; {local['Phones'][self.language]}: {class_instance.phones}; {local['Birthday'][self.language]}: {class_instance.birthday}; {local['Email'][self.language]}: {class_instance.email}; {local['Address'][self.language]}: {highlighted_address};\n"
                elif class_instance.find_in_phones(text):
                    checker = True
                    phones = "; ".join(f"{phone_number}" for phone_id,phone_number in class_instance.phones.items())
                    highlighted_phones = f"{bcolors.GREEN}{phones[:class_instance.find_in_phones(text)[0]]}{bcolors.YELLOW}{phones[class_instance.find_in_phones(text)[0]:class_instance.find_in_phones(text)[1]]}{bcolors.GREEN}{phones[class_instance.find_in_phones(text)[1]:]}"
                    string += f"{bcolors.RED}{contact_id}{bcolors.GREEN}. {local['Name'][self.language]}: {class_instance.name}; {local['Phones'][self.language]}: {highlighted_phones}; {local['Birthday'][self.language]}: {class_instance.birthday}; {local['Email'][self.language]}: {class_instance.email}; {local['Address'][self.language]}: {class_instance.address};\n"

        if checker:
            print(f"{success}{string}")
        else:
            print(f"{failure}")

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
