from PySide2 import QtCore,QtGui,QtWidgets,QtUiTools

class MyWidget(QtWidgets.QWidget): 
    def __init__(self):
       super().__init__()
       self.login=QtUiTools.QUiLoader().load("login.ui")
       self.login.stackedWidget.setCurrentWidget(self.login.page_login)
      #  self.login.resize(500,260)
       self.login.pushButton_register.clicked.connect(self.onGoRegisterPage)
       self.login.pushButton_return.clicked.connect(self.onBackLoginPage)
       self.login.pushButton_submit.clicked.connect(self.onRegister)

       
    def  onGoRegisterPage(self):
       #点击登录界面上的注册按钮时跳转到注册界面
       self.login.stackedWidget.setCurrentWidget(self.login.page_register)
       pass
       
    def   onBackLoginPage(self):
       #点击返回按钮返回到登陆界面
       self.login.stackedWidget.setCurrentWidget(self.login.page_login)   
       pass
    
    def  onRegister(self):  
       name=self.login.lineEdit_name.text()
       pwd=self.login.lineEdit_pwd.text()
       pwd2=self.login.lineEdit_pwd.text()
       num=self.login.lineEdit_num.text()
       grade=self.login.lineEdit_class.text()
       tel=self.login.lineEdit_tel.text()
       print(name,pwd,pwd2,num,grade,tel) 
       if name == "":
           QtWidgets.QMessageBox.warning(self,"警告","用户名不能为空！")
           return
       pass
    

    

if __name__ =="__main__":
  app=QtWidgets.QApplication([])
  
  #实例化一个空白界面对象
  w=MyWidget()

  w.login.show()



  app.exec_()



  #c:\users\86155\appdata\local\programs\python\python39\lib\site-packages\pyside2\designer.exe