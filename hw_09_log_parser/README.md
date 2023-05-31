### log_parser.py script to parse access.log file(s)
#### Command line options available:
"-h" or "--help" — get some hints\
"-p" or "--path" — define log file or folder with files (only *.log) to parse
#### Example of usage:
python3 log_parser.py --path ~/Downloads/logs/access.log

the main function is get_data_from_longest_request

#### example
```python
from hw_09_log_parser.log_parser import get_data_from_longest_request
blocks = get_data_from_longest_request("some")
# Do something with blocks.
```