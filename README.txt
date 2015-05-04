Read me : 

Install 

Copy files from following link and paste it where even you like. 

How to Use : 

create a text file. 

Start of the text file should be Meta script. i.e styles and properties of whole presentation.

Any style should start with '[' and end with ']'. 

Example : 
	[bgcolor:black]

Multiple styles can be included in single open closed braces, they should be seperated by ';'

Example : 
	[font:calibre; font-size:40px; text-color:white]

Note : Styles declared after '~slidestart' keyword are invalid and will be considered as slide content or plain text

Text included between the key words '~slidestart' and '~slideend' will be created as one slide.

Input text can be either markdown script or html script. 

Please refer to below link for markdown syntax.

[markdown basics] http://daringfireball.net/projects/markdown/basics
[python-markdown] https://pythonhosted.org/Markdown/


Adding new templates : 

New templates can be added by following below simple steps :

1. Make sure slider worksfor <div> or <sections> or any tag that can have text content.
2. Place '--slide content--' key word where all the generated <div> shouls be placed
3. 
