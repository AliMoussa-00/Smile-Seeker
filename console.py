#!/usr/bin/python3
""" console module """
import cmd
from models.base_model import BaseModel


class HBNBCommand(cmd.Cmd):
    """Smile Seeker console class"""
    classes = {"BaseModel": BaseModel}

    prompt = "(SS) "

    def do_EOF(self, arg):
        """Exits console"""
        return True

    def emptyline(self):
        """ overwriting the emptyline method """
        return False

    def do_quit(self, arg):
        """Quit command to exit the program"""
        return True

    # ========== create =================
    def do_create(self, line):
        """create an instance"""
        args = line.split()
        if len(args) == 0:
            print("** classname missing **")

        elif args[0] not in self.classes:
            print("** invalide class name **")

        else:
            obj = self.classes[args[0]]()
            print(obj.id)

            obj.save()

    def help_create(self):
        txt = "create an instance of the class\n"
        txt += "Usage: create <class_name>"
        print(txt)
    
    # ========== all =================


if __name__ == "__main__":
    HBNBCommand().cmdloop()
