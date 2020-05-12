from python_freeipa import ClientMeta

CommonTestPassword = 'Secret123'

client = ClientMeta('ipa.demo1.freeipa.org')
client.login('admin', CommonTestPassword)

Userlist = ['alice', 'bob', 'dave', 'frank']

# Reset, Add Users, and Set Manager
for user in UserList:
    client.user_del(user, o_continue=True)
    client.user_add(user, user.capitalize(), 'TestUser', user.capitalize() + ' TestUser', o_preferredlanguage='EN', o_userpassword=CommonTestPassword)
    alice_mgr = client.user_add_manager(user, o_user="manager")
    client.group_add_member("employees", o_user=user)

# Create New Groups
client.group_add('team1')
client.group_add('team2')
# Add to Existing Group

team1=['alice','bob','manager']
team2=['dave','frank','manager']

for user in Team1:
    client.group_add_member("team1", o_user=user)

for user in Team2:
    client.group_add_member("team2", o_user=user)


