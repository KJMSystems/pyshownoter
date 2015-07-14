# python-thursday
This is the package for compiling headers and links from chats

## Requirements:
beautifulsoup4==4.3.2
Flask==0.10.1
Flask-WTF==0.11
gunicorn==19.3.0
itsdangerous==0.24
Jinja2==2.7.3
lxml==3.4.4
Markdown==2.6.2
MarkupSafe==0.23
requests==2.7.0
Werkzeug==0.10.4
WTForms==2.0.2

### Setting Categories
The default category is "Uncategorized". To set a new category. Enter the "#" Followed by the Category. The whole line will be accepted as the category.

### Setting Links:
To add a link just enter the link by itself. There is no need for a title, as pt shownotes will find one for you. 

Accepted Links:
* [http://www.link.com][0]
* [https://www.link.com][0]
* [www.link.com][0]
* link.com

If a link fails to be read (i.e. bad syntax or false detection of a link). A "*\<link\>* Failed" will be returned and it will process the next link.

All links will belong to the previous set category

####Example
> This is some regular text to be ignored

>  \#Category1

> More random text to be ignored

> linktosite1.com

> [www.linktosite.com][0] 

> \#Category2

>[https://linktosite3/web/blog/otherthings?test][0]

will produce:

> ##Category1
>* [sitetitle1]\(linktosite1.com \)
>* [sitetitle2]\([www.linktosite.com][0] \)

> ##Category2
>* [sitetitle3]\(https://linktosite3/web/blog/otherthings?test \)

[0]:#null
