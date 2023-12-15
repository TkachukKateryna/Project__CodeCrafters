class ContactBook:
    def __init__(self):
        self.data = {}
        self.command_dict = {'add':'Add new contact', 'del':'delete existing contact'}

    # Prepares self.data to be saved.
    #Explanation: operates in two modes: 'add' and 'any_other_value'. If called with mode 'add', requires record id. returns a dict ONLY with a selected record. 
    #Used to add new data to the file.bin
    #The second mode requires no id. Used to remove/edit the record in the file (which are, in their essence, the same overwriting procedure). Prepares all self.data + technical vars.
    def prepare_data(self,mode:str,record_id:int):
        new_data = {} #{'Record_id':{'Record_name': name.value,'Name':value,'Phone':[values], 'Birthday':value},'Init_mem':{'Record_cnt':value,'Priority_ids':[]} }
        if mode == "add":
            for r_id,record in self.data.items():
                if r_id == record_id:
                    new_data[r_id] = {'Name':record.name,'Phone':record.phones,'Birthday':record.birthday.value}
        else:
            new_data['Init_mem'] = {'Record_cnt':self.record_cnt,'Priority_ids':self.priority_ids}
            for r_id,records in self.data.items():
                new_data[r_id] = {'Name':records.name,'Phone':records.phones,'Birthday':records.birthday.value}

        return new_data #---> dictionary, all data ripped from class instances
    
    
    # Dynamicly adds new records, deletes records, creates file.bin, etc.
    def update_file(self,mode:str,r_id:int):
        import pickle
        from pathlib import Path
        file = Path(self.file)
        if not file.exists():
            with open(file, 'wb') as storage:
                new_data = self.prepare_data("del",r_id)
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
                new_data = self.prepare_data("del",r_id)
                print(new_data)
                if r_id in new_data:
                    del new_data[r_id]
                    pickle.dump(new_data,storage)
                else:
                    print("ERROR!\nNo such record exists!")
        elif mode == "ed":
            with open(file, 'wb') as storage:
                new_data = self.prepare_data("del",r_id)
                pickle.dump(new_data,storage)
                self.size_check = False
        elif mode == "load":
            with open(file, 'rb') as storage:
                tmp_data = pickle.load(storage)
                # print(tmp_data)
                for ids,data in tmp_data.items():
                    if ids == 'Init_mem':
                        self.record_cnt = data['Record_cnt']
                        self.priority_ids = data['Priority_ids']
                    else:
                        self.data[data['Name']] = Record(data['Name'],data['Birthday'])
                        self.data[data['Name']].name.r_id = int(ids)
                        self.data[data['Name']].phones = data['Phone']
        # If mode == add, adding record to file (with correct id). If del, finding record by id and removing the line. With "ed", replacing the line/removing and adding a new one with the same id.
