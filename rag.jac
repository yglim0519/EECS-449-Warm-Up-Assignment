import:py from langchain_community.document_loaders {PyPDFDirectoryLoader};
import:py from langchain_text_splitters {RecursiveCharacterTextSplitter};
import:py from langchain.schema.document {Document};
import:py from langchain_community.embeddings.ollama {OllamaEmbeddings};
import:py from langchain_community.vectorstores.chroma {Chroma};

obj RagEngine {
    has file_path: str = "docs";
    has chroma_path: str = "chroma";

    can postinit {
        documents: list = self.load_documents();
        chunks: list = self.split_documents(documents);
        self.add_to_chroma(chunks);
    }

    can load_documents {
        document_loader = PyPDFDirectoryLoader(self.file_path);
        return document_loader.load();
    }

    can split_documents(documents: list[Document]) {
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=80);
        return text_splitter.split_documents(documents);
    }

    can get_embedding_function {
        embeddings = OllamaEmbeddings(model='nomic-embed-text');
        return embeddings;
    }

    can add_to_chroma(chunks: list[Document]) {
        db = Chroma(persist_directory=self.chroma_path, embedding_function=self.get_embedding_function());
        chunks_with_ids = self.add_chunk_id(chunks);
        db.add_documents(chunks_with_ids);
    }

    can get_from_chroma(query: str, chunck_nos: int=5) {
        db = Chroma(persist_directory=self.chroma_path, embedding_function=self.get_embedding_function());
        return db.similarity_search_with_score(query, k=chunck_nos);
    }

    can add_chunk_id(chunks: list[Document]) {
        # Assign chunk IDs based on source, page number, etc.
        ...
        return chunks;
    }
}



