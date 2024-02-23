# GPT Folder sort
Tired of moving files into folders?

Introducing: GPT Folder sort

# Demo
```
Before:
test
├── file1
├── file2
├── finance_report_2022
├── finance_report_2023
├── finance_report_2024
├── myunistuff
├── unistuff2
├── workdocument
└── workreport
After:
test
├── file1
├── file2
├── finance_reports
│  ├── finance_report_2022
│  ├── finance_report_2023
│  └── finance_report_2024
├── uni_stuff
│  ├── myunistuff
│  └── unistuff2
└── work_documents
   ├── workdocument
   └── workreport
```
# Usage
## requirements
you should have an openAI key as an evironment variable like this:

export OPENAI_API_KEY='your-api-key-goes-here'

## automatic folder generation:
pass in the folder to be sorted as the first argument

```python gptFS.py /path/to/folder```

the program will suggest a new way to structure the files like this
```
selected folder: ./test
suggested file structure

finance_reports/finance_report_2022
finance_reports/finance_report_2023
finance_reports/finance_report_2024
uni_stuff/myunistuff
uni_stuff/unistuff2
work_documents/workdocument
work_documents/workreport
[Hit enter to confirm]
```
Press enter to accept the suggestion and your folder will magically clean itself
## with own foldernames
if you know what folders the files should be sorted into but you are just too lazy to do that yourself, this is also a great usecase

Just pass in the destination folders as the next arguments

```python gptFS.py /path/to/folder work private hobby```

The program will make sure to sort files only into these folders.

Once again, confirm the suggestion by hitting enter.
