from CodeCrafters_assistant.utils import Utils, RecordConstructor, Translate, bcolors
from re import search

class DialogueBranches:
    def set_edit_object(self, *args):
        if self.field_id != 2:
            cfg = {   0:{ "type":"act", "prompt":f"{self.opnng}{self.translate_string('enter_new_text')}", "checks":{}, "actions":{self.edit_note:[]}}
                    }
            self.dialogue_constructor(cfg)
        else:
            cfg = {   0:{ "type":"show", "checks":{}, "string":self.print_edit_tag_options},
                        1:{ "type":"act", "prompt":f"{self.opnng_alt}{self.translate_string('choose_tag_edit_option')}", "checks":{self.correct_edit_tag_option:[]}, "actions":{self.set_edit_tag_option:[]}},
                    }
            self.dialogue_constructor(cfg)

    def set_edit_tag_option(self, option):
        option = self.input_to_id(self.single_param(option))
        if option == 0:
            cfg = {   0:{ "type":"show", "checks":{self.note_has_tags:[]}, "string":self.print_note_tags},
                        1:{ "type":"act", "prompt":f"{self.opnng_alt}{self.translate_string('choose_note_tag')}", "checks":{self.correct_tag_id:[]}, "actions":{self.set_current_field_id:[]}},
                        2:{ "type":"act", "prompt":f"{self.opnng}{self.translate_string('enter_new_tag')}", "checks":{}, "actions":{self.edit_tags:[], self.current_reset_and_save:[]}},
                    }
            self.dialogue_constructor(cfg)
        else:
            cfg = {   0:{ "type":"act", "prompt":f"{self.opnng}{self.translate_string('enter_the_tag')}", "checks":{}, "actions":{self.add_tag:[], self.current_reset_and_save:[]}},
                    }
            self.dialogue_constructor(cfg)

    def set_remove_option(self, option):
        option = self.input_to_id(self.single_param(option))
        if option == 0:
            cfg = {     0:{ "type":"show", "checks":{}, "string":self.remove_note_ask},
                        1:{ "type":"act", "prompt":self.confirmation, "checks":{}, "actions":{self.remove_note_submit:[]}},
                    }
            self.dialogue_constructor(cfg)
        else:
            cfg = {     0:{ "type":"show", "checks":{}, "string":self.print_note_attributes},
                        1:{ "type":"act", "prompt":f"{self.opnng_alt}{self.translate_string('enter_remove')}", "checks":{self.correct_field_id:[]}, "actions":{self.set_current_field_id:[], self.set_remove_object:[]}},
                    }
            self.dialogue_constructor(cfg)

    def set_remove_object(self, *args):
        if self.field_id != 2:
            cfg = {     0:{ "type":"show", "checks":{}, "string":self.remove_attribute_ask},
                        1:{ "type":"act", "prompt":self.confirmation, "checks":{}, "actions":{self.remove_attribute_submit:[]}},
                    }
            self.dialogue_constructor(cfg)
        else:
            cfg = {     0:{ "type":"show", "checks":{self.note_has_tags:[]}, "string":self.print_note_tags},
                        1:{ "type":"act", "prompt":f"{self.opnng_alt}{self.translate_string('choose_tag_to_del')}", "checks":{self.correct_tag_id:[]}, "actions":{self.set_current_field_id:[]}},
                        2:{ "type":"show", "checks":{}, "string":self.remove_tag_ask},
                        3:{ "type":"act", "prompt":self.confirmation, "checks":{}, "actions":{self.remove_tag_submit:[]}},
                    }
            self.dialogue_constructor(cfg)


class DialogueActions:
    def print_notes(self):
        string = self.translate_string('print_notes','green')
        string += ":\n" + '\n'.join(f"{bcolors.RED}{key}{bcolors.GREEN}. {self.translate_string('note_attr_p0','red','green')}: {value.data['Title']}; {self.translate_string('note_attr_p1','red','green')}: {value.data['Text']}; {self.translate_string('note_attr_p2','red','green')}: {'; '.join(f'{tag}' for tag in value.data['Tags'].values())};" for key,value in self.data.items())
        return string

    def set_current_note_id(self,note_id):
        self.ongoing = self.input_to_id(self.single_param(note_id))
        
    def set_current_field_id(self,field_id):
        self.field_id = self.input_to_id(self.single_param(field_id))
        
    def print_edit_tag_options(self, *args):
        string = f"{self.translate_string('how_to_edit_tag_p0','green')}\n{bcolors.RED}0{bcolors.GREEN}. {self.translate_string('how_to_edit_tag_p1')}\n{bcolors.RED}1{bcolors.GREEN}. {self.translate_string('how_to_edit_tag_p2')}\n"
        return string
          
    def remove_note_ask(self, *args):
        record = self.data[self.ongoing]
        string = f"{self.translate_string('note_remove_submit','green')}\n"
        string += f"{self.translate_string('note_attr_p0','yellow','red')}: {record.data['Title']}; {self.translate_string('note_attr_p1','yellow','red')}: {record.data['Text']}; {self.translate_string('note_attr_p2','yellow','red')}: {'; '.join(f'{v}' for v in record.data['Tags'].values())}\n{bcolors.GREEN}?"
        return string

    def remove_note_submit(self, answer:str):
        answer = self.single_param(answer)
        if answer.lower().strip() in self.parent.confirm:
            print(self.translate_string('note_removed','yellow','green'))
            self.update_file(mode="del", r_id=self.ongoing)
            self.ongoing = None
            return
        elif answer.lower().strip() in self.parent.deny:
            print(self.translate_string('note_remove_abort','yellow','green'))
            return

        return ' '
    
    def remove_attribute_ask(self, *args):
        ref_dict = ['note_attr_p0','note_attr_p1']
        return f"{self.translate_string('remove_attribute_ask_p0','yellow')} {self.translate_string(ref_dict[self.field_id],'red')} {self.translate_string('remove_attribute_ask_p1','yellow','green')}"

    def remove_attribute_submit(self, answer:str):
        answer = self.single_param(answer)
        record = self.data[self.ongoing]
        if answer.lower().strip() in self.parent.confirm:
            if self.field_id == 0:
                record.remove_title()
            elif self.field_id == 1:
                record.remove_text()

            self.current_reset_and_save()
            return
        elif answer.lower().strip() in self.parent.deny:
            print(self.translate_string('note_remove_abort','yellow','green'))
            return

        return ' '

    def remove_tag_ask(self):
        return f"{self.translate_string('remove_attribute_ask_p0','yellow','red')} {self.translate_string('note_attr_p2_1','red')} {self.translate_string('remove_attribute_ask_p1','yellow','red')} ( {self.data[self.ongoing].data['Tags'][self.field_id]} )"

    def remove_tag_submit(self, answer:str):
        answer = self.single_param(answer)
        note = self.data[self.ongoing]
        if answer.lower().strip() in self.parent.confirm:
            note.tag_check_and_set(mode='del',tag=note.data['Tags'][self.field_id])
            note.rearrange_tags()
            self.current_reset_and_save()
            return
        elif answer.lower().strip() in self.parent.deny:
            print(self.translate_string('note_remove_abort','yellow','green'))
            return

        return ' '
    
    def print_note_tags(self, *args):
        note = self.data[self.ongoing]
        string = self.translate_string('choose_the_tag','green')
        string += ":\n" + "".join(f'{bcolors.RED}{tag_id}{bcolors.GREEN}. {tag};\n' for tag_id, tag in note.data['Tags'].items())
        return string

    def single_param(self, param):
        return param[0][0]

    def add_note_finish(self, *args):
        record = self.data[self.ongoing]
        print(record)

        self.update_file(mode="add", r_id=self.generated_ids)
        self.ongoing = None

    def notepad_error(func):
        def true_handler(self,arg):
            try:
                result = func(self,arg)
            except ValueError as error_text:
                return str(error_text)
        return true_handler

    @notepad_error
    def add_title(self,title):
        title = self.single_param(title)
        record = self.data[self.ongoing]
        if self.dialogue_check(title):
            record.add_title(title)

    @notepad_error
    def add_text(self,text):
        text = self.single_param(text)
        record = self.data[self.ongoing]
        if self.dialogue_check(text):
            record.add_text(text)

    @notepad_error
    def add_tag(self,tag):
        tag = self.single_param(tag)
        record = self.data[self.ongoing]
        if self.dialogue_check(tag):
            record.tag_check_and_set(mode='add', tag=tag)

    def current_reset_and_save(self, *args):
        self.update_file(mode="ed")
        self.field_id = None
        self.ongoing = None
        
    @notepad_error
    def edit_tags(self, new_text):
        new_text = self.single_param(new_text)
        note = self.data[self.ongoing]
        note.tag_check_and_set(mode='ed', tag=note.data['Tags'][self.field_id], new_tag=new_text)
        print(f"{self.translate_string('note_attr_p2_1','yellow')} {self.translate_string('edited',end_color='green')}")

    @notepad_error
    def edit_note(self, new_text):
        new_text = self.single_param(new_text)
        local = ["note_attr_p0", "note_attr_p1"]
        if self.field_id == 0:
            self.data[self.ongoing].add_title(new_text)
        elif self.field_id == 1:
            self.data[self.ongoing].add_text(new_text)
        
        print(f"{self.translate_string(local[self.field_id],'yellow')} {self.translate_string('edited','yellow','green')}")
        self.current_reset_and_save()

    def print_note_attributes(self, *args):
        record = self.data[self.ongoing]
        string = self.translate_string('print_note_attr','green') + ":\n"
        parameter_id = 0
        for value in record.data.values():
            if type(value) != dict:
                string += f"{bcolors.RED}{parameter_id}{bcolors.GREEN}. {self.translate_string(f'note_attr_p{parameter_id}','red','green')}: {value}\n"
                parameter_id += 1
            else:
                string += f"{bcolors.RED}{parameter_id}{bcolors.GREEN}. {self.translate_string(f'note_attr_p{parameter_id}','red','green')}: {'; '.join(tag for tag in value.values())}\n"
                parameter_id += 1
        return string

    def print_find_modes(self):
        string = self.translate_string('search_attr_p0','green') + ":\n"
        string += f"{bcolors.RED}0{bcolors.GREEN}. {self.translate_string('search_attr_p1')}\n{bcolors.RED}1{bcolors.GREEN}. {self.translate_string('search_attr_p2')}\n{bcolors.RED}2{bcolors.GREEN}. {self.translate_string('search_attr_p3')}\n{bcolors.RED}3{bcolors.GREEN}. {self.translate_string('search_attr_p4')}\n"
        return string
    
    def find_hub(self, text):
        text = self.single_param(text)
        string = ""
        check = False
        mode = None
        if self.field_id != 3:
            mode = self.field_id
        else:
            mode = "all"
        for note_id,class_instance in self.data.items():
            elements = { "intro":f"{bcolors.RED}{note_id}{bcolors.GREEN}. ", 
                        "what":text, 
                        "where":mode, 
                        0:[self.translate_string('note_attr_p0','red','green'),f"{class_instance.data['Title']}; "], 
                        1:[self.translate_string('note_attr_p1','red','green'),f"{class_instance.data['Text']}; "],
                        2:[self.translate_string('note_attr_p2','red','green'),f"{'; '.join(f'{tag}' for tag in class_instance.data['Tags'].values())};\n"]
                        }
            result = self.constructor(elements)
            if result:
                string += result
                check = True

        if check != False:
            print(f"{self.translate_string('find_intro','green')}:\n{string}")
        else:
            print(self.translate_string('find_failure','yellow','green'))

class DialogueChecks:
    def data_not_empty(self, *args):
        if len(self.data) > 0:
            return True
        else:
            return self.translate_string('note_list_empty','yellow','green')

    def note_has_tags(self):
        if len(self.data[self.ongoing].data['Tags']) > 0:
            return True
        else:
            return self.translate_string('no_tags_error','yellow','green')

    def correct_note_id(self, note_id):
        note_id = self.input_to_id(self.single_param(note_id))
        if (type(note_id) == int) and (note_id in self.data.keys()):
            return True
        elif type(note_id) == str:
            return note_id
        else:
            return self.translate_string('note_id_not_found','yellow','green')

    def correct_field_id(self, field_id):
        field_id = self.input_to_id(self.single_param(field_id))
        record = self.data[self.ongoing]
        if (type(field_id) == int) and (field_id <= (len(record.data) - 1)):
            return True
        elif type(field_id) == str:
            return field_id
        else:
            return self.translate_string('wrong_id_error','yellow','green')

    def correct_tag_id(self, field_id):
        field_id = self.input_to_id(self.single_param(field_id))
        record = self.data[self.ongoing]
        if (type(field_id) == int) and (field_id <= (len(record.data['Tags']) - 1)):
            return True
        elif type(field_id) == str:
            return field_id
        else:
            return self.translate_string('wrong_id_error','yellow','green')

    def correct_edit_tag_option(self, option):
        option = self.input_to_id(self.single_param(option))
        if (type(option) == int) and (option == 0 or option == 1):
            return True
        elif type(option) == str:
            return option
        else:
            return self.translate_string('wrong_id_error','yellow','green')

    def correct_find_option(self, field_id):
        field_id = self.input_to_id(self.single_param(field_id))
        if (type(field_id) == int) and (field_id <= 3):
            return True
        elif type(field_id) == str:
            return field_id
        else:
            return self.translate_string('wrong_id_error','yellow','green')



class NoteChecks(Translate):
    def title_check(self,title):
        if title != '':
            return title
        else:
            raise ValueError(self.translate_string('wrong_title_format','yellow','green'))

    def text_check(self,text):
        if text != '':
            return text
        else:
            raise ValueError(self.translate_string('wrong_text_format','yellow','green'))

    def tag_check(self,text):
        if text != '':
            return text
        else:
            raise ValueError(self.translate_string('wrong_text_format','yellow','green'))

    def has_tag(self,tag:str):
        for i in self.data['Tags'].values():
            if i == tag:
                return True
           
        return False 

    def tag_check_and_set(self,mode,tag,new_tag=None):
        try:
            if tag == '':
                raise ValueError(self.translate_string('wrong_tag_format','yellow','green'))
            elif mode == 'add':
                if tag.lower() == "stop":
                    return True
                tag = self.tag_check(tag)
                self.data['Tags'][len(self.data['Tags'])] = tag
                raise ValueError(f"{self.translate_string('tag_added_p0','yellow','red')}{self.translate_string('tag_added_p1')}{self.translate_string('tag_added_p2','yellow','green')}")
            elif mode == 'ed':
                if self.has_tag(tag):
                    if type(self.tag_check(new_tag)) == str:
                        for tag_id,tag_item in self.data['Tags'].items():
                            if tag_item == tag:
                                self.data['Tags'][tag_id] = new_tag
                                return
                    
                raise ValueError(self.translate_string('tag_not_found','yellow','green'))
            elif mode == 'del':
                if self.has_tag(tag):
                    for tag_id,tag_item in self.data['Tags'].items():
                        if tag_item == tag:
                            del self.data['Tags'][tag_id]
                            print(self.translate_string('tag_removed','yellow','green'))
                            return
                
                raise ValueError(self.translate_string('tag_not_found','yellow','green'))
        except ValueError as error_text:
            raise ValueError(error_text)

class Note(NoteChecks):
    def __init__(self, parent_class):
        self.parent = parent_class
        if self.parent:
            self.data = {'Title':self.translate_string('unnamed_note'),'Text':self.translate_string('none'),'Tags':{}}
        else:
            self.data = {'Title':"Unnamed note",'Text':"None",'Tags':{}}

    def note_error(func):
        def true_handler(self,arg):
            try:
                result = func(self,arg)
            except ValueError as error_text:
                raise ValueError(error_text)
        return true_handler

    @note_error
    def add_title(self,title):
        self.data['Title'] = self.title_check(title)

    @note_error
    def add_text(self,text):
        self.data['Text'] = self.text_check(text)

    @note_error
    def add_tags(self,tag):
        self.tag_check_and_set(mode='add', tag=tag)
         
    def remove_title(self):
        self.data['Title'] = self.translate_string('unnamed_note')
        print(self.translate_string('title_removed','yellow','green'))

    def remove_text(self):
        self.data['Text'] = self.translate_string('none')
        print(self.translate_string('text_removed','yellow','green'))

    def rearrange_tags(self):
        if self.data['Tags'] != {}:
            id_generator = 0
            tmp_array = {}
            for tag in self.data['Tags'].values(): #rearranging tag ids
                tmp_array[id_generator] = tag
                id_generator += 1
            self.data['Tags'] = tmp_array

    def load_data(self,cfg): # To avoid reoccurring checks when loading from storage.bin
        id_generator = 0
        for do_not_use,tag in cfg['Tags'].items(): #rearranging tag ids, just like with notebook records.
            self.data['Tags'][id_generator] = tag
            id_generator += 1

        self.data['Title'] = cfg['Title']
        self.data['Text'] = cfg['Text']

    def __str__(self):
        return f"{self.translate_string('note_attr_p0','red','green')}: {self.data['Title']}; {self.translate_string('note_attr_p1','red','green')}: {self.data['Text']}; {self.translate_string('note_attr_p2','red','green')}: {'; '.join(tag for tag in self.data['Tags'].values())};"


class NoteFile(DialogueActions, DialogueChecks, DialogueBranches, Utils, RecordConstructor, Translate):
    def __init__(self, parent_class):
        self.parent = parent_class
        self.parent.modules.append(self)
        self.parent.module_chosen = len(self.parent.modules) - 1
        self.reinit(mode='first')
        self.data = {}
        self.priority_ids = []
        self.record_cnt = 0
        self.generated_ids = 0
        self.file = "note_storage.bin"
        
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
        self.non_obligatory = f"{bcolors.CYAN} ( {self.translate_string('please_enter_p1')} '{self.translate_string('please_enter_p2','red','cyan')}'{self.translate_string('please_enter_p3')})"
        self.method_table = {'__localization':{
                                'name':"note_manager_name", 
                                'description':"note_manager_desc"},
                            'create':{
                                'description':"create_desc", 
                                'methods':{
                                    self.create_starter:{}}},
                            'edit':{
                                'description':"edit_desc",
                                'methods':{
                                    self.edit_starter:{}}},
                            'find':{
                                'description':"find_desc", 
                                'methods':{
                                    self.find_starter:{}}},
                            'remove':{
                                'description':"remove_desc", 
                                'methods':{
                                    self.remove_starter:{}}},
                            'show_all':{
                                'description':"show_all_desc", 
                                'methods':{
                                    self.show_all_starter:{}}}}
        if mode != 'first':
            self.parent.module_chosen = tmp
  
    def create_starter(self):
        new_record = Note(parent_class=self.parent)
        self.id_assign(mode="add",record=new_record)
        cfg = {   0:{ "type":"act", "prompt":f"{self.opnng}{self.translate_string('enter_title')}{self.non_obligatory}", "checks":{}, "actions":{self.add_title:[]}},
                    1:{ "type":"act", "prompt":f"{self.opnng}{self.translate_string('enter_text')}{self.non_obligatory}", "checks":{}, "actions":{self.add_text:[]}},
                    2:{ "type":"act", "prompt":f"{self.opnng}{self.translate_string('enter_tag')}{self.non_obligatory}", "checks":{}, "actions":{self.add_tag:[], self.add_note_finish:[]}},
                }
        self.dialogue_constructor(cfg)

    def edit_starter(self):
        cfg = {   0:{ "type":"show", "checks":{self.data_not_empty:[]}, "string":self.print_notes},
                    1:{ "type":"act", "prompt":f"{self.opnng_alt}{self.translate_string('choose_note_to_edit')}", "checks":{self.data_not_empty:[],self.correct_note_id:[]}, "actions":{self.set_current_note_id:[]}},
                    2:{ "type":"show", "checks":{}, "string":self.print_note_attributes},
                    3:{ "type":"act", "prompt":f"{self.opnng_alt}{self.translate_string('enter_edit')}", "checks":{self.correct_field_id:[]}, "actions":{self.set_current_field_id:[], self.set_edit_object:[]}},
                }
        self.dialogue_constructor(cfg)

    def remove_starter(self):
        cfg = {   0:{ "type":"show", "checks":{self.data_not_empty:[]}, "string":self.print_notes},
                    1:{ "type":"act", "prompt":f"{self.opnng_alt}{self.translate_string('choose_note')}", "checks":{self.data_not_empty:[],self.correct_note_id:[]}, "actions":{self.set_current_note_id:[]}},
                    2:{ "type":"show", "checks":{}, "string":f"{self.translate_string('what_to_delete_p0','green')}\n{bcolors.RED}0{bcolors.GREEN}. {self.translate_string('what_to_delete_p1')}\n{bcolors.RED}1{bcolors.GREEN}. {self.translate_string('what_to_delete_p2')}\n"},
                    3:{ "type":"act", "prompt":f"{self.opnng_alt}{self.translate_string('enter_remove')}", "checks":{self.correct_edit_tag_option:[]}, "actions":{self.set_remove_option:[]}},
                }
        self.dialogue_constructor(cfg)

    def show_all_starter(self):
        cfg = {   0:{ "type":"show", "checks":{self.data_not_empty:[]}, "string":self.print_notes}}
        self.dialogue_constructor(cfg)

    def find_starter(self):
        cfg = {   0:{ "type":"show", "checks":{}, "string":self.print_find_modes},
                    1:{ "type":"act", "prompt":f"{self.opnng}{self.translate_string('choose_search_mode')}", "checks":{self.data_not_empty:[],self.correct_find_option:[]}, "actions":{self.set_current_field_id:[]}},
                    2:{ "type":"act", "prompt":f"{self.opnng}{self.translate_string('enter_text_to_find')}", "checks":{}, "actions":{self.find_hub:[]}},
                }
        self.dialogue_constructor(cfg)