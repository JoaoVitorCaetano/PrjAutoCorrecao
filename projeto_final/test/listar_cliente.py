from projeto_final.dao.cliente_dao import ClienteDAO, Cliente

dao = ClienteDAO()


novo_cliente = Cliente(
    nme_cliente="Joana da Silva",
    dta_nasc_cliente="1995-03-10",
    cep_cliente="71000123",
    end_cliente="Rua das Palmeiras, 10",
    cod_uf=2
)

dao.deletar(13)

lista = dao.selecionar_tudo()
for nome in lista:
    print(nome.nme_cliente, nome.dta_nasc_cliente)