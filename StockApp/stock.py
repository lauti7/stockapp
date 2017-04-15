import sqlite3
import sys
from PyQt5 import QtGui, QtCore, uic, QtWidgets

class MyWindowClass(QtWidgets.QMainWindow):
	def __init__(self):
		QtWidgets.QMainWindow.__init__(self)
		uic.loadUi('stock_main.ui', self)
		self.stockIngresar = Stock_ingresar()
		self.stockMainEntrega = Stock_MainEntrega()
		self.iniciarDB()
		self.iniciarDB2()
		self.btn_ingresar.clicked.connect(self.open_ingresar)
		self.btn_venta.clicked.connect(self.open_entregar)



	def iniciarDB(self):
		self.conn = sqlite3.connect('stock.db')
		self.cursor = self.conn.cursor()

		self.cursor.execute('''CREATE TABLE IF NOT EXISTS stock (id INTEGER PRIMARY KEY AUTOINCREMENT, nombre TEXT, n_stock INT )''')

	def iniciarDB2(self):
		self.conn = sqlite3.connect('stock2.db')
		self.cursor = self.conn.cursor()

		self.cursor.execute('''CREATE TABLE IF NOT EXISTS stock2 (id INTEGER PRIMARY KEY AUTOINCREMENT, n_cliente TEXT, n_herramienta TEXT, cantidad INT)''')

	def open_ingresar(self):
		self.stockIngresar.exec_()

	def open_entregar(self):
		self.stockMainEntrega.btn_mostrar.setEnabled(True)
		self.stockMainEntrega.listw.clear()
		self.stockMainEntrega.listx.clear()
		self.stockMainEntrega.exec_()


class Stock_ingresar(QtWidgets.QDialog):
	def __init__(self):
		QtWidgets.QDialog.__init__(self)
		uic.loadUi('stock_ingresar.ui', self)
		self.btn_cargar.clicked.connect(self.ingresar)

	def ingresar(self):
		self.conn = sqlite3.connect('stock.db')
		self.cursor = self.conn.cursor()
		self.nombre = str(self.le_nombre.text())
		self.n_stock = int(self.le_stock.text())
		self.cursor.execute('INSERT INTO stock (nombre, n_stock) VALUES (?, ?)', (self.nombre, self.n_stock))
		self.conn.commit()
		self.le_nombre.setText('')
		self.le_stock.setText('')

class Stock_MainEntrega(QtWidgets.QDialog):
	def __init__(self):
		QtWidgets.QDialog.__init__(self)
		uic.loadUi('stock_mainentrega.ui', self)
		self.btn_mostrar = self.btn_mostrar
		self.listw = self.list
		self.listx = self.list2
		self.btn_mostrar.clicked.connect(self.mostrar_datos)
		self.btn_mostrar2.clicked.connect(self.mostrar_datos2)
		self.StockEntregar = Stock_Entrega()
		self.btn_entregar.clicked.connect(self.open_entrega)

	def open_entrega(self):
		self.StockEntregar.exec_()

	def mostrar_datos(self):
		self.listw.clear()
		#self.btn_mostrar.setEnabled(False)
		self.conn = sqlite3.connect('stock.db')
		self.cursor = self.conn.cursor()
		self.cursor.execute('SELECT * FROM stock')

		for fila in self.cursor:
			self.id = str(fila[0])
			self.nombre = str(fila[1])
			self.cantidad = str(fila[2])

			self.list.addItem('ID: ' + self.id)
			self.list.addItem('Nombre: ' + self.nombre)
			self.list.addItem('N.Stock:' + self.cantidad)

	def mostrar_datos2(self):
		self.listx.clear()
		self.conn = sqlite3.connect('stock2.db')
		self.cursor = self.conn.cursor()
		self.cursor.execute('SELECT * FROM stock2')

		for fila in self.cursor:
			self.id = str(fila[0])
			self.nombre = str(fila[1])
			self.n_herramienta = str(fila[2])
			self.cantidad = str(fila[3])

			self.list2.addItem('ID: ' + self.id)
			self.list2.addItem('Nombre del cliente: ' + self.nombre)
			self.list2.addItem('Nombre del producto: ' + self.n_herramienta)
			self.list2.addItem('Cantidad: ' + self.cantidad)

class Stock_Entrega(QtWidgets.QDialog):
	def __init__(self):
		QtWidgets.QDialog.__init__(self)
		uic.loadUi('stock_entrega.ui', self)
		self.btn_entrega.clicked.connect(self.Producto_entregado)

	def Producto_entregado(self):
		self.conn = sqlite3.connect('stock.db')
		self.conn2 = sqlite3.connect('stock2.db')
		self.cursor = self.conn.cursor()
		self.cursor2 = self.conn2.cursor()
		self.id = str(self.le_id.text())
		self.cantidad = int(self.le_cantidad.text())
		self.n_cliente = str(self.le_nombre.text())
		self.n_herramienta = str(self.le_producto.text())
		self.cursor.execute('UPDATE stock SET n_stock=n_stock-? WHERE id=?', (self.cantidad, self.id))
		self.cursor2.execute('INSERT INTO stock2 (n_cliente, n_herramienta, cantidad) VALUES (?, ?, ?)', (self.n_cliente, self.n_herramienta, self.cantidad))
		self.conn.commit()
		self.conn2.commit()


app = QtWidgets.QApplication(sys.argv)
ventana = MyWindowClass()
ventana.show()
app.exec_()
