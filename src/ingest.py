"""Lê o PDF configurado, divide em chunks e grava os embeddings no PostgreSQL/pgVector."""

from langchain_community.document_loaders import PyPDFLoader
from langchain_postgres import PGVector
from langchain_text_splitters import RecursiveCharacterTextSplitter

import config


def ingest() -> None:
    print(f"Carregando PDF: {config.PDF_PATH}")
    loader = PyPDFLoader(config.PDF_PATH)
    documents = loader.load()

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=config.CHUNK_SIZE,
        chunk_overlap=config.CHUNK_OVERLAP,
    )
    chunks = splitter.split_documents(documents)
    print(f"{len(chunks)} chunks gerados (chunk_size={config.CHUNK_SIZE}, overlap={config.CHUNK_OVERLAP})")

    embeddings = config.get_embeddings()

    PGVector.from_documents(
        documents=chunks,
        embedding=embeddings,
        collection_name=config.PG_COLLECTION_NAME,
        connection=config.PG_CONNECTION_STRING,
        use_jsonb=True,
        pre_delete_collection=True,
    )
    print("Ingestão concluída com sucesso.")


if __name__ == "__main__":
    ingest()
