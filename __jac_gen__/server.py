from __future__ import annotations
<<<<<<< HEAD
from jaclang import jac_import as __jac_import__
import typing as _jac_typ
from jaclang.plugin.feature import JacFeature as _Jac
from jaclang.plugin.builtin import *
from dataclasses import dataclass as __jac_dataclass__
if _jac_typ.TYPE_CHECKING:
    from mtllm.llms import Ollama
else:
    Ollama, = __jac_import__(target='mtllm.llms', base_path=__file__, lng='py', absorb=False, mdl_alias=None, items={'Ollama': None})
llm = Ollama(model_name='llama3.1')
if _jac_typ.TYPE_CHECKING:
    from rag import RagEngine
else:
    RagEngine, = __jac_import__(target='rag', base_path=__file__, lng='jac', absorb=False, mdl_alias=None, items={'RagEngine': None})
rag_engine: RagEngine = RagEngine()

@_Jac.make_node(on_entry=[], on_exit=[])
@__jac_dataclass__(eq=False)
class Session(_Jac.Node):
    id: str
    chat_history: list[dict]
    status: int = _Jac.has_instance_default(gen_func=lambda: 1)

    def llm_chat(self, message: str, chat_history: list[dict], agent_role: str, context: list) -> str:
        return _Jac.with_llm(file_loc=__file__, model=llm, model_params={}, scope='server(Module).Session(node).llm_chat(Ability)', incl_info=[], excl_info=[], inputs=[('current message', str, 'message', message), ('chat history', list[dict], 'chat_history', chat_history), ('role of the agent responding', str, 'agent_role', agent_role), ('retrieved context from documents', list, 'context', context)], outputs=('response', 'str'), action='Respond to message using chat_history as context and agent_role as the goal of the agent', _globals=globals(), _locals=locals())

@_Jac.make_walker(on_entry=[_Jac.DSFunc('init_session', _Jac.RootType), _Jac.DSFunc('chat', Session)], on_exit=[])
@__jac_dataclass__(eq=False)
class interact(_Jac.Walker):
    message: str
    session_id: str

    def init_session(self, _jac_here_: _Jac.RootType) -> None:
        if _Jac.visit_node(self, (lambda x: [i for i in x if i.id == self.session_id])((lambda x: [i for i in x if isinstance(i, Session)])(_Jac.edge_ref(_jac_here_, target_obj=None, dir=_Jac.EdgeDir.OUT, filter_func=None, edges_only=False)))):
            pass
        else:
            session_node = _Jac.connect(left=_jac_here_, right=Session(id=self.session_id, chat_history=[], status=1), edge_spec=_Jac.build_edge(is_undirected=False, conn_type=None, conn_assign=None))
            print('Session Node Created')
            if _Jac.visit_node(self, session_node):
                pass

    def chat(self, _jac_here_: Session) -> None:
        _jac_here_.chat_history.append({'role': 'user', 'content': self.message})
        data = rag_engine.get_from_chroma(query=self.message)
        response = _jac_here_.llm_chat(message=self.message, chat_history=_jac_here_.chat_history, agent_role='You are a conversation agent designed to help users with their queries based on the documents provided', context=data)
        _jac_here_.chat_history.append({'role': 'assistant', 'content': response})
        _Jac.report({'response': response})
=======
from jaclang.plugin.feature import JacFeature as _Jac
from jaclang.plugin.builtin import *
from dataclasses import dataclass as __jac_dataclass__

@_Jac.make_walker(on_entry=[_Jac.DSFunc('return_message', _Jac.RootType)], on_exit=[])
@__jac_dataclass__(eq=False)
class interact(_Jac.Walker):

    def return_message(self, _jac_here_: _Jac.RootType) -> None:
        _Jac.report({'response': 'Hello, world!'})

@_Jac.make_walker(on_entry=[_Jac.DSFunc('return_message', _Jac.RootType)], on_exit=[])
@__jac_dataclass__(eq=False)
class interact_with_body(_Jac.Walker):
    name: str

    def return_message(self, _jac_here_: _Jac.RootType) -> None:
        _Jac.report({'response': 'Hello, ' + self.name + '!'})

@_Jac.make_walker(on_entry=[_Jac.DSFunc('calculate', _Jac.RootType)], on_exit=[])
@__jac_dataclass__(eq=False)
class add_numbers(_Jac.Walker):
    num1: int
    num2: int

    def calculate(self, _jac_here_: _Jac.RootType) -> None:
        result = self.num1 + self.num2
        _Jac.report({'result': result, 'message': 'The sum of num1 and num2 is calculated successfully!'})

@_Jac.make_walker(on_entry=[_Jac.DSFunc('say_hello', _Jac.RootType)], on_exit=[])
@__jac_dataclass__(eq=False)
class greet_user(_Jac.Walker):
    name: str

    def say_hello(self, _jac_here_: _Jac.RootType) -> None:
        greeting = 'Hello, ' + self.name + '! Welcome!'
        _Jac.report({'greeting': greeting, 'message': 'User greeted successfully!'})
>>>>>>> fb79c329fecc862336b50d344592f4b92e7c3c5a
