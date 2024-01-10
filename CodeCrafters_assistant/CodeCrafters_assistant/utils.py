
class Id_format:
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

class DialogueConstructor:
    def dialogue_constructor(self,cfg:dict):
        self.args = None
        for phrase_data in cfg.values():
            if phrase_data["type"] == 'show':
                result = self.phrase_show(phrase_data)
                if result == "abort":
                    #Might create crashes, be mindful
                    self.ongoing = None
                    self.field_id = None
                    #
                    break
            else:
                result = self.phrase_act(phrase_data)
                while result != True and result != "abort":
                    if type(result) == str:
                        print(result)
                    result = self.phrase_act(phrase_data)
                if result == "abort":
                    #Might create crashes, be mindful
                    self.ongoing = None
                    self.field_id = None
                    #
                    break
    
    def phrase_act(self, phrase_data):
        self.phrase_started = False
        if self.__class__.__name__ != "InputManager":
            self.parent.technical_actions['default']["get_input"] = { 
                                            'technical':True,
                                                'methods':{self.args_dummy:{'prompt':phrase_data["prompt"]}}}
            self.parent.start_script('get_input', mode='technical') #get input here
        else:
            self.technical_actions['default']["get_input"] = { 
                                            'technical':True,
                                                'methods':{self.args_dummy:{'prompt':phrase_data["prompt"]}}}
            self.start_script('get_input', mode='technical') #get input here
        if self.args == None:
            return "abort"
        result = None
        if phrase_data["checks"] == {}:
            for method,arguments in phrase_data["actions"].items():
                args = []
                args.append(self.args)
                if arguments != []:
                    args.append(arguments)
                    result = method(args) #execute action
                result = method(args) #execute action
                if type(result) == str:
                    return result
            self.args = None
            if type(result) != str:
                return True #True if passed ALL checks, False if failed at least one, i.e. needs to be restarted, "abort" if needs to be halted
        else:
            for method,arguments in phrase_data["checks"].items():
                args = []
                args.append(self.args)
                if arguments != []:
                    args.append(arguments)
                if method(args) != True:
                    self.args = None
                    return method(args)
            for method,arguments in phrase_data["actions"].items():
                args = []
                args.append(self.args)
                if arguments != []:
                    args.append(arguments)
                    result = method(args) #execute action
                result = method(args) #execute action
                if type(result) == str:
                    return result
            self.args = None
            if type(result) != str:
                return True #True if passed ALL checks, False if failed at least one, i.e. needs to be restarted, "abort" if needs to be halted

    def phrase_show(self, phrase_data):
        if phrase_data["checks"] == {}:
            if type(phrase_data["string"]) == str:
                print(phrase_data["string"])
            else:
                print(phrase_data["string"]())
            return True
        else:
            for method,arguments in phrase_data["checks"].items():
                if arguments != []:
                    if type(method(arguments)) == str:
                        if method(arguments) != "abort":
                            print(method(arguments))
                        return "abort"
                else:
                    if type(method()) == str:
                        if method() != "abort":
                            print(method())
                        return "abort"
            
            if type(phrase_data["string"]) == str:
                print(phrase_data["string"])
            else:
                print(phrase_data["string"]())

    def args_dummy(self, *args):
        self.phrase_started = True
        self.args = []
        for k in args:
            self.args.append(k) #saves user input

class Translate:
    def translate_string(self,string:str,st_color=None,end_color=None, mode=None):
        string = str(string).strip().lower()
        local = None
        local_def = None
        if self.__class__.__name__ == "InputManager":
            local = self.localization[0]
            local_def = self.localization[0]
            if type(mode) == int and mode < len(self.modules):
                local = self.localization[int(mode) + 1]
            elif type(self.module_chosen) == int and self.module_chosen < len(self.modules):
                local = self.localization[self.module_chosen + 1]
        else:
            local = self.parent.localization[0]
            local_def = self.parent.localization[0]
            if type(mode) == int and mode < len(self.parent.modules):
                local = self.parent.localization[int(mode) + 1]
            elif type(self.parent.module_chosen) == int and self.parent.module_chosen < len(self.parent.modules):
                local = self.parent.localization[self.parent.module_chosen + 1]
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

class DataSaver:
    # Dynamicly adds new records, deletes records, creates file.bin, etc.
    # If mode == add, adding record to file. If mode == 'del', removes the record by id, overwrites saved data with the new parsed self.data. 
    # With "ed", overwrites saved data with the new parsed self.data
    def update_file(self,mode:str,r_id=None):
        import pickle
        from pathlib import Path
        file = Path(self.file)
        if not file.exists():
            with open(file, 'wb') as storage:
                #print("No data to load! Creating new file!")
                return

        if mode == "add":
            with open(file, 'ab') as storage:
                for rid,record in self.data.items():
                    if rid == r_id:
                        pickle.dump(record.data,storage)
                        self.generated_ids += 1
                        return
                raise ValueError('Record Id not found!')
        elif mode == "del":
            with open(file, 'wb') as storage:
                if r_id in self.data:
                    del self.data[r_id]

                if len(self.data) > 0:
                    id_generator = 0
                    for id,record in self.data.items():
                        pickle.dump(record.data,storage)
                        id_generator += 1
                    self.generated_ids = id_generator
                else:
                    #print(self.parent.translate_string('note_list_empty','yellow','green'))
                    pass
        elif mode == "ed":
            with open(file, 'wb') as storage:
                if len(self.data) > 0:
                    id_generator = 0
                    for id,record in self.data.items():
                        pickle.dump(record.data,storage)
                        id_generator += 1
                    self.generated_ids = id_generator
        elif mode == "load":
            with open(file, 'rb') as storage:
                if file.stat().st_size != 0:
                    id_generator = 0
                    if self.__class__.__name__ == "ContactBook":
                        from CodeCrafters_assistant.record_manager import Record
                    else:
                        from CodeCrafters_assistant.notes import Note
                    try:
                        while True:  
                            record = pickle.load(storage)
                            if self.__class__.__name__ == "ContactBook":
                                self.data[id_generator] = Record(parent_class=self.parent)
                            else:
                                self.data[id_generator] = Note(parent_class=self.parent)
                            self.data[id_generator].load_data(record)
                            id_generator += 1
                    except EOFError:
                        self.generated_ids = id_generator
                        self.record_cnt = id_generator
                        #print('Reached the end of file!')

class Utils(DataSaver, Id_format, DialogueConstructor):
    def dialogue_check(self,variable):
        variable = self.single_param(variable)
        if variable.lower() != 'n':
            return True
        return False
 
    def id_assign(self,mode:str,record):
        if mode == "add":
            if len(self.priority_ids) > 0:
                self.data[self.priority_ids[0]] = record
                self.ongoing = self.priority_ids[0]
                del self.priority_ids[0]
            else:
                self.data[self.record_cnt] = record
                self.ongoing = self.record_cnt
                self.record_cnt += 1
        elif mode == "del":
            for k,v in self.data.items():
                if v == record:
                    self.priority_ids.append(k)

    def find_in(self, where, what:str, mode=None):
        from re import search
        what = fr"{what.lower()}"
        if not mode:
            where = where.lower()
            if where.find(what) != -1:
                return search(what,where).span()
            else:
                return False
        elif mode == 'dict':
            phones = "; ".join(f"{phone}" for phone in where.values()).lower()
            if phones.find(what) != -1:
                return search(what,phones).span()
            else:
                return False
  

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
    
class RecordConstructor:
    def constructor(self, data:dict):
        string = data["intro"]
        technical = ["intro", "what", "where"]
        check = False
        where = None
        for name,param in data.items():
            if name in technical:
                continue
            if data['where'] != "all" and data['where'] != name:
                string += f"{param[0]}: {param[1]}"
            else:
                if data['where'] == "all":
                    where = data[name][1]
                else:
                    where = data[data['where']][1]
                highlighted = ''
                if self.find_in(where,data['what']):
                    check = True
                    highlighted = f"{bcolors.GREEN}{where[:self.find_in(where,data['what'])[0]]}{bcolors.YELLOW}{where[self.find_in(where,data['what'])[0]:self.find_in(where,data['what'])[1]]}"
                    cut_where = where[self.find_in(where,data['what'])[1]:]
                    while self.find_in(cut_where,data['what']):
                        highlighted += f"{bcolors.GREEN}{cut_where[:self.find_in(cut_where,data['what'])[0]]}{bcolors.YELLOW}{cut_where[self.find_in(cut_where,data['what'])[0]:self.find_in(cut_where,data['what'])[1]]}"
                        cut_where = cut_where[self.find_in(cut_where,data['what'])[1]:]
                    
                    if cut_where != "":
                        highlighted += f"{bcolors.GREEN}{cut_where}"
                    else:
                        highlighted += bcolors.GREEN
                    string += f"{param[0]}: {highlighted}"
                else:
                    string += f"{param[0]}: {param[1]}"

        if check == True:
            return string
        else:
            return False
