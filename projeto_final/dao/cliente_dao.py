import mysql.connector
from sqlalchemy.util.preloaded import sql_naming
from projeto_final.dao.compra_dao import  CompraDAO

class Cliente:
    def __init__(self, idt_cliente: object = None, nme_cliente: object = '', dta_nasc_cliente: object = '', cep_cliente: object = None,
                 end_cliente: object = '',
                 cod_uf: object = None) -> object:
        self.idt_cliente = idt_cliente
        self.nme_cliente = nme_cliente
        self.dta_nasc_cliente = dta_nasc_cliente
        self.cep_cliente = cep_cliente
        self.end_cliente = end_cliente
        self.cod_uf = cod_uf
        self._uf = None
        self._compra = None

    @property
    def uf(self):
        if self._uf is None:
            from projeto_final.dao.uf_dao import UfDAO
            dao = UfDAO()
            self._uf = dao.selecionar_por_idt(self.cod_uf)
        return self._uf

    @property
    def compra(self):
        if self._compra is None:
            from projeto_final.dao.compra_dao import CompraDAO
            dao = CompraDAO()
            self._compra = dao.selecionar_por_id(self.idt_cliente)
        return self._compra


    def __str__(self):
        return f"ID: {self.idt_cliente}, Nome: {self.nme_cliente}, Data de Nascimento: {self.dta_nasc_cliente}, CEP: {self.cep_cliente}, Endereço: {self.end_cliente}, Código UF: {self.cod_uf}, UF: {self.uf.nme_uf}"



class ClienteDAO:
    def __init__(self, host="localhost", user="root", password="ceub123456", database="db_auto"):
        try:
            self.conexao = mysql.connector.connect(
                host=host,
                user=user,
                password=password,
                database=database
            )
            self.cursor = self.conexao.cursor()
            print("Conexão com o banco de dados estabelicida com sucesso!")
        except mysql.connector.Error as err:
            print(f"Erro ao conectar ao banco de dados: {err}")
            self.cursor = None
            self.conexao = None


    def inserir(self, cliente):
        if not self.conexao:
            print("Erro: Nenhuma conexão com o banco de dados")
            return

        sql = "INSERT INTO tb_cliente (nme_cliente, dta_nasc_cliente, cep_cliente, end_cliente, cod_uf) VALUES (%s, %s, %s, %s, %s)"
        valores = (cliente.nme_cliente, cliente.dta_nasc_cliente, cliente.cep_cliente, cliente.end_cliente, cliente.cod_uf)


        try:
            self.cursor.execute(sql, valores)
            self.conexao.commit()
            print(f"Cliente '{cliente.nme_cliente}' inserido com sucesso!")
            cliente.idt_cliente = self.cursor.lastrowid
        except mysql.connector.Error as err:
            print(f"Erro ao inserir cliente: {err}")
            self.conexao.rollback()


    def selecionar_tudo(self):
        if not self.conexao:
            print("Erro: Nenhuma conexão com o banco de dados")
            return []

        sql = sql = "SELECT idt_cliente, nme_cliente, dta_nasc_cliente, cep_cliente, end_cliente, cod_uf FROM tb_cliente ORDER BY nme_cliente"

        try:
            self.cursor.execute(sql)
            resultados = self.cursor.fetchall()

            lista_clientes = []
            for row in resultados:
                cliente = Cliente(idt_cliente=row[0], nme_cliente=row[1], dta_nasc_cliente=row[2], cep_cliente=row[3], end_cliente=row[4], cod_uf=row[5])
                lista_clientes.append(cliente)

            return lista_clientes

        except mysql.connector.Error as err:
            print(f"Erro ao selecionar cliente: {err}")
            return []


    def selecionar_por_uf(self, idt_uf):
        if not self.conexao:
            print("Erro: Nenhuma conexão com o banco de dados")
            return []

        sql = sql = "SELECT idt_cliente, nme_cliente, dta_nasc_cliente, cep_cliente, end_cliente, cod_uf FROM tb_cliente WHERE cod_uf = %s"

        try:
            self.cursor.execute(sql, (idt_uf,))
            resultados = self.cursor.fetchall()

            lista_clientes = []
            for row in resultados:
                cliente = Cliente(idt_cliente=row[0], nme_cliente=row[1], dta_nasc_cliente=row[2], cep_cliente=row[3], end_cliente=row[4], cod_uf=row[5])
                lista_clientes.append(cliente)

            return lista_clientes
        except mysql.connector.Error as err:
            print(f"Erro ao selecionar cliente: {err}")
            return []


    def selecionar_por_idt(self, idt):
        if not self.conexao:
            print("Erro: Nenhuma conexão com o banco de dados")
            return None


        sql = "SELECT idt_cliente, nme_cliente, dta_nasc_cliente, cep_cliente, end_cliente, cod_uf FROM tb_cliente WHERE idt_cliente = %s"

        try:
            self.cursor.execute(sql, [idt,])
            resultado = self.cursor.fetchone()
            if resultado is None:
                return None
            else:
                cliente = Cliente(idt_cliente=resultado[0], nme_cliente=resultado[1], dta_nasc_cliente=resultado[2], cep_cliente=resultado[3], end_cliente=resultado[4], cod_uf=resultado[5])
                return cliente

        except mysql.connector.Error as err:
            print(f"Erro ao selecionar cliente: {err}")
            return []


    def atualiar(self, cliente):
        if not self.conexao:
            print("Erro: Nenhuma conexão com o banco de dados")
            return

        sql = "UPDATE tb_cliente SET nme_cliente = %s, dta_nasc_cliente = %s,cep_cliente = %s,end_cliente = %s,cod_uf = %s WHERE idt_cliente = %s"
        valores = (cliente.nme_cliente,cliente.dta_nasc_cliente,cliente.cep_cliente,cliente.end_cliente,cliente.cod_uf,cliente.idt_cliente)

        try:
            self.cursor.execute(sql, valores)
            self.conexao.commit()
            print(f"Cliente de ID {cliente.idt_cliente} atualizado com sucesso!")
        except mysql.connector.Error as err:
            print(f"Erro ao atualizar cliente: {err}")
            self.conexao.rollback()

    def deletar(self, idt_cliente=None):
        if not self.conexao:
            print("Erro: Nenhuma conexão com o bando de dados")
            return

        sql = "DELETE FROM tb_cliente WHERE idt_cliente = %s"

        try:
            self.cursor.execute(sql, [idt_cliente])
            self.conexao.commit()
            print(f"Cliente de ID {idt_cliente} deletado com sucesso!")
            return True
        except mysql.connector.Error as err:
            print(f"Erro ao deletar cliente: {err}")
            self.conexao.rollback()
            return False

    def __dell__(self):
        if self.conexao and self.conexao.is_connected():
            self.cursor.close()
            self.conexao.close()
            print("Conexão com o banco de dados fechada.")

