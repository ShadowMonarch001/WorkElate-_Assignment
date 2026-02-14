
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer


class MemoryFAISS:
    def __init__(self):
        self.model = SentenceTransformer('all-MiniLM-L6-v2')  # lightweight embedding model
        self.dim = 384
        self.index = faiss.IndexFlatL2(self.dim)
        self.data = []  # store {'section': str, 'content': str}

    def load_from_json(self, filepath="launch_plan.json"):
        import json, os

        if not os.path.exists(filepath):
            return False

        with open(filepath, "r") as f:
            plan = json.load(f)

        self.index = faiss.IndexFlatL2(self.dim)
        self.data = []

        for section_name, section_data in plan.items():
            content_text = json.dumps(section_data["content"])
            self.store(section_name, content_text)

        return True
    
    def store(self, section_name, content):
        emb = self.model.encode([content])
        self.index.add(np.array(emb, dtype=np.float32))
        self.data.append({'section': section_name, 'content': content})

    def retrieve_relevant(self, query, k=3):

        if len(self.data) == 0:
            return []

        query_emb = self.model.encode([query])
        D, I = self.index.search(np.array(query_emb, dtype=np.float32), k)

        results = []
        for idx in I[0]:
            if idx < len(self.data):
                results.append(self.data[idx])

        return results
    
    def answer_question(self,question, memory, llm):

        if len(memory.data) == 0:
            return "No business plan found. Please generate a plan first."

        context_chunks = memory.retrieve_relevant(question)

        context = ""
        for item in context_chunks:
            context += f"\nSection: {item['section']}\nContent: {item['content']}\n"

        prompt = f"""
        You are a SaaS strategy advisor.

        Business Plan Context:
        {context}

        Question:
        {question}
        """

        return llm(prompt)

