from models.servico import Servico, ServicoDAO
from models.cliente import Cliente, ClienteDAO
from models.horario import Horario, HorarioDAO
from models.feedback import Feedback, FeedbackDAO
from models.profissional import Profissional, ProfissionalDAO
from datetime import datetime


class View:

    #ciente
    def cliente_inserir(nome, email, fone, senha):
        for obj in View.cliente_listar():
            if obj.get_email() == email or email == "admin":
                raise ValueError("E-mail já cadastrado em outro cliente, escolha outro")
        cliente = Cliente(0, nome, email, fone, senha)
        ClienteDAO.inserir(cliente)

    def cliente_listar():
        return ClienteDAO.listar()

    def cliente_listar_id(id):
        return ClienteDAO.listar_id(id)

    def cliente_atualizar(id, nome, email, fone, senha):
        for obj in View.cliente_listar():
            if obj.get_id() != id and obj.get_email() == email:
                raise ValueError("E-mail já cadastrado em outro cliente, escolha outro")
        cliente = Cliente(id, nome, email, fone, senha)
        ClienteDAO.atualizar(cliente)

    def cliente_excluir(id):
        for obj in View.horario_listar():
            if obj.get_id_cliente() == id:
                raise ValueError("Cliente tem agendamentos: não é possível excluir")
        cliente = Cliente(id, "", "", "", "")
        ClienteDAO.excluir(cliente)

    def cliente_criar_admin():
        for c in View.cliente_listar():
            if c.get_email() == "admin":
                return
        View.cliente_inserir("admin", "admin", "fone", "1234")

    def cliente_autenticar(email, senha):
        for c in View.cliente_listar():
            if c.get_email() == email and c.get_senha() == senha:
                return {"id": c.get_id(), "nome": c.get_nome()}
        return None

    #profissional
    def profissional_inserir(nome, especialidade, conselho, email, senha):
        for obj in View.profissional_listar():
            if obj.get_email() == email:
                raise ValueError("E-mail já cadastrado em outro profissional, escolha outro")
        profissional = Profissional(0, nome, especialidade, conselho, email, senha)
        ProfissionalDAO.inserir(profissional)

    def profissional_listar():
        return ProfissionalDAO.listar()

    def profissional_listar_id(id):
        return ProfissionalDAO.listar_id(id)

    def profissional_atualizar(id, nome, especialidade, conselho, email, senha):
        for obj in View.profissional_listar():
            if obj.get_id() != id and obj.get_email() == email:
                raise ValueError("E-mail já cadastrado em outro profissional, escolha outro")
        profissional = Profissional(id, nome, especialidade, conselho, email, senha)
        ProfissionalDAO.atualizar(profissional)

    def profissional_excluir(id):
        for obj in View.horario_listar():
            if obj.get_id_profissional() == id:
                raise ValueError("Profissional tem agendamentos: não é possível excluir")
        ProfissionalDAO.excluir_id(id)

    def profissional_autenticar(email, senha):
        for p in View.profissional_listar():
            if p.get_email() == email and p.get_senha() == senha:
                return {"id": p.get_id(), "nome": p.get_nome()}
        return None

    # serviços
    def servico_listar():
        return ServicoDAO.listar()

    def servico_listar_id(id):
        return ServicoDAO.listar_id(id)

    def servico_inserir(descricao, valor):
        for obj in View.servico_listar():
            if obj.get_descricao() == descricao:
                raise ValueError("Serviço já cadastrado")
        c = Servico(0, descricao, valor)
        ServicoDAO.inserir(c)

    def servico_atualizar(id, descricao, valor):
        for obj in View.servico_listar():
            if obj.get_id() != id and obj.get_descricao() == descricao:
                raise ValueError("Descrição já cadastrada em outro serviço")
        c = Servico(id, descricao, valor)
        ServicoDAO.atualizar(c)

    def servico_excluir(id):
        for obj in View.horario_listar():
            if obj.get_id_servico() == id:
                raise ValueError("Serviço já agendado: não é possível excluir")
        c = Servico(id, "sem descrição", 0)
        ServicoDAO.excluir(c)

    #horários
    def horario_inserir(data, confirmado, id_cliente, id_servico, id_profissional):
        if not isinstance(data, datetime):
            raise ValueError("Data inválida")
        for h in View.horario_listar():
            if h.get_id_profissional() == id_profissional:
                if h.get_data().strftime("%Y-%m-%d %H:%M") == data.strftime("%Y-%m-%d %H:%M"):
                    print(f"Ignorando horário duplicado: {data}")
                    return
        c = Horario(0, data)
        c.set_confirmado(confirmado)
        c.set_id_cliente(id_cliente)
        c.set_id_servico(id_servico)
        c.set_id_profissional(id_profissional)
        HorarioDAO.inserir(c)


    def horario_listar():
        return HorarioDAO.listar()

    def horario_atualizar(id, data, confirmado, id_cliente, id_servico, id_profissional):
        if not isinstance(data, datetime):
            raise ValueError("Data inválida")

        horario = View.horario_listar_id(id)
        if horario is None:
            raise ValueError("Horário não encontrado")
        horario.set_data(data)
        horario.set_confirmado(confirmado)
        horario.set_id_cliente(id_cliente)
        horario.set_id_servico(id_servico)
        horario.set_id_profissional(id_profissional)
        HorarioDAO.atualizar(horario)

    def horario_excluir(id):
        for obj in View.horario_listar():
            if obj.get_id() == id and obj.get_confirmado():
                raise ValueError("Horário confirmado: não é possível excluir")
        HorarioDAO.excluir_id(id)

    def horario_listar_id(id):
        return HorarioDAO.listar_id(id)

    def horario_agendar_horario(id_profissional):
        r = []
        agora = datetime.now()
        for h in View.horario_listar():
            data_horario = h.get_data()
            if isinstance(data_horario, str):
                try:
                    data_horario = datetime.strptime(data_horario, "%Y-%m-%d %H:%M:%S")
                except:
                    continue
            if (
                data_horario >= agora
                and not h.get_confirmado()
                and not h.get_id_cliente()
                and h.get_id_profissional() == id_profissional
            ):
                r.append(h)
        r.sort(key=lambda h: h.get_data())
        return r



     #feedback
    def feedback_inserir(id_cliente, id_profissional, id_servico, nota, comentario):
        f = Feedback(0, id_cliente, id_profissional, id_servico, nota, comentario)
        FeedbackDAO.inserir(f)

    def feedback_listar():
        return FeedbackDAO.listar()

    def feedback_listar_profissional(id_profissional):
        return [f for f in FeedbackDAO.listar() if f.get_id_profissional() == id_profissional]
