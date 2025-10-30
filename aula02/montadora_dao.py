import mysql.connector


# Classe que representa o objeto 'Montadora'
# Corresponde a uma linha da tabela tb_montadora
class Montadora:
    # O método construtor __init__ é chamado quando criamos um novo objeto Montadora.
    # Ele inicializa os atributos do objeto.
    def __init__(self, sgl_montadora, nme_montadora, idt_montadora=None):
        self.idt_montadora = idt_montadora
        self.sgl_montadora = sgl_montadora
        self.nme_montadora = nme_montadora

    # O método __str__ é útil para imprimir o objeto de forma amigável
    def __str__(self):
        return f"Id: {self.idt_montadora}, Sigla: {self.sgl_montadora}, Nome: {self.nme_montadora}"


# Classe DAO (Data Access Object) para a tabela tb_montadora
# Responsável por todas as operações de banco de dados
class MontadoraDAO:
    def __init__(self, host="localhost", user="root", password="ceub123456", database="db_auto"):
        # O construtor do DAO estabelece a conexão com o banco de dados
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

    def inserir(self, montadora):
        # Método para inserir um novo objeto Montadora no banco de dados
        if not self.conexao:
            print("Erro: Nenhuma conexão com o banco de dados.")
            return

        sql = "INSERT INTO tb_montadora (sgl_montadora, nme_montadora) VALUES (%s, %s)"
        valores = (montadora.sgl_montadora, montadora.nme_montadora)

        try:
            self.cursor.execute(sql, valores)
            self.conexao.commit()
            print(f"Montadora '{montadora.nme_montadora}' inserida com sucesso!")
            # Atualiza o ID do objeto Montadora com o ID gerado pelo banco de dados
            montadora.idt_montadora = self.cursor.lastrowid
        except mysql.connector.Error as err:
            print(f"Erro ao inserir montadora: {err}")
            self.conexao.rollback()

    def selecionar_tudo(self):
        # Método para selecionar todos os registros e retorná-los como objetos Montadora
        if not self.conexao:
            print("Erro: Nenhuma conexão com o banco de dados.")
            return []

        sql = "SELECT idt_montadora, sgl_montadora, nme_montadora FROM tb_montadora"

        try:
            self.cursor.execute(sql)
            resultados = self.cursor.fetchall()

            # Converte as tuplas do banco de dados em objetos Montadora
            lista_montadoras = []
            for row in resultados:
                montadora = Montadora(idt_montadora=row[0], sgl_montadora=row[1], nme_montadora=row[2])
                lista_montadoras.append(montadora)

            return lista_montadoras
        except mysql.connector.Error as err:
            print(f"Erro ao selecionar montadoras: {err}")
            return []

    def atualizar(self, montadora):
        # Método para atualizar um objeto Montadora no banco de dados
        if not self.conexao:
            print("Erro: Nenhuma conexão com o banco de dados.")
            return

        sql = "UPDATE tb_montadora SET sgl_montadora = %s, nme_montadora = %s WHERE idt_montadora = %s"
        valores = (montadora.sgl_montadora, montadora.nme_montadora, montadora.idt_montadora)

        try:
            self.cursor.execute(sql, valores)
            self.conexao.commit()
            print(f"Montadora de ID {montadora.idt_montadora} atualizada com sucesso!")
        except mysql.connector.Error as err:
            print(f"Erro ao atualizar montadora: {err}")
            self.conexao.rollback()

    def deletar(self, idt_montadora):
        # Método para deletar uma montadora pelo seu ID
        if not self.conexao:
            print("Erro: Nenhuma conexão com o banco de dados.")
            return

        sql = "DELETE FROM tb_montadora WHERE idt_montadora = %s"

        try:
            self.cursor.execute(sql, [idt_montadora])
            self.conexao.commit()
            print(f"Montadora de ID {idt_montadora} deletada com sucesso!")
        except mysql.connector.Error as err:
            print(f"Erro ao deletar montadora: {err}")
            self.conexao.rollback()

    def __dell__(self):
        # Método destrutor para fechar a conexão com o banco de dados
        if self.conexao and self.conexao.is_connected():
            self.cursor.close()
            self.conexao.close()
            print("Conexão com o banco de dados fechada.")


# --- Smoke Test ---
if __name__ == "__main__":

    m = Montadora(sgl_montadora='', nme_montadora='')
    print(m)
    m.sgl_montadora = input('Qual é sigla da montadora? ')
    m.nme_montadora = input('Qual o nome da montadora? ')
    print(m)
    dao = MontadoraDAO()
    dao.inserir(m)
    print(m)




'''
    # 1. Cria uma instância do DAO, estabelecendo a conexão
    dao = MontadoraDAO()

    if dao.conexao:
        # 2. Cria objetos Montadora (a lógica de negócios)
        montadora1 = Montadora("Toyota", "Alusão a campo de arroz Toyoda")
        montadora2 = Montadora("KIA", "Alusão a nativo da ásia")

        # 3. Usa o DAO para inserir os objetos no banco (a lógica de acesso a dados)
        dao.inserir(montadora1)
        dao.inserir(montadora2)

        # 4. Usa o DAO para selecionar todos os registros
        print("\nMontadoras cadastradas:")
        todas_montadoras = dao.selecionar_tudo()
        for montadora in todas_montadoras:
            print(montadora)

        # 5. Exemplo de atualização de um registro (usando o montadora1 que inserimos)
        if montadora1.idt_montadora:
            print(f"\nAtualizando a montadora de ID {montadora1.idt_montadora}...")
            montadora1.nme_montadora = "Toyota Motor Corporation"
            dao.atualizar(montadora1)

        # 6. Exemplo de deleção de um registro (usando o montadora2 que inserimos)
        if montadora2.idt_montadora:
            print(f"\nDeletando a montadora de ID {montadora2.idt_montadora}...")
            dao.deletar(montadora2.idt_montadora)

        # 7. Mostra os registros após as operações
        print("\nMontadoras cadastradas após as operações:")
        todas_montadoras = dao.selecionar_tudo()
        for montadora in todas_montadoras:
            print(montadora)
'''