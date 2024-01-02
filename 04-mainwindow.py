from PySide2 import QtCore,QtGui,QtWidgets,QtUiTools,QtMultimedia
from PySide2.QtCore import QUrl
import sqlite3

class MyWidget(QtWidgets.QWidget): 
    def __init__(self):
       super().__init__()
       #初始化数据库
       self.initDatabase()
       self.Playmusic()
       self.login=QtUiTools.QUiLoader().load("login.ui")
       self.login.stackedWidget.setCurrentWidget(self.login.page_login)
       #self.login.resize(500,260)
       self.login.pushButton_register.clicked.connect(self.onGoRegisterPage)
       self.login.pushButton_register_return.clicked.connect(self.onBackLoginPage)
       #登录
       self.login.pushButton_register_submit.clicked.connect(self.onRegister)  
       self.login.pushButton_login_submit.clicked.connect(self.onLogin) 


    def initDatabase(self):
         self.con= sqlite3.connect("book.db")    
         self.cursor=self.con.cursor()
         self.cursor.execute("create table if not exists t_user(id char(13) primary key,name varchar(15),passwd varchar(15),phone char(11),role varchar(15));")
    
    def doRegister(self,id,pwd,name,phone):
      #注册功能实现
      sql=f"insert into t_user values('{id}','{name}','{pwd}','{phone}','普通用户');"
      try:
         self.cursor.execute(sql)
         self.con.commit()
      except sqlite3.Error as e:
          print("insert error",e)
      # if self.cursor.rowcount==1:
          return False 
      return True
   
    def doLogin(self,id,pwd):
      #登录功能实现
      sql=f"select id,passwd from t_user where id='{id}' and passwd='{pwd}';"
      try:
         self.cursor.execute(sql)
         self.con.commit()
      except sqlite3.Error as e:
          print("insert error",e)
      # if self.cursor.rowcount==1:
          return False 
      return True

    #播放音乐
    def Playmusic(self):
         self.player = QtMultimedia.QMediaPlayer()
         self.player.setMedia(QtMultimedia.QMediaContent(QUrl.fromLocalFile("岑宁儿 - 追光者.mp3")))
         self.player.play()
    def  onGoRegisterPage(self):
       #点击登录界面上的注册按钮时跳转到注册界面
       self.login.stackedWidget.setCurrentWidget(self.login.page_register)
       pass
       
    def   onBackLoginPage(self):
       #点击返回按钮返回到登陆界面
       self.login.stackedWidget.setCurrentWidget(self.login.page_login)   
       pass
    
    def  onRegister(self):  
       id=self.login.lineEdit_id.text()
       pwd=self.login.lineEdit_pwd.text()
       pwd2=self.login.lineEdit_pwd2.text()
       num=self.login.lineEdit_num.text()
       name=self.login.lineEdit_name.text()
       phone=self.login.lineEdit_phone.text()
      #  print(name,pwd,pwd2,num,grade,tel) 
       if name == "" or pwd =="" or pwd2 =="" or num =="" or id =="" or phone =="" :
           QtWidgets.QMessageBox.warning(self,"警告","用户名不能为空！")
           return
       if pwd !=pwd2 :
          QtWidgets.QMessageBox.warning(self,"警告","两次密码不一致！")
          return
       if self.doRegister(id,pwd,name,phone):
           QtWidgets.QMessageBox.information(self,"提示","注册成功！")
       else:
           QtWidgets.QMessageBox.critical(self,"错误","注册失败！")

    def onLogin(self):
        id=self.login.lineEdit_id.text()
        pwd=self.login.lineEdit_pwd.text()
        if id==" " or pwd=="":
            QtWidgets.QMessageBox.warning(self,"警告","登录信息不能为空！")
        if not self.doLogin(id,pwd):
            QtWidgets.QMessageBox.critical(self,"错误","登录失败！")
        else:
            # QtWidgets.QMessageBox.information(self,"提示","登录成功！")
            #加载主界面
            self.mainwindow=QtUiTools.QUiLoader().load("mainwindow.ui")
            self.mainwindow.toolButton_user.clicked.connect(self.onGoUserPage)
            self.mainwindow.toolButton_book.clicked.connect(self.onGoBookPage)
            self.mainwindow.toolButton_borrow.clicked.connect(self.onGoBorrowPage)
            self.mainwindow.show()
            #关闭登录界面
            self.login.close()

    def onGoUserPage(self):
            self.mainwindow.stackedWidget.setCurrentWidget(self.mainwindow.page_user)

    def onGoBookPage(self):
            self.mainwindow.stackedWidget.setCurrentWidget(self.mainwindow.page_book)
    def onGoBorrowPage(self):
            self.mainwindow.stackedWidget.setCurrentWidget(self.mainwindow.page_borrow)
  
if __name__ =="__main__":
  app=QtWidgets.QApplication([])
  
  #实例化一个空白界面对象
  w=MyWidget()
  w.login.show()
  app.exec_()



  #c:\users\86155\appdata\local\programs\python\python39\lib\site-packages\pyside2\designer.exe