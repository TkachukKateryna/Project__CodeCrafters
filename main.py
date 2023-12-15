import notes
import record
import sorting

class HelpMe():
    def __init__(self,calling_class):
        print(calling_class.command_dict)
        string = "________________________\nСписок доступних команд:\n"
        string +='\n'.join(f'{key} - {value}' for key, value in calling_class.command_dict.items())
        string += "\n________________________"
        print(string)

class ContactManager:
    def __init__(self):
        #Тут завантажуємо дані з файла (якщо він є. Якщо немає - викликаємо функцію, що його створить і заповнить "скелетом" даних для збереження)
        #Тут же ініціалізуємо технічні змінні для цього класу.
        self.contacts = {}
        self.command_dict = {'add':'Add new contact', 'del':'delete existing contact'}

    def help(self):
        # Поки що видає лише команди цього класу. Як варіант, при запуску функції пропонує обрати тему (книга контактів, сортування файлів, тощо).
        # Коли користувач обере тему, видає список команд відповідного класу з референсного словника (приклад: dict = {'Створення запису': 'Record', 'Сортування файлів': 'Sorting'})
        # Відповідно, далі скрипт створює екземпляр класу та "витягає" з нього список команд. Навіщо так? А щоб кожний писав список команд для свого модуля окремо, і редагував у тому ж файлі, одразу ж при внесенні змін.
        action = HelpMe(self)

    def default_action(self):
        print("Невідома команда. Спробуйте знову, або викликайте команду help щоб отримати допомогу щодо використання програми.")

    def main(self):
        while True:
            command = input('Будь ласка, введіть необхідну команду або ключове слово "help" для відображення списку доступних команд: ').strip().lower()

            actions = {
                "help": self.help,
                "add": ContactAdder().add,
                "edit": ContactEditor().edit,
                "remove": ContactRemover().remove,
                # ...
                "quit": quit,
            }

            selected_action = actions.get(command, self.default_action)
            selected_action()


if __name__ == "__main__":
    print("Я ваш персональний помічник. Як я можу вам допомогти?")
    manager = ContactManager()
    manager.main()