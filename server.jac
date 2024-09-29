<<<<<<< HEAD
import:py from mtllm.llms {Ollama}

glob llm = Ollama(model_name='llama3.1');

import:jac from rag {RagEngine}
glob rag_engine:RagEngine = RagEngine();

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
}

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

    can chat with Session entry {
        here.chat_history.append({"role": "user", "content": self.message});
        data = rag_engine.get_from_chroma(query=self.message);
        response = here.llm_chat(
            message=self.message,
            chat_history=here.chat_history,
            agent_role="You are a conversation agent designed to help users with their queries based on the documents provided",
            context=data
        );

        here.chat_history.append({"role": "assistant", "content": response});

        report {"response": response};
    } 
}


=======
walker interact {
    can return_message with `root entry {
        report {
            "response": "Hello, world!"
        };
    }
}

walker interact_with_body {
    has name: str;

    can return_message with `root entry {
        report {
            "response": "Hello, " + self.name + "!"
        };
    }
}

walker add_numbers {
    has num1: int;
    has num2: int;

    can calculate with `root entry {
        result = self.num1 + self.num2;
        report {
            "result": result,
            "message": "The sum of num1 and num2 is calculated successfully!"
        };
    }
}

walker greet_user {
    has name: str;

    can say_hello with `root entry {
        greeting = "Hello, " + self.name + "! Welcome!";
        report {
            "greeting": greeting,
            "message": "User greeted successfully!"
        };
    }
}
>>>>>>> fb79c329fecc862336b50d344592f4b92e7c3c5a

