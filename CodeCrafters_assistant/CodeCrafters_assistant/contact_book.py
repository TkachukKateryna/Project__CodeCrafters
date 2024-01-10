from datetime import date,datetime,timedelta
from CodeCrafters_assistant.utils import Utils, RecordConstructor, Translate, bcolors

class DialogueBranches:
    def set_edit_object(self, *args):
        if self.field_id != 4:
            cfg = {   0:{ "type":"act", "prompt":f"{self.opnng}{self.translate_string('enter_new_text')}", "checks":{}, "actions":{self.edit_contact:[]}}
                    }
            self.dialogue_constructor(cfg)
        else:
            cfg = {   0:{ "type":"show", "checks":{}, "string":self.print_edit_phone_options},
                        1:{ "type":"act", "prompt":f"{self.opnng_alt}{self.translate_string('choose_phone_edit_option')}", "checks":{self.correct_edit_phone_option:[]}, "actions":{self.set_edit_phone_option:[]}},
                    }
            self.dialogue_constructor(cfg)

    def set_edit_phone_option(self, option):
        option = self.input_to_id(self.single_param(option))
        if option == 0:
            cfg = {   0:{ "type":"show", "checks":{self.contact_has_phones:[]}, "string":self.print_contact_phones},
                        1:{ "type":"act", "prompt":f"{self.opnng_alt}{self.translate_string('choose_contact_phone')}", "checks":{self.correct_phone_id:[]}, "actions":{self.set_current_field_id:[]}},
                        2:{ "type":"act", "prompt":f"{self.opnng}{self.translate_string('enter_new_phone')}", "checks":{}, "actions":{self.edit_phones:[], self.current_reset_and_save:[]}},
                    }
            self.dialogue_constructor(cfg)
        else:
            cfg = {   0:{ "type":"act", "prompt":f"{self.opnng}{self.translate_string('phone_number_add')}", "checks":{}, "actions":{self.add_phone:[], self.current_reset_and_save:[]}},
                    }
            self.dialogue_constructor(cfg)

    def set_remove_option(self, option):
        option = self.input_to_id(self.single_param(option))
        if option == 0:
            cfg = {     0:{ "type":"show", "checks":{}, "string":self.remove_contact_ask},
                        1:{ "type":"act", "prompt":self.confirmation, "checks":{}, "actions":{self.remove_contact_submit:[]}},
                    }
            self.dialogue_constructor(cfg)
        else:
            cfg = {     0:{ "type":"show", "checks":{}, "string":self.print_contact_attributes},
                        1:{ "type":"act", "prompt":f"{self.opnng_alt}{self.translate_string('enter_remove')}", "checks":{self.correct_field_id:[]}, "actions":{self.set_current_field_id:[], self.set_remove_object:[]}},
                    }
            self.dialogue_constructor(cfg)

    def set_remove_object(self, *args):
        if self.field_id != 4:
            cfg = {     0:{ "type":"show", "checks":{}, "string":self.remove_attribute_ask},
                        1:{ "type":"act", "prompt":self.confirmation, "checks":{}, "actions":{self.remove_attribute_submit:[]}},
                    }
            self.dialogue_constructor(cfg)
        else:
            cfg = {     0:{ "type":"show", "checks":{self.contact_has_phones:[]}, "string":self.print_contact_phones},
                        1:{ "type":"act", "prompt":f"{self.opnng_alt}{self.translate_string('choose_phone_to_delete')}", "checks":{self.correct_phone_id:[]}, "actions":{self.set_current_field_id:[]}},
                        2:{ "type":"show", "checks":{}, "string":self.remove_phone_ask},
                        3:{ "type":"act", "prompt":self.confirmation, "checks":{}, "actions":{self.remove_phone_submit:[]}},
                    }
            self.dialogue_constructor(cfg)

class DialogueActions:
    def print_contacts(self, *args):
        string = self.translate_string('print_contacts','green')
        string += ":\n" + '\n'.join(f"{bcolors.RED}{key}{bcolors.GREEN}. {self.translate_string('contact_attr_p1','red','green')}: {record.data['Name']}; {self.translate_string('contact_attr_p2','red','green')}: {record.data['Birthday']}; {self.translate_string('contact_attr_p3','red','green')}: {record.data['Email']}; {self.translate_string('contact_attr_p4','red','green')}: {record.data['Address']}; {self.translate_string('contact_attr_p5','red','green')}: {'; '.join(f'{phone}' for phone in record.data['Phones'].values())};" for key, record in self.data.items())
        return string

    def set_current_contact_id(self,contact_id):
        self.ongoing = self.input_to_id(self.single_param(contact_id))
        
    def set_current_field_id(self,field_id):
        self.field_id = self.input_to_id(self.single_param(field_id))
        
    def print_edit_phone_options(self, *args):
        string = f"{self.translate_string('how_to_edit_phone_p0','green')}\n{bcolors.RED}0{bcolors.GREEN}. {self.translate_string('how_to_edit_phone_p1')}\n{bcolors.RED}1{bcolors.GREEN}. {self.translate_string('how_to_edit_phone_p2')}\n"
        return string
            
    def remove_contact_ask(self, *args):
        record = self.data[self.ongoing]
        string = f"{self.translate_string('contact_remove_submit','green')}\n"
        string += f"{self.translate_string('contact_attr_p1','yellow','red')}: {record.data['Name']}; {self.translate_string('contact_attr_p2','yellow','red')}: {record.data['Birthday']}; {self.translate_string('contact_attr_p3','yellow','red')}: {record.data['Email']}; {self.translate_string('contact_attr_p4','yellow','red')}: {record.data['Address']}; {self.translate_string('contact_attr_p5','yellow','red')}: {'; '.join(f'{v}' for v in record.data['Phones'].values())}\n{bcolors.GREEN}?"
        return string

    def remove_contact_submit(self, answer:str):
        answer = self.single_param(answer)
        if answer.lower().strip() in self.parent.confirm:
            print(self.translate_string('contact_removed','yellow','green'))
            self.update_file(mode="del", r_id=self.ongoing)
            self.ongoing = None
            return
        elif answer.lower().strip() in self.parent.deny:
            print(self.translate_string('contact_remove_abort','yellow','green'))
            return

        return ' '
    
    def remove_attribute_ask(self, *args):
        ref_dict = ['contact_attr_p1','contact_attr_p2','contact_attr_p3','contact_attr_p4']
        return f"{self.translate_string('remove_attribute_ask_p0','yellow')} {self.translate_string(ref_dict[self.field_id],'red')} {self.translate_string('remove_attribute_ask_p1','yellow','green')}"

    def remove_attribute_submit(self, answer:str):
        answer = self.single_param(answer)
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

            self.current_reset_and_save()
            return
        elif answer.lower().strip() in self.parent.deny:
            print(self.translate_string('contact_remove_abort','yellow','green'))
            return

        return ' '

    def remove_phone_ask(self):
        return f"{self.translate_string('remove_attribute_ask_p0','yellow','red')} {self.translate_string('contact_attr_p5_1','red')} {self.translate_string('remove_attribute_ask_p1','yellow','red')} ( {self.data[self.ongoing].data['Phones'][self.field_id]} )"

    def remove_phone_submit(self, answer:str):
        answer = self.single_param(answer)
        record = self.data[self.ongoing]
        if answer.lower().strip() in self.parent.confirm:
            record.phone_check_and_set(mode='del',phone=record.data['Phones'][self.field_id])
            record.rearrange_phones()
            self.current_reset_and_save()
            return
        elif answer.lower().strip() in self.parent.deny:
            print(self.translate_string('contact_remove_abort','yellow','green'))
            return

        return ' '
    
    def print_contact_phones(self, *args):
        contact = self.data[self.ongoing]
        string = self.translate_string('choose_the_phone','green')
        string += ":\n" + "".join(f'{bcolors.RED}{phone_id}{bcolors.GREEN}. {phone_number};\n' for phone_id, phone_number in contact.data['Phones'].items())
        return string

    def contactbook_error(func):
        def true_handler(self,arg):
            try:
                result = func(self,arg)
            except ValueError as error_text:
                return str(error_text)
        return true_handler

    def single_param(self, param):
        return param[0][0]

    def add_contact_finish(self, *args):
        record = self.data[self.ongoing]
        #string = f"{self.translate_string('contact_attr_add_p1','yellow','red')}: {record.data['Name']}; {self.translate_string('contact_attr_add_p2','yellow','red')}: {record.data['Birthday']}; {self.translate_string('contact_attr_add_p3','yellow','red')}: {record.data['Email']}; {self.translate_string('contact_attr_add_p4','yellow','red')}: {record.data['Address']}; {self.translate_string('contact_attr_add_p5','yellow','red')}: {'; '.join(f'{v}' for k,v in record.data['Phones'].items())}"
        print(record)

        self.update_file(mode="add", r_id=self.generated_ids)
        self.ongoing = None

    @contactbook_error
    def add_name(self,name):
        name = self.single_param(name)
        record = self.data[self.ongoing]
        if self.dialogue_check(name):
            record.add_name(name)

    @contactbook_error
    def add_birthday(self,birthday):
        birthday = self.single_param(birthday)
        record = self.data[self.ongoing]
        if self.dialogue_check(birthday):
            record.add_birthday(birthday)

    @contactbook_error
    def add_email(self,email):
        email = self.single_param(email)
        record = self.data[self.ongoing]
        if self.dialogue_check(email):
            record.add_email(email)

    @contactbook_error
    def add_address(self,address):
        address = self.single_param(address)
        record = self.data[self.ongoing]
        if self.dialogue_check(address):
            record.add_address(address)

    @contactbook_error
    def add_phone(self,phone):
        phone = self.single_param(phone)
        record = self.data[self.ongoing]
        if self.dialogue_check(phone):
            record.phone_check_and_set(mode='add', phone=phone)

    def current_reset_and_save(self, *args):
        self.update_file(mode="ed")
        self.field_id = None
        self.ongoing = None
        
    @contactbook_error
    def edit_phones(self, new_text):
        new_text = self.single_param(new_text)
        record = self.data[self.ongoing]
        record.phone_check_and_set(mode='ed', phone=record.data['Phones'][self.field_id], new_phone=new_text)
        print(f"{self.translate_string('contact_attr_p5_1','yellow')} {self.translate_string('edit_contact_p1',end_color='green')}")

    @contactbook_error
    def edit_contact(self, new_text):
        new_text = self.single_param(new_text)
        local = ["contact_attr_p1", "contact_attr_p2", "contact_attr_p3", "contact_attr_p4", "contact_attr_p5_1"]
        if self.field_id == 0:
            self.data[self.ongoing].add_name(new_text)
        elif self.field_id == 1:
            self.data[self.ongoing].add_birthday(new_text)
        elif self.field_id == 2:
            self.data[self.ongoing].add_email(new_text)
        elif self.field_id == 3:
            self.data[self.ongoing].add_address(new_text)
        
        print(f"{self.translate_string(local[self.field_id],'yellow')} {self.translate_string('edit_contact_p1','yellow','green')}")
        self.current_reset_and_save()

    def print_contact_attributes(self, *args):
        record = self.data[self.ongoing]
        string = self.translate_string('print_contact_attr_p0','green') + ":\n"
        parameter_id = 0
        for value in record.data.values():
            if type(value) != dict:
                string += f"{bcolors.RED}{parameter_id}{bcolors.GREEN}. {self.translate_string(f'print_contact_attr_p{parameter_id + 1}','red','green')}: {value}\n"
                parameter_id += 1
            else:
                string += f"{bcolors.RED}{parameter_id}{bcolors.GREEN}. {self.translate_string(f'print_contact_attr_p{parameter_id + 1}','red','green')}: {'; '.join(phone for phone in value.values())}\n"
                parameter_id += 1
        return string

    def print_find_modes(self):
        string = f"{self.translate_string('print_find_modules_p0','green')}:\n"
        string += f"{bcolors.RED}0{bcolors.GREEN}. {self.translate_string('print_find_modules_p1')}\n{bcolors.RED}1{bcolors.GREEN}. {self.translate_string('print_find_modules_p2')}\n{bcolors.RED}2{bcolors.GREEN}. {self.translate_string('print_find_modules_p3')}\n{bcolors.RED}3{bcolors.GREEN}. {self.translate_string('print_find_modules_p4')}\n{bcolors.RED}4{bcolors.GREEN}. {self.translate_string('print_find_modules_p5')}\n{bcolors.RED}5{bcolors.GREEN}. {self.translate_string('print_find_modules_p6')}\n"
        return string

    def find_hub(self, text):
        text = self.single_param(text)
        string = ""
        check = False
        mode = None
        if self.field_id != 5:
            mode = self.field_id
        else:
            mode = "all"
        for contact_id,class_instance in self.data.items():
            elements = { "intro":f"{bcolors.RED}{contact_id}{bcolors.GREEN}. ", 
                        "what":text, 
                        "where":mode, 
                        0:[self.translate_string('contact_attr_p1','red','green'),f"{class_instance.data['Name']}; "], 
                        1:[self.translate_string('contact_attr_p2','red','green'),f"{class_instance.data['Birthday']}; "], 
                        2:[self.translate_string('contact_attr_p3','red','green'),f"{class_instance.data['Email']}; "], 
                        3:[self.translate_string('contact_attr_p4','red','green'),f"{class_instance.data['Address']}; "], 
                        4:[self.translate_string('contact_attr_p5','red','green'),f"{'; '.join(f'{phone_number}' for phone_number in class_instance.data['Phones'].values())};\n"]
                        }
            result = self.constructor(elements)
            if result:
                string += result
                check = True

        if check != False:
            print(f"{self.translate_string('find_hub_intro','green')}:\n{string}")
        else:
            print(self.translate_string('find_hub_fail','yellow','green'))
           
class DialogueChecks:
    def data_not_empty(self, *args):
        if len(self.data) > 0:
            return True
        else:
            return self.translate_string('contact_list_empty','yellow','green')

    def contact_has_phones(self):
        if len(self.data[self.ongoing].data['Phones']) > 0:
            return True
        else:
            return self.translate_string('no_phone_numbers_error','yellow','green')

    def correct_contact_id(self, contact_id):
        contact_id = self.input_to_id(self.single_param(contact_id))
        if (type(contact_id) == int) and (contact_id in self.data.keys()):
            return True
        elif type(contact_id) == str:
            return contact_id
        else:
            return self.translate_string('contact_id_not_found','yellow','green')

    def correct_field_id(self, field_id):
        field_id = self.input_to_id(self.single_param(field_id))
        record = self.data[self.ongoing]
        if (type(field_id) == int) and (field_id <= (len(record.data) - 1)):
            return True
        elif type(field_id) == str:
            return field_id
        else:
            return self.translate_string('wrong_id_error','yellow','green')

    def correct_phone_id(self, field_id):
        field_id = self.input_to_id(self.single_param(field_id))
        record = self.data[self.ongoing]
        if (type(field_id) == int) and (field_id <= (len(record.data['Phones']) - 1)):
            return True
        elif type(field_id) == str:
            return field_id
        else:
            return self.translate_string('wrong_id_error','yellow','green')

    def correct_edit_phone_option(self, option):
        option = self.input_to_id(self.single_param(option))
        if (type(option) == int) and (option == 0 or option == 1):
            return True
        elif type(option) == str:
            return option
        else:
            return self.translate_string('wrong_id_error','yellow','green')

    def correct_find_option(self, field_id):
        field_id = self.input_to_id(self.single_param(field_id))
        if (type(field_id) == int) and (field_id <= 5):
            return True
        elif type(field_id) == str:
            return field_id
        else:
            return self.translate_string('wrong_id_error','yellow','green')
        
class ContactBook(DialogueActions, DialogueChecks, DialogueBranches, Utils, RecordConstructor, Translate):
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
        from CodeCrafters_assistant.record_manager import Record
        self.update_file("load")

    def reinit(self, mode=None):
        tmp = None
        if type(self.parent.module_chosen) == int:
            tmp = self.parent.module_chosen
        if mode != 'first':
            self.parent.module_chosen = self.parent.modules.index(self)
        self.confirmation = f"{self.translate_string('please_enter_confirm_p0')} {self.translate_string('confirm','red','cyan')}/{self.translate_string('confirm_long','red','cyan')} {self.translate_string('please_enter_confirm_p1')} {self.translate_string('please_enter_confirm_p2')} {self.translate_string('deny','red','cyan')}/{self.translate_string('deny_long','red','cyan')} {self.translate_string('please_enter_confirm_p3')}"
        self.opnng = f"{self.translate_string('please_enter_p0','cyan')} "
        self.opnng_alt = f"{self.translate_string('please_enter_p0_1','cyan')} "
        self.non_obligatory = f"{bcolors.CYAN} ({self.translate_string('please_enter_p1')} '{self.translate_string('please_enter_p2','red','cyan')}'{self.translate_string('please_enter_p3')})"
        self.method_table = {'__localization':{
                                'name':"contact_manager_name",
                                'description':"contact_manager_desc"},
                            'create':{
                                'description':"create_desc", 
                                'methods':{
                                    self.create_starter:{}}},
                            'check_birthdays':{
                                'description':"check_birthdays_desc", 
                                'methods':{
                                    self.show_upcoming_birthdays:{
                                        'attr_id':f"{self.opnng}{self.translate_string('enter_days_number')}"}}},
                            'edit':{
                                'description':"edit_desc", 
                                'methods':{ self.edit_starter:{}}},
                            'remove':{
                                'description':"remove_desc", 
                                'methods':{self.remove_starter:{}}
                                  },
                            'find':{
                                'description':"find_desc", 
                                'methods':{
                                    self.find_starter:{}}},
                            'show_all':{
                                'description':"show_all_desc", 
                                'methods':{
                                    self.show_all_starter:{}}}}
        if mode != 'first':
            self.parent.module_chosen = tmp
  
    def show_upcoming_birthdays(self, number):
        days_ahead = 0
        if self.dialogue_check(number):
            try:
                days_ahead = int(number)
                days_ahead = (datetime(date.today().year,date.today().month,date.today().day) + timedelta(days=int(number))).date()
            except ValueError:
                return self.translate_string('invalid_day_error','yellow','green')
        
        upcoming_birthdays = []
        for record_id, record in self.data.items():
            result = record.days_to_birthday(mode='no_math')
            if result != "None" and result <= days_ahead:
                    upcoming_birthdays.append(record_id)
        if upcoming_birthdays != []:
            print(f"{self.translate_string('found_birthdays_p0','green','red')} {number} {self.translate_string('found_birthdays_p1','green')}")
            for i in upcoming_birthdays:
                print(f"  {self.data[i]}")
        else:
            print(f"{self.translate_string('not_found_birthdays_p0','yellow','red')} {number} {self.translate_string('not_found_birthdays_p1','yellow','green')}")

    def create_starter(self):
        from CodeCrafters_assistant.record_manager import Record
        new_record = Record(parent_class=self.parent)
        self.id_assign(mode="add",record=new_record)
        cfg = {   0:{ "type":"act", "prompt":f"{self.opnng}{self.translate_string('enter_name')}{self.non_obligatory}", "checks":{}, "actions":{self.add_name:[]}},
                    1:{ "type":"act", "prompt":f"{self.opnng}{self.translate_string('enter_phone_number')}{self.non_obligatory}", "checks":{}, "actions":{self.add_phone:[]}},
                    2:{ "type":"act", "prompt":f"{self.opnng}{self.translate_string('enter_birthday')}{self.non_obligatory}", "checks":{}, "actions":{self.add_birthday:[]}},
                    3:{ "type":"act", "prompt":f"{self.opnng}{self.translate_string('enter_email')}{self.non_obligatory}", "checks":{}, "actions":{self.add_email:[]}},
                    4:{ "type":"act", "prompt":f"{self.opnng}{self.translate_string('enter_address')}{self.non_obligatory}", "checks":{}, "actions":{self.add_address:[], self.add_contact_finish:[]}},
                }
        self.dialogue_constructor(cfg)

    def edit_starter(self):
        cfg = {   0:{ "type":"show", "checks":{self.data_not_empty:[]}, "string":self.print_contacts},
                    1:{ "type":"act", "prompt":f"{self.opnng_alt}{self.translate_string('choose_contact_to_edit')}", "checks":{self.data_not_empty:[],self.correct_contact_id:[]}, "actions":{self.set_current_contact_id:[]}},
                    2:{ "type":"show", "checks":{}, "string":self.print_contact_attributes},
                    3:{ "type":"act", "prompt":f"{self.opnng_alt}{self.translate_string('enter_edit')}", "checks":{self.correct_field_id:[]}, "actions":{self.set_current_field_id:[], self.set_edit_object:[]}},
                }
        self.dialogue_constructor(cfg)

    def remove_starter(self):
        cfg = {   0:{ "type":"show", "checks":{self.data_not_empty:[]}, "string":self.print_contacts},
                    1:{ "type":"act", "prompt":f"{self.opnng_alt}{self.translate_string('choose_contact')}", "checks":{self.data_not_empty:[],self.correct_contact_id:[]}, "actions":{self.set_current_contact_id:[]}},
                    2:{ "type":"show", "checks":{}, "string":f"{self.translate_string('what_to_delete_p0','green')}\n{bcolors.RED}0{bcolors.GREEN}. {self.translate_string('what_to_delete_p1')}\n{bcolors.RED}1{bcolors.GREEN}. {self.translate_string('what_to_delete_p2')}\n"},
                    3:{ "type":"act", "prompt":f"{self.opnng_alt}{self.translate_string('enter_remove')}", "checks":{self.correct_edit_phone_option:[]}, "actions":{self.set_remove_option:[]}},
                }
        self.dialogue_constructor(cfg)

    def show_all_starter(self):
        cfg = {   0:{ "type":"show", "checks":{self.data_not_empty:[]}, "string":self.print_contacts}}
        self.dialogue_constructor(cfg)

    def find_starter(self):
        cfg = {   0:{ "type":"show", "checks":{}, "string":self.print_find_modes},
                    1:{ "type":"act", "prompt":f"{self.opnng}{self.translate_string('choose_search_mode')}", "checks":{self.data_not_empty:[],self.correct_find_option:[]}, "actions":{self.set_current_field_id:[]}},
                    2:{ "type":"act", "prompt":f"{self.opnng}{self.translate_string('enter_text_to_find')}", "checks":{}, "actions":{self.find_hub:[]}},
                }
        self.dialogue_constructor(cfg)