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
    def __init__(self, parent_class):
        self.parent = parent_class
        self.parent.modules.append(self)
        self.parent.module_chosen = len(self.parent.modules) - 1
        self.reinit(mode='first')
        self.data = {}
        self.priority_ids = []
        self.record_cnt = 0
        self.generated_ids = 0
        self.file = "storage.bin"
        self.update_file("load",0)

    def reinit(self, mode=None):
        tmp = None
        if type(self.parent.module_chosen) == int:
            tmp = self.parent.module_chosen
        if mode != 'first':
            self.parent.module_chosen = self.parent.modules.index(self)
        self.confirmation = f"{self.parent.translate_string('please_enter_confirm_p0')} {self.parent.translate_string('confirm','red','cyan')}/{self.parent.translate_string('confirm_long','red','cyan')} {self.parent.translate_string('please_enter_confirm_p1')} {self.parent.translate_string('please_enter_confirm_p2')} {self.parent.translate_string('deny','red','cyan')}/{self.parent.translate_string('deny_long','red','cyan')} {self.parent.translate_string('please_enter_confirm_p3')}"
        self.opnng = f"{self.parent.translate_string('please_enter_p0','cyan')} "
        self.opnng_alt = f"{self.parent.translate_string('please_enter_p0_1','cyan')} "
        self.non_obligatory = f"{bcolors.CYAN} ({self.parent.translate_string('please_enter_p1')} '{self.parent.translate_string('please_enter_p2','red','cyan')}'{self.parent.translate_string('please_enter_p3')})"
        self.method_table = {'__localization':{
                                'name':"contact_manager_name",
                                'description':"contact_manager_desc"},
                            'create':{
                                'description':"create_desc", 
                                'methods':{
                                    self.contact_create:{},
                                    self.add_name:{
                                        'name':f"{self.opnng}{self.parent.translate_string('enter_name')}{self.non_obligatory}"},
                                    self.add_phone:{
                                        'phone':f"{self.opnng}{self.parent.translate_string('enter_phone_number')}{self.non_obligatory}"},
                                    self.add_birthday:{
                                        'birthday':f"{self.opnng}{self.parent.translate_string('enter_birthday')}{self.non_obligatory}"},
                                    self.add_email:{
                                        'email':f"{self.opnng}{self.parent.translate_string('enter_email')}{self.non_obligatory}"},
                                    self.add_address:{
                                        'address':f"{self.opnng}{self.parent.translate_string('enter_address')}{self.non_obligatory}"},
                                    self.add_contact_finish:{}}},
                            'check_birthdays':{
                                'description':"check_birthdays_desc", 
                                'methods':{
                                    self.show_upcoming_birthdays:{
                                        'attr_id':f"{self.opnng}{self.parent.translate_string('enter_days_number')}"}}},
                            'edit':{
                                'description':"edit_desc", 
                                'methods':{
                                    self.print_contacts:{},
                                    self.choose_contact_from_the_list:{
                                        'note_id':f"{self.opnng_alt}{self.parent.translate_string('choose_contact_to_edit')}"},
                                    self.print_contact_attributes:{},
                                    self.choose_contact_attribute_edit:{
                                        'attr_id':f"{self.opnng_alt}{self.parent.translate_string('enter_edit')}"},
                                    }},
                            'edit_phone':{
                                'description':"edit_phone_desc", 
                                'technical':True,
                                'methods':{
                                    self.print_edit_phone_options:{},
                                    self.choose_edit_phone_option:{
                                        'attr_id':f"{self.opnng_alt}{self.parent.translate_string('choose_phone_edit_option')}"},
                                    }},
                            'edit_phone_true':{
                                'description':"edit_phone_desc", 
                                'technical':True,
                                'methods':{
                                    self.print_contact_phones:{},
                                    self.choose_contact_phone:{
                                        'attr_id':f"{self.opnng_alt}{self.parent.translate_string('choose_contact_phone')}"},
                                    self.edit_phones:{
                                        'new_text':f"{self.opnng}{self.parent.translate_string('enter_new_phone')}"},
                                    }},
                            'edit_other':{
                                'description':"edit_phone_desc", 
                                'technical':True,
                                'methods':{
                                    self.edit_contact:{
                                        'new_text':f"{self.opnng}{self.parent.translate_string('enter_new_text')}"}
                                    }},
                            'add_phone':{
                                'description':"add_phone_desc", 
                                'technical':True,
                                'methods':{
                                    self.add_phone:{
                                        'attr_id':f"{self.opnng}{self.parent.translate_string('phone_number_add')}"},
                                    self.add_phone_finish:{},
                                    }},
                            'find':{
                                'description':"find_desc", 
                                'methods':{
                                    self.print_find_modes:{},
                                    self.choose_find_mode:{
                                        'attr_id':f"{self.opnng}{self.parent.translate_string('choose_search_mode')}"},
                                    self.find_hub:{
                                        'attr_id':f"{self.opnng}{self.parent.translate_string('enter_text_to_find')}"}}},
                            'remove':{
                                'description':"remove_desc", 
                                'methods':{
                                    self.print_contacts:{},
                                    self.choose_contact_from_the_list:{
                                        'attr_id':f"{self.opnng_alt}{self.parent.translate_string('choose_contact')}"},
                                    self.print_delete_options:{},
                                    self.choose_remove_option_from_the_list:{
                                        'attr_id':f"{self.opnng_alt}{self.parent.translate_string('enter_remove')}"}}},
                            'remove_contact':{
                                'description':"remove_desc", 
                                'technical':True,
                                'methods':{
                                    self.remove_contact_ask:{},
                                    self.remove_contact_submit:{
                                        'attr_id':self.confirmation}}},
                            'remove_attributes':{
                                'description':"remove_desc", 
                                'technical':True,
                                'methods':{
                                    self.print_contact_attributes:{},
                                    self.choose_contact_attribute_remove:{
                                        'attr_id':f"{self.opnng_alt}{self.parent.translate_string('enter_edit')}"}}},
                            'remove_other':{
                                'description':"remove_desc", 
                                'technical':True,
                                'methods':{
                                    self.remove_attribute_ask:{},
                                    self.remove_attribute_submit:{
                                        'attr_id':self.confirmation}}},
                            'remove_phone':{
                                'description':"remove_phone_desc", 
                                'technical':True,
                                'methods':{
                                    self.print_contact_phones:{},
                                    self.choose_contact_phone:{
                                        'attr_id':f"{self.opnng_alt}{self.parent.translate_string('choose_phone_to_delete')}"},
                                    self.remove_phone_ask:{},
                                    self.remove_phone_submit:{
                                        'attr_id':self.confirmation}}},
                            'show_all':{
                                'description':"show_all_desc", 
                                'methods':{
                                    self.show_contacts:{}}}}
        if mode != 'first':
            self.parent.module_chosen = tmp
  
    def show_upcoming_birthdays(self, number):
        days_ahead = 0
        if self.dialogue_check(number):
            try:
                days_ahead = int(number)
                days_ahead = (datetime(date.today().year,date.today().month,date.today().day) + timedelta(days=int(number))).date()
            except ValueError:
                return self.parent.translate_string('invalid_day_error','yellow','green')
        
        upcoming_birthdays = []
        for record_id, record in self.data.items():
            result = record.days_to_birthday(mode='no_math')
            if result != "None" and result <= days_ahead:
                    upcoming_birthdays.append(record_id)
        if upcoming_birthdays != []:
            print(f"{self.parent.translate_string('found_birthdays_p0','green','red')} {number} {self.parent.translate_string('found_birthdays_p1','green')}")
            for i in upcoming_birthdays:
                print(f"{self.data[i]}")
        else:
            print(f"{self.parent.translate_string('not_found_birthdays_p0','yellow','red')} {number} {self.parent.translate_string('not_found_birthdays_p1','yellow','green')}")

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
                    #print(self.parent.translate_string('contact_list_empty','yellow','green'))
                    pass
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
                        from CodeCrafters_assistant.record_manager import RecordManager
                        while True:  
                            record = pickle.load(storage)
                            self.data[id_generator] = RecordManager(parent_class=self.parent)
                            self.data[id_generator].load_data(name=record['Name'],phones=record['Phones'],birthday=record['Birthday'],email=record['Email'],address=record['Address'])
                            id_generator += 1
                    except EOFError:
                        self.generated_ids = id_generator
                        self.record_cnt = id_generator
                        #print('Reached the end of file!')

    def contactbook_error(func):
        def true_handler(self,arg):
            try:
                result = func(self,arg)
            except ValueError as error_text:
                return str(error_text)
        return true_handler

    def contact_create(self):
        from CodeCrafters_assistant.record_manager import RecordManager
        new_record = RecordManager(parent_class=self.parent)
        self.id_assign(mode="add",record=new_record)

    @contactbook_error
    def add_name(self,name):
        record = self.data[self.ongoing]
        if self.dialogue_check(name):
            record.add_name(name)

    @contactbook_error
    def add_phone(self,phone):
        record = self.data[self.ongoing]
        if self.dialogue_check(phone):
            record.phone_check_and_set(mode='add', phone=phone)

    @contactbook_error
    def add_birthday(self,birthday):
        record = self.data[self.ongoing]
        if self.dialogue_check(birthday):
            record.add_birthday(birthday)

    @contactbook_error
    def add_email(self,email):
        record = self.data[self.ongoing]
        if self.dialogue_check(email):
            record.add_email(email)

    @contactbook_error
    def add_address(self,address):
        record = self.data[self.ongoing]
        if self.dialogue_check(address):
            record.add_address(address)

    def print_contacts(self):
        if len(self.data) > 0:
            string = self.parent.translate_string('print_contacts','green')
            string += ":\n" + '\n'.join(f"{bcolors.RED}{key}{bcolors.GREEN}. {self.parent.translate_string('contact_attr_p1','red','green')}: {record.name}; {self.parent.translate_string('contact_attr_p2','red','green')}: {record.birthday}; {self.parent.translate_string('contact_attr_p3','red','green')}: {record.email}; {self.parent.translate_string('contact_attr_p4','red','green')}: {record.address}; {self.parent.translate_string('contact_attr_p5','red','green')}: {'; '.join(f'{phone}' for phone in record.phones.values())};" for key, record in self.data.items())
            print(string)
        else:
            print(self.parent.translate_string('contact_list_empty','yellow','green'))
            return 'abort'

    def show_contacts(self):
        if len(self.data) > 0:
            string = self.parent.translate_string('print_contacts','green')
            string += ":\n" + '\n'.join(f"{bcolors.RED}{key}{bcolors.GREEN}. {self.parent.translate_string('contact_attr_p1','red','green')}: {record.name}; {self.parent.translate_string('contact_attr_p2','red','green')}: {record.birthday}; {self.parent.translate_string('contact_attr_p3','red','green')}: {record.email}; {self.parent.translate_string('contact_attr_p4','red','green')}: {record.address}; {self.parent.translate_string('contact_attr_p5','red','green')}: {'; '.join(f'{phone}' for phone in record.phones.values())};" for key, record in self.data.items())
            print(string)
        else:
            print(self.parent.translate_string('contact_list_empty','yellow','green'))

    def print_edit_phone_options(self):
        string = f"{self.parent.translate_string('how_to_edit_phone_p0','green')}\n{bcolors.RED}0{bcolors.GREEN}. {self.parent.translate_string('how_to_edit_phone_p1')}\n{bcolors.RED}1{bcolors.GREEN}. {self.parent.translate_string('how_to_edit_phone_p2')}\n"
        print(string)

    def choose_edit_phone_option(self, option):
        try:
            option = self.input_to_id(option)
            if (type(option) == int) and option == 0:
                self.parent.start_script('edit_phone_true', mode='technical')
            elif (type(option) == int) and option == 1:
                self.parent.start_script('add_phone', mode='technical')
            elif type(option) == str:
                return option
            else:
                raise ValueError
        except ValueError:
            return self.parent.translate_string('wrong_id_error','yellow','green')

    def print_delete_options(self):
        string = f"{self.parent.translate_string('what_to_delete_p0','green')}\n{bcolors.RED}0{bcolors.GREEN}. {self.parent.translate_string('what_to_delete_p1')}\n{bcolors.RED}1{bcolors.GREEN}. {self.parent.translate_string('what_to_delete_p2')}\n"
        print(string)

    def choose_remove_option_from_the_list(self, option):
        try:
            option = self.input_to_id(option)
            if (type(option) == int) and option == 0:
                self.parent.start_script('remove_contact', mode='technical')
            elif (type(option) == int) and option == 1:
                self.parent.start_script('remove_attributes', mode='technical')
            elif type(option) == str:
                return option
            else:
                raise ValueError
        except ValueError:
            return self.parent.translate_string('wrong_id_error','yellow','green')

    def print_contact_attributes(self):
        record = self.data[self.ongoing]
        string = self.parent.translate_string('print_contact_attr_p0','green')
        string += f":\n{bcolors.RED}0{bcolors.GREEN}. {self.parent.translate_string('print_contact_attr_p1')}: {record.name}\n"
        string += f"{bcolors.RED}1{bcolors.GREEN}. {self.parent.translate_string('print_contact_attr_p2')}: {record.birthday}\n"
        string += f"{bcolors.RED}2{bcolors.GREEN}. {self.parent.translate_string('print_contact_attr_p3')}: {record.email}\n"
        string += f"{bcolors.RED}3{bcolors.GREEN}. {self.parent.translate_string('print_contact_attr_p4')}: {record.address}\n"
        string += f"{bcolors.RED}4{bcolors.GREEN}. {self.parent.translate_string('print_contact_attr_p5')}: {'; '.join(phone for phone in record.phones.values())}\n"
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
                return self.parent.translate_string('contact_id_not_found','yellow','green')
        else:
            print(self.parent.translate_string('contact_list_empty','yellow','green'))

    def choose_contact_attribute_edit(self, field_id):
        try:
            field_id = self.input_to_id(field_id)
            if type(field_id) == int and field_id == 4:
                self.field_id = field_id
                self.parent.start_script('edit_phone', mode='technical')
            elif type(field_id) == int and field_id < 4:
                self.field_id = field_id
                self.parent.start_script('edit_other', mode='technical')
            elif type(field_id) == str:
                return field_id
            else:
                raise ValueError
        except ValueError:
            print(self.parent.translate_string('wrong_id_error','yellow','green'))

    def choose_contact_attribute_remove(self, field_id):
        try:
            field_id = self.input_to_id(field_id)
            if type(field_id) == int and field_id == 4:
                self.field_id = field_id
                self.parent.start_script('remove_phone', mode='technical')
            elif type(field_id) == int and field_id < 4:
                self.field_id = field_id
                self.parent.start_script('remove_other', mode='technical')
            elif type(field_id) == str:
                return field_id
            else:
                raise ValueError
        except ValueError:
            print(self.parent.translate_string('wrong_id_error','yellow','green'))

    def remove_phone_ask(self):
        print(f"{self.parent.translate_string('remove_attribute_ask_p0','yellow','red')} {self.parent.translate_string('contact_attr_p5_1','red')} {self.parent.translate_string('remove_attribute_ask_p1','yellow','red')} ( {self.data[self.ongoing].phones[self.field_id]} )")

    def remove_phone_submit(self, answer:str):
        record = self.data[self.ongoing]
        if answer.lower().strip() in self.parent.confirm:
            #del self.data[self.ongoing].phones[self.field_id]
            record.phone_check_and_set(mode='del',phone=record.phones[self.field_id])
            #note.phone_check_and_set(mode='del', phone=self.field_id)
            self.update_file(mode="ed")
            self.ongoing = None
            self.field_id = None
            return
        elif answer.lower().strip() in self.parent.deny:
            print(self.parent.translate_string('contact_remove_abort','yellow','green'))
            return

        return ' '
    
    def remove_attribute_ask(self):
        ref_dict = ['contact_attr_p1','contact_attr_p2','contact_attr_p3','contact_attr_p4']
        print(f"{self.parent.translate_string('remove_attribute_ask_p0','yellow')} {self.parent.translate_string(ref_dict[self.field_id],'red')} {self.parent.translate_string('remove_attribute_ask_p1','yellow','green')}")

    def remove_attribute_submit(self, answer:str):
        record = self.data[self.ongoing]
        if answer.lower().strip() in self.parent.confirm:
            if self.field_id == 0:
                record.remove_name()
            elif self.field_id == 1:
                record.remove_birthday()
            elif self.field_id == 2:
                record.remove_email()
            elif self.field_id == 3:
                record.remove_address()
            self.update_file(mode="ed")
            self.ongoing = None
            self.field_id = None
            return
        elif answer.lower().strip() in self.parent.deny:
            print(self.parent.translate_string('contact_remove_abort','yellow','green'))
            return

        return ' '
    

    @contactbook_error
    def edit_contact(self, new_text):
        local = ["contact_attr_p1", "contact_attr_p2", "contact_attr_p3", "contact_attr_p4", "contact_attr_p5_1"]
        if self.field_id == 0:
            self.data[self.ongoing].add_name(new_text)
        elif self.field_id == 1:
            self.data[self.ongoing].add_birthday(new_text)
        elif self.field_id == 2:
            self.data[self.ongoing].add_email(new_text)
        elif self.field_id == 3:
            self.data[self.ongoing].add_address(new_text)
        
        self.update_file(mode="ed")
        print(f"{self.parent.translate_string(local[self.field_id],'yellow')} {self.parent.translate_string('edit_contact_p1','yellow','green')}")
        self.field_id = None
        self.ongoing = None

    def print_contact_phones(self):
        if len(self.data[self.ongoing].phones) > 0:
            contact = self.data[self.ongoing]
            string = self.parent.translate_string('choose_the_phone','green')
            string += ":\n" + "".join(f'{bcolors.RED}{phone_id}{bcolors.GREEN}. {phone_number};\n' for phone_id, phone_number in contact.phones.items())
            print(string)
        else:
            print(self.parent.translate_string('no_phone_numbers_error','yellow','green'))
            return 'abort'

    def input_to_id(self, text):
        map = {' ':'','\n':'','\t':'','\r':''}
        new_line = text.translate(map)
        try:
            if int(new_line) >= 0:
                return int(new_line)
            else:
                return self.parent.translate_string('negative_id_error','yellow','green')
        except ValueError:
            return self.parent.translate_string('wrong_id_error','yellow','green')

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
                return self.parent.translate_string('wrong_id_error','yellow','green')

    @contactbook_error
    def edit_phones(self, new_text):
        note = self.data[self.ongoing]
        note.phone_check_and_set(mode='ed', phone=note.phones[self.field_id], new_phone=new_text)
        
        self.update_file(mode="ed")
        print(f"{self.parent.translate_string('contact_attr_p5_1','yellow')} {self.parent.translate_string('edit_contact_p1',end_color='green')}")
        self.field_id = None
        self.ongoing = None

    def add_contact_finish(self):
        record = self.data[self.ongoing]
        string = f"{self.parent.translate_string('contact_attr_add_p1','yellow','red')}: {record.name}; {self.parent.translate_string('contact_attr_add_p2','yellow','red')}: {record.birthday}; {self.parent.translate_string('contact_attr_add_p3','yellow','red')}: {record.email}; {self.parent.translate_string('contact_attr_add_p4','yellow','red')}: {record.address}; {self.parent.translate_string('contact_attr_add_p5','yellow','red')}: {'; '.join(f'{v}' for k,v in record.phones.items())}"
        print(string)
            
        self.update_file(mode="add",r_id=self.generated_ids)
        self.ongoing = None

    def remove_contact_submit(self, answer:str):
        if answer.lower().strip() in self.parent.confirm:
            print(self.parent.translate_string('contact_removed','yellow','green'))
            self.update_file(mode="del", r_id=self.ongoing)
            self.ongoing = None
            return
        elif answer.lower().strip() in self.parent.deny:
            print(self.parent.translate_string('contact_remove_abort','yellow','green'))
            return

        return ' '
    
    def remove_contact_ask(self):
        record = self.data[self.ongoing]
        string = f"{self.parent.translate_string('contact_remove_submit','green')}\n"
        string += f"{self.parent.translate_string('contact_attr_p1','yellow','red')}: {record.name}; {self.parent.translate_string('contact_attr_p2','yellow','red')}: {record.birthday}; {self.parent.translate_string('contact_attr_p3','yellow','red')}: {record.email}; {self.parent.translate_string('contact_attr_p4','yellow','red')}: {record.address}; {self.parent.translate_string('contact_attr_p5','yellow','red')}: {'; '.join(f'{v}' for v in record.phones.values())}\n{bcolors.GREEN}?"
        print(string)

    def add_phone_finish(self):
        self.update_file(mode="ed")
        self.field_id = None
        self.ongoing = None
        
    def print_find_modes(self):
        string = f"{self.parent.translate_string('print_find_modules_p0','green')}:\n"
        string += f"{bcolors.RED}0{bcolors.GREEN}. {self.parent.translate_string('print_find_modules_p1')}\n{bcolors.RED}1{bcolors.GREEN}. {self.parent.translate_string('print_find_modules_p2')}\n{bcolors.RED}2{bcolors.GREEN}. {self.parent.translate_string('print_find_modules_p3')}\n{bcolors.RED}3{bcolors.GREEN}. {self.parent.translate_string('print_find_modules_p4')}\n{bcolors.RED}4{bcolors.GREEN}. {self.parent.translate_string('print_find_modules_p5')}\n{bcolors.RED}5{bcolors.GREEN}. {self.parent.translate_string('print_find_modules_p6')}\n"
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
                return self.parent.translate_string('wrong_id_error','yellow','green')
        
    def find_hub(self, text):
        checker = False
        string = ""
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
                    string += f"{bcolors.RED}{contact_id}{bcolors.GREEN}. {self.parent.translate_string('contact_attr_p1','red','green')}: {highlighted_name}; {self.parent.translate_string('contact_attr_p5','red','green')}: {class_instance.phones}; {self.parent.translate_string('contact_attr_p2','red','green')}: {class_instance.birthday}; {self.parent.translate_string('contact_attr_p3','red','green')}: {class_instance.email}; {self.parent.translate_string('contact_attr_p4','red','green')}: {class_instance.address};\n"
        elif self.field_id == 1:
            for contact_id,class_instance in self.data.items():
                if class_instance.find_in_birthday(text):
                    checker = True
                    highlighted_birthday = f"{bcolors.GREEN}{class_instance.birthday[:class_instance.find_in_birthday(text)[0]]}{bcolors.YELLOW}{class_instance.birthday[class_instance.find_in_birthday(text)[0]:class_instance.find_in_birthday(text)[1]]}{bcolors.GREEN}{class_instance.birthday[class_instance.find_in_birthday(text)[1]:]}"
                    string += f"{bcolors.RED}{contact_id}{bcolors.GREEN}. {self.parent.translate_string('contact_attr_p1','red','green')}: {class_instance.name}; {self.parent.translate_string('contact_attr_p5','red','green')}: {class_instance.phones}; {self.parent.translate_string('contact_attr_p2','red','green')}: {highlighted_birthday}; {self.parent.translate_string('contact_attr_p3','red','green')}: {class_instance.email}; {self.parent.translate_string('contact_attr_p4','red','green')}: {class_instance.address};\n"
        elif self.field_id == 2:
            for contact_id,class_instance in self.data.items():
                if class_instance.find_in_email(text):
                    checker = True
                    highlighted_email = f"{bcolors.GREEN}{class_instance.email[:class_instance.find_in_email(text)[0]]}{bcolors.YELLOW}{class_instance.email[class_instance.find_in_email(text)[0]:class_instance.find_in_email(text)[1]]}{bcolors.GREEN}{class_instance.email[class_instance.find_in_email(text)[1]:]}"
                    string += f"{bcolors.RED}{contact_id}{bcolors.GREEN}. {self.parent.translate_string('contact_attr_p1','red','green')}: {class_instance.name}; {self.parent.translate_string('contact_attr_p5','red','green')}: {class_instance.phones}; {self.parent.translate_string('contact_attr_p2','red','green')}: {class_instance.birthday}; {self.parent.translate_string('contact_attr_p3','red','green')}: {highlighted_email}; {self.parent.translate_string('contact_attr_p4','red','green')}: {class_instance.address};\n"
        elif self.field_id == 3:
            for contact_id,class_instance in self.data.items():
                if class_instance.find_in_address(text):
                    checker = True
                    highlighted_address = f"{bcolors.GREEN}{class_instance.address[:class_instance.find_in_address(text)[0]]}{bcolors.YELLOW}{class_instance.address[class_instance.find_in_address(text)[0]:class_instance.find_in_address(text)[1]]}{bcolors.GREEN}{class_instance.address[class_instance.find_in_address(text)[1]:]}"
                    string += f"{bcolors.RED}{contact_id}{bcolors.GREEN}. {self.parent.translate_string('contact_attr_p1','red','green')}: {class_instance.name}; {self.parent.translate_string('contact_attr_p5','red','green')}: {class_instance.phones}; {self.parent.translate_string('contact_attr_p2','red','green')}: {class_instance.birthday}; {self.parent.translate_string('contact_attr_p3','red','green')}: {class_instance.email}; {self.parent.translate_string('contact_attr_p4','red','green')}: {highlighted_address};\n"
        elif self.field_id == 4:
            for contact_id,class_instance in self.data.items():
                if class_instance.find_in_phones(text):
                    checker = True
                    phones = "; ".join(f"{phone_number}" for phone_id,phone_number in class_instance.phones.items())
                    highlighted_phones = f"{bcolors.GREEN}{phones[:class_instance.find_in_phones(text)[0]]}{bcolors.YELLOW}{phones[class_instance.find_in_phones(text)[0]:class_instance.find_in_phones(text)[1]]}{bcolors.GREEN}{phones[class_instance.find_in_phones(text)[1]:]}"
                    string += f"{bcolors.RED}{contact_id}{bcolors.GREEN}. {self.parent.translate_string('contact_attr_p1','red','green')}: {class_instance.name}; {self.parent.translate_string('contact_attr_p5','red','green')}: {highlighted_phones}; {self.parent.translate_string('contact_attr_p2','red','green')}: {class_instance.birthday}; {self.parent.translate_string('contact_attr_p3','red','green')}: {class_instance.email}; {self.parent.translate_string('contact_attr_p4','red','green')}: {class_instance.address};\n"
        elif self.field_id == 5:
            for contact_id,class_instance in self.data.items():
                if class_instance.find_in_name(text):
                    checker = True
                    highlighted_name = f"{bcolors.GREEN}{class_instance.name[:class_instance.find_in_name(text)[0]]}{bcolors.YELLOW}{class_instance.name[class_instance.find_in_name(text)[0]:class_instance.find_in_name(text)[1]]}{bcolors.GREEN}{class_instance.name[class_instance.find_in_name(text)[1]:]}"
                    string += f"{bcolors.RED}{contact_id}{bcolors.GREEN}. {self.parent.translate_string('contact_attr_p1','red','green')}: {highlighted_name}; {self.parent.translate_string('contact_attr_p5','red','green')}: {class_instance.phones}; {self.parent.translate_string('contact_attr_p2','red','green')}: {class_instance.birthday}; {self.parent.translate_string('contact_attr_p3','red','green')}: {class_instance.email}; {self.parent.translate_string('contact_attr_p4','red','green')}: {class_instance.address};\n"
                elif class_instance.find_in_birthday(text):
                    checker = True
                    highlighted_birthday = f"{bcolors.GREEN}{class_instance.birthday[:class_instance.find_in_birthday(text)[0]]}{bcolors.YELLOW}{class_instance.birthday[class_instance.find_in_birthday(text)[0]:class_instance.find_in_birthday(text)[1]]}{bcolors.GREEN}{class_instance.birthday[class_instance.find_in_birthday(text)[1]:]}"
                    string += f"{bcolors.RED}{contact_id}{bcolors.GREEN}. {self.parent.translate_string('contact_attr_p1','red','green')}: {class_instance.name}; {self.parent.translate_string('contact_attr_p5','red','green')}: {class_instance.phones}; {self.parent.translate_string('contact_attr_p2','red','green')}: {highlighted_birthday}; {self.parent.translate_string('contact_attr_p3','red','green')}: {class_instance.email}; {self.parent.translate_string('contact_attr_p4','red','green')}: {class_instance.address};\n"
            for contact_id,class_instance in self.data.items():
                if class_instance.find_in_email(text):
                    checker = True
                    highlighted_email = f"{bcolors.GREEN}{class_instance.email[:class_instance.find_in_email(text)[0]]}{bcolors.YELLOW}{class_instance.email[class_instance.find_in_email(text)[0]:class_instance.find_in_email(text)[1]]}{bcolors.GREEN}{class_instance.email[class_instance.find_in_email(text)[1]:]}"
                    string += f"{bcolors.RED}{contact_id}{bcolors.GREEN}. {self.parent.translate_string('contact_attr_p1','red','green')}: {class_instance.name}; {self.parent.translate_string('contact_attr_p5','red','green')}: {class_instance.phones}; {self.parent.translate_string('contact_attr_p2','red','green')}: {class_instance.birthday}; {self.parent.translate_string('contact_attr_p3','red','green')}: {highlighted_email}; {self.parent.translate_string('contact_attr_p4','red','green')}: {class_instance.address};\n"
            for contact_id,class_instance in self.data.items():
                if class_instance.find_in_address(text):
                    checker = True
                    highlighted_address = f"{bcolors.GREEN}{class_instance.address[:class_instance.find_in_address(text)[0]]}{bcolors.YELLOW}{class_instance.address[class_instance.find_in_address(text)[0]:class_instance.find_in_address(text)[1]]}{bcolors.GREEN}{class_instance.address[class_instance.find_in_address(text)[1]:]}"
                    string += f"{bcolors.RED}{contact_id}{bcolors.GREEN}. {self.parent.translate_string('contact_attr_p1','red','green')}: {class_instance.name}; {self.parent.translate_string('contact_attr_p5','red','green')}: {class_instance.phones}; {self.parent.translate_string('contact_attr_p2','red','green')}: {class_instance.birthday}; {self.parent.translate_string('contact_attr_p3','red','green')}: {class_instance.email}; {self.parent.translate_string('contact_attr_p4','red','green')}: {highlighted_address};\n"
                elif class_instance.find_in_phones(text):
                    checker = True
                    phones = "; ".join(f"{phone_number}" for phone_id,phone_number in class_instance.phones.items())
                    highlighted_phones = f"{bcolors.GREEN}{phones[:class_instance.find_in_phones(text)[0]]}{bcolors.YELLOW}{phones[class_instance.find_in_phones(text)[0]:class_instance.find_in_phones(text)[1]]}{bcolors.GREEN}{phones[class_instance.find_in_phones(text)[1]:]}"
                    string += f"{bcolors.RED}{contact_id}{bcolors.GREEN}. {self.parent.translate_string('contact_attr_p1','red','green')}: {class_instance.name}; {self.parent.translate_string('contact_attr_p5','red','green')}: {highlighted_phones}; {self.parent.translate_string('contact_attr_p2','red','green')}: {class_instance.birthday}; {self.parent.translate_string('contact_attr_p3','red','green')}: {class_instance.email}; {self.parent.translate_string('contact_attr_p4','red','green')}: {class_instance.address};\n"

        if checker:
            print(f"{self.parent.translate_string('find_hub_intro','green')}\n{string}")
        else:
            print(self.parent.translate_string('find_hub_fail','yellow','green'))

    def dialogue_check(self,variable):
        if variable.lower() != 'n':
            return True
        return False

    def id_assign(self,mode:str,record):
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
