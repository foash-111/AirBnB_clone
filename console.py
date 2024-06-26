#!/usr/bin/python3
"""my console module, the entry point of the command interpreter:"""

import cmd
from models.base_model import BaseModel
import models
from models.user import User
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review
from models.state import State


my_classes = {
        'BaseModel': BaseModel, 'User': User, 'City': City,
        'Amenity': Amenity, 'Place': Place, "Review": Review, "State": State
        }


class HBNBCommand(cmd.Cmd):
    """the entry point of the command interpreter:"""
    prompt = "(hbnb) "

    def do_create(self, line):
        """ Creates a new instance Ex: $ create BaseModel"""
        if line:
            if line not in my_classes.keys():
                print("** class doesn't exist **")
            else:
                class_name = my_classes[line]
                insta = class_name()
                print(insta.id)
                models.storage.save()
        else:
            print("** class name missing **")

    def do_show(self, line):
        """  Prints the string representation of an instance
        based on the class name and id.
        Ex: $ show <BaseModel> 1234-1234-1234"""
        if line:
            words = line.split()
            if words[0] not in my_classes.keys():
                print("** class doesn't exist **")
            else:
                if len(words) == 1:
                    print("** instance id missing **")
                else:
                    file_objs = models.storage.all()
                    for i in file_objs.values():
                        if words[1] == i.id:
                            print(i)
                            return
                    print("** no instance found **")
        else:
            print("** class name missing **")

    def do_destroy(self, line):
        """Deletes an instance based on the class name and id
          (save the change into the JSON file).
          Ex: $ destroy BaseModel 1234-1234-1234."""
        if line:
            words = line.split()
            if words[0] not in my_classes.keys():
                print("** class doesn't exist **")
            else:
                if len(words) == 1:
                    print("** instance id missing **")
                else:
                    file_objs = models.storage.all()
                    for i in file_objs.values():
                        if words[1] == i.id:
                            key = f"{i.__class__.__name__}.{i.id}"
                            del file_objs[key]
                            models.storage.save()
                            return
                    print("** no instance found **")
        else:
            print("** class name missing **")

    def do_all(self, line):
        """all: Prints all string representation of all instances
         based or not on the class name.
         Ex: $ all BaseModel or $ all."""
        file_objs = models.storage.all()
        my_list = []
        count = 0
        if line:
            for i in file_objs.values():
                if i.to_dict()['__class__'] == line:
                    my_list.append(str(i))
                    count += 1
        else:
            for i in file_objs.values():
                my_list.append(str(i))

        print(my_list)
        return (count)

    def do_update(self, line):
        """Ex: update <class name> <id> <attribute name> "<attribute value>"""
        if line:
            words = line.split()
            if words[0] not in my_classes.keys():
                print("** class doesn't exist **")
            else:
                if len(words) == 1:
                    print("** instance id missing **")
                else:
                    file_objs = models.storage.all()
                    for i in file_objs.values():
                        if words[1] == i.id:
                            if len(words) == 2:
                                print("** attribute name missing **")
                            elif len(words) == 3:
                                print("** value missing **")
                            else:
                                words[2] = words[2].replace('"', "")
                                words[3] = words[3].replace('"', "")
                                i.__dict__[words[2]] = words[3]
                                models.storage.save()
                            return
                    print("** no instance found **")
        else:
            print("** class name missing **")

    def default(self, line=None):
        """excute dynamic methods"""
        cpd_line = line
        line = line.replace('(', ' ').replace(')', ' ').replace('.', ' ')
        line = line.replace(',', ' ')
        words = line.split()
        my_objs = models.storage.all()

        if len(words) == 2:
            if words[1] == "all":
                print("all")
                self.do_all(words[0])
            elif words[1] == "count":
                counter = 0
                if words[0] not in my_classes.keys():
                    print("** class doesn't exist **")
                else:
                    for value in my_objs.values():
                        if value.__class__.__name__ == words[0]:
                            counter += 1
                    print(counter)
        elif len(words) == 3:
            line = ""
            line = words[0] + " " + words[2]
            if words[1] == "show":
                self.do_show(line)
            elif words[1] == "destroy":
                self.do_destroy(line)
        elif len(words) == 5:
            line = ""
            if words[1] == "update":
                words[2] = words[2].replace('"', "")
                words[3] = words[3].replace('"', "")
                print(words)
                line = (words[0] + " " + words[2] + " " +
                        words[3] + " " + words[4])
                self.do_update(line)
        elif words[1] == 'update':
            temp = cpd_line.split('.')
            new_temp = temp[1][6:]
            my_tuple = eval(new_temp)
            # print(my_tuple)
            # print(type(my_tuple[1]))
            for key, value in my_tuple[1].items():
                line = (words[0] + " " + my_tuple[0] + " " +
                        str(key) + " " + str(value))
                self.do_update(line)

        else:
            print("*** Unknown syntax: " + line)

    def do_EOF(self, line):
        """ctrl + d > to exit the programm"""
        print()
        return True

    def do_quit(self, line):
        """Quit command to exit the program """
        return True


if __name__ == '__main__':
    HBNBCommand().cmdloop()
