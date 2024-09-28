from __future__ import annotations
from jaclang import jac_import as __jac_import__
import typing as _jac_typ
from enum import Enum as __jac_Enum__, auto as __jac_auto__
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

class ChatType(__jac_Enum__):
    RAG = 'RAG'
    QA = 'user_qa'

@_Jac.make_node(on_entry=[], on_exit=[])
@__jac_dataclass__(eq=False)
class Router(_Jac.Node):

    def classify(self, message: str) -> ChatType:
        return _Jac.with_llm(file_loc=__file__, model=llm, model_params={'method': 'Reason', 'temperature': 0.0}, scope='server(Module).Router(node).classify(Ability)', incl_info=[], excl_info=[], inputs=[('query from the user to be routed.', str, 'message', message)], outputs=('', 'ChatType'), action='route the query to the appropriate task type', _globals=globals(), _locals=locals())

@_Jac.make_node(on_entry=[], on_exit=[])
@__jac_dataclass__(eq=False)
class Chat(_Jac.Node):
    chat_type: ChatType

@_Jac.make_node(on_entry=[_Jac.DSFunc('respond', infer)], on_exit=[])
@__jac_dataclass__(eq=False)
class RagChat(Chat, _Jac.Node):
    chat_type: ChatType = _Jac.has_instance_default(gen_func=lambda: ChatType.RAG)

    def respond(self, _jac_here_: infer) -> None:

        def respond_with_llm(message: str, chat_history: list[dict], agent_role: str, context: list) -> str:
            return _Jac.with_llm(file_loc=__file__, model=llm, model_params={}, scope='server(Module).RagChat(node).respond(Ability).respond_with_llm(Ability)', incl_info=[], excl_info=[], inputs=[('current message', str, 'message', message), ('chat history', list[dict], 'chat_history', chat_history), ('role of the agent responding', str, 'agent_role', agent_role), ('retrieved context from documents', list, 'context', context)], outputs=('response', 'str'), action='Respond to message using chat_history as context and agent_role as the goal of the agent', _globals=globals(), _locals=locals())
        data = rag_engine.get_from_chroma(query=_jac_here_.message)
        _jac_here_.response = respond_with_llm(_jac_here_.message, _jac_here_.chat_history, 'You are a conversation agent designed to help users with their queries based on the documents provided', data)

@_Jac.make_node(on_entry=[_Jac.DSFunc('respond', infer)], on_exit=[])
@__jac_dataclass__(eq=False)
class QAChat(Chat, _Jac.Node):
    chat_type: ChatType = _Jac.has_instance_default(gen_func=lambda: ChatType.QA)

    def respond(self, _jac_here_: infer) -> None:

        def respond_with_llm(message: str, chat_history: list[dict], agent_role: str) -> str:
            return _Jac.with_llm(file_loc=__file__, model=llm, model_params={}, scope='server(Module).QAChat(node).respond(Ability).respond_with_llm(Ability)', incl_info=[], excl_info=[], inputs=[('current message', str, 'message', message), ('chat history', list[dict], 'chat_history', chat_history), ('role of the agent responding', str, 'agent_role', agent_role)], outputs=('response', 'str'), action='Respond to message using chat_history as context and agent_role as the goal of the agent', _globals=globals(), _locals=locals())
        _jac_here_.response = respond_with_llm(_jac_here_.message, _jac_here_.chat_history, agent_role='You are a conversation agent designed to help users with their queries')

@_Jac.make_walker(on_entry=[_Jac.DSFunc('init_router', _Jac.RootType), _Jac.DSFunc('route', Router)], on_exit=[])
@__jac_dataclass__(eq=False)
class infer(_Jac.Walker):
    message: str
    chat_history: list[dict]

    def init_router(self, _jac_here_: _Jac.RootType) -> None:
        if _Jac.visit_node(self, (lambda x: [i for i in x if isinstance(i, Router)])(_Jac.edge_ref(_jac_here_, target_obj=None, dir=_Jac.EdgeDir.OUT, filter_func=None, edges_only=False))):
            pass
        else:
            router_node = _Jac.connect(left=_jac_here_, right=Router(), edge_spec=_Jac.build_edge(is_undirected=False, conn_type=None, conn_assign=None))
            _Jac.connect(left=router_node, right=RagChat(), edge_spec=_Jac.build_edge(is_undirected=False, conn_type=None, conn_assign=None))
            _Jac.connect(left=router_node, right=QAChat(), edge_spec=_Jac.build_edge(is_undirected=False, conn_type=None, conn_assign=None))
            if _Jac.visit_node(self, router_node):
                pass

    def route(self, _jac_here_: Router) -> None:
        classification = _jac_here_.classify(message=self.message)
        if _Jac.visit_node(self, (lambda x: [i for i in x if i.chat_type == classification])((lambda x: [i for i in x if isinstance(i, Chat)])(_Jac.edge_ref(_jac_here_, target_obj=None, dir=_Jac.EdgeDir.OUT, filter_func=None, edges_only=False)))):
            pass

@_Jac.make_node(on_entry=[_Jac.DSFunc('chat', interact)], on_exit=[])
@__jac_dataclass__(eq=False)
class Session(_Jac.Node):
    id: str
    chat_history: list[dict]
    status: int = _Jac.has_instance_default(gen_func=lambda: 1)

    def chat(self, _jac_here_: interact) -> None:
        self.chat_history.append({'role': 'user', 'content': _jac_here_.message})
        response = _Jac.spawn_call(infer(message=_jac_here_.message, chat_history=self.chat_history), _Jac.get_root())
        self.chat_history.append({'role': 'assistant', 'content': response.response})
        _Jac.report({'response': response.response})