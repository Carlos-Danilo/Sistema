import streamlit as st
import pandas as pd
from views import View

class FeedbackAdminUI:
    @staticmethod
    def main():
        st.header("Feedbacks dos Clientes")

        feedbacks = View.feedback_listar()
        if len(feedbacks) == 0:
            st.info("Nenhum feedback foi registrado ainda.")
            return
        lista = []
        for f in feedbacks:
            cliente = View.cliente_listar_id(f.get_id_cliente())
            profissional = View.profissional_listar_id(f.get_id_profissional())
            servico = View.servico_listar_id(f.get_id_servico())

            lista.append({
                "Data": f.get_data().strftime("%d/%m/%Y %H:%M") if f.get_data() else "-",
                "Cliente": cliente.get_nome() if cliente else "-",
                "Profissional": profissional.get_nome() if profissional else "-",
                "Serviço": servico.get_descricao() if servico else "-",
                "Nota": f.get_nota(),
                "Comentário": f.get_comentario()
            })

        df = pd.DataFrame(lista)
        st.dataframe(df, hide_index=True)
