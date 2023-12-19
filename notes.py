import pickle

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

    def tag_check_and_set(self,tag):
        if tag.lower() == "stop":
            return True
        if tag != '':
            self.tags.append(tag)
            error_text = {'en':f"{bcolors.GREEN}Tag added. if you want to add another one, enter it in the console. When you are done, just enter '{bcolors.RED}stop{bcolors.GREEN}' in the console.",'ua':f"{bcolors.GREEN}Тег додано. Якщо бажаєте додати ще один, введіть його у консоль. Коли додасте всі, що хотіли, просто пропишіть '{bcolors.RED}stop{bcolors.GREEN}' у консоль"}
            raise ValueError(error_text[self.language])
        else:
            error_text = {'en':"Wrong title format: the title cannot be empty.",'ua':"Некоректний формат заголовку: заголовок не може бути порожнім."}
            raise ValueError(error_text[self.language])

class Note(NoteChecks):
    def __init__(self):
        self.title = "Unnamed note" # Заголовок нотатки
        self.text = "" # Текст нашої нотатки
        self.tags = [] # Теги нашої нотатки (необов'язково)
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
            self.tag_check_and_set(tag)
            return
        except ValueError as error_text:
            raise ValueError(error_text)
            
    def load_data(self,title,text,tags): # To avoid reoccurring checks when loading from storage.bin
        self.title = title
        self.text = text
        self.tags = tags

    def __str__(self):
        return f"'{self.text}'" # Використовуємо для повернення текстових представлень об'єктів


class NoteFile:
    def __init__(self):
        self.data = {}
        self.priority_ids = []
        self.language = None
        self.record_cnt = 0
        self.generated_ids = 0
        self.file = "note_storage.bin"
        
        self.update_file("load",0)
        #print(self.data)

        self.opnng = f"{bcolors.CYAN}Введіть, будь ласка, "
        self.non_obligatory = f"{bcolors.CYAN}( або '{bcolors.RED}N{bcolors.CYAN}', якщо бажаєте додати пізніше)"
        self.opnng_en = f"{bcolors.CYAN}Please, enter the "
        self.non_obligatory_en = f"{bcolors.CYAN}( or '{bcolors.RED}N{bcolors.CYAN}', if you want to add it later)"
        self.method_table = {'__localization_insert':{
                                'name':{
                                    'en':"of the note manager", 
                                    'ua':"менеджера нотаток"},
                                'description':{
                                    'en':"note manager", 
                                    'ua':"менеджер натотак"}},
                            'create':{
                                'description':{
                                    'en':"Adds a new record to the note book. You can add a title, text, tags - either when creating a record, or later.",
                                    'ua':"Додає новий запис до книги нотаток. Можна додати заголовок, текст, та теги одразу, а можна й пізніше."}, 
                                'methods':{
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
                                            'ua':f"{self.opnng}тег{self.non_obligatory}"}}}}}

    def dialogue_check(self,variable):
        if variable.lower() != 'n':
            return True
        return False

    def add_title(self,title):
        new_note = Note()
        new_note.language = self.language
        if self.dialogue_check(title):
            try:
                new_note.add_title(title)
            except ValueError as error_text:
                return str(error_text)
            
            self.id_assign(mode="add",record=new_note)
            return True

    def add_text(self,text):
        new_note = self.data[self.ongoing]
        if self.dialogue_check(text):
            try:
                new_note.add_text(text)
            except ValueError as error_text:
                return str(error_text)
            
            return True

    def add_tags(self,tags):
        new_note = self.data[self.ongoing]
        if self.dialogue_check(tags):
            try:
                new_note.add_tags(tags)
            except ValueError as error_text:
                return str(error_text)
            
            self.update_file(mode="add",r_id=self.generated_ids)
            self.ongoing = None
            return True


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
                        pickle.dump({'Title':record.title,'Text':record.text,'Tags':record.tags},storage)
                        id_generator += 1
                    self.generated_ids = id_generator
                else:
                    print("ERROR!\nNo such record exists!")
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
                        print('Reached the end of file!')
            #print(self.data)

    # def load_notes(self):
    #     try:
    #         with open(self.file_name, 'rb') as file:
    #             notes = pickle.load(file) # Завантаження нотаток з файлу за допомогою pickle
    #     except FileNotFoundError:
    #         notes = [] # Якщо файл не знайдено, створюємо порожній список
    #     return notes

    # def save_notes(self):
    #     with open(self.file_name, 'wb') as file:
    #         pickle.dump(self.notes, file) # Збереження нотаток у файл за допомогою pickle

    # def create_note(self, title, text, tags=None):
    #     note = Note(title, text, tags) # Створення нової нотатки
    #     self.notes.append(note) # Додавання нотатки до списку
    #     self.save_notes() # Збереження нотаток у файл
    #     return note

    # def find_note_by_text(self, text):
    #     found_notes = []
    #     for note in self.notes:
    #         if text.lower() in note.text.lower(): # Переводимо текст пошуку і нотатки до нижнього регістру
    #             found_notes.append(note)
    #     return found_notes

    # def edit_note_text(self, note_title, new_text):
    #     note_title.text = new_text # Заміна тексту нотатки
    #     self.save_notes()

    # def delete_note(self, note_title):  
    #     self.notes.remove(note_title) # Видалення нотатки зі списку
    #     self.save_notes()

    # def add_tags_to_note(self, note_title, tags):
    #     note_title.tags.extend(tags) # Додавання тегів/ключових слів до знайденої нотатки
    #     self.save_notes()
 
    # def find_notes_by_tags(self, tags):
    #     found_notes = [] # Список для збереження знайдених нотаток
    #     if not tags: # Якщо список тегів порожній
    #         found_notes = [note for note in self.notes if not note.tags] # Вибираємо нотатки з пустими полями тегів
    #     else:
    #         for note in self.notes:
    #             if any(tag in note.tags for tag in tags):
    #                 found_notes.append(note)
    #     return found_notes

    # def sort_notes_by_tags(self):
    #     return sorted(self.notes, key=lambda note: note.tags) # Сортування нотаток за тегами/ключовими словами
    
    # def find_notes_by_title(self, title):
    #     found_notes = [] 
    #     for note in self.notes:
    #         if note.title.lower() == title.lower():
    #             found_notes.append(note)

    #     if found_notes:
    #         print(f"{bcolors.GREEN}\nFound {len(found_notes)} note(s) with title '{title}':{bcolors.DEFAULT}\n")
    #         for i, note in enumerate(found_notes):
    #             print(f"{bcolors.RED}{i + 1}.{bcolors.DEFAULT} {note.title}") # Для зручності користувача нумеруємо нотатки з 1, а не з 0, як індекси.
    #             print(f"{bcolors.GREEN}Selected note text:{bcolors.DEFAULT} {note.text}")
    #             print()
    #         selected_note = None # В цю змінну буде збережена обрана користувачем нотатка
    #         while selected_note is None:
    #             if len(found_notes) > 1: # Виконуємо блок, якщо вказаний заголовок є більше ніж у одної нотатки
    #                 choice = input(f"{bcolors.CYAN}Enter the number of the note you want to select:{bcolors.GREEN} ")
    #                 try:
    #                     index = int(choice) - 1 # Переводимо ввід користувача в int і зменшуємо значення на 1, щоб отримати індекс в found_notes
    #                     selected_note = found_notes[index] # Якщо в found_notes є елемент з цим індексом, то обрана нотатка буде присвоєна змінній
    #                 except (ValueError, IndexError):
    #                     print(f"{bcolors.BOLD_RED}Invalid choice. Please try again!{bcolors.DEFAULT}")
    #             else: 
    #                 selected_note = found_notes[0]
    #         return selected_note
    #     else:
    #         print(f"{bcolors.GREEN}No notes found with title {bcolors.RED}'{title}'!")
    #         return


# file_name = "notes.bin" # Назва файлу для збереження нотаток
# note_file = NoteFile(file_name) # Створення об'єкту класу NoteFile

# while True:
#     print(f"\n{bcolors.CYAN}Available operations:\n")
#     print(f"{bcolors.RED}1. {bcolors.GREEN}Create a new note")
#     print(f"{bcolors.RED}2. {bcolors.GREEN}Find a note by text")
#     print(f"{bcolors.RED}3. {bcolors.GREEN}Edit note text")
#     print(f"{bcolors.RED}4. {bcolors.GREEN}Delete a note")
#     print(f"{bcolors.RED}5. {bcolors.GREEN}Add tags/keywords to a note")
#     print(f"{bcolors.RED}6. {bcolors.GREEN}Find notes by tags/keywords")
#     print(f"{bcolors.RED}7. {bcolors.GREEN}Sort notes by tags/keywords")
#     print(f"{bcolors.RED}8. {bcolors.GREEN}Exit")

#     print(f"{bcolors.BOLD}-{bcolors.DEFAULT}" * 50)

#     choice = input(f"{bcolors.CYAN}Enter the number of the desired operation:{bcolors.GREEN} ")
    
#     if choice == "1":
#         title = input(f"{bcolors.CYAN}Enter the note title:{bcolors.GREEN} ").strip()
#         if title:
#             text = input(f"{bcolors.CYAN}Enter the note text:{bcolors.GREEN} ").strip()
#             if text:
#                 tags = input(f"{bcolors.CYAN}Enter tags/keywords for the note separated by spaces (optional):{bcolors.GREEN} ").lower().strip().split()
#                 note = note_file.create_note(title, text, tags)
#                 print(f"{bcolors.GREEN}Note with title {bcolors.RED}'{title}'{bcolors.GREEN} created successfully!")
#             else:
#                 print(f"{bcolors.BOLD_RED}Text cannot be empty. Please try again!")
#         else:
#             print(f"{bcolors.BOLD_RED}Title cannot be empty. Please try again!")

#     elif choice == "2":
#         text = input(f"{bcolors.CYAN}Enter the text to search (if space - all notes will be displayed):{bcolors.GREEN} ")
#         found_notes = note_file.find_note_by_text(text)
#         if found_notes:
#             print(f"{bcolors.GREEN}\nFound {len(found_notes)} note(s):{bcolors.DEFAULT}\n")
#             for note in found_notes:
#                 print(f"{bcolors.YELLOW}Title:{bcolors.DEFAULT} {note.title}")
#                 print(f"{bcolors.YELLOW}Text:{bcolors.DEFAULT} {note.text}")
#                 print(f"{bcolors.YELLOW}Tags/Keywords:{bcolors.DEFAULT} {note.tags}")
#                 print()
#         else:
#             print(f"{bcolors.GREEN}No notes found with that text!")
      
#     elif choice == "3":
#         title = input(f"{bcolors.CYAN}Enter the note title to edit:{bcolors.GREEN} ")
#         found_note = note_file.find_notes_by_title(title)
#         if found_note:
#             while True:
#                 question = input(f"{bcolors.CYAN}Are you sure you want to edit this note? (y/n):{bcolors.GREEN} ")
#                 if question.lower() == 'y':
#                     new_text = input(f"{bcolors.CYAN}Enter the new text:{bcolors.GREEN} ")
#                     note_file.edit_note_text(found_note, new_text)
#                     print(f"{bcolors.GREEN}Note text with title {bcolors.RED}'{title}'{bcolors.GREEN} changed to {bcolors.RED}'{new_text}'")
#                     break
#                 elif question.lower() == 'n':
#                     print(f"{bcolors.GREEN}Note editing canceled!")
#                     break
#                 else:
#                     print(f"{bcolors.BOLD_RED}Wrong input. Try again!{bcolors.DEFAULT}")

#     elif choice == "4":
#         title = input(f"{bcolors.CYAN}Enter the note title to delete:{bcolors.GREEN} ")
#         found_note = note_file.find_notes_by_title(title)
#         if found_note:
#             while True:
#                 question = input(f"{bcolors.CYAN}Are you sure you want to delete this note? (y/n):{bcolors.GREEN} ")
#                 if question.lower() == 'y':
#                     note_file.delete_note(found_note)
#                     print(f"{bcolors.GREEN}Note with title {bcolors.RED}'{title}'{bcolors.GREEN} deleted successfully")
#                     break
#                 elif question.lower() == 'n':
#                     print(f"{bcolors.GREEN}Deletion canceled!")
#                     break
#                 else:
#                     print(f"{bcolors.BOLD_RED}Wrong input. Try again!{bcolors.DEFAULT}")

#     elif choice == "5":
#         title = input(f"{bcolors.CYAN}Enter the note title to add tags/keywords to:{bcolors.GREEN} ") 
#         found_note = note_file.find_notes_by_title(title)
#         if found_note:
#             while True:
#                 question = input(f"{bcolors.CYAN}Are you sure you want to add tags/keywords to this note? (y/n):{bcolors.GREEN} ")
#                 if question.lower() == 'y':
#                     tags = input(f"{bcolors.CYAN}Enter tags/keywords to add (separated by spaces):{bcolors.GREEN} ").split()
#                     note_file.add_tags_to_note(found_note, tags)
#                     print(f"{bcolors.GREEN}Tags/keywords added to the note with title {bcolors.RED}'{title}'!")
#                     break
#                 elif question.lower() == 'n':
#                     print(f"{bcolors.GREEN}Tag addition canceled!")
#                     break
#                 else:
#                     print(f"{bcolors.BOLD_RED}Wrong input. Try again!{bcolors.DEFAULT}")

#     elif choice == "6":
#         tags = input(f"{bcolors.CYAN}Enter tags/keywords to search for notes (separated by spaces):{bcolors.GREEN} ").lower().strip().split()
#         found_notes = note_file.find_notes_by_tags(tags)
#         if found_notes:
#             print(f"{bcolors.GREEN}\nFound {len(found_notes)} note(s):{bcolors.DEFAULT}\n")
#             for note in found_notes:
#                 print(f"{bcolors.YELLOW}Title:{bcolors.DEFAULT} {note.title}")
#                 print(f"{bcolors.YELLOW}Text:{bcolors.DEFAULT} {note.text}")
#                 print(f"{bcolors.YELLOW}Tags/Keywords:{bcolors.DEFAULT} {note.tags}")
#                 print()
#         else:
#             print(f"{bcolors.GREEN}No notes found with those tags/keywords!")

#     elif choice == "7":
#         sorted_notes = note_file.sort_notes_by_tags()
#         if sorted_notes:
#             print(f"{bcolors.GREEN}\nSorted {len(sorted_notes)} notes:{bcolors.DEFAULT}\n")
#             for note in sorted_notes:
#                 print(f"{bcolors.YELLOW}Title:{bcolors.DEFAULT} {note.title}")
#                 print(f"{bcolors.YELLOW}Text:{bcolors.DEFAULT} {note.text}")
#                 print(f"{bcolors.YELLOW}Tags/Keywords:{bcolors.DEFAULT} {note.tags}")
#                 print()
#         else:
#             print(f"{bcolors.GREEN}No notes found for sorting!")

#     elif choice == "8":
#         print(f"{bcolors.DEFAULT}")
#         break

#     else:
#         print(f"{bcolors.BOLD_RED}Invalid choice. Please try again!")
#     print(f"{bcolors.BOLD}-{bcolors.DEFAULT}" * 50)