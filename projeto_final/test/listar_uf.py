from projeto_final.dao.uf_dao import Uf, UfDAO

dao = UfDAO()

nova_uf = Uf (
    sgl_uf = 'TT',
    nme_uf = 'Teste'
)

dao.deletar(30)
