from record_manager import RecordManager
from contact_book import ContactBook
import notes_manager
import sorting

class bcolors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    DEFAULT = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class HelpMe:
    def help(self):
        # При запуску функції пропонує обрати тему (книга контактів, сортування файлів, тощо). Коли користувач обере тему, видає список команд відповідного класу з self.help_modules
        # Навіщо так? А щоб кожний писав список команд для свого модуля окремо, і редагував у тому ж файлі, одразу ж при внесенні змін або створення нових методів.
        # Тільки не забуваємо перевіряти, щоб назви КОНСОЛЬНИХ команд з вашого модулю не співпадали з назвами з інших модулів.
        # Структура self.help_modules: self.help_modules = {str(index):{'name':'module_name','scripts':{'script1':'descr_text','script2':'descr_text'},'localization':{'name':'text', 'description':'text'}}}
        func_str = ''
        func_str_p2 = '\n'
        for k,v in self.help_modules.items():
            func_str += self.help_modules[k]['localization']['description'] + ', '
            func_str_p2 += f"{k}. Щоб подивитись список команд для {self.help_modules[k]['localization']['name']}, введіть у консоль '{bcolors.RED}{k}{bcolors.GREEN}'.\n"

        func_str = func_str[:len(func_str)-2]

        general_info = f"________________________\nПомічник має такі функції: {func_str}. {func_str_p2}Якщо хочете повернутися у попереднє меню, напишіть '{bcolors.RED}leave{bcolors.GREEN}'."
        print(general_info)
        while True:
            answer = input(bcolors.CYAN + 'Будь ласка, оберіть номер розділу: ' + bcolors.GREEN).strip().lower()
            if answer in self.help_modules.keys():
                string = f"________________________\nСписок доступних команд для {self.help_modules[answer]['localization']['name']}:\n"
                string += '\n'.join(f'{key} - {value}' for key, value in self.help_modules[answer]['scripts'].items()) + f"\nЯкщо хочете повернутися у попереднє меню, напишіть '{bcolors.RED}leave{bcolors.GREEN}'." + "\n________________________"
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
        self.help_modules = {}
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
        filler_ids = -1
        for item in can_have_a_command:
            if hasattr(item, 'method_table') and item.method_table != {}:
                filler_ids += 1
                for com_name,parameters in item.method_table.items():
                    actions_dict[com_name] = parameters
                    if 'description' in parameters.keys():
                        conversion_dict = {self.notepad:'Contact_book', self.record:'Record_manager'}
                        if not str(filler_ids) in self.help_modules:
                            self.help_modules[str(filler_ids)] = {'name':conversion_dict[item],'scripts':{},'localization':{}}
                        
                        if com_name != '__localization_insert':
                            self.help_modules[str(filler_ids)]['scripts'][com_name] = parameters['description']
                        else:
                            self.help_modules[str(filler_ids)]['localization']['description'] = parameters['description']
                            self.help_modules[str(filler_ids)]['localization']['name'] = parameters['name']

        return actions_dict

    def main(self):
        while True:
            command = input(f'{bcolors.CYAN}Будь ласка, введіть необхідну команду або ключове слово "{bcolors.RED}help{bcolors.CYAN}" для відображення списку доступних команд: {bcolors.GREEN}').strip().lower()
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