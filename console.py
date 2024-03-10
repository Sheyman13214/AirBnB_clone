#!/usr/bin/python3
"""This is the script for the entry point of the command line interpreter."""

import re
import cmd
import json
from models import storage
from models.base_model import BaseModel

class HBNBCommand(cmd.Cmd):
    """This is the class for the command line intepreter."""

    prompt = "(hbnb) "

    def default(self, line):
        """Catch commands if nothing else matches then."""
        # print("DEF:::", line)
        self._precmd(line)

    def do_EOF(self, arg):
        """EOF command to exit the program."""
        print()
        return True

    def _precmd(self, line):
        """Intercepts commands to test for class.syntax()"""
        # print("PRECMD:::", line)
        twin = re.search(r"^(\w*)\.(\w+)(?:\(([^)]*)\))$", line)
        if not twin:
            return line
        classname = twin.group(1)
        method = twin.group(2)
        args = twin.group(3)
        twin_uid_and_args = re.search('^"([^"]*)"(?:, (.*))?$', args)
        if twin_uid_and_args:
            uid = twin_uid_and_args.group(1)
            att_or_dict = twin_uid_and_args.group(2)
        else:
            uid = args
            attr_or_dict = False

        att_and_value = ""
        if method == "update" and att_or_dict:
            twin_dict = re.search('^({.*})$', att_or_dict)
            if twin_dict:
                self.update_dict(classname, uid, twin_dict.group(1))
                return ""
            twin_attr_and_value = re.search(
                '^(?:"([^"]*)")?(?:, (.*))?$', att_or_dict)
            if twin_attr_and_value:
                att_and_value = (twin_attr_and_value.group(
                    1) or "") + " " + (twin_attr_and_value.group(2) or "")
        command = method + " " + classname + " " + uid + " " + att_and_value
        self.onecmd(command)
        return command

    def do_create(self, line):
        """
        Creates a new instance of BaseModel.
        Saves it (to the JSON file) and prints the id.
        """
        if line is None or line == "":
            print("** class name missing **")
        elif line not in storage.classes():
            print("** class doesn't exist **")
        else:
            new_inst = storage.classes()[line]()
            new_inst.save()
            print(new_inst.id)

    def do_show(self, line):
        """This prints the string rep of an instance."""
        if line is None or line == "":
            print("** class name missing **")
        else:
            string =line.split(' ')
            if string[0] not in storage.classes():
                print("** class doesn't exist **")
            elif len(string) < 2:
                print("** instance id missing **")
            else:
                key = "{}.{}".format(string[0], string[1])
                if key not in storage.all():
                    print("** no instance found **")
                else:
                    print(storage.all()[key])

    def do_destroy(self, line):
        """Deletes an instance based on the class name and id (save the change into the JSON file)"""
        if line is None or line == "":
            print("** class name missing **")
            return
        else:
            words = line.split(' ')
            if words[0] not in storage.classes():
                print("** class doesn't exist **")
                return
            elif len(words) < 2:
                print("** instance id missing **")
            else:
                key = "{}.{}".format(words[0], words[1])
                if key not in storage.all():
                    print("** no instance found **")
                else:
                    del storage.all()[key]
                    storage.save()

    def all(self, line):
        """This prints all string representation of all instances.
        """
        if line != "":
            string = line.split(' ')
            if string[0] not in storage.classes():
                print("** class doesn't exist **")
            else:
                lis = [str(obj) for key, obj in storage.all().items()
                      if type(obj).__name__ == string[0]]
                print(lis)
        else:
            new_list = [str(obj) for key, obj in storage.all().items()]
            print(new_list)

    def do_update(self, line):
        """This updates an instance by adding or updating attribute.
        """
        if line is None or line == "":
            print("** class name missing **")
            return

        rex = r'^(\S+)(?:\s(\S+)(?:\s(\S+)(?:\s((?:"[^"]*")|(?:(\S)+)))?)?)?'
        twin = re.search(rex, line)
        classname = twin.group(1)
        uid = twin.group(2)
        attribute = twin.group(3)
        value = twin.group(4)
        if not twin:
            print("** class name missing **")
        elif classname not in storage.classes():
            print("** class doesn't exist **")
        elif uid is None:
            print("** instance id missing **")
        else:
            # Forming a key based on class name and instance ID
            key = "{}.{}".format(classname, uid)
            if key not in storage.all():
                print("** no instance found **")
            elif not attribute:
                print("** attribute name missing **")
            elif not value:
                print("** value missing **")
            else:
                cast = None  # Determine the data type of the value and perform necessary casting
                if not re.search('^".*"$', value):
                    if '.' in value:
                        cast = float
                    else:
                        cast = int
                else:
                    value = value.replace('"', '')
                # Update the attribute of the instance
                attributes = storage.attributes()[classname]
                if attribute in attributes:
                    value = attributes[attribute](value)
                elif cast:
                    try:
                        value = cast(value)
                    except ValueError:  # Error handling to handle casting cases where it is not possible
                        pass  # fine, stay a string then
                setattr(storage.all()[key], attribute, value)
                storage.all()[key].save()  # save the changes

    def update_dict(self, classname, uid, s_dict):
        """This is the helper method for update() with a dictionary."""
        t = s_dict.replace("'", '"')
        e = json.loads(s)
        if not classname:
            print("** class name missing **")
        elif classname not in storage.classes():
            print("** class doesn't exist **")
        elif uid is None:
            print("** instance id missing **")
        else:
            key = "{}.{}".format(classname, uid)
            if key not in storage.all():
                print("** no instance found **")
            else:
                attributes = storage.attributes()[classname]
                for attribute, value in e.items():
                    if attribute in attributes:
                        value = attributes[attribute](value)
                    setattr(storage.all()[key], attribute, value)
                storage.all()[key].save()

    def do_quit(self, arg):
        """Quit command to exit the program."""
        return True

    def emptyline(self):
        """Do nothing on empty input line."""
        pass


if __name__ == '__main__':
    HBNBCommand().cmdloop()
