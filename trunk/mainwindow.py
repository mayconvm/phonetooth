import gtk
import gtk.glade

import contacts
import mobilephone
import contactsdialog
import preferencesdialog

class MainWindow:
    def __init__(self):
        self.__widgetTree           = gtk.glade.XML('phonetooth.glade')
        self.__mainWindow           = self.__widgetTree.get_widget('mainWindow')
        self.__recipientBox         = self.__widgetTree.get_widget('recipientBox')
        self.__inputField           = self.__widgetTree.get_widget('textView')
                
        self.__contactlistStore = gtk.ListStore(str, str)
        self.__recipientBox.set_model(self.__contactlistStore)
        
        cell = gtk.CellRendererText()
        self.__recipientBox.pack_start (cell, False)
        self.__recipientBox.add_attribute (cell, 'text', 1)
        
        contactList = contacts.ContactList()
        contactList.load()        
        
        self.__contactsDialog = contactsdialog.ContactsDialog(self.__widgetTree, self.__contactlistStore)
        self.__contactsDialog.updateStoreFromContactList(contactList)
        
        self.__preferencesDialog = preferencesdialog.PreferencesDialog(self.__widgetTree)
        
        self.__recipientBox.set_active(0)
        
        
        dic = {'onMainWindowDestroy'            : gtk.main_quit,
               'onManageContactsActivated'      : self.__contactsDialog.run,
               'onPreferencesActivated'         : self.__preferencesDialog.run,
               'onSendButtonClicked'            : self.__sendSMS}
               
        self.__widgetTree.signal_autoconnect(dic)
        self.__mainWindow.show()
        
    def __updateContactStore(self, widget = 0):
        self.__contactlistStore.clear()
        
        contactNames = self.__contactListBeingEdited.keys()
        contactNames.sort()
        
        for contactName in contactNames:
            self.__contactlistStore.append((contactName, self.__contactListBeingEdited[contactName]))

    def __sendSMS(self, widget):
        textBuffer = self.__inputField.get_buffer()
        listStore = self.__recipientBox.get_model()
        
        message = textBuffer.get_text(textBuffer.get_start_iter(), textBuffer.get_end_iter())
        phoneNr = listStore[self.__recipientBox.get_active()][1]
        
        phone = mobilephone.MobilePhone(mobilephone.BluetoothDevice("00:16:DB:67:D3:DA", 5, "Serial device"))
        phone.sendSMS(message, phoneNr)