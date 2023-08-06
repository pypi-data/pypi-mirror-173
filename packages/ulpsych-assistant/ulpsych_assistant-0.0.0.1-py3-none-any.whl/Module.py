''' Created by Kevin O'Malley, July 18 2021.
This file should hold the code for setting up the folder structure creating the module at the start of a semester. It will take the downloaded submissions from and create a "workspace"
for storing and working with the student files. Over time I hope to add functionality that will make creating extrn packs easier, faster and less bias prone.
'''

from pathlib import Path
from shutil import move


print("let's make a module")


class Module:
    '''A class that allows us to work with teaching modules'''

    def __init__(self, name, code, year, location):
        self.name = name
        self.code = code
        self.year = year
        self.location = location



    def module_setup(self):
        '''Method for setting up the module folder structure'''
        check_coursework = input("Does this module require students to submit coursework assignments?('y' = yes, 'n' = no)\n")
        check_exams = input("Does this module have an end of semester exam?('y' = yes, 'n' = no)\n")
        count_lessons = input('Please enter the number teaching weeks for this module (positive intergers only please)\n')
        lessons_count = int(count_lessons)

        while True:
            if str.lower(check_coursework) == 'y':
                count_coursework = input('Please enter the number of coursework assignments for this module (positive intergers only please)\n')
                coursework_number = int(count_coursework)
                print(f'OK {int(count_coursework)} coursework assignments\n')
                break
            elif str.lower(check_coursework) == 'n':
                print('OK no coursework')
                break
            else:
                print('Sorry I do not understand.')
                continue
        
        
        while True:
            if str.lower(check_exams) == 'y':
                print(f'OK, this module has an exam.')
                break
            elif str.lower(check_exams) == 'n':
                print('OK no end of semester exam')
                break
            else:
                print('Sorry I do not understand.')
                continue
        module_path_string = f'{self.location}\{self.code}-{self.year}'
        set_up_check = input(f"Would you like to set up a home folder and subfolders for this module at {module_path_string}?('y' = yes, 'n' = no)\n")
        
        while True:
            if str.lower(set_up_check) == 'y':
                print(f'OK, creating folder at {module_path_string}...')
                
                if Path(module_path_string).exists():
                    print(f"I'm sorry, the folder {module_path_string} already exists, please check the folder at that location.")
                    exit()
                else:
                    assignments = Path(module_path_string) / 'Assignments'
                    documents = Path(module_path_string) / 'Module Documents'
                    exams = Path(module_path_string) / 'Exam'


                    lessons = Path(module_path_string) / 'Lesson Materials'

                    Path(module_path_string).mkdir(parents=True, exist_ok=False)
                    documents.mkdir(parents=True, exist_ok=False)
                    assignments.mkdir(parents=True, exist_ok=False)
                    lessons.mkdir(parents=True, exist_ok=False)

                    for i in range(1,coursework_number+1):
                        sub_assignment = assignments / f'Assignment {i}'
                        sub_assignment.mkdir(parents=True, exist_ok=False)
                    for i in range(1,lessons_count+1):
                        lesson = lessons / f'Teaching week {i}'
                        lesson.mkdir(parents=True, exist_ok=False)
                    
                    if check_exams == 'y':
                        exams.mkdir(parents=True, exist_ok=False)

                    
                break
            elif str.lower(set_up_check) == 'n':
                print('OK, you can create your own folder structure, or restart this function if you wish to change details')
                break
            else:
                print('Sorry I do not understand.')
                break
        print(f'OK I have created the folder {module_path_string}. This contains the sub-folders: {[x.name for x in Path(module_path_string).iterdir()]}\n')
        return(Path(module_path_string))#Maybe you can return more objects or maybe you can be more granular? Or different versions of the function depending on the usecase? 




        




