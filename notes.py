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


class Note:
    def __init__(self, title, text, tags=None):
        self.title = title # Заголовок нотатки
        self.text = text # Текст нашої нотатки
        self.tags = tags or [] # Теги нашої нотатки (необов'язково)


    def __str__(self):
        return f"'{self.text}'" # Використовуємо для повернення текстових представлень об'єктів


class NoteFile:
    def __init__(self, file_name):
        self.file_name = file_name # Ім'я файлу для збереження нотаток
        self.notes = self.load_notes() # Завантаження нотаток з файлу

    def load_notes(self):
        try:
            with open(self.file_name, 'rb') as file:
                notes = pickle.load(file) # Завантаження нотаток з файлу за допомогою pickle
        except FileNotFoundError:
            notes = [] # Якщо файл не знайдено, створюємо порожній список
        return notes

    def save_notes(self):
        with open(self.file_name, 'wb') as file:
            pickle.dump(self.notes, file) # Збереження нотаток у файл за допомогою pickle

    def create_note(self, title, text, tags=None):
        note = Note(title, text, tags) # Створення нової нотатки
        self.notes.append(note) # Додавання нотатки до списку
        self.save_notes() # Збереження нотаток у файл
        return note

    def find_note_by_text(self, text):
        found_notes = []
        for note in self.notes:
            if text.lower() in note.text.lower(): # Переводимо текст пошуку і нотатки до нижнього регістру
                found_notes.append(note)
        return found_notes

    def edit_note_text(self, note_title, new_text):
        note_title.text = new_text # Заміна тексту нотатки
        self.save_notes()

    def delete_note(self, note_title):  
        self.notes.remove(note_title) # Видалення нотатки зі списку
        self.save_notes()

    def add_tags_to_note(self, note_title, tags):
        note_title.tags.extend(tags) # Додавання тегів/ключових слів до знайденої нотатки
        self.save_notes()
 
    def find_notes_by_tags(self, tags):
        found_notes = [] # Список для збереження знайдених нотаток
        if not tags: # Якщо список тегів порожній
            found_notes = [note for note in self.notes if not note.tags] # Вибираємо нотатки з пустими полями тегів
        else:
            for note in self.notes:
                if any(tag in note.tags for tag in tags):
                    found_notes.append(note)
        return found_notes

    def sort_notes_by_tags(self):
        return sorted(self.notes, key=lambda note: note.tags) # Сортування нотаток за тегами/ключовими словами
    
    def find_notes_by_title(self, title):
        found_notes = [] 
        for note in self.notes:
            if note.title.lower() == title.lower():
                found_notes.append(note)

        if found_notes:
            print(f"{bcolors.GREEN}\nFound {len(found_notes)} note(s) with title '{title}':{bcolors.DEFAULT}\n")
            for i, note in enumerate(found_notes):
                print(f"{bcolors.RED}{i + 1}.{bcolors.DEFAULT} {note.title}") # Для зручності користувача нумеруємо нотатки з 1, а не з 0, як індекси.
                print(f"{bcolors.GREEN}Selected note text:{bcolors.DEFAULT} {note.text}")
                print()
            selected_note = None # В цю змінну буде збережена обрана користувачем нотатка
            while selected_note is None:
                if len(found_notes) > 1: # Виконуємо блок, якщо вказаний заголовок є більше ніж у одної нотатки
                    choice = input(f"{bcolors.CYAN}Enter the number of the note you want to select:{bcolors.GREEN} ")
                    try:
                        index = int(choice) - 1 # Переводимо ввід користувача в int і зменшуємо значення на 1, щоб отримати індекс в found_notes
                        selected_note = found_notes[index] # Якщо в found_notes є елемент з цим індексом, то обрана нотатка буде присвоєна змінній
                    except (ValueError, IndexError):
                        print(f"{bcolors.BOLD_RED}Invalid choice. Please try again!{bcolors.DEFAULT}")
                else: 
                    selected_note = found_notes[0]
            return selected_note
        else:
            print(f"{bcolors.GREEN}No notes found with title {bcolors.RED}'{title}'!")
            return


file_name = "notes.bin" # Назва файлу для збереження нотаток
note_file = NoteFile(file_name) # Створення об'єкту класу NoteFile

while True:
    print(f"\n{bcolors.CYAN}Available operations:\n")
    print(f"{bcolors.RED}1. {bcolors.GREEN}Create a new note")
    print(f"{bcolors.RED}2. {bcolors.GREEN}Find a note by text")
    print(f"{bcolors.RED}3. {bcolors.GREEN}Edit note text")
    print(f"{bcolors.RED}4. {bcolors.GREEN}Delete a note")
    print(f"{bcolors.RED}5. {bcolors.GREEN}Add tags/keywords to a note")
    print(f"{bcolors.RED}6. {bcolors.GREEN}Find notes by tags/keywords")
    print(f"{bcolors.RED}7. {bcolors.GREEN}Sort notes by tags/keywords")
    print(f"{bcolors.RED}8. {bcolors.GREEN}Exit")

    print(f"{bcolors.BOLD}-{bcolors.DEFAULT}" * 50)

    choice = input(f"{bcolors.CYAN}Enter the number of the desired operation:{bcolors.GREEN} ")
    
    if choice == "1":
        title = input(f"{bcolors.CYAN}Enter the note title:{bcolors.GREEN} ").strip()
        if title:
            text = input(f"{bcolors.CYAN}Enter the note text:{bcolors.GREEN} ").strip()
            if text:
                tags = input(f"{bcolors.CYAN}Enter tags/keywords for the note separated by spaces (optional):{bcolors.GREEN} ").lower().strip().split()
                note = note_file.create_note(title, text, tags)
                print(f"{bcolors.GREEN}Note with title {bcolors.RED}'{title}'{bcolors.GREEN} created successfully!")
            else:
                print(f"{bcolors.BOLD_RED}Text cannot be empty. Please try again!")
        else:
            print(f"{bcolors.BOLD_RED}Title cannot be empty. Please try again!")

    elif choice == "2":
        text = input(f"{bcolors.CYAN}Enter the text to search (if space - all notes will be displayed):{bcolors.GREEN} ")
        found_notes = note_file.find_note_by_text(text)
        if found_notes:
            print(f"{bcolors.GREEN}\nFound {len(found_notes)} note(s):{bcolors.DEFAULT}\n")
            for note in found_notes:
                print(f"{bcolors.YELLOW}Title:{bcolors.DEFAULT} {note.title}")
                print(f"{bcolors.YELLOW}Text:{bcolors.DEFAULT} {note.text}")
                print(f"{bcolors.YELLOW}Tags/Keywords:{bcolors.DEFAULT} {note.tags}")
                print()
        else:
            print(f"{bcolors.GREEN}No notes found with that text!")
      
    elif choice == "3":
        title = input(f"{bcolors.CYAN}Enter the note title to edit:{bcolors.GREEN} ")
        found_note = note_file.find_notes_by_title(title)
        if found_note:
            while True:
                question = input(f"{bcolors.CYAN}Are you sure you want to edit this note? (y/n):{bcolors.GREEN} ")
                if question.lower() == 'y':
                    new_text = input(f"{bcolors.CYAN}Enter the new text:{bcolors.GREEN} ")
                    note_file.edit_note_text(found_note, new_text)
                    print(f"{bcolors.GREEN}Note text with title {bcolors.RED}'{title}'{bcolors.GREEN} changed to {bcolors.RED}'{new_text}'")
                    break
                elif question.lower() == 'n':
                    print(f"{bcolors.GREEN}Note editing canceled!")
                    break
                else:
                    print(f"{bcolors.BOLD_RED}Wrong input. Try again!{bcolors.DEFAULT}")

    elif choice == "4":
        title = input(f"{bcolors.CYAN}Enter the note title to delete:{bcolors.GREEN} ")
        found_note = note_file.find_notes_by_title(title)
        if found_note:
            while True:
                question = input(f"{bcolors.CYAN}Are you sure you want to delete this note? (y/n):{bcolors.GREEN} ")
                if question.lower() == 'y':
                    note_file.delete_note(found_note)
                    print(f"{bcolors.GREEN}Note with title {bcolors.RED}'{title}'{bcolors.GREEN} deleted successfully")
                    break
                elif question.lower() == 'n':
                    print(f"{bcolors.GREEN}Deletion canceled!")
                    break
                else:
                    print(f"{bcolors.BOLD_RED}Wrong input. Try again!{bcolors.DEFAULT}")

    elif choice == "5":
        title = input(f"{bcolors.CYAN}Enter the note title to add tags/keywords to:{bcolors.GREEN} ") 
        found_note = note_file.find_notes_by_title(title)
        if found_note:
            while True:
                question = input(f"{bcolors.CYAN}Are you sure you want to add tags/keywords to this note? (y/n):{bcolors.GREEN} ")
                if question.lower() == 'y':
                    tags = input(f"{bcolors.CYAN}Enter tags/keywords to add (separated by spaces):{bcolors.GREEN} ").split()
                    note_file.add_tags_to_note(found_note, tags)
                    print(f"{bcolors.GREEN}Tags/keywords added to the note with title {bcolors.RED}'{title}'!")
                    break
                elif question.lower() == 'n':
                    print(f"{bcolors.GREEN}Tag addition canceled!")
                    break
                else:
                    print(f"{bcolors.BOLD_RED}Wrong input. Try again!{bcolors.DEFAULT}")

    elif choice == "6":
        tags = input(f"{bcolors.CYAN}Enter tags/keywords to search for notes (separated by spaces):{bcolors.GREEN} ").lower().strip().split()
        found_notes = note_file.find_notes_by_tags(tags)
        if found_notes:
            print(f"{bcolors.GREEN}\nFound {len(found_notes)} note(s):{bcolors.DEFAULT}\n")
            for note in found_notes:
                print(f"{bcolors.YELLOW}Title:{bcolors.DEFAULT} {note.title}")
                print(f"{bcolors.YELLOW}Text:{bcolors.DEFAULT} {note.text}")
                print(f"{bcolors.YELLOW}Tags/Keywords:{bcolors.DEFAULT} {note.tags}")
                print()
        else:
            print(f"{bcolors.GREEN}No notes found with those tags/keywords!")

    elif choice == "7":
        sorted_notes = note_file.sort_notes_by_tags()
        if sorted_notes:
            print(f"{bcolors.GREEN}\nSorted {len(sorted_notes)} notes:{bcolors.DEFAULT}\n")
            for note in sorted_notes:
                print(f"{bcolors.YELLOW}Title:{bcolors.DEFAULT} {note.title}")
                print(f"{bcolors.YELLOW}Text:{bcolors.DEFAULT} {note.text}")
                print(f"{bcolors.YELLOW}Tags/Keywords:{bcolors.DEFAULT} {note.tags}")
                print()
        else:
            print(f"{bcolors.GREEN}No notes found for sorting!")

    elif choice == "8":
        print(f"{bcolors.DEFAULT}")
        break

    else:
        print(f"{bcolors.BOLD_RED}Invalid choice. Please try again!")
    print(f"{bcolors.BOLD}-{bcolors.DEFAULT}" * 50)