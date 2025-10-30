from projeto_final.dao.compra_dao import CompraDAO, Compra

dao = CompraDAO()

nova_compra = Compra(
        idt_compra=2,
        dta_compra="2025-10-28",
        num_nf_compra=35,
        vlr_final_compra=12,
        cod_cliente=2,
        cod_versao=2
)

dao.deletar(3)
