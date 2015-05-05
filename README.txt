Read me : 

Requirements :
--------------

python3 or above is required.

Install :
---------

Copy files from following link and paste it where even you like. 

https://github.com/vnalluri141/easyPresentation

How to Use : 
------------
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

After finishing a text  file just run python easyPresentation.py [optional args] <input_file.txt>

Adding new templates : 
----------------------

New templates can be added by following below simple steps :

1. Make sure slider worksfor <div> or <sections> or any tag that can have text content.
2. Place '--slide content--' key word where all the generated <div> shouls be placed
3. Should include the details of following attributes in config file 

Template id : <unique_id>
Template name : <Name of the main html file in which geenerated div slides should go in>
Template path : <path of the template>
current slide : <Html tag element syntax of currently selected slide element> ex : <div style="display: inline-block;">  # It can be same as all slides value, this depends on template design
all slides : <Html tag element syntax of slide element> ex : <div style="display: none;"> 

