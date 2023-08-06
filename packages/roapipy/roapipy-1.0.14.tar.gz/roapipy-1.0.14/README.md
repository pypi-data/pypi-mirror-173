# roapipy Documentation
roapipy - A python wrapper for the roblox api
## class Client()
For usage of roapipy, upon importing, you need to define your client - this will be your main mode of using the wrapper. Recommended names for its variable are; **robloxclient, roclient & client**<br>
For the purpose of simplicity, this documentation will be using **roclient**.<br>
If you are unsure on how to get your roblosecurity cookie, use the following [tutorial](https://ro.py.jmk.gg/dev/roblosecurity/) (link from popular roblox python api wrapper, the purpose of this wrapper is to be a simpler version of it).
```py
roclient = roapipy.Client(“.roblosecurity”)
```
**Parameters:**
*  **rosec** (Optional[str]) - roblosecurity code (only required if using authenticated commands like accepting users into a group or setting shout)
### class User()
Used to interact with users
#### Info(user)
Returns information on the user with the given id<br>
**Parameters:**
*  **user** ( Any[int(id), str(username)] ) - the user you wish to get information on
#### Activity(user)
Returns the activity of the user with the given id<br>
**A [roblosecurity](https://ro.py.jmk.gg/dev/roblosecurity/) is __optional__ within the Client’s parameters for this command to give extra information**<br>
**Parameters:**
*  **user** ( Any[int(id), str(username)] ) - the user you wish to get the activity of
#### Groups(user)
Returns the groups the user with the given id is in<br>
**Parameters:**
*  **user** ( Any[int(id), str(username)] ) - the user you wish to get the groups of
### class Group()
Used to interact with groups
#### Info(id)
Returns information on the group with the given id<br>
**Parameters:**
*  **id** ( int ) - id of the group you wish to get the information on
#### Roles(id)
Returns the roles of the group with the given id<br>
**Parameters:**
*  **id** ( int ) - id of the group you wish to get the roles of
#### Shout(groupid, shout)
Sets the shout of the group with the given id<br>
**A [roblosecurity](https://ro.py.jmk.gg/dev/roblosecurity/) is required within the Client’s parameters for this command to work**<br>
**Parameters:**
* **groupid** ( int ) - id of the group you wish to set the shout of
* **shout** ( str ) - what the shout should be set to
#### Accept(groupid)
Accepts the user with the given id into the group with the given id<br>
**A [roblosecurity](https://ro.py.jmk.gg/dev/roblosecurity/) is required within the Client’s parameters for this command to work**<br>
**Parameters:**
* **groupid** ( int ) - id of the group you wish to accept all users into
#### AcceptAll(groupid)
Accepts all pending requests into the group with the given id<br>
**A [roblosecurity](https://ro.py.jmk.gg/dev/roblosecurity/) is required within the Client’s parameters for this command to work**<br>
**Parameters:**
* **groupid** ( int ) - id of the group you wish to accept all requests for
#### DeclineAll(groupid)
Declines all pending requests into the group with the given id<br>
**A [roblosecurity](https://ro.py.jmk.gg/dev/roblosecurity/) is required within the Client’s parameters for this command to work**<br>
**Parameters:**
* **groupid** ( int ) - id of the group you wish to decline all requests for
#### Rank(groupid, userid, rank)
Rank the user with the given id into the group with the given id to the given rank<br>
**A [roblosecurity](https://ro.py.jmk.gg/dev/roblosecurity/) is required within the Client’s parameters for this command to work**<br>
**Parameters:**
* **groupid** ( int ) - id of the group you wish to rank the user in
* **user** ( Any[int(id), str(username)] ) - the user you wish to rank
* **rank** ( Any[int(Unique ID/Group ID (1-255)), str(rank name)] ) - the rank you wish to set the user to
#### Exile(groupid, userid)
Exiles the user with the given id from the group with the given id.
**A [roblosecurity](https://ro.py.jmk.gg/dev/roblosecurity/) is required within the Client’s parameters for this command to work**<br>
**Parameters:**
* **groupid** ( int ) - id of the group you wish to exile the user from
* **user** ( Any[int(id), str(username)] ) - the user you wish to exile from the group
## Examples
To get information on a user, the following code would be written;
```
roclient.User.Info(103956751) #Can use id or username
#Returns;
#{'name': 'Gytis5089', 'nick': 'Gytis', 'id': 103956751, 'creation': '2016-01-05T01:39:52.407Z', 'avatar': 'https://tr.rbxcdn.com/eda0a319e15547f339c4ff582982a770/720/720/Avatar/Png', 'friends': 17, 'followers': 290, 'following': 2}
```
Or, to get all of the roles within a group;
```
roclient.Group.Roles(5215428)
#Returns;
#{'Guest': {'id': 34713977, 'rank': 0, 'holders': 0}, 'Member': {'id': 34713976, 'rank': 1, 'holders': 0}, 'Admin': {'id': 34713975, 'rank': 254, 'holders': 0}, 'Chairman': {'id': 34713974, 'rank': 255, 'holders': 1}}
```
And ranking a user within a group;
```
roclient.Group.Rank(5215428, "Gytis5089", "Admin") #Can use id or username for user #And can use name, hierarchical id (1-255) & unique id for rank
#Returns;
#Ranked (or an error if you don't have a roblosecurity, whether it's invalid, or if the account doesn't have admin access to the group)
```
## Credits
### jmk
Creator of original roblox api wrapper/inspiration (ropy)
[Github](https://github.com/jmkd3v) [Twitter](https://twitter.com/jmkdev)