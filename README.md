# Karoo Tools

Karoo Tools help you prepare your data for Machine Learning runs. Each Tool has one function. The intent is easy to
use, simple to learn. Let me know if I have achieved this goal. An introduction to each Tool is included in the header. 

All data is anticipated to be in the following fomat:
 - comma separated values .csv
 - Apple's Numbers spreadsheet is *not* recommended as their line breaks are non-ASCII standard
 - header contains alpha-numeric names of features (variables)
 - right-most column is the solution (label)
 - left-most column may be the ID (used in the pipeline)
 - rows are instances, but not necessarily steps in time


To learn how to use each tool:

	less karoo_[tool].py

If you combine the fundamental tools Clean, Sort, and Normalize, you'll see the progression of names:

	sample_data.csv
	sample_data-CLEAN.csv
	sample_data-CLEAN-SORT.csv
	sample_data-CLEAN-SORT-NORM.csv

Such that the final dataset is the one prepared for your Machine Learning algorithm.

More tools coming ...
