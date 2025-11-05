import streamlit as st
from views import View
import time
from datetime import datetime

class AgendarServicoUI:
    @staticmethod
    def main():
        st.header("Agendar Serviço")

        if "usuario_id" not in st.session_state:
            st.warning("Você precisa estar logado como cliente para agendar um serviço.")
            return
        profissionais = View.profissional_listar()
        if len(profissionais) == 0:
            st.info("Nenhum profissional cadastrado.")
            return
        profissional = st.selectbox(
            "Selecione o profissional",
            profissionais,
            format_func=lambda p: f"{p.get_nome()} - {p.get_especialidade()}"
        )
        if profissional is None:
            return
        horarios = View.horario_agendar_horario(profissional.get_id())
        if len(horarios) == 0:
            st.info("Nenhum horário disponível para este profissional.")
            return
        horario = st.selectbox(
            "Escolha um horário livre",
            horarios,
            format_func=lambda h: h.get_data().strftime("%d/%m/%Y %H:%M")
        )
        servicos = View.servico_listar()
        if len(servicos) == 0:
            st.warning("Nenhum serviço cadastrado. Peça ao administrador para cadastrar.")
            return

        servico = st.selectbox(
            "Selecione o serviço",
            servicos,
            format_func=lambda s: f"{s.get_descricao()} - R${s.get_valor():.2f}"
        )
        if st.button("Agendar"):
            try:
                View.horario_atualizar(
                    horario.get_id(),
                    horario.get_data(),
                    False,
                    st.session_state["usuario_id"],  # cliente logado
                    servico.get_id(),
                    profissional.get_id()
                )
                st.success("Serviço agendado com sucesso!")
                time.sleep(2)
                st.rerun()
            except ValueError as erro:
                st.error(erro)
