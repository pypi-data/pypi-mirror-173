# py-file-change

py-file-change is a tool that execute specific command when any file changes in the directory.

## Usage

Start cmd/terminal and run following command.

```bash
$ python -m py-file-change config.json
```
---

## Config file

py-file-change requires a configuration file to continue/start the process.

Create a configuration file in root directory or current working directory where you execute the **py-file-change**

Configuration file must be JSON file and should content required data.

| Name | Type | Default value | Description |
| ---- | ---- | ---- | ----- |
| cmd | required | - | command to execute |
| watch | optional | . | directory to watch |
| exclude_ends | optional | [] | ending files will be excluded |
| do_print | optional | false | print created, changed, deleted files |
| use_kill | optional | false | uses kill method instead terminate method |

Below is the configuration file example that will used to execute command `python app.py` , watch current directory(`.`) , if the name of file changed is ending with `.json` process won't terminate

```json
{
    "cmd" : "python app.py",
    "watch" : ".",
    "exclude_ends" : [
        ".json"
    ],
    "do_print" : false,
    "use_kill" : false
}
```

**py-file-change** will take more **CPU** and **Memory** when you use it to detect changes in directory that contains large number of files.