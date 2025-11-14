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


