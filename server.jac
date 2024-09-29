import:py from mtllm.llms {Ollama}

glob llm = Ollama(model_name='llama3.1');

import:jac from rag {RagEngine}
glob rag_engine:RagEngine = RagEngine();

walker interact {
    has message: str;
    has session_id: str;

    can init_session with `root entry {
         visit [-->](`?Session)(?id == self.session_id) else {
            session_node = here ++> Session(id=self.session_id, chat_history=[], status=1);
            print("Session Node Created");

            visit session_node;
        }
    }

    # """"
    # can chat with Session entry {
    #     here.chat_history.append({"role": "user", "content": self.message});
    #     data = rag_engine.get_from_chroma(query=self.message);
    #     response = here.llm_chat(
    #         message=self.message,
    #         chat_history=here.chat_history,
    #         agent_role="You are a conversation agent designed to help users with their queries based on the documents provided",
    #         context=data
    #     );

    #     here.chat_history.append({"role": "assistant", "content": response});

    #     report {"response": response};
    # } """"
}

node Session {
    has id: str;
    has chat_history: list[dict];
    has status: int = 1;

    can 'Respond to message using chat_history as context and agent_role as the goal of the agent'
    llm_chat(
        message:'current message':str,
        chat_history: 'chat history':list[dict],
        agent_role:'role of the agent responding':str,
        context:'retrieved context from documents':list
    ) -> 'response':str by llm();

    can chat with interact entry {
            self.chat_history.append({"role": "user", "content": here.message});
            response = infer(message=here.message, chat_history=self.chat_history) spawn root;
            self.chat_history.append({"role": "assistant", "content": response.response});

            report {
                "response": response.response
            };
        }
}

enum ChatType {
    RAG : 'Need to use Retrievable information in specific documents to respond' = "RAG",
    QA : 'Given context is enough for an answer' = "user_qa",
    FAQ : 'Commonly asked questions stored in a knowledge base' = "faq"
}

node Router {
    can 'route the query to the appropriate task type'
    classify(message:'query from the user to be routed.':str) -> ChatType by llm(method="Reason", temperature=0.0);
}

node Chat {
    has chat_type: ChatType;
}

walker infer {
    has message:str;
    has chat_history: list[dict];

    can init_router with `root entry {
        visit [-->](`?Router) else {
            router_node = here ++> Router();
            router_node ++> RagChat();
            router_node ++> QAChat();
            router_node ++> FAQChat();
            visit router_node;
        }
    }

    can route with Router entry {
        classification = here.classify(message = self.message);
        visit [-->](`?Chat)(?chat_type==classification);
    }
}

node RagChat :Chat: {
    has chat_type: ChatType = ChatType.RAG;

    can respond with infer entry {
        can 'Respond to message using chat_history as context and agent_role as the goal of the agent'
        respond_with_llm(   message:'current message':str,
                    chat_history: 'chat history':list[dict],
                    agent_role:'role of the agent responding':str,
                    context:'retirved context from documents':list
                        ) -> 'response':str by llm();
        data = rag_engine.get_from_chroma(query=here.message);
        here.response = respond_with_llm(here.message, here.chat_history, "You are a conversation agent designed to help users with their queries based on the documents provided", data);
    }
}

node QAChat :Chat: {
    has chat_type: ChatType = ChatType.QA;

    can respond with infer entry {
        can 'Respond to message using chat_history as context and agent_role as the goal of the agent'
        respond_with_llm(   message:'current message':str,
            chat_history: 'chat history':list[dict],
            agent_role:'role of the agent responding':str
                ) -> 'response':str by llm();
        here.response = respond_with_llm(here.message, here.chat_history, agent_role="You are a conversation agent designed to help users with their queries");
    }
}

node FAQChat :Chat: {
    has chat_type: ChatType = ChatType.FAQ;

    can respond with infer entry {
        can 'Respond to message using chat_history as context and agent_role as the goal of the agent'
        respond_with_llm(   message:'current message':str,
                    agent_role:'role of the agent responding':str,
                    context:'retirved context from documents':list
                        ) -> 'response':str by llm();
        faq_data = {
            "What is your name?": "I am a chatbot created to assist with queries.",
            "What is the weather like today?": "I cannot answer that right now, please check a weather service."
        };
        here.response = respond_with_llm(here.message, "You are a conversation agent designed to answer the frequently asked questions from the data", faq_data);
    }
}








