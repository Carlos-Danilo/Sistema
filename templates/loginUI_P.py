import streamlit as st
from views import View

class LoginUI_P:
    @staticmethod
    def main():
        st.header("Entrar no Sistema de Profissionais")
        email = st.text_input("E-mail")
        senha = st.text_input("Senha", type="password")

        if st.button("Entrar"):
            p = View.profissional_autenticar(email, senha)
            if p is None:
                st.error("E-mail ou senha inválidos")
            else:
                st.session_state["usuario_id"] = p["id"]
                st.session_state["usuario_nome"] = p["nome"]
                st.success("Login realizado com sucesso!")
                st.rerun()
