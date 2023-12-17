#import pickle
from collections import UserDict
#from record_manager import MiscChecks, RecordManager
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
        help_phrase = {'part_1':{'en':". To see the list of commands for ",'uk':". Щоб подивитись список команд для "},
                       'part_2':{'en':", enter in the console '",'uk':", введіть у консоль '"},
                       'part_3':{'en':"The assistant has the next functions: ",'uk':"Помічник має такі функції: "},
                       'part_4':{'en':"If you want to go back to the main menu, enter '",'uk':"Якщо хочете повернутися у головне меню, напишіть '"},
                       'part_5':{'en':"'Please, choose the section number: ",'uk':"'Будь ласка, оберіть номер розділу: "},
                       'part_6':{'en':"A list of commands, available for ",'uk':"Список доступних команд для "},
                       'part_7':{'en':"If you want to go back to the main menu, enter '",'uk':"Якщо хочете повернутися у головне меню, напишіть '"}}
        func_str = ''
        func_str_p2 = '\n'
        for k,v in self.help_modules.items():
            func_str += self.help_modules[k]['localization']['description'][self.language] + ', '
            func_str_p2 += f"{k}{help_phrase['part_1'][self.language]}{self.help_modules[k]['localization']['name'][self.language]}{help_phrase['part_2'][self.language]}{bcolors.RED}{k}{bcolors.GREEN}'.\n"

        func_str = func_str[:len(func_str)-2]

        general_info = f"________________________\n{help_phrase['part_3'][self.language]}{func_str}. {func_str_p2}{help_phrase['part_4'][self.language]}{bcolors.RED}back{bcolors.GREEN}'."
        print(general_info)
        while True:
            answer = input(f"{bcolors.CYAN}{help_phrase['part_5'][self.language]}{bcolors.GREEN}").strip().lower()
            if answer in self.help_modules.keys():
                string = f"________________________\n{help_phrase['part_6'][self.language]}{self.help_modules[answer]['localization']['name'][self.language]}:\n"
                string += '\n'.join(f'{key} - {value[self.language]}' for key, value in self.help_modules[answer]['scripts'].items()) + f"\n{help_phrase['part_7'][self.language]}{bcolors.RED}back{bcolors.GREEN}'." + "\n________________________"
                print(string)
            elif answer == "back":
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
        self.notepad = "None" #NoteFile()
        self.contactbook = ContactBook()
        can_have_a_command = [self.contactbook]
        self.actions = self.action_filler(can_have_a_command)
        self.actions["change_language"] = {'class':'Default', 'description':{'en':"Sets the programm's language",'uk':"Встановлює мову програми."}, 'methods':{self.print_languages:{},self.set_language:{'lang':{'en':"Please,choose the language",'uk':f"Будь ласка, оберіть мову"}}}}
        
        self.actions["help"] = self.help
        self.actions["quit"] = quit
        self.actions["close"] = quit
        self.actions["exit"] = quit
        self.actions["leave"] = quit

        self.input_phrase = {'part_1':{'en':"Please, enter the command, or the key word '",'uk':"Будь ласка, введіть необхідну команду або ключове слово '"},'part_2':{'en':"' to display the list of available commands: ",'uk':"' для відображення списку доступних команд: "}}
        self.language = None
        self.languages = {'0':'en','1':'uk'}
        self.languages_local = {'0':'English','1':'Українська'}

    def default_action(self):
        print("Невідома команда. Спробуйте знову, або викликайте команду help щоб отримати допомогу щодо використання програми.")

    def set_language(self,lang):
        if lang in self.languages:
            self.language = self.languages[lang]
    
    def print_languages(self):
        string = "Список доступних мов:  /   Languages available:\n"
        string += '\n'.join(f'{key}. {value}' for key, value in self.languages_local.items()) 
        print(string)


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
                        conversion_dict = {self.contactbook:'Contact_book', self.notepad:'Note_manager'}
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
            command = ''
            if self.language != None:
                command = input(f"{bcolors.CYAN}{self.input_phrase['part_1'][self.language]}{bcolors.RED}help{bcolors.CYAN}{self.input_phrase['part_2'][self.language]}{bcolors.GREEN}").strip().lower()
            else:
                command = 'change_language'
                self.language = 'en'
            
                # TODO: додати функціонал, зазначений нижче, використовуючи нову систему виклику методів.
                # commands for contact book: 
                # help(input - action_type(sorting/contact_book'etc). If None or undefined input - show general tips, i.e. a list of modules, their general description, how to use 'help' properly), 
                # contact_edit(input - record_name. Ask which element of a record the user desires to change, give a list of options. After succssessfully editing chosen field, return to the question. To stop editing, user must write 'done' in console), 
                # contact_find(input - any_contact_related_data), 
                # contact_show_all(), 
                # remove (input - record name, but removing only by record_id. if multiple found, show all and ask to choose (by assigning temporary index to every element)), 
                # show_birthdays(input - timedelta{days}) 

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
                                    command = input(v[self.language] + ':   ')
                                    if command != '':
                                        arguments_list.append(command)
                                        break
                            key(*arguments_list)
                            command = ''


if __name__ == "__main__":
    print("Я ваш персональний помічник. Як я можу вам допомогти?")
    manager = InputManager()
    manager.main()