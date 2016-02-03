FILES = $(find -name *.dia)

for file in $FILES
do
    dia -e pdf/file.pdf -t pdf
done

in 