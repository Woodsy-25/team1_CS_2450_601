from tkinter import*
from tkinter import ttk


root = Tk()
# l = ttk.Label(root, text = "Starting...")
# l.grid()
# l.bind('<Enter>', lambda e:l.configure(text = 'Moved mouse inside'))
# l.bind('<Leave>', lambda e:l.configure(text = 'Moved mouse outside'))
# l.bind('<1>', lambda e:l.configure(text = 'Clicked left mouse button'))
# l.bind('<Double-1>',lambda e:l.configure(text = 'Double clicked'))
# l.bind('<B3-Motion>',lambda e:l.configure(text = 'right button drag to %d, %d'%(e.x,e.y)))

# content = ttk.Frame(root, padding = (3, 3, 23, 12))
# frame = ttk.Frame(content, borderwidth = 5, relief="sunken", width = 200, height = 100)
# namelbl = ttk.Label(content, text="Name")
# name=ttk.Entry(content)
#
# onevar = BooleanVar()
# twovar = BooleanVar()
# threevar = BooleanVar()
#
# onevar.set(True)
# twovar.set(False)
# threevar.set(True)
#
# one = ttk.Checkbutton(content, text = "One", variable = onevar, onvalue = True)
# two = ttk.Checkbutton(content, text = "Two", variable = twovar, onvalue = True)
# three = ttk.Checkbutton(content, text = "Three", variable = threevar, onvalue = True)
# ok = ttk.Button(content, text = "Okay")
# cancel = ttk.Button(content, text = "Cancel")
#
# content.grid(column = 0, row = 0, sticky = (N, S, E, W))
# frame.grid(column = 0, row = 0, columnspan = 3, rowspan = 2, sticky = (N, S, E, W))
# namelbl.grid(column = 3, row = 0, columnspan = 2, sticky = (N, W), padx = 5)
# name.grid(column = 3, row = 1, columnspan = 2, sticky = (N, E, W), padx = 5)
# one.grid(column = 0, row = 3)
# two.grid(column = 1, row = 3)
# three.grid(column = 2, row = 3)
# ok.grid(column = 3, row = 3)
# cancel.grid(column = 4, row = 3)
#
# root.columnconfigure(0, weight = 1)
# root.rowconfigure(0, weight = 1)
# content.columnconfigure(0, weight = 3)
# content.columnconfigure(1, weight = 3)
# content.columnconfigure(2, weight = 3)
# content.columnconfigure(3, weight = 3)
# content.columnconfigure(4, weight = 3)
# root.rowconfigure(1, weight = 1)
#
# content.grid_slaves()
# for w in content.grid_slaves():print(w)

#Initialize country database list
#    the list of country codes
#     a parallet list of country names in the same order
#     a hash table mapping country code to population

countrycodes = ('ar', 'au', 'be', 'br', 'ca', 'cn', 'dk', 'fi', 'fr', 'gr', 'in', 'it', 'jp', 'mx', \
'nl', 'no', 'es', 'se', 'ch')
countrynames = ('Argentena', 'Australia', 'Belgium', 'Brazil', 'Canada', 'China', 'Denmark',\
'Finland', 'France', 'Greece', 'India', 'Italy', 'Japan', 'Mexico', 'Netherlands', 'Norway', \
'Spain', 'Sweden', 'Switzerland')
cnames = StringVar(value = countrynames)
populations = {'ar':41000000, 'au':21179211, 'be':10584534, 'br':185971537, \
'ca':33148682, 'cn':1323128240, 'dk':5457415, 'fi':5302000, 'fr':64102140, 'gr':11147000, \
'in':1131043000, 'it':59206382, 'jp':127718000, 'mx':106535000, 'nl':16402414, \
'no':4738085, 'es':45116894, 'se':9174082, 'ch':7508700}
#
gifts = {'card':'Greeting card', 'flowers':'Flowers','nastygram':'Nastygram'}
#
gift = StringVar()
sentmsg = StringVar()
statusmsg = StringVar()

# Called when the user double clicks an item in the listbox, presses
# which county is currently selected, an then lookup its country
# code, and form that, its population. Update the status message
# with the new population. As well, clear the mssaged about the
# gift being sent, so it doesn't stick around after we start doing
# other things.

def showPopulation(*args):
    idxs = lbox.curselection()
    if len(idxs) == 1:
        idx = int(idxs[0])
        code = countrycodes[idx]
        name = countrynames[idx]
        popn = populations[code]
        statusmsg.set("The population of %s (%s) is %d" %(name, code, popn))
    sentmsg.set('')

# Called when the user double clicks an item in the listbox, presses
# the "send Gift" button, or presses the Return key. In case the selected
# item is scrolled out of view, make sure it is visible.
# #
# Figure out which country is selected, which gift is selected with the
# radiobuttons, "send the give", and provide feedback that is was sent.

def sendGift(*args):
    idxs = lbox.curselection()
    if len(idxs) == 1:
        idx = int(idxs[0])
        lbox.see(idx)
        name = countrynames[idx]
        #Gift sending left as an exercise to the reader
        sentmsg.set("Sent %s to leader of %s" %(gifts[gift.get()], name))

#Create and grid the outer content frame
c=ttk.Frame(root, padding = (5, 5, 12, 0))
c.grid(column = 0, row = 0, sticky = (N, W, E, S))
root.grid_columnconfigure(0, weight = 1)
root.grid_rowconfigure(0, weight = 1)
#
#Create the different widgets; note the variables that many
# of them are found to, as well as the button callback.
# Note we're using the StringVar() 'cname', constructed from 'countrynames'
#
lbox = Listbox(c, listvariable = cnames, height = 5)
lbl = ttk.Label(c, text = "Send to country's leader:")
g1 = ttk.Radiobutton(c, text = gifts['card'], variable = gift, value = 'card')
g2 = ttk.Radiobutton(c, text = gifts['flowers'], variable = gift, value = 'flowers')
g3 = ttk.Radiobutton(c, text = gifts['nastygram'], variable = gift, value = 'nastygram')
send = ttk.Button(c, text = 'Send gift', command = sendGift, default = 'active')
#
sentlbl = ttk.Label(c, textvariable = sentmsg, anchor = 'center')
status = ttk.Label(c, textvariable = statusmsg, anchor = W)
#
#Grid all the widgets
lbox.grid(column = 0, row = 0, rowspan = 6, sticky = (N, S, E, W))
lbl.grid(column = 1, row = 0, padx = 10, pady = 5)
g1.grid(column = 1, row = 1, sticky = W, padx = 20)
g2.grid(column = 1, row = 2, sticky = W, padx = 20)
g3.grid(column = 1, row = 3, sticky = W, padx = 20)
send.grid(column = 2, row = 4, sticky = E)
sentlbl.grid(column=1, row = 5, columnspan = 2, sticky = N, pady = 5, padx = 5)
status.grid(column=0, row = 6, columnspan = 2, sticky = (W, E))
c.grid_columnconfigure(0, weight = 1)
c.grid_rowconfigure(5, weight = 1)
#
#Set even bindings for when the selection in the listbox changes,
#when the user double clicks the list, and when they hit the return key
lbox.bind('<<ListboxSelect>>', showPopulation)
lbox.bind('<Double-1>', sendGift)
lbox.bind('<Return>', sendGift)
#
#Colorize alternating lines of the listbox
for i in range(0, len(countrynames), 2):
    lbox.itemconfigure(i, background = '#f0f0ff')
#
#Set thestarting state of the interface, including selecting the
# default givt to send, and clearing the messages. Select the first
# country in the list; because the <<ListboxSelect>> event is only
# generated when the user makes a change, we explicityly call showPopulation.
#
gift.set('card')
sentmsg.set('')
statusmsg.set('')
lbox.selection_set(0)
showPopulation()
#
root.mainloop()
