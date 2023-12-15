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

        modules = {'0':{'class':'self.command_data[section_name]', 'name':'сортувальника файлів'},'1':{'class':self.command_data['Contact_book'], 'name':'менеджера контактів'},'2':{'class':'self.command_data[section_name]', 'name':'менеджера записів'}}
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
        # структура збереження даних (не у файлі): {record_id:Record_class_instance}
        # Record_class_instance зберігає ім'я, Д/Р, телефони, пошти, тощо. Питання тільки в тому, чи треба для усього цього свої окремі класи, чи буде достатньо просто змінних? 
        # Я вважаю, що змінних вистачить (але якщо треба "під капотом" виконувати різні перевірки, то можна просто використати об'єкт класу і "витягнути" з нього оброблену змінну).
            # Upd: або просто записати функцію перевірки у клас RecordManager - від цього, в теорії, ніхто не постраждає.
        self.command_data = {}
        self.notepad = ContactBook()
        self.record = RecordManager()
        can_have_a_command = [self.notepad, self.record]
        self.actions = self.action_filler(can_have_a_command)
        self.actions["help"] = self.help
        self.actions["quit"] = quit
        self.actions["close"] = quit
        self.actions["exit"] = quit
        self.actions["leave"] = quit
        

    def default_action(self):
        print("Невідома команда. Спробуйте знову, або викликайте команду help щоб отримати допомогу щодо використання програми.")

    # Список actions автоматично заповнюється командами з відповідних класів (окрім загальних команд, таких як 'help', 'exit', тощо - вони записуються напряму, у _init__() класу Input_manager).
    # У кожного класу, що має певні консольні команди, є поле self.method_table - 
    # в ньому і зберігається назва консольної команди, відповідний метод і екземпляр класу, а також локалізація тексту (що програма буде казати користувачеві перед отриманням аргументів).
    # структура нового списку actions: 
    #{'console_command_name':{'class':'class_name', 'description':'description_text', 'methods':{'method1_name':[argument,argument_2],'method2_name':[argument,argument_2]}}}
    def action_filler(self, can_have_a_command):
        actions_dict = {}
        for item in can_have_a_command:
            if hasattr(item, 'method_table') and item.method_table != {}:
                for com_name,parameters in item.method_table.items():
                    actions_dict[com_name] = parameters
                    if 'description' in parameters.keys():
                        conversion_dict = {self.notepad:'Contact_book', self.record:'Record_manager'}
                        if not conversion_dict[item] in self.command_data:
                            self.command_data[conversion_dict[item]] = {}
                            
                        self.command_data[conversion_dict[item]][com_name] = parameters['description']

        return actions_dict

    def main(self):
        while True:
            command = input('Будь ласка, введіть необхідну команду або ключове слово "help" для відображення списку доступних команд: ').strip().lower()
                # TODO: додати функціонал, зазначений нижче, використовуючи нову систему виклику методів.
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


            # Тут в нас перевіряється, чи це команда класу InputManager, чи ні. Якщо ні - витягуємо необхідні дані зі словника. Ітеруємо словник методів. Якщо у метода немає аргументів, 
            # просто запускаємо його виконання. Якщо аргументи є, то ітеруємо по словнику аргументів, кожного разу видаваючи відповідну текстову фразу, що також є у словнику, і 
            # чекаючи на інпут.
            if command in self.actions.keys():
                if type(self.actions[command]) != dict:
                    selected_action = self.actions[command]
                    selected_action()
                else:
                    for key,value in self.actions[command]['methods'].items():
                        if value == {}:
                            key()
                        else:
                            arguments_list = []
                            for k,v in value.items():
                                while True:
                                    command = input(v)
                                    if command != '':
                                        arguments_list.append(command)
                                        break
                            key(*arguments_list)


if __name__ == "__main__":
    print("Я ваш персональний помічник. Як я можу вам допомогти?")
    manager = InputManager()
    manager.main()