# Function that scrapes description of function of a gene from genecards.org.
# url containing gene name is contacted and html file copied to script. Next, html is dissected to get the UNIPROT description on the genecards site.
# To do so, constant expression before and after description are searched for, sliced and html tags removed. If a gene does not have a description, return "no entry found".


# To use the script, run the following in terminal: python Genecards_get_gene_function.py GENENAME


import urllib2
import httplib 
import re
import sys

def getfunction(gene_name='PTEN'):
    '''
    This function scrapes the Uniprot description of a gene from genecards.org
    '''

    try:
        url='http://www.genecards.org/cgi-bin/carddisp.pl?gene='+str(gene_name)
        html_response = urllib2.urlopen(url)
        html_output=html_response.read()  #return information from url
        search_string_start='GeneCards Summary'
        match_start=html_output.find(search_string_start)
        html_output=html_output[match_start:]
        search_string_start='Function</b>:  '
        match_start=html_output.find(search_string_start)
        if match_start!=-1:
            match_start=match_start+len(search_string_start)
            html_output=html_output[match_start:]
            search_string_end='<TD align=center valign=top><a name=genomic_location></a><center>'
            match_end=html_output.find(search_string_end)
            if match_end!=-1:
                html_output=html_output[:match_end]
                extract_string=re.sub(r'\<.{0,3}>',' ', html_output)
                extract_string=re.sub(r'\  ',' ', extract_string)
                try:
                    find_wiki=extract_string.find('Gene Wiki')+1
                    if find_wiki>1: 
                        extract_string=extract_string[:find_wiki].strip()
                except:
                    extract_string=extract_string.strip()
                try:
                    find_tocris=extract_string.find('<img src="/pics/tocris_small.gif" valign="top">')
                    extract_string=extract_string[:find_tocris].strip()
                except:
                    extract_string=extract_string.strip()
            else:
                extract_string='no entry found'
        else:
            extract_string='no entry found'
    except ValueError:
        extract_string='no entry found'
    except httplib.IncompleteRead, e:
    	html_output=e.partial
    return extract_string

gene_name=sys.argv[1]
print 'Gene:'+'\t'+gene_name
print 'Function:'+'\t'+getfunction(gene_name)
