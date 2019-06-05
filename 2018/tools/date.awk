#! /usr/bin/awk -f
#


FS = "/"

{
    l = $0;
    m = $1;
    d = $2;

    o = 0;
    if (m>=2) o+= 31;
    if (m>=3) o+= 28;  
    if (m>=4) o+= 31;
    if (m>=5) o+= 30;
    if (m>=6) o+= 31;
    if (m>=7) o+= 30;
    if (m>=8) o+= 31;
    if (m>=9) o+= 31;
    if (m>=10) o+= 30;
    if (m>=11) o+= 31;
    if (m>=12) o+= 30;

    o = o + d
    print o,m,d
	
}
