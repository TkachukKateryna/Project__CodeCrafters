from CodeCrafters_assistant.contact_book import ContactBook
from CodeCrafters_assistant.notes import NoteFile
from CodeCrafters_assistant.sorting import FileSorter
from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.styles import Style
import xml.etree.ElementTree as ET

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
    


class InputManager():
    def __init__(self):
        # Тут завантажуємо дані з файла (якщо він є. Якщо немає - викликаємо функцію, що його створить і заповнить "скелетом" даних для збереження)
        # Тут же ініціалізуємо технічні змінні для цього класу.
        self.languages = {0:"en",1:"ua",2:"ru"}
        self.languages_local = {0:'English',1:'Українська',2:'Русский'}
        import locale
        system_language = locale.getdefaultlocale()[0].lower().split('_')
        tree = None
        if system_language[0] in self.languages.values():
            tree = ET.parse(f"localization_{system_language[0]}.xml")
        else:
            tree = ET.parse("localization_en.xml")
        self.localization = tree.getroot()
        self.module_chosen = None
        self.command = 'change_language'
        self.modules = []
        self.contactbook = ContactBook(self)
        self.notepad = NoteFile(self)
        self.sorter = FileSorter(self)
        
        self.reinit(mode='first')
        
        self.current_module_commands = []
        self.menu_delay = None

    def reinit(self, mode=None):
        if mode != 'first':
            self.contactbook.reinit()
            self.notepad.reinit()
            self.sorter.reinit()
        self.actions = {}
        self.technical_actions = {}
        self.technical_actions['default'] = {}
        self.actions = self.action_filler(self.modules)
        tmp = None
        if mode != 'first' and self.module_chosen != None:
            tmp = self.module_chosen
        self.confirm = ['y','yes']
        self.confirm.append(self.translate_string('confirm').lower())
        self.confirm.append(self.translate_string('confirm_long').lower())
        self.deny = ['n','no']
        self.deny.append(self.translate_string('deny').lower())
        self.deny.append(self.translate_string('deny_long').lower())
        self.actions['default'] = {}
        self.actions['default']["change_language"] = { 
                                           'description':"change_language_desc", 
                                            'methods':{self.print_languages:{},
                                                       self.set_language:{
                                                           'lang':self.translate_string('select_language','cyan')}}}
        self.actions['default']["change_module"] = {
                                           'description':"change_module_desc", 
                                            'methods':{self.print_modules:{},
                                                       self.set_module:{
                                                           'module_id':self.translate_string('select_module','cyan')}}}
        self.actions['default']["leave"] = {
                                           'description':"exit", 
                                            'methods':{self.say_goodbye:{},
                                                       quit:{}}}

        if mode != 'first':
            self.module_chosen = tmp
        else:
            self.module_chosen = None


    def translate_string(self,string:str,st_color=None,end_color=None, mode=None):
        string = str(string).strip().lower()
        local = self.localization[0]
        local_def = self.localization[0]
        if type(mode) == int and mode < len(self.modules):
            local = self.localization[int(mode) + 1]
        elif type(self.module_chosen) == int and self.module_chosen < len(self.modules):
            local = self.localization[self.module_chosen + 1]
        colors = {'header':'\033[95m',
                  'blue':'\033[94m',
                  'cyan':'\033[96m',
                  'green':'\033[92m',
                  'yellow':'\033[93m',
                  'red':'\033[91m',
                  'default':'\033[0m',
                  'bold':'\033[1m',
                  'underline':'\033[4m'}
        return_string = ""
        if st_color and st_color in colors.keys():
            return_string += colors[st_color]
        if local.find(string) != None and local.find(string).attrib['text'] != None:
            return_string += local.find(string).attrib['text']
        elif local_def.find(string) != None and local_def.find(string).attrib['text'] != None:
            return_string += local_def.find(string).attrib['text']
        else:
            if local_def.find("local_not_found_1") and local_def.find("local_not_found_2"):
                print(f"{colors['yellow']}{local.find('local_not_found_1').attrib['text']} {colors['red']}{string}{colors['yellow']} {local.find('local_not_found_2').attrib['text']}{colors['green']}")
            else:
                print(f"{colors['yellow']}Item {colors['red']}{string}{colors['yellow']} not found in the XML-file!{colors['green']}")
            return_string += string
        if end_color and end_color in colors.keys():
            return_string += colors[end_color]
        return return_string

    def set_language(self,lang):
        try:
            lang = self.input_to_id(lang)
            if lang in self.languages.keys():
                tree = ET.parse(f"localization_{self.languages[lang]}.xml")
                self.localization = tree.getroot()
                self.reinit()
            else:
                return self.translate_string('wrong_id_error','yellow')
            
            print(self.translate_string('assistant_welcome','green'))
        except ValueError:
            return self.translate_string('wrong_id_error','yellow')

    
    def print_languages(self):
        string = self.translate_string('change_language_list','green')
        string += '\n' + '\n'.join(f'{bcolors.RED}{key}{bcolors.GREEN}. {value}' for key, value in self.languages_local.items()) + '\n'
        print(string)
    
    def print_modules(self):
        self.module_chosen = None
        string = self.translate_string('print_module_p0','green') + ':\n'
        string += '\n'.join(f"{bcolors.RED}{self.modules.index(key)}{bcolors.GREEN}. {self.translate_string('print_module_p1')} {self.translate_string(key.method_table['__localization']['name'],'red','green',mode=self.modules.index(key))} {self.translate_string('print_module_p2')} '{bcolors.RED}{self.modules.index(key)}{bcolors.GREEN}' {self.translate_string('print_module_p3')}" for key in self.modules) + '\n'
        print(string)

    def set_module(self,module_id):
        try:
            module_id = self.input_to_id(module_id)
            if module_id < len(self.modules):
                self.module_chosen = module_id
                self.actions['default']["back"] = {
                                            'description':"change_module_desc", 
                                                'methods':{self.reset_module:{}}}
                self.current_module_commands = []
                for script in self.actions[self.module_chosen].keys():
                    self.current_module_commands.append(script) 
                
                self.current_module_commands.append("cancel")
                for script in self.actions['default'].keys():
                    self.current_module_commands.append(script) 

                self.command_completer = WordCompleter(self.current_module_commands)
                self.command = ''
            else:
                print(self.translate_string('wrong_module_number','yellow','green'))
        except ValueError:
            print(self.translate_string('wrong_module_number','yellow','green'))


    def reset_module(self):
            self.current_module_commands = []
            self.module_chosen = None
            del self.actions['default']["back"] 
    
    def input_to_id(self, text):
        map = {' ':'','\n':'','\t':'','\r':''}
        new_line = text.translate(map)
        try:
            if int(new_line) >= 0:
                return int(new_line)
            else:
                return self.translate_string('negative_id_error','yellow','green')
        except ValueError:
            return self.translate_string('wrong_id_error','yellow','green')

    # Список actions автоматично заповнюється командами з відповідних класів (окрім загальних команд, таких як 'help', 'exit', тощо - вони записуються напряму, у _init__() класу Input_manager).
    # У кожного класу, що має певні консольні команди, є поле self.method_table - 
    # в ньому і зберігається назва консольної команди, відповідний метод і екземпляр класу, а також локалізація тексту (що програма буде казати користувачеві перед отриманням аргументів).
    def action_filler(self, modules):
        actions_dict = {}
        filler_ids = -1
        for item in modules:
            if hasattr(item, 'method_table') and item.method_table != {}:
                filler_ids += 1
                actions_dict[modules.index(item)] = {}
                self.technical_actions[modules.index(item)] = {}
                for com_name,parameters in item.method_table.items():
                    if com_name != '__localization':
                        if 'technical' in parameters.keys():
                            self.technical_actions[modules.index(item)][com_name] = parameters
                        else:
                            actions_dict[modules.index(item)][com_name] = parameters

        return actions_dict
    
    def main(self):
        while True:
            if self.menu_delay:
                while True: 
                    self.command = input(f"{self.translate_string('enter_back_p0','cyan')} {self.translate_string('enter_back_p1','red','cyan')} {self.translate_string('enter_back_p2')}:   {bcolors.RED}")
                    if self.command.lower() in self.confirm:
                        self.menu_delay = None
                        break
            if self.command == '':
                if self.module_chosen != None:
                    string = f"{self.translate_string('menu_entered_p0','green')} {self.translate_string(self.modules[self.module_chosen].method_table['__localization']['name'], 'red', 'green')}{self.translate_string('menu_entered_p1')}\n"
                    string += "\n".join(f"{'  '}{bcolors.RED}{key}{bcolors.GREEN} - {self.translate_string(value['description'])}" for key, value in self.actions[self.module_chosen].items()) + f"\n{'  '}{bcolors.RED}back{bcolors.GREEN} - {self.translate_string('return_to_main')}. \n{'  '}{bcolors.RED}leave{bcolors.GREEN} - {self.translate_string('exit')}. \n{'  '}{bcolors.RED}cancel{bcolors.GREEN} - {self.translate_string('cancel')}.\n{'_' * 80}"
                    print(string)
        
                    style = Style.from_dict({
                        '': 'fg:ansigreen',

                        'part_1': 'fg:ansicyan',
                    })

                    message = [
                        ('class:part_1', self.translate_string('enter_the_command')),
                    ]
                    self.command = prompt(message, completer=self.command_completer, style=style).strip().lower()
                elif self.module_chosen == None:
                    self.command = 'change_module'
            if self.command != '':
                result = self.start_script(self.command)
                if result == 'leave':
                    break
    # Тут в нас перевіряється, чи це команда класу InputManager, чи ні. Якщо ні - витягуємо необхідні дані зі словника. Ітеруємо словник методів. Якщо у метода немає аргументів, 
    # просто запускаємо його виконання. Якщо аргументи є, то ітеруємо по словнику аргументів, кожного разу видаваючи відповідну текстову фразу, що також є у словнику, і 
    # чекаючи на інпут.
    def start_script(self,command,mode=None):
        scripts = None
        if mode != 'technical':
            scripts = self.actions
        else:
            scripts = self.technical_actions
        category = None
        command_exceptions = ['change_language', 'change_module', 'back', 'leave', 'cancel']
        if type(self.module_chosen) == int and not command in command_exceptions and (command in scripts['default'].keys() or command in scripts[self.module_chosen].keys()):
            self.menu_delay = True
        if type(self.module_chosen) == int:
            if (command in scripts[self.module_chosen].keys()):
                category = self.module_chosen
        if (command in scripts['default'].keys()):
            category = 'default'
        if category != None:
            if type(scripts[category][command]) != dict:
                selected_action = scripts[category][command]
                selected_action()
            else:
                for key,value in scripts[category][command]['methods'].items():
                    if value == {}:
                        result = key()
                        if result == 'abort':
                            return
                    else:
                        arguments_list = []
                        result = ' '
                        while type(result) == str:
                            silent_restart = None
                            for k,v in value.items():
                                while True:
                                    argument = input(f"{bcolors.CYAN}{v}" + f':   {bcolors.RED}')
                                    if argument.strip().lower() == 'leave':
                                        self.say_goodbye()
                                        return 'leave'
                                    if argument.strip().lower() == 'cancel':
                                        silent_restart = True
                                        return
                                    if argument != '':
                                        arguments_list.append(argument)
                                        break
                            if not silent_restart:
                                result = key(*arguments_list)
                                if type(result) == str:
                                    if result == 'abort':
                                        return
                                    arguments_list = []
                                    print(result)
        self.command = ''

    def say_goodbye(self):
        print(self.translate_string('goodbye', 'yellow','default'))

def starter():
    manager = InputManager()
    manager.main()