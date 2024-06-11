import sys
import os

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *


class StateTreeItem(QTreeWidgetItem):
    # def __init__(self, parent, column, file='',geom='',state=0,spin=0):
    #     super(parent,column)

    #     self.state = State(filename=file,geom=geom,state=state,spin=spin)

    #     self.setText(self.state.getText())

    def __init__(self, parent, column, state):
        super().__init__(parent,column)
        self.state = state
        self.setText(0,self.state.getText())

class StateListItem(QListWidgetItem):
    # def __init__(self,parent, file='',geom='',state=0,spin=0):
    #     super(parent)

    #     self.file = file
    #     self.geom = geom
    #     self.state = state
    #     self.spin = spin

    #     self.setText(self.state.getText())

    def __init__(self, parent, state):
        super().__init__(parent)
        self.state = state
        self.setText(self.state.getText())

class myQTableWidgetItem(QTableWidgetItem):
    def __init__(self,text,pathname=''):
        super().__init__(text)
        self.path=pathname


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow,self).__init__()
        self.resize(700, 500)
        # page setup
        self.mainLayout = QVBoxLayout()
        self.centralWidget = QWidget()
        self.centralWidget.setLayout(self.mainLayout)

        

        self.startDir = os.getcwd()
        self.nfiles = 0 



        self.setup_tabs()

        self.go_button=QPushButton(self.centralWidget)
        self.go_button.setText("Go!")
        self.mainLayout.addWidget(self.go_button)

        self.setup_listeners()


        self.setCentralWidget(self.centralWidget)
        self._output = {}

    def setup_tabs(self):
        # tab setup
        self.tabwidget = QTabWidget(self.centralWidget)
        self.tabwidget.setObjectName(u"tabwidget")
        self.tabwidget.setTabPosition(QTabWidget.North)
        self.tabwidget.setDocumentMode(False)
        self.tabwidget.setTabsClosable(False)
        self.tabwidget.setMovable(False)
        
        self.setup_tab_1()
        self.setup_tab_2()
        self.setup_tab_3()

        self.tabwidget.setTabText(0,"File Selection")
        self.tabwidget.setTabText(1,"State Ordering")
        self.tabwidget.setTabText(2,"Parameters")
        
        self.mainLayout.addWidget(self.tabwidget)
        self.tabwidget.setCurrentIndex(0)

    def setup_tab_1(self):
        # tab 1 - File Selection
        self.tab_1 = QWidget()
        
        self.tab_1_layout = QGridLayout(self.tab_1)
        self.select_files_button = QPushButton(self.tab_1)
        self.select_files_button.setText("Select Files")


        self.tab_1_layout.addWidget(self.select_files_button, 0, 0, 1, 1)

        self.files_table_widget = QTableWidget(self.tab_1)
        cols = ['File','Geom','Nstates','Spin','']
        self.files_table_widget.setColumnCount(len(cols))
        self.files_table_widget.setHorizontalHeaderLabels(cols)
        # for i,col in eenumerate(cols):
        #     self.files_table_widget.setHorizontalHeaderItem(i, QTableWidgetItem())
        #     self.files_table_widget.setHorizontalHeaderItem(i, QTableWidgetItem())

        self.tab_1_layout.addWidget(self.files_table_widget, 1, 0, 1, 1)

        self.tabwidget.addTab(self.tab_1, "")

    def setup_tab_2(self):
        # tab 2 - State ordering
        self.tab_2 = QWidget()
        self.tab_2_layout = QGridLayout(self.tab_2)
        self.add_mixed_state_button = QPushButton(self.tab_2)
        self.add_mixed_state_button.setText("Add States")

        self.tab_2_layout.addWidget(self.add_mixed_state_button, 1, 1, 1, 1)

        self.states_list_widget = QListWidget(self.tab_2)

        # how to add an item to the list
        # QListWidgetItem(self.states_list_widget)

        self.states_list_widget.setMouseTracking(True)
        self.states_list_widget.setAcceptDrops(False)
        self.states_list_widget.setDragEnabled(True)
        self.states_list_widget.setDragDropMode(QAbstractItemView.InternalMove)

        self.tab_2_layout.addWidget(self.states_list_widget, 0, 0, 2, 1)

        
        self.state_tree = QTreeWidget(self.tab_2)
        self.state_tree.setColumnCount(2)
        self.state_tree.setHeaderLabels(["State","Checkbox"])
        self.tab_2_layout.addWidget(self.state_tree, 0, 1, 1, 1)

        self.tabwidget.addTab(self.tab_2, "")

    def setup_tab_3(self):
        # tab 3 - plot parameters
        self.tab_3 = QWidget()
        self.gridLayout = QGridLayout(self.tab_3)
        self.gridLayout.setContentsMargins(10, 3, 0, 0)


        self.parameters_label = QLabel(self.tab_3)
        self.parameters_label.setText("Graph Parameters")
        self.gridLayout.addWidget(self.parameters_label,0,0,1,1)



        self.graph_title_prompt = QLabel(self.tab_3)
        self.graph_title_prompt.setText("Graph Title")

        self.gridLayout.addWidget(self.graph_title_prompt, 1, 0, 1, 1)

        self.title_input = QLineEdit(self.tab_3)
        self.title_input.setObjectName(u"title_input")

        self.gridLayout.addWidget(self.title_input, 1, 1, 1, 2)
        self.peak_width_prompt = QLabel(self.tab_3)
        self.peak_width_prompt.setText(u"Peak Width")

        self.gridLayout.addWidget(self.peak_width_prompt,2, 0, 1, 1)

        self.sigma_spin_box = QDoubleSpinBox(self.tab_3)
        self.sigma_spin_box.setObjectName(u"sigma_spin_box")
        self.sigma_spin_box.setMaximum(1.000000000000000)
        self.sigma_spin_box.setSingleStep(0.010000000000000)
        self.sigma_spin_box.setValue(0.400000000000000)

        self.gridLayout.addWidget(self.sigma_spin_box, 2, 1, 1, 1)

        self.region_prompt = QLabel(self.tab_3)
        self.region_prompt.setText("Region")

        self.gridLayout.addWidget(self.region_prompt, 3, 0, 4, 1)
        self.range_button_group = QButtonGroup()
        buttons = [QRadioButton('UV-Vis'),
                  QRadioButton("IR"),
                  QRadioButton("Large"),
                  QRadioButton("Custom")]
        
        for i, button in enumerate(buttons):
            self.gridLayout.addWidget(button,i+3,1,1,1)
            self.range_button_group.addButton(button,i)
        buttons[0].setChecked(True)

        self.custom_start_wavelength = QLineEdit(self.tab_3)
        self.custom_start_wavelength.setPlaceholderText("start")
        self.custom_start_wavelength.setEnabled(False)
        self.custom_start_wavelength.setEchoMode(QLineEdit.Normal)

        self.gridLayout.addWidget(self.custom_start_wavelength,6,2,1,1)

        self.dash_label = QLabel(self.tab_3)
        self.dash_label.setText("-")
        self.gridLayout.addWidget(self.dash_label,6,3,1,1)

        self.custom_end_wavelength = QLineEdit(self.tab_3)
        self.custom_end_wavelength.setPlaceholderText(u"end")
        self.custom_end_wavelength.setEnabled(False)
        self.gridLayout.addWidget(self.custom_end_wavelength,6,4,1,1)

        self.nm_label = QLabel(self.tab_3)
        self.nm_label.setText("nm")
        self.gridLayout.addWidget(self.nm_label,6,5,1,1)

        self.custom_radio = buttons[-1]
        self.custom_radio.toggled.connect(self.custom_start_wavelength.setEnabled)
        self.custom_radio.toggled.connect(self.custom_end_wavelength.setEnabled)



        self.plots_prompt = QLabel(self.tab_3)
        self.plots_prompt.setText(u"Plots")

        self.gridLayout.addWidget(self.plots_prompt, 7, 0, 3, 1)


        self.absorbance_checkbox = QCheckBox(self.tab_3)
        self.absorbance_checkbox.setText("Absorbance")
        self.gridLayout.addWidget(self.absorbance_checkbox,7,1,1,1)
        self.absorbance_checkbox.setChecked(True)

        self.DADS_checkbox = QCheckBox(self.tab_3)
        self.DADS_checkbox.setText("DADS")
        self.gridLayout.addWidget(self.DADS_checkbox,8,1,1,1)
        self.DADS_checkbox.setChecked(True)

        self.Jablonski_checkbox = QCheckBox(self.tab_3)
        self.Jablonski_checkbox.setText("Jablonski")
        self.gridLayout.addWidget(self.Jablonski_checkbox,9,1,1,1)
        self.Jablonski_checkbox.setEnabled(False) # I'll enable it when it does something


        self.tabwidget.addTab(self.tab_3, "")

    def setup_listeners(self):
        self.select_files_button.clicked.connect(self.addFile)
        self.add_mixed_state_button.clicked.connect(self.addState)

        self.tabwidget.currentChanged.connect(self.onTabChanged)

        self.go_button.clicked.connect(self.go)

    def addFile(self):
        file = QFileDialog.getOpenFileName(self.select_files_button,"file", self.startDir)
        # file = ('C:\\Users\\gabri\\LU Student Dropbox\\Gabe Masso\\Fredin Group\\Gabe\\pump_probe_TDDFT\\computational\\solution_phase\\bodipy\\s0\\td_s\\bodipy_td_transitions.txt','')
        if file != ('',''):
            filename = os.path.basename(file[0])
            self.startDir = os.path.dirname(file[0])
            # Add to files table
            # print(file)
            self.files_table_widget.insertRow(self.nfiles)
        
            file_item = myQTableWidgetItem(filename,file[0])
            self.files_table_widget.setItem(self.nfiles,0,file_item)

            geom_name = QLineEdit()
            geom_name.setText('')
            self.files_table_widget.setCellWidget(self.nfiles,1,geom_name)

            nstates_box = QSpinBox()
            nstates_box.setValue(30)
            self.files_table_widget.setCellWidget(self.nfiles,2,nstates_box)
            
            spin_box = QSpinBox()
            spin_box.setValue(1)
            self.files_table_widget.setCellWidget(self.nfiles,3,spin_box)

            delbut = QPushButton()
            delbut.setText('X')
            self.files_table_widget.setCellWidget(self.nfiles,4,delbut)
            delbut.clicked.connect(self.row_deleter(file_item))

            self.nfiles += 1

    def row_deleter(self, item):
        def delete_file():
            self.files_table_widget.removeRow(self.files_table_widget.row(item))
            self.nfiles -= 1

        return delete_file

    def onTabChanged(self,index):
        if index == 1:
            # print("HI: ", index)
            self.update_state_tree()

    def update_state_tree(self):
        self.state_tree.clear()

        for i in range(self.nfiles):
            file_widget = QTreeWidgetItem(self.state_tree,0)

            filename = self.files_table_widget.itemAt(i,0).text()
            geomName = self.files_table_widget.cellWidget(i,1).text()
            if geomName =='':
                file_widget.setText(0,filename)
            else:
                file_widget.setText(0,geomName)

            self.state_tree.addTopLevelItem(file_widget)

            spin = self.files_table_widget.cellWidget(i,3).value()

            for j in range(self.files_table_widget.cellWidget(i,2).value()+1):
                # QTreeWidgetItem(file_widget,f"{j}")
                pathname=self.files_table_widget.itemAt(i,0).path
                item=StateTreeItem(file_widget,0,State(filename=filename,path=pathname,geom=geomName,state=j,spin=spin))
                self.state_tree.setItemWidget(item,1,QCheckBox())

    def addState(self):
        root = self.state_tree.invisibleRootItem()

        for i in range(root.childCount()):
            file_item = root.child(i)
            for j in range (file_item.childCount()):
                state_item = file_item.child(j)
                if self.state_tree.itemWidget(state_item,1).isChecked():
                    print(state_item.text(0))
                    StateListItem(self.states_list_widget,state=state_item.state)
                        # file=file_item.text(0)
                        # geom=state_item.text(0)

    def go(self):
        if self.states_list_widget.count() == 0:
            print("No states selected. Exiting...")
            sys.exit(1)
            
        self._output={
            'title':self.title_input.text(),
            'peak_width':self.sigma_spin_box.value(),
            'plots': {
                'absorbance': self.absorbance_checkbox.isChecked(),
                'dads': self.DADS_checkbox.isChecked(),
                'jablonski': self.Jablonski_checkbox.isChecked()
            },
            'states': []
        }
        if self.custom_radio.isChecked():
            try:
                self._output['region'] = range(int(self.custom_start_wavelength.text()),
                                              int(self.custom_end_wavelength.text()),
                                              1)
            except:
                print("Invalid custom range: using Large range")
                self._output['region'] = 'LARGE'
        else:
            self._output['region']=self.range_button_group.checkedButton().text().upper().replace('-','')
        



        for i in range(self.states_list_widget.count()):
            self._output['states'].append(self.states_list_widget.item(i).state)
        self.close()

    def get_output(self):
        # print(self._output)
        return self._output


def main():
    app = QtWidgets.QApplication(sys.argv)
    ui = MainWindow()
 
    ui.show()
    app.exec_()
    return ui.get_output()

if __name__ == "__main__":
    from state import State
    main()
else:
    from library.state import State
