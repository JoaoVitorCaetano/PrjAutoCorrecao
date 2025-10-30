from projeto_final.dao.montadora_dao import MontadoraDAO

dao = MontadoraDAO()

lista = dao.selecionar_tudo()
for m in lista:
    print(m.sgl_montadora, m.nme_montadora)

print('-' * 30)
gwm = dao.selecionar_por_idt(4)
print(gwm.sgl_montadora, gwm.nme_montadora)
for mod in gwm.modelos:
    print(mod.nme_modelo)

from projeto_final.dao.modelo_dao import ModeloDAO
print('-' * 30)
daoModelo = ModeloDAO()
nivus = daoModelo.selecionar_por_idt(3)
print(nivus.montadora.sgl_montadora, nivus.nme_modelo)
for ver in nivus.versoes:
    print(ver.nme_versao, ver.vlr_modelo)


