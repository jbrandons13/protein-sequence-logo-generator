from flask import Flask, render_template, request, url_for
import pandas as pd
import logomaker as lm
import numpy as np
from matplotlib.figure import Figure
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process():
    text = request.form['text']
    if not text.isupper():
        return "Please enter uppercase letters only.", 400
    
    input = text.split('\r\n')

    if(len(input) > 16):
        return "The maximum number of sequences is 16", 400
    
    if(len(input) > 1):
        for i in range (len(input)-1):
            if (len(input[i]) != len(input[i+1])):
                return "The sequences length must be the same.", 400
            
    for i in range(len(input)):
        if (len(input[i]) > 16):
            return "The maximum length for each sequence is 16", 400
    
    tranform_input = ['' for _ in range(16)]
    for each in input:
        counter = 0
        for letter in each:
            tranform_input[counter] += letter
            counter += 1
    input = [item for item in tranform_input if item != '']

    amino_acids = list('ACDEFGHIKLMNPQRSTVWY')

    base_dict = {aa: 0 for aa in amino_acids}

    data = [base_dict.copy() for _ in range(20)]
            
    count = 0
    for each in input:
        for letter in each:
            data[count][letter] += 1
        count += 1
    
    newlist = []
    for each in data:

        total_count = sum(each.values())
        f = {amino_acid: (count / total_count if count != 0 else 0) for amino_acid, count in each.items()}
        newlist.append(f)

    filtered_list = [d for d in newlist if any(value != 0 for value in d.values())]
    output = base_dict
    for each in output:
        output[each] = []
        
    for each in filtered_list:
        for letter, count in each.items():
            output[letter].append(count)
            
    nt_df = pd.DataFrame(output)
    nt_df = lm.transform_matrix(nt_df, from_type='probability', to_type='information')

    print(nt_df)
    colors = {
    'A': '#1f77b4', 
    'C': '#ff7f0e', 
    'D': '#2ca02c', 
    'E': '#d62728', 
    'F': '#9467bd', 
    'G': '#8c564b', 
    'H': '#e377c2', 
    'I': '#7f7f7f', 
    'K': '#bcbd22', 
    'L': '#17becf', 
    'M': '#9edae5', 
    'N': '#aec7e8', 
    'P': '#ffbb78', 
    'Q': '#98df8a', 
    'R': '#ff9896', 
    'S': '#c5b0d5', 
    'T': '#c49c94', 
    'V': '#f7b6d2', 
    'W': '#c7c7c7', 
    'Y': '#dbdb8d'
    }
    
    fig = Figure(figsize=(10, 5))  
    ax = fig.subplots()
    logo = lm.Logo(nt_df, ax=ax, color_scheme=colors)

    ax.set_xlabel("Position in Sequence", fontsize=12)
    ax.set_ylabel("Information (bits)", fontsize=12)

    ax.tick_params(axis='both', which='major', labelsize=12)

    logo.style_glyphs(linewidth=2)

    ax.set_title("Sequence Logo", fontsize=16)

    ax.set_xticks(range(0, len(nt_df.index)))

    formats = ['png','jpg','svg']
    img_filenames = {}
    for img_format in formats:
        img_filename = f"logo.{img_format}"
        fig.savefig(os.path.join('static',img_filename), format=img_format)
        img_filenames[img_format] = url_for('static', filename=img_filename)
    
    return render_template('result.html', img_filenames = img_filenames)

if __name__ == '__main__':
    app.run()