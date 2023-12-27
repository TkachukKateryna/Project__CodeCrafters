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

class NoteChecks:
    def title_check(self,title):
        if title != '':
            return title
        else:
            raise ValueError(self.parent.translate_string('wrong_title_format','yellow','green'))

    def text_check(self,text): #Закоментував, бо немає необхідності використовувати. Треба - розкоментовуєш та коментуєш останній return.
        # if text != '':
        #     return text
        # else:
        #     raise ValueError(self.parent.translate_string('wrong_text_format','yellow','green'))
        return text

    def tag_check_and_set(self,mode,tag,new_tag=None):
        if tag == '':
            raise ValueError(self.parent.translate_string('wrong_tag_format','yellow','green'))
        elif mode == 'add':
            if tag.lower() == "stop":
                return True
            self.tags.append(tag)
            raise ValueError(f"{self.parent.translate_string('tag_added_p0','yellow','red')}{self.parent.translate_string('tag_added_p1')}{self.parent.translate_string('tag_added_p2','yellow','green')}")
        elif mode == 'ed':
            self.tags[tag] = new_tag
        elif mode == 'del':
            try:
                del self.tags[tag]
                print(self.parent.translate_string('tag_removed','yellow','green'))
            except:
                raise ValueError(self.parent.translate_string('tag_not_found','yellow','green'))
            

    def find_the_text(self, text):
        if self.text.lower().find(text.lower()) != -1:
            return True
        else:
            return False

    def find_in_title(self, text):
        if self.title.lower().find(text.lower()) != -1:
            return search(text.lower(),self.title.lower()).span()
        else:
            return False

    def find_in_text(self, text):
        if self.text.lower().find(text.lower()) != -1:
            return search(text.lower(),self.text.lower()).span()
        else:
            return False

    def find_in_tags(self, text):
        tags = "; ".join(f"{tag}" for tag in self.tags)
        if tags.lower().find(text.lower()) != -1:
            return search(text.lower(),tags.lower()).span()
        else:
            return False

class Note(NoteChecks):
    def __init__(self, parent_class):
        self.parent = parent_class
        if self.parent:
            self.title = self.parent.translate_string('unnamed_note')
            self.text = self.parent.translate_string('none')
        else:
            self.title = "Unnamed note"
            self.text = "None"
        self.tags = []

    def note_error(func):
        def true_handler(self,arg):
            try:
                result = func(self,arg)
            except ValueError as error_text:
                raise ValueError(error_text)
        return true_handler

    @note_error
    def add_title(self,title):
        self.title = self.title_check(title)

    @note_error
    def add_text(self,text):
        self.text = self.text_check(text)

    @note_error
    def add_tags(self,tag):
        self.tag_check_and_set(mode='add', tag=tag)
            
    def load_data(self,title,text,tags): # To avoid reoccurring checks when loading from storage.bin
        self.title = title
        self.text = text
        self.tags = tags

    def __str__(self):
        return f"{self.parent.translate_string('str_self_p0','red','green')}: {self.title}; {self.parent.translate_string('str_self_p1','red','green')}: {self.tags}; {self.parent.translate_string('str_self_p2','red','green')}: {self.text}"


class NoteFile:
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
        
        self.update_file("load",0)

    def reinit(self, mode=None):
        tmp = None
        if type(self.parent.module_chosen) == int:
            tmp = self.parent.module_chosen
        if mode != 'first':
            self.parent.module_chosen = self.parent.modules.index(self)
        self.opnng = f"{self.parent.translate_string('please_enter_p0','cyan')} "
        self.non_obligatory = f"{bcolors.CYAN} ( {self.parent.translate_string('please_enter_p1')} '{self.parent.translate_string('please_enter_p2','red','cyan')}'{self.parent.translate_string('please_enter_p3')})"
        self.method_table = {'__localization':{
                                'name':"note_manager_name", 
                                'description':"note_manager_desc"},
                            'create':{
                                'description':"create_desc", 
                                'methods':{ 
                                    self.note_create:{},
                                    self.add_title:{
                                        'name':f"{self.opnng}{self.parent.translate_string('note_attr_p0')}{self.non_obligatory}"},
                                    self.add_text:{
                                        'name':f"{self.opnng}{self.parent.translate_string('note_attr_p1')}{self.non_obligatory}"},
                                    self.add_tags:{
                                        'address':f"{self.opnng}{self.parent.translate_string('note_attr_p2')}{self.non_obligatory}"},
                                    self.add_note_finisher:{}}},
                            'edit':{
                                'description':"edit_desc", 
                                'methods':{
                                    self.print_notes:{},
                                    self.choose_note_from_the_list:{
                                        'note_id':f"{self.opnng}{self.parent.translate_string('choose_note')}"},
                                    self.print_note_attributes:{},
                                    self.choose_note_attribute:{
                                        'attr_id':f"{self.opnng}{self.parent.translate_string('choose_note_attr')}"},
                                    self.edit_note:{
                                        'new_text':f"{self.opnng}{self.parent.translate_string('edit_note_text')}"},
                                    }},
                            'edit_tags':{
                                'description':"edit_tags_desc", 
                                'methods':{
                                    self.print_notes:{},
                                    self.choose_note_from_the_list:{
                                        'note_id':f"{self.opnng}{self.parent.translate_string('choose_note')}"},
                                    self.print_note_tags:{},
                                    self.choose_note_tag:{
                                        'attr_id':f"{self.opnng}{self.parent.translate_string('choose_note_tag')}"},
                                    self.edit_tags:{
                                        'new_text':f"{self.opnng}{self.parent.translate_string('edit_note_tag')}"},
                                    }},
                            'add_tag':{
                                'description':"add_tag_desc", 
                                'methods':{
                                    self.print_notes:{},
                                    self.choose_note_from_the_list:{
                                        'attr_id':f"{self.opnng}{self.parent.translate_string('choose_note')}"},
                                    self.add_tags:{
                                        'attr_id':f"{self.opnng}{self.parent.translate_string('enter_the_tag')}"},
                                    self.add_tag_finish:{},
                                    }},
                            'find':{
                                'description':"find_desc", 
                                'methods':{
                                    self.print_find_modes:{},
                                    self.choose_find_mode:{
                                        'attr_id':f"{self.opnng}{self.parent.translate_string('choose_find_mode')}"},
                                    self.find_hub:{
                                        'attr_id':f"{self.opnng}{self.parent.translate_string('find_text')}"}}},
                            'remove':{
                                'description':"remove_desc", 
                                'methods':{
                                    self.print_notes:{},
                                    self.choose_note_from_the_list:{
                                        'attr_id':f"{self.opnng}{self.parent.translate_string('choose_note')}"},
                                    self.remove_note_finish:{}}},
                            'remove_tag':{
                                'description':"remove_tag_desc", 
                                'methods':{
                                    self.print_notes:{},
                                    self.choose_note_from_the_list:{
                                        'attr_id':f"{self.opnng}{self.parent.translate_string('choose_note')}"},
                                    self.print_note_tags:{},
                                    self.choose_note_tag:{
                                        'attr_id':f"{self.opnng}{self.parent.translate_string('choose_tag_to_del')}"},
                                    self.remove_tag_finish:{}}},
                            'show_all':{
                                'description':"show_all_desc", 
                                'methods':{
                                    self.show_contacts:{}}}}
        if mode != 'first':
            self.parent.module_chosen = tmp
  


    def show_contacts(self):
        if len(self.data) > 0:
            string = self.parent.translate_string('print_contact_p0','green')
            string += ":\n" + '\n'.join(f"{bcolors.RED}{key}{bcolors.GREEN}. {self.parent.translate_string('print_contact_p1','red','green')}: {value.title}; {self.parent.translate_string('print_contact_p2','red','green')}: {value.text}; {self.parent.translate_string('print_contact_p3','red','green')}: {'; '.join(f'{tag}' for tag in value.tags)};" for key,value in self.data.items())
            print(string)
        else:
            print(self.parent.translate_string('note_list_empty','yellow','green'))
    
    def dialogue_check(self,variable):
        if variable.lower() != 'n':
            return True
        return False

    def note_create(self):
        new_note = Note(self.parent)
        self.id_assign(mode="add",record=new_note)

    def notepad_error(func):
        def true_handler(self,arg):
            try:
                result = func(self,arg)
            except ValueError as error_text:
                return str(error_text)
        return true_handler

    @notepad_error
    def add_title(self,title):
        new_note = self.data[self.ongoing]
        if self.dialogue_check(title):
            new_note.add_title(title)

    @notepad_error
    def add_text(self,text):
        new_note = self.data[self.ongoing]
        if self.dialogue_check(text):
            new_note.add_text(text)

    @notepad_error
    def add_tags(self,tags):
        new_note = self.data[self.ongoing]
        if self.dialogue_check(tags):
            new_note.add_tags(tags)

    def add_note_finisher(self):
            self.update_file(mode="add",r_id=self.generated_ids)
            self.ongoing = None

    def print_notes(self):
        if len(self.data) > 0:
            string = self.parent.translate_string('print_contact_p0','green')
            string += ":\n" + '\n'.join(f"{bcolors.RED}{key}{bcolors.GREEN}. {self.parent.translate_string('print_contact_p1','red','green')}: {value.title}; {self.parent.translate_string('print_contact_p2','red','green')}: {value.text}; {self.parent.translate_string('print_contact_p3','red','green')}: {'; '.join(f'{tag}' for tag in value.tags)};" for key,value in self.data.items())
            print(string)
        else:
            print(self.parent.translate_string('note_list_empty','yellow','green'))
            return 'abort'
    
    def print_note_attributes(self):
        string = f"{bcolors.GREEN}{self.parent.translate_string('choose_what_to_edit')}:\n"
        string += f"{bcolors.RED}0{bcolors.GREEN}. {self.parent.translate_string('print_contact_p1')}: {self.data[self.ongoing].title}\n"
        string += f"{bcolors.RED}1{bcolors.GREEN}. {self.parent.translate_string('print_contact_p2')}: {self.data[self.ongoing].text}\n"
        #string += f"{bcolors.RED}2{bcolors.GREEN}. {self.parent.translate_string('print_contact_p3')}: {self.data[self.ongoing].tags}\n"
        print(string)

    def choose_note_from_the_list(self, note_id):
        if len(self.data) > 0:
            try:
                note_id = self.input_to_id(note_id)
                if (type(note_id) == int) and (note_id in self.data.keys()):
                    self.ongoing = note_id
                elif type(note_id) == str:
                    return note_id
                else:
                    raise ValueError
            except ValueError:
                return self.parent.translate_string('note_not_found','yellow','green')
        else:
            return self.parent.translate_string('note_list_empty','yellow','green')

    def choose_note_attribute(self, field_id):
        try:
            field_id = self.input_to_id(field_id)
            if type(field_id) == int and field_id < 2:
                self.field_id = field_id
            elif type(field_id) == str:
                return field_id
            else:
                raise ValueError
        except:
                return self.parent.translate_string('wrong_id_error','yellow','green')

    @notepad_error
    def edit_note(self, new_text):
        tmp = ['print_contact_p1','print_contact_p2','print_contact_p3']
        if self.field_id == 0:
            self.data[self.ongoing].add_title(new_text)
        elif self.field_id == 1:
            self.data[self.ongoing].add_text(new_text)
        elif self.field_id == 2:
            self.data[self.ongoing].edit_tag(new_text)
        
        self.update_file(mode="ed")
        print(f"{self.parent.translate_string(tmp[self.field_id],'yellow')} {self.parent.translate_string('edited','yellow','green')}")
        self.field_id = None
        self.ongoing = None

    def print_note_tags(self):
        if len(self.data[self.ongoing].tags) > 0:
            note = self.data[self.ongoing]
            string = self.parent.translate_string('choose_the_tag','green') + ":\n"
            for i in range(len(note.tags)):
                string += f"{bcolors.RED}{i}{bcolors.GREEN}. {note.tags[i]}\n"
            print(string)
        else:
            print(self.parent.translate_string('no_tags','yellow','green'))
            return 'abort'

    def input_to_id(self, text):
        new_line = text
        if new_line.find(" "):
            map = {' ':''}
            new_line = new_line.translate(map)
        try:
            if int(new_line) >= 0:
                return int(new_line)
            else:
                return self.parent.translate_string('negative_id_error','yellow','green')
        except ValueError:
            return self.parent.translate_string('wrong_id_error','yellow','green')

    def choose_note_tag(self, field_id):
        note = self.data[self.ongoing]
        try:
            field_id = self.input_to_id(field_id)
            if type(field_id) == int and field_id < len(note.tags):
                self.field_id = field_id
            elif type(field_id) == str:
                return field_id
            else:
                raise ValueError
        except:
                return self.parent.translate_string('wrong_id_error','yellow','green')

    @notepad_error
    def edit_tags(self, new_text):
        note = self.data[self.ongoing]
        note.tag_check_and_set(mode='ed', tag=self.field_id, new_tag=new_text)
        
        print(f"{self.parent.translate_string('print_contact_p3_1','yellow','green')} {self.parent.translate_string('edited','yellow','green')}.")
        self.update_file(mode="ed")
        self.field_id = None
        self.ongoing = None

    def remove_note_finish(self):
        self.update_file(mode="del", r_id=int(self.ongoing))
        print(self.parent.translate_string('note_removed','yellow','green'))
        self.ongoing = None
  
    def add_tag_finish(self):
        self.update_file(mode="ed")
        self.field_id = None
        self.ongoing = None

    @notepad_error
    def remove_tag_finish(self):
        note = self.data[self.ongoing]
        note.tag_check_and_set(mode='del', tag=self.field_id)
        
        self.update_file(mode="ed")
        self.field_id = None
        self.ongoing = None
  
    def print_find_modes(self):
        string = self.parent.translate_string('search_attr_p0','green') + ":\n"
        string += f"{bcolors.RED}0{bcolors.GREEN}. {self.parent.translate_string('search_attr_p1')}\n{bcolors.RED}1{bcolors.GREEN}. {self.parent.translate_string('search_attr_p2')}\n{bcolors.RED}2{bcolors.GREEN}. {self.parent.translate_string('search_attr_p3')}\n{bcolors.RED}3{bcolors.GREEN}. {self.parent.translate_string('search_attr_p4')}\n"
        print(string)

    def choose_find_mode(self, field_id):
        try:
            field_id = self.input_to_id(field_id)
            if type(field_id) == int and field_id <= 3:
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
        highlighted_title = ''
        highlighted_text = ''
        highlighted_tags = ''
        if self.field_id == 0:
            for note_id,class_instance in self.data.items():
                if class_instance.find_in_title(text):
                    checker = True
                    highlighted_title = f"{bcolors.GREEN}{class_instance.title[:class_instance.find_in_title(text)[0]]}{bcolors.YELLOW}{class_instance.title[class_instance.find_in_title(text)[0]:class_instance.find_in_title(text)[1]]}{bcolors.GREEN}{class_instance.title[class_instance.find_in_title(text)[1]:]}"
                    string += f"{bcolors.RED}{note_id}{bcolors.GREEN}. {self.parent.translate_string('print_contact_p1','red','green')}: {highlighted_title}; {self.parent.translate_string('print_contact_p3','red','green')}: {class_instance.tags}; {self.parent.translate_string('print_contact_p2','red','green')}: {class_instance.text};\n"
        elif self.field_id == 1:
            for note_id,class_instance in self.data.items():
                if class_instance.find_in_text(text):
                    checker = True
                    highlighted_text = f"{bcolors.GREEN}{class_instance.text[:class_instance.find_in_text(text)[0]]}{bcolors.YELLOW}{class_instance.text[class_instance.find_in_text(text)[0]:class_instance.find_in_text(text)[1]]}{bcolors.GREEN}{class_instance.text[class_instance.find_in_text(text)[1]:]}"
                    string += f"{bcolors.RED}{note_id}{bcolors.GREEN}. {self.parent.translate_string('print_contact_p1','red','green')}: {class_instance.title}; {self.parent.translate_string('print_contact_p3','red','green')}: {class_instance.tags}; {self.parent.translate_string('print_contact_p2','red','green')}: {highlighted_text};\n"
        elif self.field_id == 2:
            for note_id,class_instance in self.data.items():
                if class_instance.find_in_tags(text):
                    checker = True
                    tags = "; ".join(f"{tag}" for tag in class_instance.tags)
                    highlighted_tags = f"{bcolors.GREEN}{tags[:class_instance.find_in_tags(text)[0]]}{bcolors.YELLOW}{tags[class_instance.find_in_tags(text)[0]:class_instance.find_in_tags(text)[1]]}{bcolors.GREEN}{tags[class_instance.find_in_tags(text)[1]:]}"
                    string += f"{bcolors.RED}{note_id}{bcolors.GREEN}. {self.parent.translate_string('print_contact_p1','red','green')}: {class_instance.title}; {self.parent.translate_string('print_contact_p3','red','green')}: {highlighted_tags}; {self.parent.translate_string('print_contact_p2','red','green')}: {class_instance.text};\n"
        elif self.field_id == 3:
            for note_id,class_instance in self.data.items():
                if class_instance.find_in_title(text):
                    checker = True
                    highlighted_title = f"{bcolors.GREEN}{class_instance.title[:class_instance.find_in_title(text)[0]]}{bcolors.YELLOW}{class_instance.title[class_instance.find_in_title(text)[0]:class_instance.find_in_title(text)[1]]}{bcolors.GREEN}{class_instance.title[class_instance.find_in_title(text)[1]:]}"
                    string += f"{bcolors.RED}{note_id}{bcolors.GREEN}. {self.parent.translate_string('print_contact_p1','red','green')}: {highlighted_title}; {self.parent.translate_string('print_contact_p3','red','green')}: {class_instance.tags}; {self.parent.translate_string('print_contact_p2','red','green')}: {class_instance.text};\n"
                elif class_instance.find_in_text(text):
                    checker = True
                    highlighted_text = f"{bcolors.GREEN}{class_instance.text[:class_instance.find_in_text(text)[0]]}{bcolors.YELLOW}{class_instance.text[class_instance.find_in_text(text)[0]:class_instance.find_in_text(text)[1]]}{bcolors.GREEN}{class_instance.text[class_instance.find_in_text(text)[1]:]}"
                    string += f"{bcolors.RED}{note_id}{bcolors.GREEN}. {self.parent.translate_string('print_contact_p1','red','green')}: {class_instance.title}; {self.parent.translate_string('print_contact_p3','red','green')}: {class_instance.tags}; {self.parent.translate_string('print_contact_p2','red','green')}: {highlighted_text};\n"
                elif class_instance.find_in_tags(text):
                    checker = True
                    tags = "; ".join(f"{tag}" for tag in class_instance.tags)
                    highlighted_tags = f"{bcolors.GREEN}{tags[:class_instance.find_in_tags(text)[0]]}{bcolors.YELLOW}{tags[class_instance.find_in_tags(text)[0]:class_instance.find_in_tags(text)[1]]}{bcolors.GREEN}{tags[class_instance.find_in_tags(text)[1]:]}"
                    string += f"{bcolors.RED}{note_id}{bcolors.GREEN}. {self.parent.translate_string('print_contact_p1','red','green')}: {class_instance.title}; {self.parent.translate_string('print_contact_p3','red','green')}: {highlighted_tags}; {self.parent.translate_string('print_contact_p2','red','green')}: {class_instance.text};\n"

        if checker:
            print(f"{self.parent.translate_string('find_intro','green')}:\n{string}")
        else:
            print(self.parent.translate_string('find_intro','yellow','green'))

    
    def id_assign(self,mode:str,record:Note):
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

    # Prepares self.data[id] to be saved.
    # Explanation: operates in one mode: 'add' (requires record id). returns prepared dict with record variables. 
    # Used to add new lines to the file.bin
    def prepare_data(self,mode:str,record_id=None):
        if mode == "add":
            for rid,record in self.data.items():
                if rid == record_id:
                    return {'Title':record.title,'Text':record.text,'Tags':record.tags}
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
                        pickle.dump({'Title':record.title,'Text':record.text,'Tags':record.tags},storage)
                        id_generator += 1
                    self.generated_ids = id_generator
                else:
                    print(self.parent.translate_string('note_list_empty','yellow','green'))
        elif mode == "ed":
            with open(file, 'wb') as storage:
                if len(self.data) > 0:
                    id_generator = 0
                    for id,record in self.data.items():
                        pickle.dump({'Title':record.title,'Text':record.text,'Tags':record.tags},storage)
                        id_generator += 1
                    self.generated_ids = id_generator
        elif mode == "load":
            with open(file, 'rb') as storage:
                if file.stat().st_size != 0:
                    id_generator = 0
                    try:
                        while True:  
                            record = pickle.load(storage)
                            self.data[id_generator] = Note(parent_class=self.parent)
                            self.data[id_generator].load_data(title=record['Title'],text=record['Text'],tags=record['Tags'])
                            id_generator += 1
                    except EOFError:
                        self.generated_ids = id_generator
                        self.record_cnt = id_generator
                        #print('Reached the end of file!')
