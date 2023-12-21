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
            error_text = {'en':"Wrong title format: the title cannot be empty.",'ua':"Некоректний формат заголовку: заголовок не може бути порожнім."}
            raise ValueError(error_text[self.language])

    def text_check(self,text): #Закоментував, бо немає необхідності використовувати. Треба - розкоментовуєш та коментуєш останній return.
        # if text != '':
        #     return text
        # else:
        #     error_text = {'en':"Wrong note format: the note cannot be empty.",'ua':"Некоректний формат нотатки: нотатка не може бути порожньою."}
        #     raise ValueError(error_text[self.language])
        return text

    def tag_check_and_set(self,mode,tag,new_tag=None):
        if tag == '':
            error_text = {'en':"Wrong tag format: the tag cannot be empty.",'ua':"Некоректний формат тегу: тег не може бути порожнім."}
            raise ValueError(error_text[self.language])
        elif mode == 'add':
            if tag.lower() == "stop":
                return True
            self.tags.append(tag)
            error_text = {'en':f"{bcolors.GREEN}Tag added. if you want to add another one, enter it in the console. When you are done, just enter '{bcolors.RED}stop{bcolors.GREEN}' in the console.",'ua':f"{bcolors.GREEN}Тег додано. Якщо бажаєте додати ще один, введіть його у консоль. Коли додасте всі, що хотіли, просто пропишіть '{bcolors.RED}stop{bcolors.GREEN}' у консоль"}
            raise ValueError(error_text[self.language])
        elif mode == 'ed':
            self.tags[tag] = new_tag
        elif mode == 'del':
            error_text = {}
            try:
                del self.tags[tag]
                error_text = {'en':f"{bcolors.YELLOW}Tag removed.{bcolors.GREEN}",'ua':f"{bcolors.YELLOW}Тег видалено.{bcolors.GREEN}"}
                print(error_text[self.language])
            except:
                error_text = {'en':f"{bcolors.GREEN}No tag with such name!",'ua':f"{bcolors.GREEN}Такого тегу не існує!"}
                raise ValueError(error_text[self.language])
            

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
    def __init__(self):
        self.title = "Unnamed note"
        self.text = ""
        self.tags = []
        self.language = None


    def add_title(self,title):
        try:
            self.title = self.title_check(title)
            return
        except ValueError as error_text:
            raise ValueError(error_text)

    
    def add_text(self,text):
        try:
            self.text = self.text_check(text)
            return
        except ValueError as error_text:
            raise ValueError(error_text)
            
            
    def add_tags(self,tag):
        try:
            self.tag_check_and_set(mode='add', tag=tag)
            return
        except ValueError as error_text:
            raise ValueError(error_text)
            
    def load_data(self,title,text,tags): # To avoid reoccurring checks when loading from storage.bin
        self.title = title
        self.text = text
        self.tags = tags

    def __str__(self):
        string = {'en':f"Note found with title {self.title}; tags {self.tags}; text {self.text}",'ua':f"Нотатку знайдено з заголовком {self.title}; тегами {self.tags}; текстом {self.text}"}
        return string[self.language]


class NoteFile:
    def __init__(self):
        self.data = {}
        self.priority_ids = []
        self.language = None
        self.record_cnt = 0
        self.generated_ids = 0
        self.file = "note_storage.bin"
        
        self.update_file("load",0)

        self.opnng = f"{bcolors.CYAN}Введіть, будь ласка, "
        self.non_obligatory = f"{bcolors.CYAN}( або '{bcolors.RED}N{bcolors.CYAN}', якщо бажаєте додати пізніше)"
        self.opnng_en = f"{bcolors.CYAN}Please, enter the "
        self.non_obligatory_en = f"{bcolors.CYAN}( or '{bcolors.RED}N{bcolors.CYAN}', if you want to add it later)"
        self.method_table = {'__localization_insert':{
                                'name':{
                                    'en':"note manager", 
                                    'ua':"менеджера нотаток"},
                                'description':{
                                    'en':"note manager", 
                                    'ua':"менеджер нотаток"}},
                            'create':{
                                'description':{
                                    'en':"Adds a new record to the note book. You can add a title, text, tags - either when creating a record, or later.",
                                    'ua':"Додає новий запис до книги нотаток. Можна додати заголовок, текст та теги одразу, а можна й пізніше."}, 
                                'methods':{ 
                                    self.note_create:{},
                                    self.add_title:{
                                        'name':{
                                            'en':f"{self.opnng_en}title{self.non_obligatory_en}",
                                            'ua':f"{self.opnng}заголовок{self.non_obligatory}"}},
                                    self.add_text:{
                                        'name':{
                                            'en':f"{self.opnng_en}text{self.non_obligatory_en}",
                                            'ua':f"{self.opnng}текст{self.non_obligatory}"}},
                                    self.add_tags:{
                                        'address':{
                                            'en':f"{self.opnng_en}tag{self.non_obligatory_en}",
                                            'ua':f"{self.opnng}тег{self.non_obligatory}"}},
                                    self.add_note_finisher:{}}},
                            'edit':{
                                'description':{
                                    'en':"Edits the title, or the text of a note.",
                                    'ua':"Редагує заголовок, або текст нотатки."}, 
                                'methods':{
                                    self.print_notes:{},
                                    self.choose_note_from_the_list:{
                                        'note_id':{
                                            'en':f"{self.opnng_en}number of a note you want to edit",
                                            'ua':f"{self.opnng}номер нотатки, яку ви хочете відредагувати"}},
                                    self.print_note_attributes:{},
                                    self.choose_note_attribute:{
                                        'attr_id':{
                                            'en':f"{self.opnng_en}what you are going to edit",
                                            'ua':f"{self.opnng}що ви збираєтесь редагувати"}},
                                    self.edit_note:{
                                        'new_text':{
                                            'en':f"{self.opnng_en}new text",
                                            'ua':f"{self.opnng}новий текст"}},
                                    }},
                            'edit_tags':{
                                'description':{
                                    'en':"Edits the tags of a note.",
                                    'ua':"Редагує теги нотатки."}, 
                                'methods':{
                                    self.print_notes:{},
                                    self.choose_note_from_the_list:{
                                        'note_id':{
                                            'en':f"{self.opnng_en}number of a note, which has the tag you want to edit",
                                            'ua':f"{self.opnng}номер нотатки, тег якої ви хочете відредагувати"}},
                                    self.print_note_tags:{},
                                    self.choose_note_tag:{
                                        'attr_id':{
                                            'en':f"{self.opnng_en}tag you are going to edit",
                                            'ua':f"{self.opnng}тег, який ви збираєтесь редагувати"}},
                                    self.edit_tags:{
                                        'new_text':{
                                            'en':f"{self.opnng_en}new tag",
                                            'ua':f"{self.opnng}новий тег"}},
                                    }},
                            'add_tag':{
                                'description':{
                                    'en':"Add a new tag to the note.",
                                    'ua':"Додає новий тег до нотатки."}, 
                                'methods':{
                                    self.print_notes:{},
                                    self.choose_note_from_the_list:{
                                        'attr_id':{
                                            'en':f"{self.opnng_en}number of the note, which you are going to edit",
                                            'ua':f"{self.opnng}номер нотатки, теги якої ви збираєтесь редагувати"}},
                                    self.add_tags:{
                                        'attr_id':{
                                            'en':f"{self.opnng_en}tag, which you are going to add",
                                            'ua':f"{self.opnng}тег, який ви хочете додати"}},
                                    self.add_tag_finish:{},
                                    }},
                            'find':{
                                'description':{
                                    'en':"Looks for a specified text in the notes.",
                                    'ua':"Шукає введений текст у нотатках."}, 
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
                                    'en':"Deletes the note.",
                                    'ua':"Видаляє нотатку."}, 
                                'methods':{
                                    self.print_notes:{},
                                    self.choose_note_from_the_list:{
                                        'attr_id':{
                                            'en':f"{self.opnng_en}note you are going to delete",
                                            'ua':f"{self.opnng}нотатку, яку збираєтесь видалити"}},
                                    self.remove_note_finish:{}}},
                            'remove_tag':{
                                'description':{
                                    'en':"Deletes one of the tags of the chosen note.",
                                    'ua':"Видаляє один з тегів обраної нотатки."}, 
                                'methods':{
                                    self.print_notes:{},
                                    self.choose_note_from_the_list:{
                                        'attr_id':{
                                            'en':f"{self.opnng_en}note, where the tag is",
                                            'ua':f"{self.opnng}нотатку, де знаходиться тег"}},
                                    self.print_note_tags:{},
                                    self.choose_note_tag:{
                                        'attr_id':{
                                            'en':f"{self.opnng_en}the tag you are going to delete",
                                            'ua':f"{self.opnng}тег, який ви збираєтеся видалити"}},
                                    self.remove_tag_finish:{}}}}


    def dialogue_check(self,variable):
        if variable.lower() != 'n':
            return True
        return False

    def note_create(self):
        new_note = Note()
        new_note.language = self.language
        self.id_assign(mode="add",record=new_note)


    def add_title(self,title):
        new_note = self.data[self.ongoing]
        new_note.language = self.language
        if self.dialogue_check(title):
            try:
                new_note.add_title(title)
            except ValueError as error_text:
                return str(error_text)
            
            return True

    def add_text(self,text):
        new_note = self.data[self.ongoing]
        new_note.language = self.language
        if self.dialogue_check(text):
            try:
                new_note.add_text(text)
            except ValueError as error_text:
                return str(error_text)
            
            return True

    def add_tags(self,tags):
        new_note = self.data[self.ongoing]
        new_note.language = self.language
        if self.dialogue_check(tags):
            try:
                new_note.add_tags(tags)
                return True
            except ValueError as error_text:
                return str(error_text)
            

    def add_note_finisher(self):
            self.update_file(mode="add",r_id=self.generated_ids)
            self.ongoing = None


    def print_notes(self):
        local = {'part_0':{
                    'en':"Saved notes list",
                    'ua':"Наразі збережені такі нотатки"},
                'part_1':{
                    'en':"Title",
                    'ua':"Заголовок"},
                'part_2':{
                    'en':"Text",
                    'ua':"Текст"},
                'part_3':{
                    'en':"Tags",
                    'ua':"Теги"},
                'part_4':{
                    'en':"To choose the note, enter it's respective number in a console",
                    'ua':"Щоб обрати нотатку, введіть у консоль її номер у списку"},}
        string = f"{bcolors.GREEN}{local['part_0'][self.language]}:\n"
        string += '\n'.join(f"{bcolors.RED}{key}{bcolors.GREEN}. {local['part_1'][self.language]}: {value.title}; {local['part_2'][self.language]}: {value.text}; {local['part_3'][self.language]}: {'; '.join(f'{tag}' for tag in value.tags)};" for key,value in self.data.items()) + f"\n{bcolors.RED}{local['part_4'][self.language]}{bcolors.GREEN}\n"
        print(string)
    
    def print_note_attributes(self):
        local = {'part_0':{
                    'en':"Choose, what you are going to edit",
                    'ua':"Оберіть, що ви хочете редагувати"},
                'part_1':{
                    'en':"Title",
                    'ua':"Заголовок"},
                'part_2':{
                    'en':"Text",
                    'ua':"Текст"},
                'part_3':{
                    'en':"Tags",
                    'ua':"Теги"}}
        string = f"{bcolors.GREEN}{local['part_0'][self.language]}:\n"
        string += f"{bcolors.RED}0{bcolors.GREEN}. {local['part_1'][self.language]}: {self.data[self.ongoing].title}\n"
        string += f"{bcolors.RED}1{bcolors.GREEN}. {local['part_2'][self.language]}: {self.data[self.ongoing].text}\n"
        #string += f"{bcolors.RED}2{bcolors.GREEN}. {local['part_3'][self.language]}: {self.data[self.ongoing].tags}\n"
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
                error_text = {'en':f"{bcolors.YELLOW}There is no note with this id, try again!{bcolors.GREEN}",'ua':f"{bcolors.YELLOW}Нотатки з таким id немає, спробуйте ще раз!{bcolors.GREEN}"}
                return error_text[self.language]
        else:
            error_text = {'en':f"{bcolors.YELLOW}Note list is empty!{bcolors.GREEN}",'ua':f"{bcolors.YELLOW}Список нотаток порожній!{bcolors.GREEN}"}
            return error_text[self.language]

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
                error_text = {'en':f"{bcolors.YELLOW}Wrong id, try again!{bcolors.GREEN}",'ua':f"{bcolors.YELLOW}Некоректний id, спробуйте ще раз!{bcolors.GREEN}"}
                return error_text[self.language]
        
    def edit_note(self, new_text):
        self.data[self.ongoing].language = self.language
        tmp = [{'en':"Title", 'ua':"Заголовок"},{'en':"Text", 'ua':"Текст"},{'en':"Tags", 'ua':"Теги"}]
        done_text = {'en':f"{bcolors.GREEN}{tmp[self.field_id][self.language]} edited.",'ua':f"{bcolors.YELLOW}{tmp[self.field_id][self.language]} відредагований.{bcolors.GREEN}"}
        if self.field_id == 0:
            try:
                self.data[self.ongoing].add_title(new_text)
            except ValueError as error_text:
                return str(error_text)
        elif self.field_id == 1:
            try:
                self.data[self.ongoing].add_text(new_text)
            except ValueError as error_text:
                return str(error_text)
        elif self.field_id == 2:
            try:
                self.data[self.ongoing].edit_tag(new_text)
            except ValueError as error_text:
                return str(error_text)
        
        self.update_file(mode="ed")
        self.field_id = None
        self.ongoing = None
        print(done_text[self.language])

    def print_note_tags(self):
        local = {'part_0':{
                    'en':"Choose the tag you need",
                    'ua':"Оберіть потрібний тег"}}
        note = self.data[self.ongoing]
        string = f"{bcolors.GREEN}{local['part_0'][self.language]}:\n"
        for i in range(len(note.tags)):
            string += f"{bcolors.RED}{i}{bcolors.GREEN}. {note.tags[i]}\n"
        print(string)

    def input_to_id(self, text):
        new_line = text
        if new_line.find(" "):
            map = {' ':''}
            new_line = new_line.translate(map)
        try:
            if int(new_line) >= 0:
                return int(new_line)
            else:
                error_text = {'en':f"{bcolors.YELLOW}An id cannot be a negative number!{bcolors.GREEN}",'ua':f"{bcolors.YELLOW}Id не може бути від'ємним числом!{bcolors.GREEN}"}
                return error_text[self.language]
        except ValueError:
            error_text = {'en':f"{bcolors.YELLOW}Wrong id, try again!{bcolors.GREEN}",'ua':f"{bcolors.YELLOW}Некоректний id, спробуйте ще раз!{bcolors.GREEN}"}
            return error_text[self.language]

    def choose_note_tag(self, field_id):
        note = self.data[self.ongoing]
        try:
            field_id = self.input_to_id(field_id)
            if type(field_id) == int and field_id <= len(note.tags):
                self.field_id = field_id
            elif type(field_id) == str:
                return field_id
            else:
                raise ValueError
        except:
                error_text = {'en':f"{bcolors.YELLOW}Wrong id, try again!{bcolors.GREEN}",'ua':f"{bcolors.YELLOW}Некоректний id, спробуйте ще раз!{bcolors.GREEN}"}
                return error_text[self.language]
        
    def edit_tags(self, new_text):
        note = self.data[self.ongoing]
        note.language = self.language
        local = {'en':"Tag", 'ua':"Тег"}
        done_text = {'en':f"{bcolors.GREEN}{local[self.language]} edited.",'ua':f"{bcolors.YELLOW}{local[self.language]} відредагований.{bcolors.GREEN}"}
        try:
            note.tag_check_and_set(mode='ed', tag=self.field_id, new_tag=new_text)
        except ValueError as error_text:
            return str(error_text)
        
        self.update_file(mode="ed")
        self.field_id = None
        self.ongoing = None
        print(done_text[self.language])

    def remove_note_finish(self):
        self.update_file(mode="del", r_id=int(self.ongoing))
        done_text = {'en':f"{bcolors.YELLOW}Note removed.{bcolors.GREEN}",'ua':f"{bcolors.YELLOW}Нотатка видалена.{bcolors.GREEN}"}
        print(done_text[self.language])
        self.ongoing = None
  
    def add_tag_finish(self):
        self.update_file(mode="ed")
        self.field_id = None
        self.ongoing = None
  
    def remove_tag_finish(self):
        note = self.data[self.ongoing]
        note.language = self.language
        try:
            note.tag_check_and_set(mode='del', tag=self.field_id)
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
                    'en':"In the titles.",
                    'ua':"У заголовках."},
                'part_2':{
                    'en':"In the text.",
                    'ua':"У тексті."},
                'part_3':{
                    'en':"In the tags.",
                    'ua':"У тегах."},
                'part_4':{
                    'en':"Everywhere.",
                    'ua':"Всюди."}}
        
        string = f"{bcolors.GREEN}{local['part_0'][self.language]}:\n"
        string += f"{bcolors.RED}0{bcolors.GREEN}. {local['part_1'][self.language]}\n{bcolors.RED}1{bcolors.GREEN}. {local['part_2'][self.language]}\n{bcolors.RED}2{bcolors.GREEN}. {local['part_3'][self.language]}\n{bcolors.RED}3{bcolors.GREEN}. {local['part_4'][self.language]}\n"
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
                error_text = {'en':f"{bcolors.YELLOW}Wrong id, try again!{bcolors.GREEN}",'ua':f"{bcolors.YELLOW}Некоректний id, спробуйте ще раз!{bcolors.GREEN}"}
                return error_text[self.language]
        
    def find_hub(self, text):
        checker = False
        string = ""
        local = {'Failure':{'en':f"Specified text not found",'ua':f"Вказаний текст не знайдено"},'Intro':{'en':f"Specified text found in the next notes",'ua':f"Вказаний текст знайдено у наступних нотатках"},'Title':{'en':f"Title",'ua':f"Заголовок"},'Text':{'en':f"text",'ua':f"текст"},'Tags':{'en':f"tags",'ua':f"теги"}}
        success = f"{local['Intro'][self.language]}:\n"
        failure = f"{local['Failure'][self.language]}!"
        highlighted_title = ''
        highlighted_text = ''
        highlighted_tags = ''
        if self.field_id == 0:
            for note_id,class_instance in self.data.items():
                if class_instance.find_in_title(text):
                    checker = True
                    highlighted_title = f"{bcolors.GREEN}{class_instance.title[:class_instance.find_in_title(text)[0]]}{bcolors.YELLOW}{class_instance.title[class_instance.find_in_title(text)[0]:class_instance.find_in_title(text)[1]]}{bcolors.GREEN}{class_instance.title[class_instance.find_in_title(text)[1]:]}"
                    string += f"{bcolors.RED}{note_id}{bcolors.GREEN}. {local['Title'][self.language]}: {highlighted_title}; {local['Tags'][self.language]}: {class_instance.tags}; {local['Text'][self.language]}: {class_instance.text};\n"
        elif self.field_id == 1:
            for note_id,class_instance in self.data.items():
                if class_instance.find_in_text(text):
                    checker = True
                    highlighted_text = f"{bcolors.GREEN}{class_instance.text[:class_instance.find_in_text(text)[0]]}{bcolors.YELLOW}{class_instance.text[class_instance.find_in_text(text)[0]:class_instance.find_in_text(text)[1]]}{bcolors.GREEN}{class_instance.title[class_instance.find_in_text(text)[1]:]}"
                    string += f"{bcolors.RED}{note_id}{bcolors.GREEN}. {local['Title'][self.language]}: {class_instance.title}; {local['Tags'][self.language]}: {class_instance.tags}; {local['Text'][self.language]}: {highlighted_text};\n"
        elif self.field_id == 2:
            for note_id,class_instance in self.data.items():
                if class_instance.find_in_tags(text):
                    checker = True
                    tags = "; ".join(f"{tag}" for tag in class_instance.tags)
                    highlighted_tags = f"{bcolors.GREEN}{tags[:class_instance.find_in_tags(text)[0]]}{bcolors.YELLOW}{tags[class_instance.find_in_tags(text)[0]:class_instance.find_in_tags(text)[1]]}{bcolors.GREEN}{tags[class_instance.find_in_tags(text)[1]:]}"
                    string += f"{bcolors.RED}{note_id}{bcolors.GREEN}. {local['Title'][self.language]}: {class_instance.title}; {local['Tags'][self.language]}: {highlighted_tags}; {local['Text'][self.language]}: {class_instance.text};\n"
        elif self.field_id == 3:
            for note_id,class_instance in self.data.items():
                if class_instance.find_in_title(text):
                    checker = True
                    highlighted_title = f"{bcolors.GREEN}{class_instance.title[:class_instance.find_in_title(text)[0]]}{bcolors.YELLOW}{class_instance.title[class_instance.find_in_title(text)[0]:class_instance.find_in_title(text)[1]]}{bcolors.GREEN}{class_instance.title[class_instance.find_in_title(text)[1]:]}"
                    string += f"{bcolors.RED}{note_id}{bcolors.GREEN}. {local['Title'][self.language]}: {highlighted_title}; {local['Tags'][self.language]}: {class_instance.tags}; {local['Text'][self.language]}: {class_instance.text};\n"
                elif class_instance.find_in_text(text):
                    checker = True
                    highlighted_text = f"{bcolors.GREEN}{class_instance.text[:class_instance.find_in_text(text)[0]]}{bcolors.YELLOW}{class_instance.text[class_instance.find_in_text(text)[0]:class_instance.find_in_text(text)[1]]}{bcolors.GREEN}{class_instance.text[class_instance.find_in_text(text)[1]:]}"
                    string += f"{bcolors.RED}{note_id}{bcolors.GREEN}. {local['Title'][self.language]}: {class_instance.title}; {local['Tags'][self.language]}: {class_instance.tags}; {local['Text'][self.language]}: {highlighted_text};\n"
                elif class_instance.find_in_tags(text):
                    checker = True
                    tags = "; ".join(f"{tag}" for tag in class_instance.tags)
                    highlighted_tags = f"{bcolors.GREEN}{tags[:class_instance.find_in_tags(text)[0]]}{bcolors.YELLOW}{tags[class_instance.find_in_tags(text)[0]:class_instance.find_in_tags(text)[1]]}{bcolors.GREEN}{tags[class_instance.find_in_tags(text)[1]:]}"
                    string += f"{bcolors.RED}{note_id}{bcolors.GREEN}. {local['Title'][self.language]}: {class_instance.title}; {local['Tags'][self.language]}: {highlighted_tags}; {local['Text'][self.language]}: {class_instance.text};\n"

        if checker:
            print(f"{success}{string}")
        else:
            print(f"{failure}")

    
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
                    error_text = {'en':f"{bcolors.YELLOW}Note list is empty!{bcolors.GREEN}",'ua':f"{bcolors.YELLOW}Список нотаток порожній!{bcolors.GREEN}"}
                    print(error_text[self.language])
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
                            self.data[id_generator] = Note()
                            self.data[id_generator].load_data(title=record['Title'],text=record['Text'],tags=record['Tags'])
                            id_generator += 1
                    except EOFError:
                        self.generated_ids = id_generator
                        self.record_cnt = id_generator
                        #print('Reached the end of file!')
