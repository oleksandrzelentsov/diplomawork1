FILES=$(find -name "*.dia")

for file in $FILES
do
    name="$(basename $file)"
    dia -e "pdf/${name%.*}.pdf" -t pdf $file
done
