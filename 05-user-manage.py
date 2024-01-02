from PySide2 import QtCore,QtGui,QtWidgets,QtUiTools,QtMultimedia
from PySide2.QtCore import QUrl
import sqlite3

class MyWidget(QtWidgets.QWidget): 
    def __init__(self):
       super().__init__()
       #初始化数据库
       self.initDatabase()
    #    self.Playmusic()
       self.login=QtUiTools.QUiLoader().load("login.ui")
       self.login.stackedWidget.setCurrentWidget(self.login.page_login)
       #self.login.resize(500,260)
       self.login.pushButton_register.clicked.connect(self.onGoRegisterPage)
       self.login.pushButton_register_return.clicked.connect(self.onBackLoginPage)
       #登录
       self.login.pushButton_register_submit.clicked.connect(self.onRegister)  
       self.login.pushButton_login_submit.clicked.connect(self.onLogin) 


    #初始化数据库
    def initDatabase(self):
         self.con= sqlite3.connect("book.db")    
         self.cursor=self.con.cursor()
         self.cursor.execute("create table if not exists t_user(id char(13) primary key,name varchar(15),passwd varchar(15),phone char(11),role varchar(15));")
         self.cursor.execute("create table if not exists t_book (isbn varchar(13) primary key, title varchar(100), author varchar(60), publisher varchar(100), publishdate varchar(10), number int);")
         self.cursor.execute("CREATE TABLE if not exists t_borrow (user_id varchar(13), book_isbn varchar(13), borrow_date char(10), return_date char(10), PRIMARY KEY(user_id, book_isbn), FOREIGN KEY(user_id) REFERENCES t_user(id), FOREIGN KEY(book_isbn) REFERENCES t_book(isbn));")

    def doRegister(self,id,pwd,name,phone):
      #注册功能实现
      sql=f"insert into t_user values('{id}','{name}','{pwd}','{phone}','普通用户');"
      try:
         self.cursor.execute(sql)
         self.con.commit()
      except sqlite3.Error as e:
          print("insert error",e)
          return False 
      return True
   
    def doLogin(self,id,pwd):
      #登录功能实现
      sql=f"select id,name,role from t_user where id='{id}' and passwd='{pwd}';"
      self.cursor.execute(sql)
      record=self.cursor.fetchone()
      if record is None:
          return False 
      self.login_user_id=record[0]
      self.login_user_name=record[1]
      self.login_user_role=record[2]
      print(self.login_user_id,self.login_user_name,self.login_user_role)
      return True   

    #播放音乐
    # def Playmusic(self):
    #      self.player = QtMultimedia.QMediaPlayer()
    #      self.player.setMedia(QtMultimedia.QMediaContent(QUrl.fromLocalFile("岑宁儿 - 追光者.mp3")))
    #      self.player.play()

    #点击登录界面上的注册按钮时跳转到注册界面     
    def onGoRegisterPage(self):
       self.login.stackedWidget.setCurrentWidget(self.login.page_register)
       pass
       
    #点击返回按钮返回到登陆界面
    def onBackLoginPage(self):
       self.login.stackedWidget.setCurrentWidget(self.login.page_login)   
       pass
    
    #判断注册
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
   
    #判断登录
    def onLogin(self):
        id=self.login.lineEdit_login_id.text()
        pwd=self.login.lineEdit_login_pwd.text()
        print(id, pwd)
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

            self.mainwindow.pushButton_query_user.clicked.connect(self.onQueryUser)
            self.mainwindow.pushButton_delete_user.clicked.connect(self.onDeleteUser)
            self.mainwindow.pushButton_update_user.clicked.connect(self.onUpdateUser)
            # self.mainwindow.pushButton_modify_user.clicked.connect(self.onModifyUser)

            self.mainwindow.pushButton_query_book.clicked.connect(self.onQueryBook)
            self.mainwindow.pushButton_delete_book.clicked.connect(self.onDeleteBook)
            self.mainwindow.pushButton_update_book.clicked.connect(self.onUpdateBook)
            self.mainwindow.pushButton_add_book.clicked.connect(self.onAddBook) 
            self.mainwindow.pushButton_borrow_book.clicked.connect(self.onBorrowBook)   

            self.mainwindow.pushButton_query_borrow.clicked.connect(self.onQueryBorrow)
            self.mainwindow.pushButton_return_borrow.clicked.connect(self.onReturnBorrow)

            #显示主界面
            if(self.login_user_role == "普通用户"):
                self.mainwindow.lineEdit_user.hide()
                self.mainwindow.pushButton_query_user.hide()
                self.mainwindow.pushButton_delete_user.hide()
                self.mainwindow.pushButton_update_user.hide()
            self.mainwindow.show()
            #关闭登录界面
            self.login.close()

    #跳转到user界面
    def onGoUserPage(self):
            self.mainwindow.stackedWidget.setCurrentWidget(self.mainwindow.page_user)
    #跳转到book界面
    def onGoBookPage(self):
            self.mainwindow.stackedWidget.setCurrentWidget(self.mainwindow.page_book)
    #跳转到borrow界面        
    def onGoBorrowPage(self):
            self.mainwindow.stackedWidget.setCurrentWidget(self.mainwindow.page_borrow)
    #查询功能
    def onQueryUser(self):
        condition = self.mainwindow.lineEdit_user.text()
        sql = f"select id, name, passwd, phone, role from t_user where id like '%{condition}%'"
        self.cursor.execute(sql)
        model = QtGui.QStandardItemModel()
        model.setHorizontalHeaderLabels(['学号', '姓名', '密码', '手机', '身份'])
        result_set = self.cursor.fetchall()
        for i in range(len(result_set)):
            for j in range(5):
                item = QtGui.QStandardItem(result_set[i][j])
                item.setTextAlignment(QtCore.Qt.AlignCenter)
                model.setItem(i, j, item)
        self.mainwindow.tableView_user.setModel(model)
    #删除功能 
    def onDeleteUser(self):
        row=self.mainwindow.tableView_user.currentIndex().row()
        if row == -1:
          return
        model=self.mainwindow.tableView_user.model()
        id=model.item(row,0).text()
        print(row,id)
        r=QtWidgets.QMessageBox.question(self,"删除",f"是否要删除{id}这条记录?")
        print(r)
        if r is QtWidgets.QMessageBox.StandardButton.No:
            return
        sql= f"delete from t_user where id='{id}';"
        self.cursor.execute(sql)
        self.con.commit()
        if self.cursor.rowcount ==1:
            QtWidgets.QMessageBox.information(self,"提示","删除成功！")
    #修改密码功能
    # def onModifyUser(self):    
    #     # 获取数据
    #     model=self.mainwindow.login_user.model()
    #     #加载界面
    #     self.updateuser=QtUiTools.QUiLoader().load("modifyuser.ui")
    #     self.updateuser.pushButton_submit.clicked.connect(self.onSubmitUpdateuser)
        
    #修改功能    
    def onUpdateUser(self):
        row=self.mainwindow.tableView_user.currentIndex().row()
        if row == -1:
          return
        model=self.mainwindow.tableView_user.model()
        id=model.item(row,0).text()
        name=model.item(row,1).text()
        pwd=model.item(row,2).text()
        phone=model.item(row,3).text()
        role=model.item(row,4).text()
        #加载界面
        self.updateuser=QtUiTools.QUiLoader().load("updateuser.ui")
        self.updateuser.pushButton_submit.clicked.connect(self.onSubmitModifyeuser)
        #修改信息
        self.updateuser.lineEdit_id.setText(id)
        self.updateuser.lineEdit_name.setText(name)
        self.updateuser.lineEdit_pwd.setText(pwd)
        self.updateuser.lineEdit_phone.setText(phone)
        self.updateuser.comboBox_role.setCurrentText(role)
        #显示界面
        self.updateuser.show()

    #提交修改信息
    def onSubmitUpdateuser(self):
        #获取数据
        id=self.updateuser.lineEdit_id.text()
        name=self.updateuser.lineEdit_name.text()
        pwd=self.updateuser.lineEdit_pwd.text()
        phone=self.updateuser.lineEdit_phone.text()
        role=self.updateuser.comboBox_role.currentText()
        sql = f"update t_user set name='{name}', passwd='{pwd}', phone='{phone}', role='{role}' where id='{id}';"
        #执行sql
        self.cursor.execute(sql)
        self.con.commit()
        if self.cursor.rowcount ==1:
            QtWidgets.QMessageBox.information(self,"提示","修改成功！")
        else:
            QtWidgets.QMessageBox.critical(self,"错误","修改失败！")
    # def onSubmitModifyUser(self):
    #       #获取数据
    #     id=self.updateuser.lineEdit_id.text()
    #     name=self.updateuser.lineEdit_name.text()
    #     pwd=self.updateuser.lineEdit_pwd.text()
    #     phone=self.updateuser.lineEdit_phone.text()
    #     role=self.updateuser.comboBox_role.currentText()
    #     sql = f"update t_user set name='{name}', passwd='{pwd}', phone='{phone}', role='{role}' where id='{id}';"
    #     #执行sql
    #     self.cursor.execute(sql)
    #     self.con.commit()
    #     if self.cursor.rowcount ==1:
    #         QtWidgets.QMessageBox.information(self,"提示","修改成功！")
    #     else:
    #         QtWidgets.QMessageBox.critical(self,"错误","修改失败！")

    def onQueryBook(self):
        condition = self.mainwindow.lineEdit_book.text()
        sql = f"select isbn,title, author, publisher, publishdate,number from t_book where title like '%{condition}%'"
        self.cursor.execute(sql)
        model = QtGui.QStandardItemModel()
        model.setHorizontalHeaderLabels(['书号', '姓名', '作者', '出版社', '出版时间','数量'])
        result_set = self.cursor.fetchall()
        for i in range(len(result_set)):
            for j in range(6):
                item = QtGui.QStandardItem(str(result_set[i][j]))
                item.setTextAlignment(QtCore.Qt.AlignCenter)
                model.setItem(i, j, item)
        self.mainwindow.tableView_book.setModel(model)     
    def onDeleteBook(self):
        row=self.mainwindow.tableView_book.currentIndex().row()
        if row == -1:
          return
        model=self.mainwindow.tableView_book.model()
        isbn=model.item(row,0).text()
        print(row,isbn)
        r=QtWidgets.QMessageBox.question(self,"删除",f"是否要删除{isbn}这条记录?")
        print(r)
        if r is QtWidgets.QMessageBox.StandardButton.No:
            return
        sql= f"delete from t_book where isbn='{isbn}';"
        self.cursor.execute(sql)
        self.con.commit()
        if self.cursor.rowcount ==1:
            QtWidgets.QMessageBox.information(self,"提示","删除成功！")
    def onUpdateBook(self):
        row=self.mainwindow.tableView_book.currentIndex().row()
        if row == -1:
          return
        model=self.mainwindow.tableView_book.model()
        isbn=model.item(row,0).text()
        title=model.item(row,1).text()
        author=model.item(row,2).text()
        publish=model.item(row,3).text()
        publishdate=model.item(row,4).text()
        number=model.item(row,5).text()
        #加载界面
        self.updatebook=QtUiTools.QUiLoader().load("updatebook.ui")
        self.updatebook.pushButton_submit.clicked.connect(self.onSubmitUpdatebook)
        #修改信息
        self.updatebook.lineEdit_isbn.setText(isbn)
        self.updatebook.lineEdit_title.setText(title)
        self.updatebook.lineEdit_author.setText(author)
        self.updatebook.lineEdit_pub.setText(publish)
        self.updatebook.lineEdit_pubdate.setText(publishdate)
        self.updatebook.lineEdit_number.setText(number)
        #显示界面
        self.updatebook.show()
    def onSubmitUpdatebook(self):
        isbn=self.updatebook.lineEdit_isbn.text()
        title=self.updatebook.lineEdit_title.text()
        author=self.updatebook.lineEdit_author.text()
        publish=self.updatebook.lineEdit_pub.text()
        publishdate=self.updatebook.lineEdit_pubdate.text()
        number=self.updatebook.lineEdit_number.text()
        sql = f"update t_book set title='{title}', author='{author}', publisher='{publish}',publishdate='{publishdate}',number='{number}' where isbn='{isbn}';"
        #执行sql
        self.cursor.execute(sql)
        self.con.commit()
        if self.cursor.rowcount ==1:
            QtWidgets.QMessageBox.information(self,"提示","修改成功！")
        else:
            QtWidgets.QMessageBox.critical(self,"错误","修改失败！")
    def onAddBook(self):
        # 加载添加新书的界面
        self.addbook = QtUiTools.QUiLoader().load("addbook.ui")
        self.addbook.pushButton_submit.clicked.connect(self.onSubmitAddBook)
        # 显示界面
        self.addbook.show()
    def onSubmitAddBook(self):
        isbn = self.addbook.lineEdit_isbn.text()
        title = self.addbook.lineEdit_title.text()
        author = self.addbook.lineEdit_author.text()
        publish = self.addbook.lineEdit_pub.text()
        publishdate = self.addbook.lineEdit_pubdate.text()
        number = self.addbook.lineEdit_number.text()
        # 检查ISBN是否已存在
        sql_check = "SELECT * FROM t_book WHERE isbn=?"
        self.cursor.execute(sql_check, (isbn,))
        if self.cursor.fetchone() is not None:
            QtWidgets.QMessageBox.critical(self, "错误", "该书籍已存在！")
            return
        # 添加新书
        sql_insert = "INSERT INTO t_book (isbn, title, author, publisher, publishdate, number) VALUES (?, ?, ?, ?, ?, ?)"
        self.cursor.execute(sql_insert, (isbn, title, author, publish, publishdate, number))
        self.con.commit()

        if self.cursor.rowcount == 1:
            QtWidgets.QMessageBox.information(self, "提示", "添加成功！")
        else:
            QtWidgets.QMessageBox.critical(self, "错误", "添加失败！")
   
    #借书
    # def onBorrowBook(self):
    #     row=self.mainwindow.tableView_book.currentIndex().row()
    #     if row == -1:
    #         return
    #     model=self.mainwindow.tableView_book.model()
    #     isbn=model.item(row,0).text()
    #     #login_user_id
    #     borrow_date=QtCore.QDate.currentDate().toString("yyyy/MM/dd")
    #     sql=f"insert into t_borrow(user_id,book_isbn,borrow_date,return_date) values('{self.login_user_id}','{isbn}','{borrow_date}',''); "
    #     try:
    #         self.cursor.execute(sql) 
    #         if   self.cursor.rowcount ==1:
    #             QtWidgets.QMessageBox.information(self,"提示","借阅成功！")
    #             #更新图书数量
    #             sql=f"update t_book set number=number-1 where isbn='{isbn}'and number >0;"
    #             self.cursor.execute(sql)
    #         self.con.commit()     
    #     except sqlite3.Error as e:
    #             QtWidgets.QMessageBox.critical(self,"错误","借阅失败！")
    #查询借书记录
    def onQueryBorrow(self):
        sql=f"select id,name,isbn,title,borrow_date,return_date from t_borrow join t_user on user_id=id join t_book on book_isbn=isbn;"   
        self.cursor.execute(sql)
        model = QtGui.QStandardItemModel()
        model.setHorizontalHeaderLabels(['用户号', '姓名', '序列号', '书名', '借书时间','还书时间'])
        result_set=self.cursor.fetchall()
        for i in range(len(result_set)):
            for j in range(6):
                item = QtGui.QStandardItem(str(result_set[i][j]))
                item.setTextAlignment(QtCore.Qt.AlignCenter)
                model.setItem(i, j, item)
        self.mainwindow.tableView_borrow.setModel(model)     
    # def onReturnBorrow(self):
    #     row = self.mainwindow.tableView_borrow.currentIndex().row()
    #     if row == -1:
    #         return
    #     model = self.mainwindow.tableView_borrow.model()
    #     id = model.item(row, 0).text()  # 获取借阅记录ID
    #     isbn = model.item(row, 2).text()
    #     return_date = QtCore.QDate.currentDate().toString("yyyy/MM/dd")
    #     # 检查用户是否有该书的借阅记录
    #     sql_check = f"SELECT * FROM t_borrow WHERE user_id={id} AND book_isbn='{isbn}' AND return_date='';"
    #     self.cursor.execute(sql_check)
    #     borrowing_record = self.cursor.fetchone()
    #     if borrowing_record is not None:
    #         # 更新还书日期
    #         sql = f"UPDATE t_borrow SET return_date='{return_date}' WHERE user_id={borrowing_record[0]};"
    #         self.cursor.execute(sql)
    #         # 更新图书数量
    #         sql_number = f"UPDATE t_book SET number=number+1 WHERE isbn='{isbn}';"
    #         self.cursor.execute(sql_number)
    #         self.con.commit()
    #         if self.cursor.rowcount == 1:
    #             QtWidgets.QMessageBox.information(self, "提示", "还书成功！")
    #         else:
    #             QtWidgets.QMessageBox.critical(self, "错误", "还书失败！")
    #     else:
    #         QtWidgets.QMessageBox.critical(self, "提示", "该书未被借阅或已归还，请重新选择书籍！")
    
    def onBorrowBook(self):
        selected_rows = set(index.row() for index in self.mainwindow.tableView_book.selectionModel().selectedRows())
        if not selected_rows:
            return

        model = self.mainwindow.tableView_book.model()
        borrow_date = QtCore.QDate.currentDate().toString("yyyy/MM/dd")
        success_count = 0
        failure_count = 0
        failure_messages = []

        for row in selected_rows:
            isbn = model.item(row, 0).text()

            # Check if the user has already borrowed the book
            sql_check_borrowed = f"SELECT * FROM t_borrow WHERE user_id='{self.login_user_id}' AND book_isbn='{isbn}' AND return_date IS NULL;"
            self.cursor.execute(sql_check_borrowed)
            existing_borrowing = self.cursor.fetchone()

            if existing_borrowing is None:
                # Book is available for borrowing, insert a new borrowing record
                sql_borrow = f"INSERT INTO t_borrow(user_id, book_isbn, borrow_date, return_date) VALUES ('{self.login_user_id}', '{isbn}', '{borrow_date}', '');"
                try:
                    self.cursor.execute(sql_borrow)

                    # Update book quantity
                    update_sql = f"UPDATE t_book SET number=number-1 WHERE isbn='{isbn}' AND number > 0;"
                    self.cursor.execute(update_sql)

                    success_count += 1
                except sqlite3.Error as e:
                    failure_count += 1
                    failure_messages.append(f"借阅失败（ISBN: {isbn}）: {str(e)}")
            else:
                failure_count += 1
                failure_messages.append(f"您已借阅过该书，无法重复借阅（ISBN: {isbn}）")

        self.con.commit()

        if success_count > 0:
            success_message = f"成功借阅 {success_count} 本书。"
            QtWidgets.QMessageBox.information(self, "提示", success_message)

        if failure_count > 0:
            failure_message = "部分借阅失败，详情如下:\n\n" + '\n'.join(failure_messages)
            QtWidgets.QMessageBox.warning(self, "警告", failure_message)

        self.onQueryBorrow()

    def onReturnBorrow(self):
        selected_rows = set(index.row() for index in self.mainwindow.tableView_borrow.selectionModel().selectedRows())
        if not selected_rows:
            return

        model = self.mainwindow.tableView_borrow.model()
        return_date = QtCore.QDate.currentDate().toString("yyyy/MM/dd")

        for row in selected_rows:
            user_id = model.item(row, 0).text()
            isbn = model.item(row, 2).text()

            # Update return date
            sql_update = f"UPDATE t_borrow SET return_date='{return_date}' WHERE user_id={user_id} AND book_isbn='{isbn}' AND return_date='';"
            self.cursor.execute(sql_update)

            # Update book quantity
            sql_number = f"UPDATE t_book SET number=number+1 WHERE isbn='{isbn}';"
            self.cursor.execute(sql_number)

        self.con.commit()
        QtWidgets.QMessageBox.information(self, "提示", "归还成功！")

        # Refresh the records
        self.onQueryBorrow()




if __name__ =="__main__":
  app=QtWidgets.QApplication([])
  #实例化一个空白界面对象
  w=MyWidget()
  w.login.show()
  app.exec_()


  #c:\users\86155\appdata\local\programs\python\python39\lib\site-packages\pyside2\designer.exe