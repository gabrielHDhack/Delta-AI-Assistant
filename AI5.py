import torch
import torch.nn as nn
from torch.utils.data import DataLoader, TensorDataset
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.preprocessing import LabelEncoder
from torch.optim import AdamW
import spacy
import json

nlp = spacy.load("en_core_web_lg")

with open('data3.json', 'r') as file:
    data = json.load(file)

questions = [entry['question'] for entry in data]
answers = [entry['answer'] for entry in data]

tokenized_questions = [" ".join([token.text.lower() for token in nlp(question)]) for question in questions]

vectorizer = CountVectorizer()
X = vectorizer.fit_transform(tokenized_questions).toarray()

label_encoder = LabelEncoder()
y = label_encoder.fit_transform(answers)

X_tensor = torch.tensor(X, dtype=torch.float32)
y_tensor = torch.tensor(y, dtype=torch.long)
dataset = TensorDataset(X_tensor, y_tensor)
dataloader = DataLoader(dataset, batch_size=256, shuffle=True)


class ScalingRandomizedTransformer(nn.Module):
    def __init__(self, input_size, embedding_size, hidden_sizes, output_size, num_layers, dropout_rate=0.2):
        super(ScalingRandomizedTransformer, self).__init__()

        self.embedding = nn.Embedding(input_size, embedding_size)

        self.cnn_layer = nn.Conv1d(embedding_size, hidden_sizes[0], kernel_size=3, padding=1)
        
        self.transformer_layer = nn.TransformerEncoderLayer(embedding_size, nhead=16, batch_first=True)
        self.transformer_encoder = nn.TransformerEncoder(self.transformer_layer, num_layers=2)

        self.lstm_layers = nn.ModuleList([
            nn.LSTM(hidden_sizes[i], hidden_sizes[i+1], batch_first=True) for i in range(num_layers - 1)
        ])
        self.lstm_layers.append(nn.LSTM(hidden_sizes[-2], hidden_sizes[-1], batch_first=True))
        self.dropout_layers = nn.ModuleList([nn.Dropout(dropout_rate) for _ in range(num_layers)])

        self.fc_layers = nn.Sequential(
            nn.Linear(hidden_sizes[-1], hidden_sizes[-1]),
            nn.ReLU(),
            nn.Dropout(dropout_rate),
            nn.Linear(hidden_sizes[-1], hidden_sizes[-1]),
            nn.ReLU(),
            nn.Dropout(dropout_rate),
            nn.Linear(hidden_sizes[-1], output_size)
        )

        for lstm in self.lstm_layers:
            for name, param in lstm.named_parameters():
                if 'bias' in name:
                    nn.init.constant_(param, 0.0)
                elif 'weight' in name:
                    nn.init.xavier_normal_(param)

    def forward(self, x):
        x = self.embedding(x.long())
        x = x.to_dense()
        x = x.permute(0, 2, 1)  
        x = self.cnn_layer(x)
        x = x.permute(0, 2, 1)  
        x = self.transformer_encoder(x)

        for lstm_layer, dropout_layer in zip(self.lstm_layers, self.dropout_layers):
            x, _ = lstm_layer(x)
            x = dropout_layer(x)
        
        x = x.mean(dim=1)

        output = self.fc_layers(x)
        return output


def predict_answer(question, model, vectorizer, label_encoder, confidence_threshold=0.5):
    tokenized_question = " ".join([token.text.lower() for token in nlp(question)])
    
    question_vector = vectorizer.transform([tokenized_question]).toarray()
    question_tensor = torch.tensor(question_vector, dtype=torch.float32)
    
    predicted_scores = model(question_tensor).softmax(dim=1)
    confidence, predicted_label = torch.max(predicted_scores, dim=1)
    
    if confidence.item() > confidence_threshold:
        predicted_answer = label_encoder.inverse_transform([predicted_label])[0]
    else:
        predicted_answer = "I'm not sure."
    
    return predicted_answer, confidence.item()

input_size = X.shape[1]
output_size = len(set(y))
embedding_size = 4096  
hidden_size = [4096, 4096, 4096, 4096, 4096, 4096, 4096] 
num_layers = 6

scaling_randomized_model = ScalingRandomizedTransformer(input_size, embedding_size, hidden_size, output_size, num_layers)
criterion = nn.CrossEntropyLoss()
optimizer = AdamW(scaling_randomized_model.parameters(), lr=0.001)
total_params = sum(p.numel() for p in scaling_randomized_model.parameters())
print(f'Total parameters in the model: {total_params}')

num_epochs = 200
for epoch in range(num_epochs):
    for batch_X, batch_y in dataloader:
        optimizer.zero_grad()
        outputs = scaling_randomized_model(batch_X)
        loss = criterion(outputs, batch_y)
        loss.backward()
        optimizer.step()

    print(f'Epoch {epoch + 1}/{num_epochs}, Loss: {loss.item():.4f}')

while True:
    user_question = input("Ask me something (or 'exit' to quit): ")

    if user_question.lower() == 'exit':
        print("Goodbye!")
        break
    else:
        predicted_answer, confidence = predict_answer(user_question, scaling_randomized_model, vectorizer, label_encoder)
        print(f'AI: {predicted_answer} (Confidence: {confidence * 100:.2f}%)')
