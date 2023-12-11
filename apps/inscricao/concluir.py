from .models import Inscricao

def analisarInscricao(inscricao, info_acad, concurso, certificados, carga_horaria, termo):
    if inscricao and info_acad and concurso and certificados and carga_horaria and termo:
        inscricao.concluido = True
        inscricao.save(force_update=True)
    else:
        inscricao.concluido = False
        inscricao.save(force_update=True)
    return  ''
