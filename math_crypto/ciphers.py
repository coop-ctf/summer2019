
import re
import pandas as pd
import itertools as it
from scipy.stats import kendalltau, spearmanr

lets = b"ABCDEFGHIJKLMNOPQRSTUVWXYZ"

eng_freqs = pd.read_csv("english_letter_freq.csv", index_col=False,
						keep_default_na=False)
eng_freqs["frequency"] = eng_freqs["frequency"] / 100
eng_freqs["letter"] = eng_freqs["letter"].apply(lambda x: 
												bytes(x, encoding="ascii"))
eng_bigr = pd.read_csv("english_bigrams.csv", index_col=False,
						keep_default_na=False)
eng_bigr["frequency"] = eng_bigr["frequency"] / sum(eng_bigr["frequency"])
eng_bigr["bigram"] = eng_bigr["bigram"].apply(lambda x: 
												bytes(x, encoding="ascii"))

def normalize_text(text) -> bytes:
	if type(text) == str:
		text = bytes(text, encoding="ascii")
	return re.sub(b"[^a-zA-Z]", b"", text).upper()

def shift_cipher(text: bytes, key: int):
	#assert text is normalized
	return bytes([65 + ((x - 65 + key) % 26) for x in text])

def substitution_cipher(text: bytes, key: dict, normalizer=lambda x: x,
						denormalizer=lambda x: x):
	return normalizer([key[denormalizer(x)] for x in text])

def get_frequencies(seq, complete_set=None) -> dict:
	freqs = {}
	for elt in seq:
		if elt not in freqs:
			freqs[elt] = 0
		freqs[elt] += 1
	if complete_set is not None:
		for elt in complete_set:
			if elt not in freqs:
				freqs[elt] = 0
	return freqs

def get_freq_df(seq, complete_set=lets, 
				to_char=(lambda x: bytes([x]))) -> pd.DataFrame:
	freqs = get_frequencies(seq, complete_set)
	df = pd.DataFrame([[x, y] for x, y in freqs.items()],
					columns=["letter", "frequency"]).sort_values("frequency",
														ascending=False)
	if to_char is not None:
		df["letter"] = df["letter"].apply(to_char)
	df["frequency"] = df["frequency"] / sum(df["frequency"])
	df.index = range(len(df))
	return df

def get_bigram_df(seq, 
				  complete_set=map(bytes,
								   it.product(lets, repeat=2)),
				  to_char=None):
	out = get_freq_df(map(bytes, zip(seq[:-1], seq[1:])), 
						complete_set=complete_set,
						to_char=to_char)
	out.columns = ["bigram", "frequency"]
	return out

def shift_freq_analyze(text: bytes, comp=kendalltau) -> bytes:
	shift_corr = {shift:comp(get_freq_df(shift_cipher(text,
													shift))["lets"].tolist(),
							eng_freqs["Letter"].tolist()).correlation 
				for shift in range(26)}
	max_ = max(shift_corr.values())
	return {x for x, y in shift_corr.items() if max_ == y}

## FREQUENCY ANALYSIS

def bigr_comp(c_let, p_let, c_df, p_df=eng_bigr):
    out = 1
    for pos in [0, 1]:
        vecc = bigr_vec(c_let, pos, c_df)["frequency"]
        vecp = bigr_vec(p_let, pos, p_df)["frequency"]
        out *= sum((1/(i+1))*(x - y)**2
                for i, (x, y) in enumerate(zip(vecc, vecp)))
    return out
    
def let_comp(c_let, p_let, c_df, p_df=eng_freqs):
    return sum((c_df[c_df["letter"] == c_let]["frequency"].values
                   - p_df[p_df["letter"] == p_let]["frequency"].values)**2)
    
def bigr_vec(let, pos, df):
    return df[df["bigram"].apply(lambda x: x[pos] in let)]
    
def metric(c_let, p_let, c_freq, c_bigr, p_freq=eng_freqs, p_bigr=eng_bigr):
    return (let_comp(c_let, p_let, c_freq, p_freq)
           *bigr_comp(c_let, p_let, c_bigr, p_bigr))

def frequency_key_mappings(ciphertext):
	c_freqs = get_freq_df(ciphertext)
	c_bigr = get_bigram_df(ciphertext)
	mapping = {}
	for c_let in lets:
		c_let = bytes([c_let])
		dists = {}
		for p_let in lets:
		    p_let = bytes([p_let])
		    dists[p_let] = metric(c_let, p_let, c_freqs, c_bigr)
		mapping[c_let] = sorted(dists.items(), key=lambda x: x[1])
	return mapping
