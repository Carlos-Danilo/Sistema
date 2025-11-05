import json
from datetime import datetime
from models.dao import DAO

class Feedback:
    def __init__(self, id, id_cliente, id_profissional, id_servico, nota, comentario, data=None):
        self.set_id(id)
        self.set_id_cliente(id_cliente)
        self.set_id_profissional(id_profissional)
        self.set_id_servico(id_servico)
        self.set_nota(nota)
        self.set_comentario(comentario)
        self.__data = data if data else datetime.now()


    def get_id(self): return self.__id
    def get_id_cliente(self): return self.__id_cliente
    def get_id_profissional(self): return self.__id_profissional
    def get_id_servico(self): return self.__id_servico
    def get_nota(self): return self.__nota
    def get_comentario(self): return self.__comentario
    def get_data(self): return self.__data


    def set_id(self, id): self.__id = id
    def set_id_cliente(self, id_cliente): self.__id_cliente = id_cliente
    def set_id_profissional(self, id_profissional): self.__id_profissional = id_profissional
    def set_id_servico(self, id_servico): self.__id_servico = id_servico
    def set_nota(self, nota):
        if nota < 1 or nota > 5:
            raise ValueError("A nota deve ser entre 1 e 5")
        self.__nota = nota
    def set_comentario(self, comentario):
        self.__comentario = comentario.strip() if comentario else ""
    def to_json(self):
        return {
            "id": self.__id,
            "id_cliente": self.__id_cliente,
            "id_profissional": self.__id_profissional,
            "id_servico": self.__id_servico,
            "nota": self.__nota,
            "comentario": self.__comentario,
            "data": self.__data.isoformat()
        }

    @staticmethod
    def from_json(dic):
        data = datetime.fromisoformat(dic["data"]) if "data" in dic else None
        return Feedback(dic["id"], dic["id_cliente"], dic["id_profissional"], dic["id_servico"],
                        dic["nota"], dic["comentario"], data)


class FeedbackDAO(DAO):
    @classmethod
    def abrir(cls):
        cls._objetos = []
        try:
            with open("feedback.json", "r") as arquivo:
                list_dic = json.load(arquivo)
                for dic in list_dic:
                    cls._objetos.append(Feedback.from_json(dic))
        except FileNotFoundError:
            pass

    @classmethod
    def salvar(cls):
        with open("feedback.json", "w") as arquivo:
            json.dump(cls._objetos, arquivo, default=Feedback.to_json)
