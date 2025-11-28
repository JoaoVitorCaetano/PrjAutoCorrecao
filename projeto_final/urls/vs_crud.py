import os
from flask import Blueprint, render_template, request, current_app
from werkzeug.utils import secure_filename
from projeto_final.dao.versao_dao import Versao, VersaoDAO
from projeto_final.dao.modelo_dao import ModeloDAO


UPLOAD_FOLDER = 'C:\\Users\\joao.caetano\\Documents\\PrjAutoCorrecao\\projeto_final\\static\\imgs\\versao'


bp_vs = Blueprint('vs', __name__)




@bp_vs.route('/form_create')
def form_create():
   dao = ModeloDAO()
   lst = dao.selecionar_tudo()
   return render_template('/vs/form_create.html', msg="", display="none", lst=lst)




@bp_vs.route('/create', methods=['POST'])
def create():
   # 1. Obter os dados do formulário
   nme_versao = request.form['nme_versao']
   cod_modelo = request.form['cod_modelo']
   vlr_modelo = request.form['vlr_modelo']


   # 2. Lidar com o arquivo de upload
   if 'img_modelo' not in request.files:
       msg = 'Nenhum arquivo de imagem enviado.'
       display = "block"
       # Recarrega a lista de modelos para o formulário
       modelo_dao = ModeloDAO()
       lst_modelos = modelo_dao.selecionar_tudo()
       return render_template('/vs/form_create.html', msg=msg, display=display, lst=lst_modelos)


   file = request.files['img_modelo']


   if file.filename == '':
       msg = 'Nenhum arquivo selecionado.'
       display = "block"
       # Recarrega a lista de modelos para o formulário
       modelo_dao = ModeloDAO()
       lst_modelos = modelo_dao.selecionar_tudo()
       return render_template('/vs/form_create.html', msg=msg, display=display, lst=lst_modelos)


   # 3. Salvar o arquivo de forma segura
   if file:
       filename = secure_filename(file.filename)
       img_path = UPLOAD_FOLDER + '//' + filename
       file.save(img_path)


       # 4. Criar o objeto Versao e preencher com os dados e o caminho da imagem
       v = Versao()
       v.nme_versao = nme_versao
       v.cod_modelo = int(cod_modelo)
       v.vlr_modelo = float(vlr_modelo)
       v.img_modelo = f'/imgs/versao/{filename}'  # O caminho relativo para o template


       # 5. Salvar a nova Versão no banco de dados
       dao = VersaoDAO()
       dao.inserir(v)


       if v.idt_versao is None:
           msg = 'Erro ao inserir a versão. Procure o administrador do sistema.'
           display = "block"
       else:
           msg = f'Versão número {v.idt_versao} inserida com sucesso.'
           display = "block"
   else:
       msg = 'Erro inesperado no upload do arquivo.'
       display = "block"


   # Recarregar os modelos para o formulário de cadastro de nova versão
   modelo_dao = ModeloDAO()
   lst_modelos = modelo_dao.selecionar_tudo()


   return render_template('/vs/form_create.html', msg=msg, display=display, lst=lst_modelos)




@bp_vs.route('/read')
def read():
   # Buscar as versões para listar em uma tabela
   dao = VersaoDAO()
   lst = dao.selecionar_tudo()


   if not lst:
       msg = 'Não há versões na base de dados.'
   else:
       msg = f'Listados {len(lst)} versões da base de dados.'


   return render_template('/vs/read.html', msg=msg, lst=lst)


@bp_vs.route('/edit')
def edit():
   # Buscar as versões para listar em uma tabela
   dao = VersaoDAO()
   lst = dao.selecionar_tudo()


   if not lst:
       msg = 'Não há versões na base de dados.'
   else:
       msg = f'Listados {len(lst)} versões da base de dados.'


   return render_template('/vs/edit.html', msg=msg, lst=lst)




@bp_vs.route('/delete/<int:idt>')
def delete(idt):
   dao = VersaoDAO()
   if dao.deletar(idt):
       msg = 'Versão excluída com sucesso!'
   else:
       msg = "Erro ao tentar excluir versão, provavelmente tem compra associada!"


   # Recarregar a lista sem o objeto excluído
   lst = dao.selecionar_tudo()
   if not lst:
       msg = ' | Não há versões na base de dados.'
   else:
       msg = f' | Listados {len(lst)} versões da base de dados.'
   return render_template('/vs/edit.html', msg=msg, lst=lst)




@bp_vs.route('/form_update/<int:idt>')
def form_update(idt):
   # Buscar os dados da versão escolhida para edição
   dao = VersaoDAO()
   versao = dao.selecionar_por_idt(idt)
   dao_modelo = ModeloDAO()
   lst = dao_modelo.selecionar_tudo()


   return render_template('/vs/form_update.html', versao=versao, msg='', lst=lst, display="none")




@bp_vs.route('/save_update', methods=['POST'])
def save_update():
   # 1. Obter os dados do formulário
   v = Versao()
   v.idt_versao = request.form['idt_versao']
   v.nme_versao = request.form['nme_versao']
   v.cod_modelo = request.form['cod_modelo']
   v.vlr_modelo = request.form['vlr_modelo']


   # 2. Lidar com o upload de nova imagem (opcional)
   if 'img_modelo' in request.files and request.files['img_modelo'].filename != '':
       file = request.files['img_modelo']
       filename = secure_filename(file.filename)
       img_path = os.path.join(UPLOAD_FOLDER, filename)
       file.save(img_path)
       v.img_modelo = f'/imgs/versao/{filename}'  # Caminho relativo para o banco de dados
   else:
       # Se nenhuma nova imagem foi enviada, mantenha a imagem existente
       dao_versao = VersaoDAO()
       versao_existente = dao_versao.selecionar_por_idt(v.idt_versao)
       v.img_modelo = versao_existente.img_modelo


   # 3. Chamar o DAO de Versão para atualizar
   dao_versao = VersaoDAO()
   dao_versao.atualizar(v)
   msg = f'Versão número {v.idt_versao} alterada com sucesso.'


   # 4. Recarregar os dados para o formulário de edição
   dao_modelo = ModeloDAO()
   lst_modelos = dao_modelo.selecionar_tudo()


   # 5. Renderizar o formulário de alteração novamente com a mensagem de sucesso
   return render_template('/vs/form_update.html', versao=v, msg=msg, lst=lst_modelos, display="block")


