# FreeIPA Modifications 

Python has some descent capabilities to add users and groups etc

## Whats happening

- Add users: 'alice', 'bob', 'dave', 'frank'
- Assign them to group 'employees', and managed by 'manager'
- Additionally assign them to: 'team1' or 'team2' 

## Install

```
python3 -m venv env
source env/bin/activate
```

```
pip install -r requirements.txt
```

## Run

```
python add_user.py
```
