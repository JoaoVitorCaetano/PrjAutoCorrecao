import mysql.connector

class Uf:
    def __init__(self, sgl_uf ='', nme_uf='', idt_uf = None):
        self.idt_uf = idt_uf
        self.sgl_uf = sgl_uf
        self.nme_uf = nme_uf
        self._cliente = None

    @property
    def cliente(self):
        if self._cliente is None:
            from projeto_final.dao.cliente_dao import ClienteDao
            dao = ClienteDao
            self._cliente = dao.selecionar_por_uf(self.idt_uf)
        return self._cliente

    def __str__(self):
        return f"Id: {self.idt_uf}, Sigla: {self.sgl_uf}, Nome: {self.nme_uf}"

class UfDAO:
    def __init__(self, host="localhost", user="root", password="ceub123456", database="db_auto"):
        self.idt_uf = None
        try:
            self.conexao = mysql.connector.connect(
                host=host,
                user=user,
                password=password,
                database=database
            )
            self.cursor = self.conexao.cursor()
            print("Conexão com o banco de dados estabelecida com sucesso")
        except mysql.connector.Error as err:
            print(f"Erro ao conectar ao banco de dados: {err}")
            self.conexao = None
            self.cursor = None

    def inserir(self, uf):
        if not self.conexao:
            print("Error: Nenhuma conexão com o banco de dados")
            return

        sql = "INSERT INTO tb_uf (sgl_uf, nme_uf) VALUES (%s, %s)"
        valores = (uf.sgl_uf, uf.nme_uf)

        try:
            self.cursor.execute(sql, valores)
            self.conexao.commit()
            print(f"Uf '{uf.nme_uf}' inserido com sucesso")
            uf.idt_uf = self.cursor.lastrowid
        except mysql.connector.Error as err:
            print(f"Erro ao inserir UF: {err}")
            self.conexao.rollback()

    def selecionar_tudo(self):
        if not self.conexao:
            print("Erro: Nenhuma conexão com o banco de dados.")
            return []

        sql = "SELECT idt_uf, sgl_uf, nme_uf FROM tb_uf ORDER BY sgl_uf, nme_uf"


        try:
            self.cursor.execute(sql)
            resultados = self.cursor.fetchall()

            lista_uf = []
            for row in resultados:
                uf = Uf(idt_uf=row[0], sgl_uf=row[1], nme_uf=row[2])
                lista_uf.append(uf)

            return lista_uf
        except mysql.connector.Error as err:
            print(f"Erro ao selecionar montadoras: {err}")
            return []


    def selecionar_por_idt(self, idt):
        if not self.conexao:
            print("Erro: nenhuma conexão com o banco de dados.")
            return None


        sql = "SELECT idt_uf, sgl_uf, nme_uf FROM tb_uf WHERE idt_uf = %s"


        try:
            self.cursor.execute(sql, [idt])
            resultado = self.cursor.fetchone()
            if resultado is None:
                return None
            else:
                uf = Uf(idt_uf=resultado[0], sgl_uf=resultado[1], nme_uf=resultado[2])
                return uf
        except mysql.connector.Error as err:
            print(f"Error ao selecionar uf: {err}")
            return None


    def atualizar(self, uf):
        if not self.conexao:
            print("Erro: Nenhuma conexão com o banco de dados.")
            return

        sql = "UPDATE tb_uf SET sgl_uf = %s, nme_uf = %s WHERE idt_uf = %s"
        valores = (uf.sgl_uf, uf.nme_uf, uf.idt_uf)


        try:
            self.cursor.execute(sql, valores)
            self.conexao.commit()
            print(f"Uf de ID {uf.idt_uf} atualizada com sucesso")
        except mysql.connector.Error as err:
            print(f"Error ao atualizar uf: {err}")
            self.conexao.rollback()


    def deletar(self, idt_uf):
        if not self.conexao:
            print("Erro: nenhuma conexão com o banco de dados.")
            return

        sql = "DELETE FROM tb_uf WHERE idt_uf = %s"

        try:
            self.cursor.execute(sql, [idt_uf])
            self.conexao.commit()
            print(f"Uf de ID {idt_uf} deletada com sucesso!")
            return True
        except mysql.connector.Error as err:
            print(f"Erro ao deletar uf: {err}")
            self.conexao.rollback()
            return False

    def __dell__(self):
        if self.conexao and self.conexao.is_connected():
            self.cursor.close()
            self.conexao.close()
            print("Conexão com o banco de dados fechada")
