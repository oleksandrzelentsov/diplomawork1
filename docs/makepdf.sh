FILES=$(find -name "*.dia") # get all filenames with whole paths

for file in $FILES # go through all of these files
do
    name="$(basename $file)"                        # remove path info in filename
    newfilename=${name%.*}                          # create new filename extracting extension
    dia -e "pdf/$newfilename.pdf" -t pdf $file      # create pdf
done
