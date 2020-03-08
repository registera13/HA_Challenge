CHILD=$1
PARENTA=$2
PARENTB=$3
CHILD_ID="$(cut -d'_' -f1 <<<"$CHILD")"
OUTF_MID="${CHILD_ID}_child_unique_mid.bed"
OUTF="${CHILD_ID}_child_unique.bed"
echo $OUTF
echo $PARENTB
bedtools subtract -a $CHILD -b $PARENTA -A > $OUTF_MID
bedtools subtract -a $OUTF_MID -b $PARENTB -A > $OUTF
rm $OUTF_MID
