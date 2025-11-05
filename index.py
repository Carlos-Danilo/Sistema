import streamlit as st
from templates.manterclienteUI import ManterClienteUI
from templates.manterServicoUI import ManterServicoUI
from templates.manterhorarioUI import ManterHorarioUI
from templates.manterprofissionalUI import ManterProfissionalUI
from templates.alterarsenhaUI import AlterarSenhaUI
from templates.abrircontaUI import AbrirContaUI
from templates.loginUI import LoginUI
from templates.loginUI_P import LoginUI_P
from templates.perfilclienteUI import PerfilClienteUI
from templates.perfilprofissionalUI import PerfilProfissionalUI
from templates.agendarservicoUI import AgendarServicoUI
from templates.gerenciaragenda import GerenciarAgendaUI
from templates.meu_servicoUI import MeusServicosUI
from templates.c_servicoUI import ConfirmarServicoUI
from templates.feedbackAdminUI import FeedbackAdminUI
from templates.feedbackUI import FeedbackUI
from views import View


def reiniciar_app():
    try:
        st.experimental_rerun()
    except AttributeError:
        try:
            st.rerun()
        except Exception as e:
            st.error(f"Não foi possível reiniciar o app automaticamente: {e}")


class IndexUI:
    @staticmethod
    def main():
        View.cliente_criar_admin()
        IndexUI.sidebar()

    @staticmethod
    def menu_visitante():
        op = st.sidebar.selectbox("Menu", ["Entrar no Sistema", "Entrar no Sistema de profissionais", "Abrir Conta"])
        if op == "Entrar no Sistema":
            LoginUI.main()
        if op == "Entrar no Sistema de profissionais":
            LoginUI_P.main()
        if op == "Abrir Conta":
            AbrirContaUI.main()

    @staticmethod
    def menu_cliente():
        op = st.sidebar.selectbox("Menu", ["Meus Dados", "Agendar Serviço", "Meus Serviços", "Deixar Feedback"])
        if op == "Meus Dados":
            PerfilClienteUI.main()
        if op == "Agendar Serviço":
            AgendarServicoUI.main()
        if op == "Meus Serviços":
            MeusServicosUI.main()
        if op == "Deixar Feedback":
            FeedbackUI.main()


    @staticmethod
    def menu_profissional():
        op = st.sidebar.selectbox("Menu", ["Meus Dados", "Gerenciar Agenda", "Confirmar Serviço"])
        if op == "Meus Dados":
            PerfilProfissionalUI.main()
        if op == "Gerenciar Agenda":
            GerenciarAgendaUI.main()
        if op == "Confirmar Serviço":
            ConfirmarServicoUI.main()
       

    @staticmethod
    def menu_admin():
        op = st.sidebar.selectbox("Menu", [
            "Cadastro de Clientes",
            "Cadastro de Serviços",
            "Cadastro de Horários",
            "Cadastro de Profissionais",
            "Alterar Senha",
            "Feedbacks"
        ])
        if op == "Cadastro de Clientes":
            ManterClienteUI.main()
        if op == "Cadastro de Serviços":
            ManterServicoUI.main()
        if op == "Cadastro de Horários":
            ManterHorarioUI.main()
        if op == "Cadastro de Profissionais":
            ManterProfissionalUI.main()
        if op == "Alterar Senha":
            AlterarSenhaUI.main()
        if op == "Feedbacks":
            FeedbackAdminUI.main()


    @staticmethod
    def sair_do_sistema():
        if st.sidebar.button("Sair"):
            del st.session_state["usuario_id"]
            del st.session_state["usuario_nome"]
            reiniciar_app()

    @staticmethod
    def sidebar():
        if "usuario_id" not in st.session_state:
            IndexUI.menu_visitante()
        else:
            admin = st.session_state["usuario_nome"] == "admin"
            profissional = not admin and View.profissional_listar_id(st.session_state["usuario_id"]) is not None
            st.sidebar.write("Bem-vindo(a), " + st.session_state["usuario_nome"])
            if admin:
                IndexUI.menu_admin()
            elif profissional:
                IndexUI.menu_profissional()
            else:
                IndexUI.menu_cliente()
            IndexUI.sair_do_sistema()


IndexUI.main()
