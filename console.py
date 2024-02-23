#!/usr/bin/python3
""" console module """
import cmd
import shlex

import models
from models.base_model import BaseModel


class HBNBCommand(cmd.Cmd):
    """Smile Seeker console class"""
    classes = {"BaseModel": BaseModel}

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

    # ========== create =================
    def do_create(self, line):
        """create an instance"""
        args = line.split()
        if len(args) == 0:
            print("** class name missing **")

        elif args[0] not in self.classes:
            print("** invalid class name **")

        else:
            obj = self.classes[args[0]]()
            print(obj.id)

            obj.save()

    def help_create(self):
        txt = "create an instance of the class\n"
        txt += "Usage: create <class_name>"
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
