import pickle

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
            print(f"\n\033[32mFound {len(found_notes)} note(s) with title '{title}':\033[0m\n")
            for i, note in enumerate(found_notes):
                print(f"{i + 1}. {note.title}") # Для зручності користувача нумеруємо нотатки з 1, а не з 0, як індекси.
                print(f"Selected note text: {note.text}")
                print()
            selected_note = None # В цю змінну буде збережена обрана користувачем нотатка
            while selected_note is None:
                if len(found_notes) > 1: # Виконуємо блок, якщо вказаний заголовок є більше ніж у одної нотатки
                    choice = input("Enter the number of the note you want to select: ")
                    try:
                        index = int(choice) - 1 # Переводимо ввід користувача в int і зменшуємо значення на 1, щоб отримати індекс в found_notes
                        selected_note = found_notes[index] # Якщо в found_notes є елемент з цим індексом, то обрана нотатка буде присвоєна змінній
                    except (ValueError, IndexError):
                        print("\033[1m\033[91mInvalid choice. Please try again.\033[0m")
                else: 
                    selected_note = found_notes[0]
            return selected_note
        else:
            print(f"\033[1m\033[91mNo notes found with title '{title}'!\033[0m")
            return


file_name = "notes.bin" # Назва файлу для збереження нотаток
note_file = NoteFile(file_name) # Створення об'єкту класу NoteFile

while True:
    print("\nAvailable operations:\n")
    print("1. Create a new note")
    print("2. Find a note by text")
    print("3. Edit note text")
    print("4. Delete a note")
    print("5. Add tags/keywords to a note")
    print("6. Find notes by tags/keywords")
    print("7. Sort notes by tags/keywords")
    print("8. Exit")

    print("-" * 50)
    choice = input("Enter the number of the desired operation: ")
    
    if choice == "1":
        title = input("Enter the note title: ").strip()
        if title:
            text = input("Enter the note text: ").strip()
            if text:
                tags = input("Enter tags/keywords for the note separated by spaces (optional): ").lower().strip().split()
                note = note_file.create_note(title, text, tags)
                print(f"\033[32mNote with title '{title}' created successfully!\033[0m")
            else:
                print("\033[1m\033[91mText cannot be empty. Please try again!\033[0m")
        else:
            print("\033[1m\033[91mTitle cannot be empty. Please try again!\033[0m")

    elif choice == "2":
        text = input("Enter the text to search (if space - all notes will be displayed): ")
        found_notes = note_file.find_note_by_text(text)
        if found_notes:
            print(f"\n\033[32mFound notes: {len(found_notes)}:\033[0m\n")
            for note in found_notes:
                print(f"Title: {note.title}")
                print(f"Text: {note.text}")
                print(f"Tags/Keywords: {note.tags}")
                print()
        else:
            print("\033[1m\033[91mNo notes found with that text!\033[0m")
      
    elif choice == "3":
        title = input("Enter the note title to edit: ")
        found_note = note_file.find_notes_by_title(title)
        if found_note:
            question = input("Are you sure you want to edit this note? (y/n): ")
            if question.lower() == 'y':
                new_text = input("Enter the new text: ")
                note_file.edit_note_text(found_note, new_text)
                print(f"\033[32mNote text with title '{title}' changed to '{new_text}'\033[0m")
            else:
                print("Note editing canceled!")

    elif choice == "4":
        title = input("Enter the note title to delete: ")
        found_note = note_file.find_notes_by_title(title)
        if found_note:
            question = input("Are you sure you want to delete this note? (y/n): ")
            if question.lower() == 'y':
                note_file.delete_note(found_note)
                print(f"\033[32mNote with title '{title}' deleted successfully\033[0m")
            else:
                print("Deletion canceled!")

    elif choice == "5":
        title = input("Enter the note title to add tags/keywords to: ") 
        found_note = note_file.find_notes_by_title(title)
        if found_note:
            question = input("Are you sure you want to add tags/keywords to this note? (y/n): ")
            if question.lower() == 'y':
                tags = input("Enter tags/keywords to add (separated by spaces): ").split()
                note_file.add_tags_to_note(found_note, tags)
                print(f"\033[32mTags/keywords added to the note with title '{title}'!\033[0m")
            else:
                print("Tag addition canceled!")

    elif choice == "6":
        tags = input("Enter tags/keywords to search for notes (separated by spaces): ").lower().strip().split()
        found_notes = note_file.find_notes_by_tags(tags)
        if found_notes:
            print(f"\n\033[32mFound notes: {len(found_notes)}:\033[0m\n")
            for note in found_notes:
                print(f"Title: {note.title}")
                print(f"Text: {note.text}")
                print(f"Tags/Keywords: {note.tags}")
                print()
        else:
            print("\033[1m\033[91mNo notes found with those tags/keywords!\033[0m")

    elif choice == "7":
        sorted_notes = note_file.sort_notes_by_tags()
        if sorted_notes:
            print(f"\n\033[32mSorted notes {len(sorted_notes)}:\033[0m\n")
            for note in sorted_notes:
                print(f"Title: {note.title}")
                print(f"Text: {note.text}")
                print(f"Tags/Keywords: {note.tags}")
                print()
        else:
            print("\033[1m\033[91mNo notes found for sorting!\033[0m")

    elif choice == "8":
        break

    else:
        print("\033[1m\033[91mInvalid choice. Please try again!\033[0m")
    print("-" * 50)