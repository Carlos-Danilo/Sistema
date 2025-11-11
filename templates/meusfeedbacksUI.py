import streamlit as st
from views import View

class MeusFeedbacksUI:
    @staticmethod
    def main():
        st.header("Minhas Avaliações")
        if "usuario_id" not in st.session_state:
            st.warning("Você precisa estar logado como profissional.")
            return 
        profissional_id = st.session_state["usuario_id"]
        feedbacks = View.feedback_listar()
        meus_feedbacks = [
            f for f in feedbacks
            if f.get_id_profissional() == profissional_id]
        if len(meus_feedbacks) == 0:
            st.info("Você ainda não recebeu nenhum feedback.")
            return
        for fb in meus_feedbacks:
            cliente = View.cliente_listar_id(fb.get_id_cliente())
            servico = View.servico_listar_id(fb.get_id_servico())
            with st.container(border=True):
                st.write(f" **Nota:** {fb.get_nota()}/5")
                st.write(f" **Cliente:** {cliente.get_nome() if cliente else 'Desconhecido'}")
                st.write(f" **Serviço:** {servico.get_descricao() if servico else 'Indefinido'}")
                st.write(f" **Comentário:** {fb.get_comentario()}")
                st.write(f" **Data:** {fb.get_data().strftime('%d/%m/%Y %H:%M')}")
                st.markdown("---")
