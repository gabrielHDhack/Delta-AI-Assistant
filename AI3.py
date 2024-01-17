import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, TensorDataset
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.preprocessing import LabelEncoder
import spacy
import json

# Carregar modelo spaCy para NLP
nlp = spacy.load("en_core_web_lg")

with open('data3.json', 'r') as file:
    data = json.load(file)

questions = [entry['question'] for entry in data]
answers = [entry['answer'] for entry in data]

# Utilizar spaCy para tokenização
tokenized_questions = [" ".join([token.text.lower() for token in nlp(question)]) for question in questions]

vectorizer = CountVectorizer()
X = vectorizer.fit_transform(tokenized_questions).toarray()

label_encoder = LabelEncoder()
y = label_encoder.fit_transform(answers)

X_tensor = torch.tensor(X, dtype=torch.float32)
y_tensor = torch.tensor(y, dtype=torch.long)

dataset = TensorDataset(X_tensor, y_tensor)
dataloader = DataLoader(dataset, batch_size=32, shuffle=True)

class NeuralNetwork(nn.Module):
    def __init__(self, input_size, hidden_sizes, output_size, dropout_rate=0.3):
        super(NeuralNetwork, self).__init__()

        layers = []
        prev_size = input_size

        for hidden_size in hidden_sizes:
            layers.append(nn.Linear(prev_size, hidden_size))
            layers.append(nn.ReLU())
            layers.append(nn.Dropout(dropout_rate))
            prev_size = hidden_size

        layers.append(nn.Linear(prev_size, output_size))

        self.model = nn.Sequential(*layers)

    def forward(self, x):
        return self.model(x)

input_size = X.shape[1]
output_size = len(set(y))
hidden_sizes = [1024, 1024]  # Aumentar a complexidade da rede
dropout_rate = 0.3
neural_net_model = NeuralNetwork(input_size, hidden_sizes, output_size, dropout_rate)
criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(neural_net_model.parameters(), lr=0.001)
total_params = sum(p.numel() for p in neural_net_model.parameters())
print(f'Total de parâmetros no modelo: {total_params}')

num_epochs = 100
for epoch in range(num_epochs):
    for batch_X, batch_y in dataloader:
        optimizer.zero_grad()
        outputs = neural_net_model(batch_X)
        loss = criterion(outputs, batch_y)
        loss.backward()
        optimizer.step()

    print(f'Epoch {epoch + 1}/{num_epochs}, Loss: {loss.item():.4f}')

def predict_answer(question, model, vectorizer, label_encoder):
    # Utilizar spaCy para tokenizar a pergunta
    tokenized_question = " ".join([token.text.lower() for token in nlp(question)])
    
    # Utilizar vetorizador para transformar tokens em vetor
    question_vector = vectorizer.transform([tokenized_question]).toarray()
    question_tensor = torch.tensor(question_vector, dtype=torch.float32)
    
    # Obter a resposta prevista do modelo
    predicted_label = model(question_tensor).argmax().item()
    predicted_answer = label_encoder.inverse_transform([predicted_label])[0]
    return predicted_answer

while True:
    user_question = input("Ask me something (or 'exit' to quit): ")

    if user_question.lower() == 'exit':
        print("Goodbye!")
        break
    else:
        predicted_answer = predict_answer(user_question, neural_net_model, vectorizer, label_encoder)
        print(f'AI: {predicted_answer}')
