#!/bin/bash

echo 265149 | perl -pae '$o=1;do{$o+=2}until$s=$o**2>=$_;$_=--$o-($s-$_)%$o'
echo
