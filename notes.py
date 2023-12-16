import pickle
# Уф. Навіть не знаю, з чого почати. Скоріше за все, буду розбирати на созвоні, бо писанини тут, з моєї сторони, має бути (надто) багато. Team Lead.
class Note:
    def __init__(self, text, tags=None):
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

    def create_note(self, text, tags=None):
        note = Note(text, tags)  # Створення нової нотатки
        self.notes.append(note)  # Додавання нотатки до списку
        self.save_notes()  # Збереження нотаток у файл
        return note

    def find_note_by_text(self, text):
        found_notes = []  # Список для збереження знайдених нотаток
        for i, note in enumerate(self.notes):
            if text in note.text:
                found_notes.append((i, note))  # Запам'ятовуємо індекс та нотатку
        return found_notes

    def edit_note_text(self, note_index, new_text):
        if 0 <= note_index < len(self.notes):
            self.notes[note_index].text = new_text  # Заміна тексту нотатки
            self.save_notes()

    def delete_note(self, note_index):
        if 0 <= note_index < len(self.notes):
            question = input("Ви дійсно хочете видалити цю нотатку (y/n)?: ")
            if question == 'y':
                del self.notes[note_index]  # Видалення нотатки зі списку
                self.save_notes()
        else:
            print("Нотатки з таким індексом не існує або список нотаток пустий\n")

    def add_tags_to_note(self, note_index, tags):
        if 0 <= note_index < len(self.notes):
            self.notes[note_index].tags.extend(tags)  # Додавання тегів/ключових слів до нотатки
            self.save_notes()

    def find_notes_by_tags(self, tags):
        found_notes = []  # Список для збереження знайдених нотаток
        for note in self.notes:
            if any(tag in note.tags for tag in tags):
                found_notes.append(note)  # Додавання знайденої нотатки до списку
        return found_notes

    def sort_notes_by_tags(self):
        return sorted(self.notes, key=lambda note: note.tags)  # Сортування нотаток за тегами/ключовими словами



file_name = "notes.bin"  # Назва файлу для збереження нотаток
note_file = NoteFile(file_name)  # Створення об'єкту класу NoteFile

while True:
    print("Можливі дії:")
    print("1. Створити нотатку")
    print("2. Знайти нотатку за текстом")
    print("3. Змінити текст нотатки")
    print("4. Видалити нотатку")
    print("5. Додати теги/ключові слова до нотатки")
    print("6. Знайти нотатки за тегами/ключовими словами")
    print("7. Сортувати нотатки за тегами/ключовими словами")
    print("8. Вийти")

    print("_________________________________")
    choice = input("Виберіть дію: ")
    
    if choice == "1":
        text = input("Введіть текст нотатки: ")
        tags = input("Введіть теги/ключові слова нотатки (через пробіл): ").lower().strip().split()
        note = note_file.create_note(text, tags)
        print(f"Нотатка {note} створена")
        print("_________________________________\n")


    elif choice == "2":
        text = input("Введіть текст для пошуку: ")
        found_notes = note_file.find_note_by_text(text)
        if found_notes:
            print("Знайдені нотатки:")
            for i, note in found_notes:
                print(f"Index: {i}")
                print(f"Текст: {note.text}")
                print(f"Теги/ключові слова: {note.tags}")
                print()
            print("_________________________________\n")

        else:
            print("Нотатки з таким текстом не знайдено")
            print("_________________________________\n")

            
    elif choice == "3":
        note_index = int(input("Введіть індекс нотатки для зміни тексту: "))
        new_text = input("Введіть новий текст: ")
        note_file.edit_note_text(note_index, new_text)
        print(f"Текст нотатки з індексом '{note_index}' змінено на '{new_text}'")
        print("_________________________________\n")


    elif choice == "4":
        note_index = int(input("Введіть індекс нотатки для видалення: "))
        if 0 <= note_index < len(note_file.notes):
            selected_note = note_file.notes[note_index]
            print(f"Для видалення обрана нотатка з текстом: '{selected_note.text}'")
        else:
            print("Нотатки з таким індексом не існує або список нотаток порожній")
        note_file.delete_note(note_index)
        print("Нотатку успішно видалено")
        print("_________________________________\n")


    elif choice == "5":
        note_index = int(input("Введіть індекс нотатки для додавання тегів/ключових слів: "))
        if 0 <= note_index < len(note_file.notes):
            selected_note = note_file.notes[note_index]
            print(f"Обрана нотатка з текстом: {selected_note.text}")
        else:
            print("Нотатки з таким індексом не існує або список нотаток порожній")
        
        tags = input("Введіть теги/ключові слова для додавання (через пробіл): ").split()
        note_file.add_tags_to_note(note_index, tags)
        print("Теги/ключові слова додано до нотатки.")
        print("_________________________________\n")


    elif choice == "6":
        tags = input("Введіть теги/ключові слова для пошуку нотатки (через пробіл): ").lower().strip().split()
        found_notes = note_file.find_notes_by_tags(tags)
        if found_notes:
            print("Знайдені нотатки:")
            for note in found_notes:
                print(f"Текст: {note.text}")
                print(f"Теги/ключові слова: {note.tags}")
                print()
                print("_________________________________\n")

        else:
            print("Нотатки з такими тегами/ключовими словами не знайдено")
            print("_________________________________\n")


    elif choice == "7":
        sorted_notes = note_file.sort_notes_by_tags()
        if sorted_notes:
            print("Відсортовані нотатки:")
            for note in sorted_notes:
                print(f"Текст: {note.text}")
                print(f"Теги/ключові слова: {note.tags}")
                print()
        else:
            print("Нотатки для сортування не знайдено")
            print("_________________________________\n")


    elif choice == "8":
        break

    else:
        print("Невірний вибір. Спробуйте ще раз.")
        print("_________________________________\n")
