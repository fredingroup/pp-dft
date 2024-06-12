import window as pyfl

# Staring Functions for Execution
dinput = ['LastName','Country','Age']
# Call the UI and get the inputs
dialog = pyfl.Dialog(dinput)
if dialog.exec_() == pyfl.Dialog.Accepted:
    name, item, value = dialog.get_output()
    print(name, item, value)