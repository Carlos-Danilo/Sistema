import streamlit as st
from views import View
import time

class FeedbackUI:
    @staticmethod
    def main():
        st.header("Deixar Feedback")
        if "usuario_id" not in st.session_state:
            st.warning("Você precisa estar logado como cliente para enviar um feedback.")
            return

        cliente_id = st.session_state["usuario_id"]
        horarios = View.horario_listar()
        agendamentos = [
            h for h in horarios 
            if h.get_id_cliente() == cliente_id and h.get_confirmado()
        ]

        if len(agendamentos) == 0:
            st.info("Você não possui serviços confirmados para avaliar.")
            return

        horario = st.selectbox(
            "Selecione um atendimento para avaliar",
            agendamentos,
            format_func=lambda h: f"{h.get_data().strftime('%d/%m/%Y %H:%M')} - {View.profissional_listar_id(h.get_id_profissional()).get_nome()}"
        )

        nota = st.slider("Nota (1 a 5 estrelas)", 1, 5, 5)
        comentario = st.text_area("Comentário", placeholder="Como foi seu atendimento?")

        if st.button("Enviar Feedback"):
            try:
                View.feedback_inserir(
                    cliente_id,
                    horario.get_id_profissional(),
                    horario.get_id_servico(),
                    nota,
                    comentario
                )
                st.success("Feedback enviado com sucesso! Obrigado pela sua avaliação ")
                time.sleep(2)
                st.rerun()
            except ValueError as erro:
                st.error(erro)
