from record_manager import MiscChecks, RecordManager
#from collections import UserDict
      
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

class ContactBook(): #UserDict
    def __init__(self):
        self.data = {}
        self.priority_ids = []
        self.record_cnt = 0
        self.generated_ids = 0
        self.file = "storage.bin"
        self.update_file("load",0)


        self.method_table = {'__localization_insert':{'name':'менеджера контактів','description':'менеджер контактів та записів'},
                            'contact_create':{'class':'ContactBook', 'description':"Додає новий запис до книги контактів. Потрібно обов'язково вказати ім'я, а телефони та день народження можна додати й пізніше.", 'methods':{self.add_contact:{'name':"Введіть, будь ласка, ім'я (обов'язково)",'phone':f"Введіть, будь ласка, номер телефону (або '{bcolors.RED}N{bcolors.GREEN}',якщо бажаєте додати пізніше)", 'birthday':f"Введіть, будь ласка, день народження контакта (або '{bcolors.RED}N{bcolors.GREEN}',якщо бажаєте додати пізніше)"}}}, 
                            'try_to_check':{'class':'ContactBook', 'description':'description_text', 'methods':{self.test_printer:{'argument_name':'The one argument you are supposed to avoid at any costs. Beware!','argument_dame':'The second one argument you are supposed to avoid at any costs. Beware!','argument_fame':'The last one argument you are supposed to avoid at any costs. Beware!'}}}}

    def test_printer(self,*args):
        print(args)

    # Prepares self.data to be saved.
    #Explanation: operates in two modes: 'add' and 'any_other_value'. If called with mode 'add', requires record id. returns a dict ONLY with a selected record. 
    #Used to add new data to the file.bin
    #The second mode requires no id. Used to remove/edit the record in the file (which are, in their essence, the same overwriting procedure). 
    #Prepares all of self.data + technical vars. Be mindful, that technical variables are always saved under 'Init_mem' id.
    def prepare_data(self,mode:str,record_id=None):
        if mode == "add":
            for rid,record in self.data.items():
                if rid == record_id:
                    return {'Name':record.name,'Phones':record.phones,'Birthday':record.birthday}
    
    
    # Dynamicly adds new records, deletes records, creates file.bin, etc.
    def update_file(self,mode:str,r_id=None):
        import pickle
        from pathlib import Path
        file = Path(self.file)
        if not file.exists():
            with open(file, 'wb') as storage:
                print("No data to load! Creating new file!")
                return

        if mode == "add":
            with open(file, 'ab') as storage:
                st_r_id = self.generated_ids
                class PersPickler(pickle.Pickler):
                    def persistent_id(self, obj):
                        """Return a persistent id for the `bar` object only"""
                        return st_r_id if st_r_id else None

                PersPickler(storage).dump(self.prepare_data("add",record_id=r_id))
        elif mode == "del":
            with open(file, 'wb') as storage:
                if r_id in self.data:
                    del self.data[r_id]

                if len(self.data) > 0:
                    id_generator = 0
                    class PersPickler(pickle.Pickler):
                        def persistent_id(self, obj):
                            """Return a persistent id for the `bar` object only"""
                            return id_generator if id_generator else None
                    
                    for id,record in self.data.items():
                        PersPickler(storage).dump({'Name':record.name,'Phones':record.phones,'Birthday':record.birthday})
                        id_generator += 1
                    self.generated_ids = id_generator
                else:
                    print("ERROR!\nNo such record exists!")
        elif mode == "ed":
            with open(file, 'wb') as storage:
                if len(self.data) > 0:
                    id_generator = 0
                    class PersPickler(pickle.Pickler):
                        def persistent_id(self, obj):
                            """Return a persistent id for the `bar` object only"""
                            return id_generator if id_generator else None
                    
                    for id,record in self.data.items():
                        PersPickler(storage).dump({'Name':record.name,'Phones':record.phones,'Birthday':record.birthday})
                        id_generator += 1
                    self.generated_ids = id_generator
        elif mode == "load":
            with open(file, 'rb') as storage:
                class PersUnpickler(pickle.Unpickler):
                    def persistent_load(self, pers_id):
                        try:
                            if int(pers_id) or int(pers_id) == 0:
                                return pers_id
                        except TypeError(f'{pers_id} Cant be converted into int!'):
                            raise pickle.UnpicklingError("Persistent id is not number in string!")
                
                if file.stat().st_size != 0:
                    id_generator = 0
                    try:
                        while True:  
                            record = PersUnpickler(storage).load()
                            print(record)
                            self.data[id_generator] = RecordManager(record['Name'])
                            self.data[id_generator].load_data(name=record['Name'],phones=record['Phones'],birthday=record['Birthday'])
                            id_generator += 1
                    except EOFError:
                        self.generated_ids = id_generator
                        self.record_cnt = id_generator
                        print('Reached the end of file!')
            print(self.data)

        # If mode == add, adding record to file (with correct id). If mode == 'del', removes the record by id, overwrites saved data with the new self.data + technical variables. 
        #With "ed", overwrites saved data with the new self.data + technical variables

    #Saves self.data and some technical variables. Can be used, although everything should be saved automatically. may be used to ensure, that nothing will be lost.
    def save_changes(self):
        self.update_file("ed")

    def add_contact(self,name,phone,birthday):
        new_record = RecordManager(name)
        if phone.lower() != 'n':
            new_record.add_phone(phone)
        if birthday.lower() != 'n':
            new_record.add_birthday(birthday)

        self.id_assign(mode="add",record=new_record)
        self.update_file("add",self.generated_ids)
        print(new_record)
    
    def id_assign(self,mode:str,record:RecordManager):
        if mode == "add":
            if len(self.priority_ids) > 0:
                self.data[self.priority_ids[0]] = record
                del self.priority_ids[0]
            else:
                self.data[self.record_cnt] = record
                self.record_cnt += 1
        elif mode == "del":
            for k,v in self.data.items():
                if v == record:
                    self.priority_ids.append(k)
        

# if __name__ == '__main__':
#     book = ContactBook()
#     test_record = RecordManager('Biba')
#     test_record.add_phone('0201592745')
#     test_record.add_phone('1201592746')
#     test_record.birthday = '01-01-2002'

#     book.add_record(test_record)
#     print(book.data)
    # book.data['0'] = {'Name':'Santa','Birthday':'20-02-3012','Phones':['01','73']}
    # book.update_file(mode="add",r_id='0')
    # book.data['1'] = {'Name':'Biba','Birthday':'11-02-3012','Phones':['55','29']}
    # book.update_file(mode="add",r_id='1')
    # book.data['2'] = {'Name':'Boba','Birthday':'30-02-3011','Phones':['90','06']}
    # book.update_file(mode="add",r_id='2')