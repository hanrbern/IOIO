# **IOIO Game**
#### This app is based off of a social learning game: Inferring on the Intentions of Others, as developed by [Andreea Diaconescu](https://doi.org/10.1371/journal.pcbi.1003810)
##### Results can link with parameter testing, developed by [Hannah Bernstein](https://github.com/hanrbern) and [David Rene](https://github.com/dreneuw) using the [Compi Toolbox](https://github.com/andreeadiaconescu/compi).


Running the game requires the following files:
- main.py
- database.py
- my.kv
- all png files

Description of the text files
- subjects.txt
    - Subject ID with date and time created
    - First column is correct colour: 0 - blue, 1 - green
    - Second column is probability of blue in the pie chart: value between 0.25 and 0.75
    - Third column is probability of adviser giving right advice: blocks of 10 between 0.1 and 0.9
    - Fourth column is colour selected by subject: 0 - blue, 1 - green
- IOIO.txt
    - Subject ID with date and time created
    - User's response to how helpful the adviser has been after 25, 50 and 75 rounds

Additional files:
- piechart.py
    - creates pie charts for the game 
    - must save each as a png file to use in the game


