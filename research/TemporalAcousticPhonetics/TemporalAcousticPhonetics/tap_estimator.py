import torch

class Estimator(torch.nn.Module):

    def __init__(self, return_phoneme_logits=True):

        super(Estimator, self).__init__()

        # Return Phoneme Logits Flag
        self.return_phoneme_logits = return_phoneme_logits

        # Recurrent Layers
        self.lstm = torch.nn.LSTM(
            input_size    = 642  ,
            hidden_size   = 256  ,
            num_layers    = 4    ,
            bidirectional = True ,
            batch_first   = True )

        # Linear Layers
        self.linear1 = torch.nn.Linear(512, 256)
        self.linear2 = torch.nn.Linear(256, 128)
        self.linear3 = torch.nn.Linear(128,  25)
        self.linear4 = torch.nn.Linear( 25,  40)

        # Non-linear Activations
        self.gelu1 = torch.nn.GELU()
        self.gelu2 = torch.nn.GELU()

    def forward(self, spectrogram):

        hidden, _ = self.lstm(spectrogram)
        hidden    = self.linear1(hidden)
        hidden    = self.gelu1(hidden)
        hidden    = self.linear2(hidden)
        hidden    = self.gelu2(hidden)
        acoustics = self.linear3(hidden)

        if self.return_phoneme_logits == True:
            phonemeLogits = self.linear4(acoustics)
            return acoustics, phonemeLogits

        return acoustics
