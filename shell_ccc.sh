#!/bin/bash

csv=$1

echo $csv
project_id=$(date +%y_%m_%d_%H_%S)
echo $project_id
if [[ $csv == *.csv ]]; then
	mkdir ~/Documents/shell_ccc/$project_id
	cp $csv ~/Documents/shell_ccc/$project_id/$project_id.csv
else
	echo "file is not a csv file!!!"
fi


echo "Please give sample article_title:"
read article_title
echo "please give sample article_link:"
read article_link
echo "please give sample species:"
read species
echo "please give sample sample_type:"
read sample_type
echo "please give sample treatment info:"
read treatment
echo "please give sample tissue_info:"
read tissue_info


all_info="$project_id,$article_title,$article_link,$species,$sample_type,$treatment,$tissue_info"
echo "$all_info" >> /Users/boyongwei/Documents/shell_ccc/sample_info.csv 


python /Users/boyongwei/Documents/shell_ccc/sql.py --cccfile /Users/boyongwei/Documents/shell_ccc/$project_id/$project_id.csv
echo "updated $project_id"
