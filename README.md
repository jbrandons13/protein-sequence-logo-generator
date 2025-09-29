# Protein Sequence Logo Generator

A simple **Flask web application** to generate **sequence logos** from protein sequences. 

Sequence logos are graphical representations of the conservation of amino acids at each position in a set of aligned sequences, showing the most frequent residues at each position.

## Features

- Input up to 16 protein sequences at a time.
- Maximum sequence length: 16 amino acids.
- Validates input to ensure proper formatting.
- Generates sequence logos in **PNG, JPG, and SVG** formats.
- Displays sequence logos with custom colors for each amino acid.
- Shows information content (bits) for each position.

## Technologies

- **Python 3**
- **Flask** - Web framework
- **Pandas** - Data handling
- **Logomaker** - Sequence logo generation
- **Matplotlib** - Plotting
