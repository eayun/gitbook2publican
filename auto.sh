BASEDIR=$(dirname $0)

rm -rf docbook
python $BASEDIR/im.py $BASEDIR/FileTranslations . docbook/

echo '=================================================='

cd docbook
find . -type f -print0 | xargs -0 sed -i 's/<br>$/\n/g'
find . -type f -print0 | xargs -0 sed -i 's/<\/br>$/\n/g'
find . -type f -print0 | xargs -0 sed -i 's/<br\/>$/\n/g'
find . -type f -print0 | xargs -0 sed -i 's/<\/li><br\/><li>/<\/li><li>/g'
find . -type f -print0 | xargs -0 sed -i 's/<\/li><\/br><li>/<\/li><li>/g'
find . -type f -print0 | xargs -0 sed -i 's/<br\/><br\/>/fanhang/g'
find . -type f -print0 | xargs -0 sed -i 's/<\/br><\/br>/fanhang/g'
find . -type f -print0 | xargs -0 sed -i 's/<\/br><br\/>/fanhang/g'
find . -type f -print0 | xargs -0 sed -i 's/<br\/><\/br>/fanhang/g'
find . -type f -print0 | xargs -0 sed -i 's/<br\/>/fanhang/g'
find . -type f -print0 | xargs -0 sed -i 's/<\/br>/fanhang/g'
find . -type f -print0 | xargs -0 sed -i 's/<ul>/youer/g'
find . -type f -print0 | xargs -0 sed -i 's/<\/ul>/splashyou/g'
find . -type f -print0 | xargs -0 sed -i 's/<ul\/>/splashyou/g'
find . -type f -print0 | xargs -0 sed -i 's/<li>/elouai/g'
find . -type f -print0 | xargs -0 sed -i 's/<\/li>/splashlee/g'
find . -type f -print0 | xargs -0 sed -i 's/<li\/>/splashlee/g'
find . -type f -print0 | xargs -0 sed -i 's/..\/images\//images\//'
find . -type f -print0 | xargs -0 sed -i '1N;$!N;s/\(!\[.*\](.*)\)[\n[ ]*]*\n[ ]*\*\*.*\*\*/\1/;P;D'
python $BASEDIR/con.py ./SUMMARY.md docbook $1
cd docbook
find . -type f -print0 | xargs -0 sed -i 's/sect1/section/g'
find . -type f -print0 | xargs -0 sed -i 's/sect2/section/g'
find . -type f -print0 | xargs -0 sed -i 's/informaltable/table/g'
find . -type f -print0 | xargs -0 sed -i '1N;$!N;s/<para>\n[ ]*<emphasis role="strong">介绍<\/emphasis>\n[ ]*<\/para>/<formalpara><title>介绍<\/title><para><\/para><\/formalpara>/;P;D'
find . -type f -print0 | xargs -0 sed -i '1N;$!N;s/<para>\n[ ]*<emphasis role="strong">概述<\/emphasis>\n[ ]*<\/para>/<formalpara><title>概述<\/title><para><\/para><\/formalpara>/;P;D'
find . -type f -print0 | xargs -0 sed -i '1N;$!N;s/<para>\n[ ]*<emphasis role="strong">结果<\/emphasis>\n[ ]*<\/para>/<formalpara><title>结果<\/title><para><\/para><\/formalpara>/;P;D'
find . -type f -execdir python $BASEDIR/xmlmod.py {} \;
find . -type f -print0 | xargs -0 sed -i 's/\(<imagedata fileref="\)\(.*png" \)\(\/>\)/\1\2format="PNG" scale="100" \3/'
find . -type f -print0 | xargs -0 sed -i 's/fanhang/<\/para><para>/g'
find . -type f -print0 | xargs -0 sed -i 's/<entry>/<entry><para>/g'
find . -type f -print0 | xargs -0 sed -i 's/<\/entry>/<\/para><\/entry>/g'
find . -type f -print0 | xargs -0 sed -i 's/youer/<itemizedlist>/g'
find . -type f -print0 | xargs -0 sed -i 's/splashyou/<\/itemizedlist>/g'
find . -type f -print0 | xargs -0 sed -i 's/elouai/<listitem><para>/g'
find . -type f -print0 | xargs -0 sed -i 's/splashlee/<\/para><\/listitem>/g'

cp -r ../../images/ ./zh-CN
