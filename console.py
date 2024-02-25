#!/usr/bin/python3
""" console module """
import cmd
import re
import shlex

import models
from models.appointment import Appointments
from models.base_model import BaseModel
from models.doctors import Doctors
from models.location import Location
from models.reviews import Reviews
from models.users import Users


class HBNBCommand(cmd.Cmd):
    """Smile Seeker console class"""
    classes = {"BaseModel": BaseModel, "Users": Users, "Doctors": Doctors,
               "Reviews": Reviews, "Appointments": Appointments, "Location": Location}

    prompt = "(SS) "

    def do_EOF(self, arg):
        """Exits console"""
        return True

    def emptyline(self):
        """ overwriting the empty line method """
        return False

    def do_quit(self, arg):
        """Quit command to exit the program"""
        return True

    # ------------------------------------------
    # ----------- Default - --------------------
    # ------------------------------------------
    def default(self, line):
        """
        overriding the 'default' function
        I will be able to enter command: <class>.<command>(params)
        """

        cmds = {
            "all": self.do_all,
            "create": self.do_create,
            "count": self.do_count,
            "show": self.do_get,
            "destroy": self.do_delete,
            "update": self.do_update
        }
        match = re.search(r"\.", line)

        if match:
            # split the line into two part based on '.'
            line_list = [line[:match.span()[0]], line[match.span()[1]:]]

            match = re.search(r"\((.*?)\)", line_list[1])

            if match:
                match = re.search(r"""(\w+)\.(\w+)\((.*?)\)$""", line)
                if match:
                    args = match.groups()

                    class_name = args[0]
                    command = args[1]
                    param = args[2]

                    # get all the parameters
                    matches = re.findall(r'"([^"]*)"', param)
                    parameters = '='.join(matches)

                    if command in cmds.keys() and class_name in self.classes.keys():
                        return cmds[command](class_name + " " + parameters)

        print(f"*** Unknown syntax: {line}")
        return False

    # ======== pars_params =============
    def parse_params(self, params_str):
        """
        parse params as a string
        and return params as a dict
        """
        params_list = params_str.split("=")
        if len(params_list) > 0 and len(params_list) % 2 == 0:
            i = 0
            data_types = [int, float]
            params_dict = {}
            while i < len(params_list):
                key = params_list[i]
                value = params_list[i + 1]

                # checking if value is an int or float
                for type in data_types:
                    try:
                        casted_value = type(value)
                        value = casted_value
                        break
                    except ValueError:
                        pass

                params_dict[key] = value
                i += 2

            return params_dict
        return None

    # ========== create =================
    def do_create(self, line):
        """create an instance"""
        args = line.split(" ", 1)
        cls = args[0] if len(args) > 0 else None
        params = args[1] if len(args) > 1 else None

        if not cls:
            print("** class name missing **")

        elif cls not in self.classes:
            print("** invalid class name **")

        else:
            params_dict = {}
            if params:
                params_dict = self.parse_params(params)

            obj = self.classes[cls](**params_dict)
            print(obj.id)
            obj.save()

    def help_create(self):
        txt = "create an instance of the class\n"
        txt += "Usage_1: create <class_name>\n"
        txt += 'Usage_2: <class>.create("key": "value", "key": "value"...)'
        print(txt)

    # ========== all =================
    def do_all(self, line):
        args = line.split()
        if len(args) > 0 and args[0] not in self.classes:
            print("** invalid class name **")
            return
        if len(args) == 0:
            cls = None
        else:
            cls = args[0]

        objs_dict = {}
        for k, v in models.storage.all(cls).items():
            objs_dict[k] = v.to_dict()

        print(objs_dict)

    def help_all(self):
        txt = "get all instances of class or all\n"
        txt += "Usage: all <class_name(optional)>"
        print(txt)

    # ========== get =================
    def do_get(self, line):
        args = line.split()
        if len(args) == 0:
            print("** class name is missing **")
            return
        if len(args) > 0 and args[0] not in self.classes:
            print("** invalid class name **")
            return
        if len(args) < 2:
            print("** id is missing **")
            return

        cls = args[0]
        obj_id = args[1]
        obj = models.storage.get(cls, obj_id)
        if not obj:
            print("** invalid instance id **")
            return

        print(obj)

    def help_get(self):
        txt = "get an instance\n"
        txt += "Usage: get <class_name> <instance_id>"
        print(txt)

    # ========== update =================
    def do_update(self, line):
        args = shlex.split(line)
        if len(args) == 0:
            print("** class name is missing **")
            return
        if len(args) > 0 and args[0] not in self.classes:
            print("** invalid class name **")
            return
        if len(args) < 2:
            print("** id is missing **")
            return

        cls = args[0]
        obj_id = args[1]
        obj = models.storage.get(cls, obj_id)
        if not obj:
            print("** invalid instance id **")
            return
        if len(args) < 3:
            print("** key is missing **")
            return
        if len(args) < 4:
            print("** value is missing **")
            return
        key = args[2]
        value = args[3]
        obj.update(**{key: value})

    def help_update(self):
        txt = "update a class instance\n"
        txt += "Usage: update <class> <id> <key> <value>"
        print(txt)

    # ========== delete =================
    def do_delete(self, line):
        args = shlex.split(line)
        if len(args) == 0:
            print("** class name is missing **")
            return
        if len(args) > 0 and args[0] not in self.classes:
            print("** invalid class name **")
            return
        if len(args) < 2:
            print("** id is missing **")
            return

        cls = args[0]
        obj_id = args[1]
        obj = models.storage.get(cls, obj_id)
        if not obj:
            print("** invalid instance id **")
            return

        obj.delete()

    def help_delete(self):
        txt = "delete a class instance\n"
        txt += "Usage: delete <class> <id>"
        print(txt)

    # ========== count =================
    def do_count(self, line):
        args = shlex.split(line)
        if len(args) == 0:
            print("** class name is missing **")
            return
        if len(args) > 0 and args[0] not in self.classes:
            print("** invalid class name **")
            return

        cls = args[0]
        print(len(models.storage.all(cls)))

    def help_count(self):
        txt = "count the number of instances of a class\n"
        txt += "Usage: count <class>"


if __name__ == "__main__":
    HBNBCommand().cmdloop()
