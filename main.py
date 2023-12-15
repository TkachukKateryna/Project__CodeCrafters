from record_manager import RecordManager
from contact_book import ContactBook
import notes_manager
import sorting

class HelpMe:
    def help(self):
        # При запуску функції пропонує обрати тему (книга контактів, сортування файлів, тощо).
        # Коли користувач обере тему, видає список команд відповідного класу з референсного словника 
        # (приклад: dict = {'номер, що відповідає номеру у діалоговому вікні': {'class':'RecordManager.command_dict','name':'text'}, 'номер, що відповідає номеру у діалоговому вікні': {'class':'Sorting.command_dict', 'name':text'}})
        # Відповідно, далі скрипт створює екземпляр класу та "витягає" з нього список команд. Навіщо так? А щоб кожний писав список команд для свого модуля окремо, і редагував у тому ж файлі, одразу ж при внесенні змін або створення нових методів.

        modules = {'0':{'class':'class_name().command_dict', 'name':'сортувальника файлів'},'1':{'class':ContactBook(True).command_dict, 'name':'менеджера контактів'}}
        module_tips = ["Помічник має декілька функцій: сортування файлів у заданій директорії, менеджер контактів та записів, тут могла бути ваша реклама.","0. Щоб подивитись список команд для сортування файлів, введіть у консоль '0'.","1. Щоб подивитись список команд для менеджера контактів та записів, введіть у консоль '1'."]
        general_info = "________________________\n" + '\n'.join(f'{key}' for key in module_tips) + "\n________________________"
        print(general_info)
        while True:
            answer = input('Будь ласка, оберіть номер розділу або напишіть "leave" щоби повернутися у попереднє меню: ').strip().lower()
            if answer in modules:
                string = "________________________\nСписок доступних команд для " + modules[answer]['name'] + ":\n"
                string +='\n'.join(f'{key} - {value}' for key, value in modules[answer]['class'].items()) + "\n________________________"
                print(string)
            elif answer == "leave":
                break



class InputManager(HelpMe):
    def __init__(self):
        # Тут завантажуємо дані з файла (якщо він є. Якщо немає - викликаємо функцію, що його створить і заповнить "скелетом" даних для збереження)
        # Тут же ініціалізуємо технічні змінні для цього класу.
        # структура збереження даних: {record_id:Record_class_instance}
        # Record_class_instance зберігає ім'я, Д/Р, телефони, пошти, тощо. Питання тільки в тому, чи треба для усього цього свої окремі класи, чи буде достатньо просто змінних? 
        # Я вважаю, що змінних вистачить (але якщо треба "під капотом" виконувати різні перевірки, то можна просто використати об'єкт класуі "витягнути" з нього оброблену змінну).
        self.data = {}

    def default_action(self):
        print("Невідома команда. Спробуйте знову, або викликайте команду help щоб отримати допомогу щодо використання програми.")

    def main(self):
        while True:
            command = input('Будь ласка, введіть необхідну команду або ключове слово "help" для відображення списку доступних команд: ').strip().lower()
            # TODO: додати автоматичне заповнення списку командами з відповідних класів (окрім загальних команд, таких як 'help', 'exit', тощо). Для цього можна створити додатковий словник
            # для кожного такого класу, накшталт command_dict, тільки вже з назвою команди у якості ключа і, власне, методом та аргументами у якості значення. Це має працювати разом з генералізованим
            # діалоговим вікном, куди будуть передаватися метод та аргументи. Діалоговим вікном займусь я (Team Lead). 
            # структура нового списку actions: {'help':{'class':'class_name', 'method':'method_name', 'arguments':[arg1,arg2,arg3]}}
            # яким чином створюється діалог? Зчитується кількість методів, і доти, доки всі ці методи не отримали певні значення, менеджер буде просити ці значення надати (тут, напевно, треба буде прикрутити словник з локалізацією).
            # В кінці, створюється екземпляр зазначеного класа і в нього викликається метод з цими аргументами.
            actions = {
                "help": self.help,
                #"add": ContactAdder().add, 
                #"edit": ContactEditor().edit,
                #"remove": ContactRemover().remove,
                # commands for contact book: 
                # help(input - action_type(sorting/contact_book'etc). If None or undefined input - show general tips, i.e. a list of modules, their general description, how to use 'help' properly), 
                # add(input - record_name. Starts dialogue, which can be cancelled at any point (record will not be saved). Bot will be asking to fill the fields one-by-one. if user doesn't want to fill a certain field, he can write '-' in console. ), 
                #edit(input - record_name. Ask which element of a record the user desires to change, give a list of options. After succssessfully editing chosen field, return to the question. To stop editing, user must write 'done' in console), 
                #find(input - record_name), 
                #show_all(), 
                #remove(input - record name, but removing only by record_id. if multiple found, show all and ask to choose (by assigning temporary index to every element)), 
                #show_birthdays(input - timedelta{days}) 

                #commands for file sorter:
                #set_directory(input - default directory.)
                #sort_files(input - directory)
                #P.S: all file_format and category key-value pairs must be dislocated to the configs. 
                "quit": quit,
                "close": quit,
                "exit": quit,
                "leave": quit,
            }

            selected_action = actions.get(command, self.default_action)
            selected_action()


if __name__ == "__main__":
    print("Я ваш персональний помічник. Як я можу вам допомогти?")
    manager = InputManager()
    manager.main()