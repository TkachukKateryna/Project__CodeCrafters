class ContactBook:
    def __init__(self):
        self.command_dict = {'command':'description', 'sample_text2':'sample_text2'}
        self.data = {}
        self.priority_ids = []
        self.record_cnt = 0
        self.size_check = False
        self.file = "storage.bin"
        self.update_file("load",0)


        self.method_table = {'save_notes':{'class':'ContactBook', 'methods':{self.save_changes:[],self.update_file:['mode','r_id']}}, 
                             'try_to_check':{'class':'ContactBook', 'methods':{self.test_printer:{'argument_name':'The one argument you are supposed to avoid at any costs. Beware!','argument_dame':'The second one argument you are supposed to avoid at any costs. Beware!','argument_fame':'The last one argument you are supposed to avoid at any costs. Beware!'}}}}

    def test_printer(self,*args):
        print(args)

    # Prepares self.data to be saved.
    #Explanation: operates in two modes: 'add' and 'any_other_value'. If called with mode 'add', requires record id. returns a dict ONLY with a selected record. 
    #Used to add new data to the file.bin
    #The second mode requires no id. Used to remove/edit the record in the file (which are, in their essence, the same overwriting procedure). 
    #Prepares all of self.data + technical vars. Be mindful, that technical variables are always saved under 'Init_mem' id.
    def prepare_data(self,mode:str,record_id=None):
        new_data = {} #{'Record_id':{'Name':value,'Phone':[values], 'Birthday':value},'Init_mem':{'Record_cnt':value,'Priority_ids':[]} }
        if mode == "add":
            for r_id,record in self.data.items():
                if r_id == record_id:
                    new_data[r_id] = {'Name':record.name,'Phone':record.phones,'Birthday':record.birthday.value}
                    # TODO: add support for saving the notes
        else:
            new_data['Init_mem'] = {'Record_cnt':self.record_cnt,'Priority_ids':self.priority_ids}
            for r_id,records in self.data.items():
                new_data[r_id] = {'Name':records.name,'Phone':records.phones,'Birthday':records.birthday.value}
                # TODO: add support for saving the notes

        return new_data #---> dictionary, all data ripped from class instances
    
    
    # Dynamicly adds new records, deletes records, creates file.bin, etc.
    def update_file(self,mode:str,r_id=None):
        import pickle
        from pathlib import Path
        file = Path(self.file)
        if not file.exists():
            with open(file, 'wb') as storage:
                new_data = self.prepare_data("del")
                pickle.dump(new_data,storage)
                print("No data to load! Creating new file!")
                return
        if file.stat().st_size == 0 and not self.size_check:
            self.size_check = True
            self.save_changes()
            return
        
        if mode == "add":
            with open(file, 'ab') as storage:
                new_data = self.prepare_data("add",r_id)
                pickle.dump(new_data,storage)
        elif mode == "del":
            with open(file, 'wb') as storage:
                new_data = self.prepare_data("del")
                print(new_data)
                if r_id in new_data:
                    del new_data[r_id]
                    pickle.dump(new_data,storage)
                else:
                    print("ERROR!\nNo such record exists!")
        elif mode == "ed":
            with open(file, 'wb') as storage:
                new_data = self.prepare_data("del")
                pickle.dump(new_data,storage)
                self.size_check = False
        elif mode == "load":
            with open(file, 'rb') as storage:
                tmp_data = pickle.load(storage)
                for ids,data in tmp_data.items():
                    if ids == 'Init_mem':
                        self.record_cnt = data['Record_cnt']
                        self.priority_ids = data['Priority_ids']
                    else:
                        self.data[data[ids]] = RecordManager(data['Name'],data['Birthday']) # Re-creating Record() class. Can be named differently, rewrite if neccessary.
                        self.data[data[ids]].phones = data['Phone']
                        # TODO: add support for loading the notes

        # If mode == add, adding record to file (with correct id). If mode == 'del', removes the record by id, overwrites saved data with the new self.data + technical variables. 
        #With "ed", overwrites saved data with the new self.data + technical variables

    #Saves self.data and some technical variables. Can be used, although everything should be saved automatically. may be used to ensure, that nothing will be lost.
    def save_changes(self):
        self.update_file("ed")
