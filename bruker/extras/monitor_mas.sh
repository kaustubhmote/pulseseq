#!/bin/bash



# Configuration
server="kaustubh@10.10.0.47"  
remote_folder="/opt/topspin3.5pl7/prog/logfiles"    

mas_file=$1

# Rsync the file
if ! rsync "$server:$remote_folder/$mas_file" "$mas_file"; then
  echo "Failed to rsync file '$mas_file'."
  exit 1
fi

# file_a=`ssh $server ls -ht $remote_folder | head -2 | awk "NR==1"`
# file_b=`ssh $server ls -ht $remote_folder | head -2 | awk "NR==2"`

# echo $file_a
# echo $file_b


# # if [[ -z "$mas_file" ]]; then
# #   echo "Usage: $0 <filename>"
# #   exit 1
# # fi

# # Rsync the file
# if ! rsync "$server:$remote_folder/$file_a" "$file_a"; then
#   echo "Failed to rsync file '$file_a'."
#   exit 1
# fi
# if ! rsync "$server:$remote_folder/$file_b" "$file_b"; then
#   echo "Failed to rsync file '$file_a'."
#   exit 1
# fi


# if [[ `awk 'NR==2' $file_a` = "# Bruker MAS Unit record file                                   #" ]]; then
#     mas_file=$file_a
# fi

# if [[ `awk 'NR==2' $file_b` = "# Bruker MAS Unit record file                                   #" ]]; then
#     mas_file=$file_b
# fi

# if [[ `awk 'NR==2' $file_a` = "# Bruker VTU record file                                    #" ]]; then
#     temp_file=$file_a
# fi

# if [[ `awk 'NR==2' $file_b` = "# Bruker VTU record file                                    #" ]]; then
#     temp_file=$file_b
# fi

# Check if the file exists locally now
if [[ ! -f "$mas_file" ]]; then
  echo "Error: File '$mas_file' not found after rsync."
  exit 1
fi




echo " "
echo "==================================="
echo "===   Table for Last 1 Minute   ==="
echo "==================================="
echo " "





tail -5 "$mas_file" | column -s , -t -N Date,MAS,MASs,Lock,SysPres,SysPres2,Bearing,Sense,Drive,Temp -H MASs,SysPres2


echo " "
echo "==================="
echo "===   Summary   ==="
echo "==================="
echo " "


tail -10 "$mas_file" | awk -F',' '
BEGIN {
 name[2] = "MAS"; name[5] = "System Pressure"; name[7] = "Bearing"; name[8] = "Sense"; name[9] = "Drive"; name[10] = "Temp";
}

{
   s[2] += $2;    s[5] += $5;    s[7] += $7;    s[8] += $8;    s[9] += $9;    s[10] += $10;
  sq[2] += $2^2; sq[5] += $5^2; sq[7] += $7^2; sq[8] += $8^2; sq[9] += $9^2; sq[10] += $10^2;
}

END {
  for (c in s) {
    printf "%s: %.0f +/- %.0f \n", name[c], s[c]/NR, sqrt((sq[c] - s[c]^2/NR)/NR);
  }
}

' | column 
