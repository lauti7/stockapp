#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
from PyQt4 import QtCore, QtGui, uic
import sqlite3

class Ventana(QtGui.QMainWindow):
	def __init__(self):
		QtGui.QMainWindow.__init__(self)
		uic.loadUi('base.ui', self)
		QtGui.QMainWindow.setWindowTitle(self, 'Base de datos')
		self.dialogoing = DialogIngr()
		self.dialogomostr = DialogMostr()
		self.dialogoelim = DialogElim()
		self.dialogoup = DialogUp()
		self.btn_ingresar.clicked.connect(self.ingr_data)
		self.btn_show.clicked.connect(self.mostr_data)
		self.btn_eliminar.clicked.connect(self.elim_data)
		self.btn_update.clicked.connect(self.up_data)

		self.IniciarDB()

	def IniciarDB(self):
		self.conn = sqlite3.connect('base.db')
		self.cursor = self.conn.cursor()
		self.cursor.execute('''CREATE TABLE IF NOT EXISTS clientes (id INTEGER PRIMARY KEY AUTOINCREMENT, nombre TEXT, apellido TEXT, localidad TEXT, servicios TEXT)''')
		self.conn.commit()

	def ingr_data(self):
		self.dialogoing.exec_()

	def mostr_data(self):
		self.dialogomostr.exec_()
		self.dialogomostr.listw.clear()
		self.dialogomostr.btn_car.setEnabled(True)

	def elim_data(self):
		self.dialogoelim.exec_()

	def up_data(self):
		self.dialogoup.exec_()





class DialogIngr(QtGui.QDialog):
	def __init__(self):
		QtGui.QDialog.__init__(self)
		uic.loadUi('dialogbase.ui', self)
		QtGui.QDialog.setWindowTitle(self, 'Ingresar clientes')
		self.btn_guardar.clicked.connect(self.data_guard)


	def data_guard(self):
		#Conenctando la base de datos
		self.conn = sqlite3.connect('base.db')
		self.cursor = self.conn.cursor()
		#Datos y line edits para ingresar
		self.nombre = str(self.lenomb.text())
		self.apellido = str(self.leapel.text())
		self.localidad = str(self.leloca.text())
		self.servicios = str(self.serv.toPlainText())
		self.datos = (self.nombre, self.apellido, self.localidad, self.servicios)

		#se insertan los datos en la tabla y se guardan
		self.cursor.execute('INSERT INTO clientes (nombre, apellido, localidad, servicios) VALUES (?, ?, ?, ?)', self.datos)
		self.conn.commit()


		#los line edits quedan vacios
		self.lenomb.setText("")
		self.leapel.setText("")
		self.leloca.setText("")
		self.serv.setPlainText("")
		#Se guarda y se cierra conexion
		self.conn.commit()
		self.conn.close()

class DialogMostr(QtGui.QDialog):
	def __init__(self):
		QtGui.QDialog.__init__(self)
		uic.loadUi('dialogmostr.ui', self)
		QtGui.QDialog.setWindowTitle(self, 'Mostar clientes')
		self.btn_car = self.cargar
		self.btn_car.clicked.connect(self.cargarData)
		self.listw = self.list

	def cargarData(self):
		self.cargar.setEnabled(False)
		self.conn = sqlite3.connect('base.db')
		self.cursor = self.conn.cursor()

		self.cursor.execute('SELECT id, nombre, apellido, localidad, servicios FROM clientes')





		for fila in self.cursor:
			self.id = str(fila[0])
			self.nombre = str(fila[1])
			self.apellido = str(fila[2])
			self.localidad = str(fila[3])
			self.servicios = str(fila[4])

			self.list.addItem("ID:" + self.id)
			self.list.addItem('Nombre:' + ' ' + self.nombre)
			self.list.addItem('Apellido:' + ' ' + self.apellido)
			self.list.addItem('Localidad:' + ' ' + self.localidad)
			self.list.addItem("Servicios:" + ' ' + self.servicios)



class DialogElim(QtGui.QDialog):
	def __init__(self):
		QtGui.QDialog.__init__(self)
		uic.loadUi('dialogelim.ui', self)
		#self.lineEditBuscar = str(self.le_buscar.text())
		self.btn_buscar.clicked.connect(self.busqueda)
		self.btn_eliminar.clicked.connect(self.eliminar)
		self.mbox = QtGui.QMessageBox()


	def busqueda(self):
		self.list.clear()
		self.conn = sqlite3.connect('base.db')
		self.cursor = self.conn.cursor()
		self.lineEditBuscar = str(self.le_buscar.text())
		self.datos = (self.lineEditBuscar)



		self.cursor.execute('SELECT * FROM clientes WHERE nombre=? OR id=?', (self.datos, self.datos,))

		for fila in self.cursor:
			self.id = str(fila[0])
			self.nombre = str(fila[1])
			self.apellido = str(fila[2])
			self.localidad = str(fila[3])
			self.servicios = str(fila[4])

			self.list.addItem("ID:" + self.id)
			self.list.addItem('Nombre:' + ' ' + self.nombre)
			self.list.addItem('Apellido:' + ' ' + self.apellido)
			self.list.addItem('Localidad:' + ' ' + self.localidad)
			self.list.addItem("Servicios:" + ' ' + self.servicios)

	def eliminar(self):
		self.conn = sqlite3.connect('base.db')
		self.cursor = self.conn.cursor()


		#self.cursor.execute("DELETE FROM clientes WHERE nombre=?", (self.datos,))



		result = self.mbox.question(self, "Mensage", "¿Estas seguro que quieres eliminar el contacto?", QtGui.QMessageBox.Yes | QtGui.QMessageBox.No)
		print result

		if result == QtGui.QMessageBox.Yes:
			self.cursor.execute("DELETE FROM clientes WHERE nombre=? OR id=?", (self.datos, self.datos,))
			self.conn.commit()

			self.list.clear()
		else:
			print 'No.'

		self.conn.commit()
		self.conn.close()

class DialogUp(QtGui.QDialog):
	def __init__(self):
		QtGui.QDialog.__init__(self)
		uic.loadUi('dialogup.ui', self)
		self.up.clicked.connect(self.update)
		self.mostrar.clicked.connect(self.mostardata)
		self.error = QtGui.QMessageBox()

	def mostardata(self):
		self.mostrar.setEnabled(False)
		self.conn = sqlite3.connect('base.db')
		self.cursor = self.conn.cursor()

		self.cursor.execute('SELECT id, nombre, apellido, localidad, servicios FROM clientes')

		for fila in self.cursor:
			self.id = str(fila[0])
			self.nombre = str(fila[1])
			self.apellido = str(fila[2])
			self.localidad = str(fila[3])
			self.servicios = str(fila[4])

			self.list.addItem("ID:" + self.id)
			self.list.addItem('Nombre:' + ' ' + self.nombre)
			self.list.addItem('Apellido:' + ' ' + self.apellido)
			self.list.addItem('Localidad:' + ' ' + self.localidad)
			self.list.addItem("Servicios:" + ' ' + self.servicios)




	def update(self):
		item = self.cbox.currentText()
		self.b_nombre = str(self.line1.text())
		self.up_nombre = str(self.line2.text())
		self.datos1 = (self.up_nombre)
		self.datos2 = (self.b_nombre)
		self.conn = sqlite3.connect('base.db')
		self.cursor = self.conn.cursor()


		if item == 'Nombre':
			self.cursor.execute('UPDATE clientes SET nombre=? WHERE id=?', (self.datos1, self.datos2,))
			self.conn.commit()
		elif item == 'Apellido':
			self.cursor.execute('UPDATE clientes SET apellido=? WHERE id=?', (self.datos1, self.datos2,))
			self.conn.commit()
		elif item == 'Localidad':
			self.cursor.execute('UPDATE clientes SET localidad=? WHERE id=?', (self.datos1, self.datos2,))
			self.conn.commit()
		elif item == 'Servicios':
			self.cursor.execute('UPDATE clientes SET servicios=? WHERE id=?', (self.datos1, self.datos2,))
			self.conn.commit()
		else:
			self.error.question(self, 'Error', 'Hubo un error al actualizar el contacto, verifique si los datos que ingreso son correctos', QtGui.QMessageBox.Ok)


		self.conn.commit()
		self.conn.close()

app = QtGui.QApplication(sys.argv)
ventana = Ventana()
ventana.show()
app.exec_()
