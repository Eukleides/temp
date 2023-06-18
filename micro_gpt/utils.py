import glob, os
from PyPDF2 import PdfReader
import tiktoken
import torch

def set_seed(seed):
    torch.manual_seed(seed)

# extract all the text from a pdf file
def extract_text_from_pdf(doc, npages=None, verbose=False):
    reader = PdfReader(doc)

    n = len(reader.pages)
    if npages is not None:
        npages = min(npages, n)
    else:
        npages = n

    if verbose:
        print(f'You have {n:,} page(s) in your file, loading {npages:,}')

    text = ''
    for i in range(npages):
        text += reader.pages[i].extract_text()

    return text

def get_all_files_ending_with(txt='pdf', folder='data'):
    res = []
    for file in glob.glob(f'{folder}\\*.{txt}'):
        res.append(file)
    return res

def load_encoding(enc='gpt2', verbose=False):
    enc = tiktoken.encoding_for_model(enc)
    vocab_size = enc.n_vocab
    if verbose:
        print(f'Vocabulary size={vocab_size:,}')
    return enc, vocab_size


def in_progress_token_extraction():
    enc, vocab_size = load_encoding('gpt2')
    pdfs = get_all_files_ending_with('pdf')

    for book in pdfs:
        text = extract_text_from_pdf(book)
        tokens_integer = enc.encode(text)
        tokens_string = enc.decode(tokens_integer)

        ntokens = len(tokens_integer)

        assert len(tokens_string) == len(text), 'incompatible token count'

        print(f'Vocabulary size: {vocab_size:,} tokens.')

        print(f'Book name: {book}, Number of tokens: {ntokens:,}\n'
              f'Total characters: {len(tokens_string):,}\n'
              f'Average characters per token: {float(len(text) / ntokens):.1f}\n'
              f'------------------------------------------------------')