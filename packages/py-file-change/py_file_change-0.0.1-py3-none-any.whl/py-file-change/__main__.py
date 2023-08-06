import json
import os
import sys
from . import __about__
from . import main

def print_help():
    """
    Print help for py-file-change
    """
    print("\nHelp :")
    print("config file keys : "
        "\n\tcmd(required) : command to execute"
        "\n\twatch(optional) : <default:\".\"> : directory to watch"
        "\n\texclude_ends(optional) : <default:\"[]\">: won't restart if file ending in this"
        "\n\tdo_print(optional) : <default:\"False\"> : print changed, created, deleted files"
        "\n\tuse_kill(optional) : <default:\"False\"> : use kill method of process instead terminate")
    print("\nsyntax : %s [config_filename or h]" %(__package__))
    print()

if __name__ == "__main__":
    print("\n[%s] version \"%s\""%(__package__,__about__.__version__))
    print("use \"h\" for help.")

    if len(sys.argv) < 2:
        print("\n\t*Please enter configuration filename")
        print("\t Ex: python -m %s config.json"%(__package__))
        sys.exit(1)
    
    file = sys.argv[1].strip()

    if file.lower() == "h":
        print_help()
        sys.exit(0)

    if not os.path.exists(file):
        print("\n\t*File not found \"%s\""%(file))
        sys.exit(1)
    
    if not os.path.isfile(file):
        print("\n\t*Name provided for configuration is not a file \"%s\""%(file))
        sys.exit(1)

    f = open(file,"r")
    try:
        data = json.load(f)
    except json.decoder.JSONDecodeError:
        f.close()
        print("\n\t*File content is not in JSON format!")
        sys.exit(1)
    else:
        f.close()
    
    command = data.get("cmd")
    if not command:
        print("\n\t*Command[\"cmd\"] not found in file \"%s\""%(file))
        sys.exit(1)
    
    directory = data.get("watch",".")
    exclude_ends = data.get("exclude_ends",[])
    do_print = data.get("do_print",False)
    use_kill = data.get("use_kill",False)

    if not os.path.exists(directory):
        print("\n\tDirectory[\"watch\"] does not exists \"%s\""%(directory))
        sys.exit(1)
    
    if type(exclude_ends) != list:
        print("\n\tExcluding data[\"exclude_ends\"] must be in list format.")
        sys.exit(1)
    
    main(
        command=command,
        watchdir=directory,
        exclude_ends=exclude_ends,
        do_print=do_print,
        use_kill=use_kill
    )