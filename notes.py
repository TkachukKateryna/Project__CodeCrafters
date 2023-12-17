import pickle
# Уф. Навіть не знаю, з чого почати. Скоріше за все, буду розбирати на созвоні, бо писанини тут, з моєї сторони, має бути (надто) багато. Team Lead.
class Note:
    def __init__(self, title, text, tags=None):
        self.title = title # Заголовок нотатки
        self.text = text  # Текст нашої нотатки
        self.tags = tags or []  # Теги нашої нотатки (необов'язково)

    def __str__(self):
        return f"'{self.text}'" # Використовуємо для повернення текстових представлень об'єктів

class NoteFile:
    def __init__(self, file_name):
        self.file_name = file_name  # Ім'я файлу для збереження нотаток
        self.notes = self.load_notes()  # Завантаження нотаток з файлу

    def load_notes(self):
        try:
            with open(self.file_name, 'rb') as file:
                notes = pickle.load(file)  # Завантаження нотаток з файлу за допомогою pickle
        except FileNotFoundError:
            notes = []  # Якщо файл не знайдено, створюємо порожній список
        return notes

    def save_notes(self):
        with open(self.file_name, 'wb') as file:
            pickle.dump(self.notes, file)  # Збереження нотаток у файл за допомогою pickle

    def create_note(self, title, text, tags=None):
        note = Note(title, text, tags)  # Створення нової нотатки
        self.notes.append(note)  # Додавання нотатки до списку
        self.save_notes()  # Збереження нотаток у файл
        return note

    def find_note_by_text(self, text):
        found_notes = []  # Список для збереження знайдених нотаток
        for note in self.notes:
            if text.lower() in note.text.lower(): # Переводимо текст пошуку і нотатки до нижнього регістру
                found_notes.append(note)  # Запам'ятовуємо нотатку
        return found_notes

    def edit_note_text(self, note_title, new_text):
        for note in self.notes:
            if note.title == note_title:  # Знайдена нотатка за заголовком
                note.text = new_text  # Заміна тексту нотатки
                self.save_notes()
                return

    def delete_note(self, note_title):
        for note in self.notes:
            if note.title == note_title:  
                self.notes.remove(note)  # Видалення нотатки зі списку
                self.save_notes()
                return

    def add_tags_to_note(self, note_title, tags):
        for note in self.notes:
            if note.title == note_title:
                note.tags.extend(tags)  # Додавання тегів/ключових слів до нотатки
                self.save_notes()
                return
 
    def find_notes_by_tags(self, tags):
        found_notes = []  # Список для збереження знайдених нотаток
        if not tags:  # Якщо список тегів порожній
            found_notes = [note for note in self.notes if not note.tags]  # Вибираємо нотатки з пустими полями тегів
        else:
            for note in self.notes:
                if any(tag in note.tags for tag in tags):
                    found_notes.append(note)  # Додавання знайденої нотатки до списку
        return found_notes


    def sort_notes_by_tags(self):
        return sorted(self.notes, key=lambda note: note.tags)  # Сортування нотаток за тегами/ключовими словами
    
    def find_notes_by_title(self, title):
        if any(note.title.lower() == title.lower() for note in note_file.notes): # Перевірка наявності нотатки з введеним заголовком
            for note in note_file.notes:
                if note.title.lower() == title.lower():
                    print(f"Текст обраної нотатки: {note.text}")
                    return note
            return None


file_name = "notes.bin"  # Назва файлу для збереження нотаток
note_file = NoteFile(file_name)  # Створення об'єкту класу NoteFile

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
            question = input("Is this the note you're looking for? (y/n): ")
            if question.lower() == 'y':
                new_text = input("Enter the new text: ")
                note_file.edit_note_text(found_note.title, new_text)
                print(f"\033[32mNote text with title '{title}' changed to '{new_text}'\033[0m")
            else:
                print("Note editing canceled!")
        else:
            print(f"\033[1m\033[91mNo notes found with title '{title}'!\033[0m")

    elif choice == "4":
        title = input("Enter the note title to delete: ")
        found_note = note_file.find_notes_by_title(title)
        if found_note:
            question = input("Is this the note you're looking for? (y/n): ")
            if question.lower() == 'y':
                note_file.delete_note(found_note.title)
                print(f"\033[32mNote with title '{title}' deleted successfully\033[0m")
            else:
                print("Deletion canceled!")
        else:
            print(f"\033[1m\033[91mNo notes found with title '{title}' or the list of notes is empty!\033[0m")

    elif choice == "5":
        title = input("Enter the note title to add tags/keywords to: ")  
        found_note = note_file.find_notes_by_title(title)
        if found_note:
            question = input("Is this the note you're looking for? (y/n): ")
            if question.lower() == 'y':
                tags = input("Enter tags/keywords to add (separated by spaces): ").split()
                note_file.add_tags_to_note(found_note.title, tags)
                print(f"\033[32mTags/keywords added to the note with title '{title}'!\033[0m")
            else:
                print("Tag addition canceled!")
        else:
            print(f"\033[1m\033[91mNo notes found with title '{title}'!\033[0m")

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
