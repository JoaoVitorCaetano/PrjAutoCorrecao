import mysql.connector

class Compra:
    def __init__(self, idt_compra=None, dta_compra="", num_nf_compra=None, vlr_final_compra=None, cod_cliente=None, cod_versao=None):
        self.idt_compra = idt_compra
        self.dta_compra = dta_compra
        self.num_nf_compra = num_nf_compra
        self.vlr_final_compra = vlr_final_compra
        self.cod_cliente = cod_cliente
        self.cod_versao = cod_versao
        self._cliente = None
        self._versao = None


    @property
    def cliente(self):
        if self._cliente is None:
            from projeto_final.dao.cliente_dao import ClienteDAO
            dao = ClienteDAO()
            self._cliente = dao.selecionar_por_idt(self.cod_cliente)
        return self._cliente



    def __str__(self):
        return f"Id: {self.idt_compra}, Data da Compra: {self.dta_compra}, Número da nota fiscal: {self.num_nf_compra}, Valor Final:{self.vlr_final_compra}, Código Cliente: {self.cod_cliente}, Código Versão: {self.cod_versao}"


class CompraDAO:
    def __init__(self, host="localhost", user="root", password="ceub123456", database="db_auto"):
        try:
            self.conexao = mysql.connector.connect(
                host=host,
                user=user,
                password=password,
                database=database
            )
            self.cursor = self.conexao.cursor()
            print("Conexão com o banco de dados estabelecida com sucesso!")

        except mysql.connector.Error as err:
            print(f"Erro ao conectar ao banco de dados: {err}")
            self.conexao = None
            self.cursor = None

    def inserir(self, compra):
        if not self.conexao:
            print("Erro: Nenhuma conexão com o banco de dados.")
            return

        sql = "INSERT INTO ta_compra (dta_compra, num_nf_compra, vlr_final_compra, cod_cliente, cod_versao) VALUES (%s, %s, %s, %s, %s)"
        valores = (compra.dta_compra, compra.num_nf_compra, compra.vlr_final_compra, compra.cod_cliente,compra.cod_versao)

        try:
            self.cursor.execute(sql, valores)
            self.conexao.commit()
            print(f"Compra '{compra.idt_compra}' inserida com sucesso!")
            # Atualiza o ID do objeto Modelo com o ID gerado pelo banco de dados
            compra.idt_compra = self.cursor.lastrowid
        except mysql.connector.Error as err:
            print(f"Erro ao inserir modelo: {err}")
            self.conexao.rollback()


    def selecionar_tudo(self):
        if not self.conexao:
            print("Erro: Nenhuma conexão com o banco de dados.")
            return []

        sql = "SELECT idt_compra, dta_compra, num_nf_compra, vlr_final_compra, cod_cliente, cod_versao FROM ta_compra ORDER BY idt_compra"


        try:
            self.cursor.execute(sql)
            resultados = self.cursor.fetchall()

            lista_compras = []
            for row in resultados:
                compra = Compra(idt_compra=row[0], dta_compra=row[1], num_nf_compra=row[2], vlr_final_compra=row[3], cod_cliente=row[4], cod_versao=row[5])
                lista_compras.append(compra)

            return lista_compras
        except mysql.connector.Error as err:
            print(f"Erro ao selecionar compras: {err}")
            return[]


    def selecionar_por_cliente(self, idt_cliente):
        if not self.conexao:
            print("Erro: Nenhuma conexão com o banco de dados.")
            return []

        sql = "SELECT idt_compra, dta_compra, num_nf_compra, vlr_final_compra, cod_cliente, cod_versao FROM ta_compra WHERE cod_cliente = %s ORDER BY idt_compra"

        try:
            self.cursor.execute(sql, [idt_cliente])
            resultados = self.cursor.fetchall()

            lista_compras = []
            for row in resultados:
                compra =  Compra(idt_compra=row[0], dta_compra=row[1], num_nf_compra=row[2], vlr_final_compra=row[3], cod_cliente=row[4], cod_versao=row[5])
                lista_compras.append(compra)

                return lista_compras
        except mysql.connector.Error as err:
            print(f"Erro ao selecionar compras: {err}")
            return []


    def selecionar_por_versao(self, idt_versao):
        if not self.conexao:
            print("Erro: Nenhuma conexão com o banco de dados.")
            return []

        sql = "SELECT idt_compra, dta_compra, num_nf_compra, vlr_final_compra, cod_cliente, cod_versao FROM ta_compra WHERE cod_versao = %s ORDER BY idt_compra"

        try:
            self.cursor.execute(sql, [idt_versao])
            resultados = self.cursor.fetchall()

            lista_compras = []
            for row in resultados:
                compra = Compra(idt_compra=row[0], dta_compra=row[1], num_nf_compra=row[2], vlr_final_compra=row[3],
                                cod_cliente=row[4], cod_versao=row[5])
                lista_compras.append(compra)

                return lista_compras
        except mysql.connector.Error as err:
            print(f"Erro ao selecionar compras: {err}")
            return []



    def selecionar_por_idt(self, idt):
        if not self.conexao:
            print("Erro: Nenhuma conexão com o banco de dados.")
            return None


        sql = "SELECT idt_compra, dta_compra, num_nf_compra, vlr_final_compra, cod_cliente, cod_versao FROM ta_compra WHERE idt_compra = %s"


        try:
            self.cursor.execute(sql, [idt])
            resultado = self.cursor.fetchone()
            if resultado is None:
                return None
            else:
                compra = Compra(idt_compra=resultado[0], dta_compra=resultado[1], num_nf_compra=resultado[2], vlr_final_compra=resultado[3],
                                cod_cliente=resultado[4], cod_versao=resultado[5])
                return compra

        except mysql.connector.Error as err:
            print(f"Erro ao selecionar compra: {err}")
            return[]


    def atualizar(self, compra):
        if not self.conexao:
            print("Erro: Nenhuma conexão com o banco de dados.")
            return

        sql = "UPDATE ta_compra SET dta_compra = %s, num_nf_compra = %s, vlr_final_compra = %s, cod_cliente = %s, cod_versao = %s WHERE idt_compra = %s"
        valores = (compra.dta_compra, compra.num_nf_compra, compra.vlr_final_compra, compra.cod_cliente, compra.cod_versao, compra.idt_compra)

        try:
            self.cursor.execute(sql, valores)
            self.conexao.commit()
            print(f"Compra de ID {compra.idt_compra} atualizada com sucesso!")
        except mysql.connector.Error as err:
            print(f"Erro ao atualizar compra: {err}")
            self.conexao.rollback()



    def deletar(self, idt_compra):
        if not self.conexao:
            print("Erro: Nenhuma conexão com o banco de dados.")
            return


        sql = "DELETE FROM ta_compra WHERE idt_compra = %s"


        try:
            self.cursor.execute(sql, [idt_compra])
            self.conexao.commit()
            print(f"Compra de ID {idt_compra} deletada com sucesso!")
            return True
        except mysql.connector.Error as err:
            print(f"Erro ao deletar compra: {err}")
            self.conexao.rollback()
            return False

    def __dell__(self):
        if self.conexao and self.conexao.is_connected():
            self.cursor.close()
            self.conexao.close()
            print("Conexão com o banco de dados fechada.")