#!/usr/bin/python

"""
WiKo: this script generates a web pages, PDF article or blog
considering the files found in the local directory.
See http://www.iua.upf.edu/~dgarcia/wiko/usage.html
"""
# Bugs: 
# * @cite:some at end of line, or @cite:some, something.
# * don't work with iso encoding only utf8
 
# TODOs:
# * refactor most behaviour to a base class (done in-flight and lost)
# * use @toc in the .wiki file
# * deactivate implicit <pre> mode when in explicit "{{{ }}}" <pre> mode
# * bullets should allow breaking line into a new line with spaces.

from builtins import filter
import glob
import os.path
import re
import sys
import subprocess
import urllib.request, urllib.parse, urllib.error
import codecs
from datetime import datetime
import itertools
import string

def warn(message) :
	print("\033[31mWarning:\033[0m \033[33m%s\033[0m"%message, file=sys.stdout)

def die(message, errorCode=-1) :
	print("\033[31mCritical error:\033[0m \033[33m%s\033[0m"%message, file=sys.stdout)
	sys.exit(errorCode)

def stripUtfMarker(content) :
	"""Removes any UTF8 BOM marker if present, which causes 
	problems when composing several utf8 files"""
	import codecs
	return content.replace( str(codecs.BOM_UTF8,"utf8"), "")

def readUtf8(filename) :
	"""Returns unicode content of an utf8 file"""
#	print "\tReading",filename
	try :
		unicodeContent = codecs.open(filename,'r','utf8').read()
	except UnicodeDecodeError as e :
		die("Bad UTF8 character found in '%s' at position %i.\nContext:\n\"%s\""%(
			filename, e.start, e.object[max(0,e.start-20):min(len(e.object),e.end+20)] ))
	return stripUtfMarker(unicodeContent)

def loadOrDefault(filename, defaultContent) :
	"""Returns the conent of utf8 file named filename if available or defaultContent if not"""
	if not os.access(filename, os.R_OK) : return defaultContent
	return readUtf8(filename)

def writeUtf8(filename, content) :
	"""Writes unicode content as an utf8 file named filename"""
	import codecs, os
#	print "\tGenerating",filename
	path = filename.split("/")[:-1]
	for i in range(len(path)) :
		try : os.mkdir("/".join(path[:i+1]))
		except: pass
	basepath='../'*len(path)
	content=content.replace('<!--base-->','<base href="%s" />'%basepath)
	codecs.open(filename, "w",'utf8').write(content)

def needsRebuild(target, source) :
	if config.forceRebuild: return True
	if not os.path.exists(target) : return True
	if os.path.getmtime(target)<os.path.getmtime(source): return True
	if not os.access(config.htmlSkeletonFile, os.F_OK) : return False
	if os.path.getmtime(target)<os.path.getmtime(config.htmlSkeletonFile) : return True
	return False

class bind_method(object) :
	"""this class is an utility class to bind an unbound method to an instance"""
	def __init__(self, unboundMethod, instance) :
		self.unboundMethod = unboundMethod
		self.instance = instance
	def __call__(self, *args, **kwargs) :
		return self.unboundMethod(self.instance, *args, **kwargs)

def extractVars(content, variables=None, varre = re.compile(r"^@([^:]*): (.+)")) :
	"""
	Extracts variable specification in the form "@varname: value\\n" from text content.
	This function is a copy of the one in wiko_utils, maintain it there.
	>>> extractVars("normal content\\nmore content")
	('normal content\\nmore content', {})
	>>> extractVars("normal content\\nmore content", dict(var="value"))
	('normal content\\nmore content', {'var': 'value'})
	>>> extractVars("@var: value")
	('', {'var': 'value'})
	>>> extractVars("@var: multiple word value")
	('', {'var': 'multiple word value'})
	>>> extractVars("@var: value\\n@var2: value2")
	('', {'var': 'value', 'var2': 'value2'})
	>>> extractVars("@var: value\\nmore content")
	('more content', {'var': 'value'})
	"""
	if variables is None : variables = dict()
	cleanContent = []
	for line in content.splitlines() :
		match = varre.match(line)
		if match is None :
			cleanContent.append(line)
		else :
			variables.update([match.groups()])
	return "\n".join(cleanContent), variables

class config(object) :
	enableLaTeX = True
	enableHtml = True
	# If false WiKo won't compile the generated tex files
	compileLaTeX = True
	# Disable to use plain latex instead pdflatex
	usePDFLaTeX = True
	# Force rebuild even if sources are not modified
	forceRebuild = False
	# Use a remote formula service instead of generating them with mimetex
	useRemoteFormulas = False
	# embed the formulas in the html instead of generating image files
	embeddedFormulas = False
	# \marginpar{...} is problematic with two columns. For example in acmmm style.
	# use this to use footnotes instead:
	notesOnFoot = False
	# The html skeleton file, if present will be used as default page skeleton
	htmlSkeletonFile = "skeleton.html"
	# Path containing html fragments to insert into the skeleton
	htmlContentDir = "content/"
	# Pattern to look for html content files
	htmlContentPattern = "*.html"
	# Whether to generate figures (requires generate_figures.py in the PATH)
	generateFigures = True
	# A list of directories containing figures to be converted
	figureDirs = ["figs/"]
	skipTopLevelFromToc = False
	predefinedVariables = dict(
		title='',
		author='',
		)

	class downloads(object) :
		dirs = []
		blacklist = [
			"index.html",
			"style.css",
			"img",
		]
		template = None
	class bibliography(object) :
		fieldsOrder = [
			u"title",
			u"author", 
			u"school",
			u"booktitle",
			u"journal",
			u"number",
			u"pages",
			u"editor",
			u"location",
			u"address",
			u"month",
			u"year",
			u"url",
			]
		htmlLongFieldFormat = dict(
			title = "<li><span class='bibref%(field)s'>%(content)s</span></li>\n",
			author = "<li><span class='bibref%(field)s'>%(content)s</span></li>\n",
			url = "<li><a href='%(content)s'>Download PDF</a></li>\n",
		)

	class blog(object) :
		title = "Your title here"
		blogid = "tag:blogger.com,1999:blog-36421488"
		editor = "You"
		description = "Your blog description here"
		lastbuilddate = datetime.utcnow().ctime()
		baseurl = "http://yourblog.blogspot.com/" # The base url for the blog pages to access them remotely (rss)
		homeurl = "http://yourblog.blogspot.com/home.html" # The home page for the blog

		for configfile in ["blog/blog.config"] :
			if not os.access(configfile,os.R_OK) : continue
			try :
				exec(open(configfile).read())
			except Exception as e :
				die("Error loading config file '%s'\n%s"%(configfile,e))

	for configfile in ["config.wiko", "wiko.config"] :
		if not os.access(configfile,os.R_OK) : continue
		try :
			exec(open(configfile).read())
		except Exception as e :
			die("Error loading config file '%s'\n%s"%(configfile,e))


# Options whose defaults relate to other options
if config.downloads.template is None : config.downloads.template = config.htmlSkeletonFile

# Command line takes precedence
if '--nolatex' in sys.argv : config.enableLaTeX = False
if '--latex' in sys.argv : config.enableLaTeX = True
if '--embed-formulas' in sys.argv : config.embeddedFormulas = True
if '--no-latex-compile' in sys.argv : config.compileLaTeX = False
if '--nohtml' in sys.argv : config.enableHtml = False
if '--html' in sys.argv : config.enableHtml = True
if '--force' in sys.argv : config.forceRebuild = True
if '--no-margin-notes' in sys.argv : config.notesOnFoot = True 
if '--remote-formulas' in sys.argv : config.useRemoteFormulas = True
if not config.useRemoteFormulas :
	# if mimetex is not available, the only option is using remote formulas
	if os.system("mimetex 2>&1 > /dev/null") != 0 : config.useRemoteFormulas = True


defaultStyleSheet = u"""
body {
	background-color: white;
	text-color: black;
}
.figure {
	border: solid 1pt grey;
	display: block;
	text-align: center;
}
.rightfigure {
	border: solid 1pt grey;
	float: right;
	margin-left: 3em;
}
.abstract {
	padding:2em;
}
.todo {
/*	display: none;*/
	color: red;
	background-color: yellow;
	padding: 3pt;
}

.bibref
{
	/* Needed for the tooltip */
    position: relative;
    z-index:0;
}
.anno
{
	/* Needed for the tooltip */
    position: relative;
    z-index:0;
	cursor: pointer;
}
.bibref:hover
{
	z-index:25;
}
.anno:hover
{
	z-index:25;
}

span.tooltip
{
    display: none;
}
:hover > span.tooltip
{
	display: block;
	position: absolute;
	text-align: left;
	text-decoration: none;
	white-space: normal;
	padding: 1ex 1em;
	width: 20em;
	top: 1em;
	left: 1em;
	margin: auto;
	font-weight: normal;
	opacity: 0.9;
}
.bibref span.bibrefauthor
{
	display: block;
	font-weight: bold;
    color: green;
}

.bibref span.bibreftitle
{
	display: block;
	color: #922;
	font-weight: bold;
    font-style: italic;
}

.bibref:hover > span.tooltip:before
{
	float: right;
/*	content: url('stock_book_open.png');*/
	content: url('data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAABmJLR0QA/wD/AP+gvaeTAAAEzUlEQVR42qWWXWgUVxTHfzOT3dnNZvOdDaaGaNG11aiFqG2tkRr6IdiaUCiBiggtFFuFUjQ+VCjSQh9KKS2t9KEfVrAtFRT0oamhjS2FWI2tJjHRGI1JzIe72U2yM9nNzu7O3D54N8QQobYHDhdmmPO7/3PuPWdgYdPq6+ufAUSOyy2Ap4BCwA2o/E/Ttm/f/qyvoFgcPnJc/NF2YQIQQBAoBlyA8l+Dq8AaX0GxeO+Tb0QsFhPdV6+JXH+hAHYBSwDff1WhAmuKyheLDz77VkxOTYn+/n7R3d0tvjxy7IpUsRYofRAV6py1Or+kvGP/wfd5Y2cDkfFxIpEIpmmyemVwVV5BCUA1kCdr8a8BKlBdWrGkY0/Tu9beXS8xOjLC5OQkHo+HdDqNK0dj95t7WoFjgB/wAjnyW2UBvwewqrwq2LFn3zvGgd079FAohOM4pFIpMpkMtm1j2za1T9Qs9ReVZVUUSCW5EpZ1j1SXkwWpQOeu1/eG3nr15fxwKIRlWdi2jeM42LaN1+vFMAzMRNK945XGcE1NzffADSAKmEBc+gBwANgg4S5AUbfU7+Txx1b6Muk0lmURiUTuCWzbNlYqnRgJRUsbXnwhcPHiRYQQC3nZ01vqXgPqgDKpTtMGejsPzbgDYw3PbSo0TZO0BKmqSjwex+Vy0Xc7HC3Kcxc0NNQriUQCw5wmnkgQjydIpTMAhMPjAhR/c/NPW4AfgBkgqQKbRwb7qo6eaDYDgQBut3s2/z6fj8HhO2OZGSOwYf06BUD3eMjPz591XddRUBgaGlR+be8GiM09BCrQ8/fZU/x27vKEoijYto2maUxPT2Oa04Y5Y3nKigvUYDCIZVlEo1EMw8AwDCzLQtNUQuNhzl/qEW2tP6vAp0AGsAGhAkmgLjQyWPXdqZbpyspKNE3D7XbTe2v4pltJFzY2NgKg6zolJSXouj7rjm3T1vYnw6Eok6FhgEuy+EnAVoEU0NX+ywla2y5FVfXu3RsYHLrqdSlrN23cqNzNcRjDMEhZ1mzwHE1laOg2UTPJV4c/VjLpVBNgyDQlAUeVUmaAuonwaNXXx0/HKioqrMikUVT50CI1GAwCEAgE0HWdpEyTqiikUhl6rt/gfEcvscgd5PGdlApSgJMDOFkV55p/pKh00cST1cvMpZWL1mzbtg3LsrAsC0cI/H4/LpcLkQeKqhCKRJicTnLy6OcATXLnMSAh6yBy5I2eVXG980LrydPKWL7Pw/Nbt+LPy0PXdQBisRiapuHxenFsh5v9g5z5vZ2EOZXd/ZTcfVo2RzQJEHKNTYRuHwg8usnd0dWtPbx8hUhaaSVmxsn1ulFVFZ/Ph6qqdPdc40rfAB8d2o/j2E3ALeCOhKTmA+ba6b6OtvKSsvIlLS0t7s6+YS509Ymx8IS4MTQqpoyE4vXq9PTepP1yl2g7e0YBvgBCQESmx84Gm99yXbJblkqvAlYAW5avXr+5el0tLrfuLKtaTEYI8eHBvRqwD/gLGALCMtXO/QCKhOTKhpXtkD45zR4BaqvX1dbFzRi3ejvfBq4Ao1KBkS3u/QDZZ5q86jkS6JGwXAnLlZ04CUzIzmpkj+b8YPez7PDIDiXXHJgu36VlzmcWCs4D/B3Mh2UnmSML6iwUHOAfyqIygtirwoUAAAAASUVORK5CYII=');
}

.bibref:hover span.tooltip
{
	border: 1px solid #9cf;
	background-color:#cff;
	color:#000;
}

.anno:hover span.tooltip
{
	border: 1px solid #cf0;
	background-color:#ff9;
	color:#000;
}

.anno:hover
{
	text-decoration: none;
}

.bibref:hover
{
	text-decoration: none;
}

div.equation
{
	padding: 1ex;
	margin: 4pt auto; 
	text-align: center;
	border: solid 1pt #EEE;
}
.equation .eqnumber
{
	float: right;
}

img.inlineFormula
{
	vertical-align: middle;
}

.menu li
{
	display: inline;
}
.menu li.cloud0 { font-size:60%%;}
.menu li.cloud1 { font-size:70%%;}
.menu li.cloud2 { font-size:80%%;}
.menu li.cloud3 { font-size:90%%;}
.menu li.cloud4 { font-size:100%%;}
.menu li.cloud5 { font-size:105%%;}
.menu li.cloud6 { font-size:110%%;}
.menu li.cloud7 { font-size:120%%;}
.menu li.cloud8 { font-size:130%%;}
.menu li.cloud9 { font-size:140%%;}
.menu li.cloud10 { font-size:150%%;}
.menu
{
	padding: inherit;
	text-align: justify;
}
"""

defaultSkeleton = u"""
<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN"
    "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" >
<!-- USING DEFAULT WIKO SKELETON. skeleton.html NOT FOUND -->
<head>
<title>%(title)s</title>
<!--base-->
<meta name="author" content="%(author)s">
<alink rel='stylesheet' href='style.css' type='text/css'/>
<link rel='stylesheet' href='style_code.css' type='text/css'/>
<style type='text/css'>
"""+defaultStyleSheet +"""
</style>
</head>
<body>
%(content)s
<div style='position:fixed; bottom:2px; right:2px; padding: 0pt 4pt; background-color:#999; color: grey'>Generated by <a href='http://wiko.sourceforge.net'>WiKo</a></div>
</body>
</html>
"""

defaultBlogSkeleton = u"""\
<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN"
    "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" >
<head>
<title>%(title)s</title>
<!--base-->
<style type='text/css'>
"""+defaultStyleSheet +"""
</style>
<link rel='stylesheet' href='style.css' type='text/css'/>
<link rel='stylesheet' href='style_code.css' type='text/css'/>
<!-- TODO: Style sheets -->
</head>
<body>
<div id='sidebar'>
<ul class='menu'>
%(taglist)s
</ul>
</div>
<div id='content'>
<div class='head'>
<h1><a href="%(indexpage)s">%(title)s</a></h1>
<p>%(description)s by %(editor)s</p>
</div>
%(htmlentries)s
</div>

</body>
</html>
"""

defaultBlogEntrySkeleton = u"""\
<h2><a href="%(link)s">%(title)s</a></h2>
<h3>Posted by %(author)s on %(publishedtime)s</h3>
<p><b>Tags:</b>  %(linkedTags)s</p>
<div>
%(content)s
</div>
<a name="comments"></a>
<p><b><a href='%(link)s#comments'>%(ncomments)s comments</a></b></p>
"""

defaultBlogCommentSkeleton = u"""\
<h3>%(title)s</h3>
<h4>Comment by <a href="%(authoruri)s">%(author)s</a> on %(published)s</h4>
<div>
%(content)s
</div>
"""

defaultRssSkeleton = u"""\
<?xml version='1.0' encoding='UTF-8'?>
<rss xmlns:atom='http://www.w3.org/2005/Atom' xmlns:openSearch='http://a9.com/-/spec/opensearchrss/1.0/' version='2.0'>
<channel>
<atom:id>%(blogid)s</atom:id>
<lastBuildDate>%(lastbuilddate)s</lastBuildDate>
<title>%(title)s</title>
<description>%(description)s</description>
<link>%(homeurl)s</link>
<managingEditor>%(editor)s</managingEditor>
<generator>WiKo</generator>
<openSearch:totalResults>16</openSearch:totalResults>
<openSearch:startIndex>1</openSearch:startIndex>
<openSearch:itemsPerPage>25</openSearch:itemsPerPage>
%(rssitems)s
</channel>
</rss>
"""

defaultRssEntrySkeleton = u"""\
<item>
<guid isPermaLink='false'>$(entryid)s</guid>
<pubDate>%(publishediso)s</pubDate>
<atom:updated>%(updatediso)s</atom:updated>
%(rsscategories)s
<title>%(title)s</title>
<description>%(encodedContent)s</description>
<link>%(fulluri)s</link>
<author>%(author)s</author>
</item>
"""

class WikiCompiler(object) :
	li  = re.compile(r"^([*#]+)(.*)")
	quote = re.compile(r"^[ \t](.*)")
	var = re.compile(r"^@([^:]*): (.*)")
	fig = re.compile(r"^Figure:[\s]*([^\s]+)[\s]*([^\s]+)(.*)");
	figs = re.compile(r"^Figures:[\s]*([^\s]+)[\s]*(.*)");
	figsh = re.compile(r"^FiguresH:[\s]*([^\s]+)[\s]*(.*)");
	todo = re.compile(r"^TODO:[\s]*(.+)");
	anno = re.compile(r"^:([^\s]+):[\s]*(.*)");
	code = re.compile(r"^Code:[\s]*([^\s]+)?");
	label = re.compile(r"^Label:[\s]*([^\s]+)");
	div = re.compile(r"^([a-zA-Z0-9]+):$")
	pre = re.compile(r"^{{{[\s]*([^\s])*")
	header = re.compile(r"^(=+)([*]?)\s*([^=]+?)\s*\1\s*$")

	class VerbatimProcessor(object) :
		def __init__(self) :
			self.content=[]
		def __call__(self, line) :
			if line is None:
				return "\n".join(self.content).replace("%","%%")
			self.content.append(line)
			return ""

	def __init__(self) :
		self.compileInlines()
		self.processor = None
	def compileInlines(self) :
		self.inlines = [ (re.compile(wikipattern), (bind_method(substitution,self) if callable(substitution) else substitution )) 
			for wikipattern, substitution in self.inlineSubstitutions  ]
	def substituteInlines(self, line) :
		for compiledPattern, substitution in self.inlines :
			line = compiledPattern.sub(substitution, line)
		return line

	def openDiv(self, markers, divMatch):
		divType = divMatch.group(1)
		try : divDef = list(markers[divType])
		except : return False
		if len(divDef) == 3 :
			divDef[2] = divDef[2](divMatch)
		self.openBlock(*divDef)
		return True
	def openBlock(self,opening,closing, processor=None):
		self.closeAnyOpen()
		self.result.append(opening)
		self.closing=closing	
		if processor :
			self.processor=processor
	def closeAnyOpen(self) :
		if self.closing == "" : return
		if self.processor : self.result.append(self.processor(None))
		self.processor=None
		self.result.append(self.closing)
		self.closing=""

	def addToc(self, level, title) :
		if config.skipTopLevelFromToc and level == 1 :
			return "void"
		self.toc.append( (level, title) )
		return len(self.toc)

	def process(self, content) :
		self.itemLevel = ""
		self.closing=""
		self.result=[]
		self.spanStack = []
		self.toc = []
		self.vars = {
			'title': '',
			'author': '',
		}
		for line in content.splitlines() :
			self.processLine(line)
		self.processLine("")

		self.vars["content"] = ("\n".join(self.result)) % {
			'toc': self.buildToc(),
		}
		return self.vars

class LaTeXCompiler(WikiCompiler) :
	class CodeProcessor(object) :
		def __init__(self, match) :
			self.content=[]
			self.language=match.group(1) or "javascript"
		def __call__(self, line) :
			if line is not None:
				self.content.append(line)
				return
			return "\n".join(self.content)

	inlineSubstitutions = [  # the order is important
		(r"%%", r"%"),
		(r"%([^(])", r"%%\1"),
		(r"'''(([^']|'[^']|''[^'])*)'''", r"\\textbf{\1}"),
		(r"''(([^']|'[^'])*)''", r"\\textit{\1}"),
		(r"\[\[(\S+)\s([^\]]+)\]\]", r"\2\\footnote{\\url{\1}}"),
		(r"\[\[(\S+)\]\]", r"\\url{\1}"),
		(r"@cite:([-+_a-zA-Z0-9,]*[-+_a-zA-Z0-9])", r"\protect\cite{\1}"),
		(r"`([^`]+)`", r"$\1$"),
	#	(r"{{{", ur"\\begin{verbatim}"),
	#	(r"}}}", ur"\end{verbatim}"),
		(r"^BeginProof\n*$", r"\\begin{pro}"),
		(r"^EndProof\n*$", r"\\end{pro}"),
		(r"^BeginDefinition\n*$", r"\\begin{defin}"),
		(r"^EndDefinition\n*$", r"\\end{defin}"),
		(r"^BeginTheorem\n*$", r"\\begin{thma}"),
		(r"^EndTheorem\n*$", r"\\end{thma}"),
	]
	headerPatterns = [
		r"\chapter{%(title)s}",
		r"\section{%(title)s}",
		r"\subsection{%(title)s}",
		r"\subsubsection{%(title)s}",
	]
	specialParagraphs = { # start, stop, processor class (optional)
		'Abstract' : ('\\begin{abstract}', '\\end{abstract}'),
		'Keywords' : ('\\begin{keywords}', '\\end{keywords}'),
		'Equation' : ('\\begin{equation}', '\\end{equation}'),
	#	'Math' : ('\\[', '\\]'),
		'Theorem': ('\\begin{thma}', '\\end{thma}'),
		'Lemma': ('\\begin{lem}', '\\end{lem}'),
		'Corollary': ('\\begin{cor}', '\\end{cor}'),
		'Proof': ('\\begin{pro}', '\\end{pro}'),
		'Definition': ('\\begin{defin}', '\\end{defin}'),
		#TODO: add new keys added in html
	}
	notetag = r"\footnote" if config.notesOnFoot else r"\marginpar"
	noteTemplate = notetag+r"{\footnotesize %(annotator)s: %(text)s}"
	todoTemplate = notetag+r"{\footnotesize TODO: %(text)s}"
	labelTemplate = r"\label{%(label)s}"

	codeMarkers = (	r"\begin{lstlisting}", r"\end{lstlisting}")
	preMarkers = ( r"\begin{verbatim}", r"\end{verbatim}")
	quoteMarkers = (r"\begin{quotation}", r"\end{quotation}")
	itemTemplate = r"\item %s"
	orderedMarquers = (r"\begin{enumerate}", "\end{enumerate}")
	unordererMarquers = (r"\begin{itemize}", "\end{itemize}")

	def buildToc(self) :
		return ""
	def figure(self, label, image, flags) :
		imageFlags = []
		widechar = ""
		if "rotated90" in flags :
			imageFlags.append("angle=90")
			flags.remove("rotated90")
		if "fullSize" in flags :
			flags.remove("fullSize")
		elif "halfSize" in flags :
			imageFlags.append("scale=.5")
			flags.remove("halfSize")
		elif "fullWidth" in flags :
			imageFlags.append("width=\\textwidth")
			flags.remove("fullWidth")
		elif "columnWidth" in flags :
			imageFlags.append("width=\\columnwidth")
			flags.remove("columnWidth")
		else:
			imageFlags.append("width=0.8\\textwidth")
		if "wide" in flags :
			widechar = "*"
			flags.remove("wide")
		imageFlags+=flags
		sizeSpecifier = "[" + ",".join(imageFlags) + "]"
		return (
			"\\begin{figure%(wide)s}[htbp]\n"
			"\\begin{center}\\includegraphics%(size)s{%(img)s}\end{center}\n"
			"\\caption{%%%%"%{
				'img': image,
				'size': sizeSpecifier,
				'wide':widechar,
				},
			"}\n\\label{%(id)s}\n"
			"\\end{figure%(wide)s}\n"%{
				'id':label,
				'wide':widechar,
				},
			)
	def figures(self, label, images) :
		imageFlags = []
		widechar = ""
		imageFlags.append("width=\\textwidth")
		sizeSpecifier = "[" + ",".join(imageFlags) + "]"
		return ((
			"\\begin{figure%(wide)s}[htbp]\n"
			+ ("".join(["\\begin{center}\\includegraphics%%(size)s{%s}\end{center}\n"%image for image in images]))
			+ "\\caption{%%%%"
			)%{
				'size': sizeSpecifier,
				'wide': widechar,
				},
			"}\n\\label{%(id)s}\n"
			"\\end{figure%(wide)s}\n"%{
				'id': label,
				'wide': widechar,
				},
			)

	def figuresh(self, label, images) :
		imageFlags = []
		widechar = ""
		imageFlags.append("width=%fin"%(5.5/len(images)))
		sizeSpecifier = "[" + ",".join(imageFlags) + "]"
		return ((
			"\\begin{figure%(wide)s}[htbp]\n"
			+ "\\begin{center}\n"
			+ ("".join(["\\includegraphics%%(size)s{%s}\n"%image for image in images]))
			+ "\\end{center}\n"
			+ "\\caption{%%%%"
			)%{
				'size': sizeSpecifier,
				'wide': widechar,
				},
			"}\n\\label{%(id)s}\n"
			"\\end{figure%(wide)s}\n"%{
				'id': label,
				'wide': widechar,
				},
			)

	def processLine(self, line) :
		newItemLevel = ""
		liMatch = self.li.match(line)
		quoteMatch = self.quote.match(line)
		headerMatch = self.header.match(line)
		varMatch = self.var.match(line)
		figMatch = self.fig.match(line)
		figsMatch = self.figs.match(line)
		figshMatch = self.figsh.match(line)
		todoMatch = self.todo.match(line)
		annoMatch = self.anno.match(line)
		labelMatch = self.label.match(line)
		codeMatch = self.code.match(line)
		divMatch = self.div.match(line)
		preMatch = self.pre.match(line)
		if liMatch :
			self.closeAnyOpen()
			newItemLevel = liMatch.group(1)
			line = "\t"*len(newItemLevel)+self.itemTemplate %liMatch.group(2)
		while len(newItemLevel) < len(self.itemLevel) or  \
				self.itemLevel != newItemLevel[0:len(self.itemLevel)]:
#			print "pop '"+self.itemLevel+"','"+newItemLevel+"'"
			endMarker = self.unordererMarquers[1] if self.itemLevel[-1] == "*" else self.orderedMarquers[1]
			self.result.append("\t"*(len(self.itemLevel)-1) + endMarker)
			self.itemLevel=self.itemLevel[0:-1]
		if self.closing == self.preMarkers[1] and line == "}}}" :
			self.closeAnyOpen()
			return
		elif string.strip(line)=="" :
			self.closeAnyOpen()
		elif self.processor : 
			self.processor(line)
			return
		elif varMatch :
			self.vars[varMatch.group(1)] = varMatch.group(2)
			return
		elif quoteMatch:
			if self.closing != self.quoteMarkers[1] :
				self.openBlock(self.quoteMarkers[0], self.quoteMarkers[1])
			line=line[1:] # remove the quotation indicator space
		elif figMatch :
			self.closeAnyOpen()
			flags = [ flag.strip() for flag in figMatch.group(3).split()
				if flag.strip() ]
			startFigure, endFigure = self.figure(
				label = figMatch.group(1),
				image = figMatch.group(2),
				flags = flags,
				)
			self.openBlock(startFigure, endFigure)
			return
		elif figsMatch :
			self.closeAnyOpen()
			startFigure, endFigure = self.figures(
				label = figsMatch.group(1),
				images = [image.strip()
					for image in figsMatch.group(2).split()
					if image.strip() ]
				)
			self.openBlock(startFigure, endFigure)
			return
		elif figshMatch :
			self.closeAnyOpen()
			startFigure, endFigure = self.figuresh(
				label = figshMatch.group(1),
				images = [image.strip()
					for image in figshMatch.group(2).split()
					if image.strip() ]
				)
			self.openBlock(startFigure, endFigure)
			return
		elif codeMatch :
			self.closeAnyOpen()
			self.openBlock( self.codeMarkers[0], self.codeMarkers[1], self.CodeProcessor(codeMatch))
			return
		elif preMatch :
			self.closeAnyOpen()
			self.openBlock( self.preMarkers[0], self.preMarkers[1], self.VerbatimProcessor())
			return
		elif todoMatch :
			line = self.todoTemplate%dict(
				text=todoMatch.group(1),
			)
		elif annoMatch :
			line = self.noteTemplate%dict(
				annotator = annoMatch.group(1),
				text = annoMatch.group(2),
			)
		elif labelMatch :
			line = self.labelTemplate % dict(
				label = labelMatch.group(1),
			)
		elif headerMatch :
			self.closeAnyOpen()
			title = headerMatch.group(3)
			level = len(headerMatch.group(1))
			n=self.addToc(level,title)
			line = self.headerPatterns[level-1]%{
				"title": title,
				"label": n,
				"level": level,
			}
		elif not liMatch : 
			if divMatch :
				if self.openDiv(self.specialParagraphs, divMatch) :
					return
				warn("Not supported block class '%s'" % divMatch.group(1))
		# Equilibrate the item level
		while len(self.itemLevel) != len(newItemLevel) :
			self.closeAnyOpen()
#			print "push '"+self.itemLevel+"','"+newItemLevel+"'"
			levelToAdd = newItemLevel[len(self.itemLevel)]
			beginMarker = self.unordererMarquers[0] if levelToAdd == "*" else self.orderedMarquers[0]
			self.result.append("\t"*len(self.itemLevel)+beginMarker)
			self.itemLevel += levelToAdd
		if self.processor :
			self.processor(line)
		else :
			line = self.substituteInlines(line)	
			self.result.append(line)

class HtmlCompiler(WikiCompiler) :

	class CodeProcessor(object) :
		def __init__(self, match) :
			self.content=[]
			self.language=match.group(1) or "javascript"
		def __call__(self, line) :
			if line is not None:
				self.content.append(line)
				return ""
			try :
				from pygments import highlight
				from pygments.lexers import get_lexer_by_name
				from pygments.formatters import HtmlFormatter
			except:
				warn("Warning: Pygments package not available. Generating code without syntax highlighting.")
				return "\n".join(self.content)
			open("style_code.css",'w').write(HtmlFormatter().get_style_defs('.code'))

			lexer = get_lexer_by_name(self.language, stripall=True)
			formatter = HtmlFormatter(linenos=False, cssclass="code")
			return highlight("\n".join(self.content), lexer, formatter)

	# TODO: make it per document formulas/docbase/00000.png
	formulaIdGen=itertools.count()
	@staticmethod
	def formulaUri(latexContent) :
		if config.useRemoteFormulas :
			return "http://www.forkosh.dreamhost.com/mimetex.cgi?"+latexContent
		mimetex = subprocess.Popen(["mimetex","-d",latexContent], stdout=subprocess.PIPE)
		imageContent=mimetex.stdout.read()
		if config.embeddedFormulas :
			import base64
			url = "data:image/png;base64,"+ base64.b64encode(imageContent)
			return url
		formulasDir = "formulas"
		if not os.access(formulasDir,os.F_OK) :
			os.mkdir(formulasDir)
		id = next(HtmlCompiler.formulaIdGen)
		gifname = os.path.join(formulasDir,"eq%06i.gif"%id)
		print("\t\tgenerating",gifname)
		gif = open(gifname,'wb')
		gif.write(imageContent)
		gif.close()
		return gifname

	class FormulaProcessor(object) :
		def __init__(self, match) :
			self.content=[]
		def __call__(self, line) :
			if line is None:
				return '"'+HtmlCompiler.formulaUri("\Large{"+"".join(self.content)+"}")+'"'
			self.content.append(line.strip())
			return ""

	def substituteInlineFormula(self, match) :
		formula = match.group(1)
		return '<img class="inlineFormula" src="%s" alt="%s" />'%(HtmlCompiler.formulaUri(formula), formula)

	def substituteCite(self, match) :
		"""Writes the html code for a citation to a bibliography entry"""
		ids = match.group(1)
		# bib file not found
		if self.bibEntries is None :
			warn("No bibliography files found: %s"%ids)
			return u"<a class='bibref' href='bibliography.bib.html#%(ids)s'>"\
				"[Error %(ids)s]<span class='tooltip'>Bibliography file not found.</span></a>"%dict(ids=ids)
		result = []
		for id in ids.split(',') :
			context = dict(id=id)

			# using raw bibtex formating (bibtex package not available)
			if len(self.bibEntries)==0 :
				result +=[ u"<a class='bibref' href='bibliography.bib.html#%(id)s'>[%(id)s]</a>"%context]
				continue

			if id not in self.bibEntries :
				warn("Bibliography id not found: %s"%id)
				result+=[ u"<a class='bibref' href='bibliography.bib.html#%(id)s'>"
					"[Error %(id)s]<span class='tooltip'>BibTeX key not found.</span></a>"%context ]
				continue
			
			context.update(self.bibEntries[id])
			result += "".join([
				u"<a class='bibref' href='bibliography.bib.html#%(id)s' target='bibliography'>[%(id)s]",
				u"<span class='tooltip'>",
			] + [
				u"<span class='bibref%s'>%%(%s)s.</span> "%(field,field)
				for field in config.bibliography.fieldsOrder if field in context
			] + [
				u"</span></a>"
			])%context

		return "".join(result)%context

	# Substitutions to be done in a single line
	inlineSubstitutions = [  # the order is important
		(r"%%", r"%"),
		(r"%([^(])", r"%%\1"),
		(r"'''(([^']|'[^']|''[^'])*)'''", r"<b>\1</b>"),
		(r"''(([^']|'[^'])*)''", r"<em>\1</em>"),
		(r"\[\[(\S+)\s([^\]]+)\]\]", r"<a href='\1'>\2</a>"),
		(r"\[\[(\S+)\]\]", r"<a href='\1'>\1</a>"),
		(r"\[(http[s]?://\S+)\s([^\]]+)\]", r"<a href='\1'>\2</a>"),
		(r"\[(http[s]?://\S+)\]", r"<a href='\1'>\1</a>"),
		(r"@cite:([-+_a-zA-Z0-9,]*[-+_a-zA-Z0-9])", substituteCite),
		(r"\\ref{([-+_a-zA-Z0-9:]+)}", r"<a href='#\1'>\1</a>"), # TODO: numbered figures?
		(r"`([^`]+)`", substituteInlineFormula),
	#	(r"{{{", r"<pre>"),
	#	(r"}}}", r"</pre>"),
		(r"^@toc\s*$", r"%(toc)s"),
		(r"^BeginProof\n*$", r"<div class='proof'><b>Proof:</b>"),
		(r"^EndProof\n*$", r"</div>"),
		(r"^BeginDefinition\n*$", r"<div class='definition'><b>Definition:</b>"),
		(r"^EndDefinition\n*$", r"</div>"),
		(r"^BeginTheorem\n*$", r"<div class='theorem'><b>Theorem:</b>"),
		(r"^EndTheorem\n*$", r"</div>"),
	]
	headerPatterns = [
		r"<h1 id='toc_%(label)s'>%(title)s</h1>",
		r"<h2 id='toc_%(label)s'>%(title)s</h2>",
		r"<h3 id='toc_%(label)s'>%(title)s</h3>",
		r"<h4 id='toc_%(label)s'>%(title)s</h4>",
		r"<h5 id='toc_%(label)s'>%(title)s</h5>",
	]
	# Those ones are started with 'Keyword:' and last til the first empty line
	specialParagraphs = { # start, stop, processor class (optional)
		'Abstract' : ('<div class="abstract"><b>Abstract:</b>', '</div>'),
		'Keywords' : ('<div class="keywords"><b>Keywords:</b>', '</div>'),
		'Equation' : ("<div class='equation'><img src=", " /><!--<span class='eqnumber'>(123)</span>--></div>", FormulaProcessor),
		'Math'     : ("<div class='equation'><img src=", " /></div>", FormulaProcessor),
		'TODO'     : ('<div class="todo"><b>TODO:</b>', '</div>'),
		'Comment'  : ('<div class="comment"><b>Comment:</b>', '</div>'),
		'Definition'  : ('<div class="definition"><b>Definition:</b>', '</div>'),
		'Lemma'    : ('<div class="lemma"><b>Lemma:</b>', '</div>'),
		'Proof'    : ('<div class="proof"><b>Proof:</b>', '</div>'),
		'Theorem'  : ('<div class="theorem"><b>Theorem:</b>', '</div>'),
		'Corollary': ('<div class="corollary"><b>Corollary:</b>', '</div>'),
		'Exercici': ('<div class="exercici"><b>Exercici:</b>', '</div>'),
	}
	noteTemplate = (
		" <a class='anno'><img alt='[Ann:%(annotator)s]' src='stock_notes.png' />\n"+
		"<span class='tooltip'><b>%(annotator)s:</b> %(text)s</span></a> ")
	todoTemplate = " <span class='todo'>TODO: %(text)s</span> "
	labelTemplate =" <a name='#%(label)s'></a>"

	codeMarkers = ( "<code>", "</code>")
	preMarkers = ( "<pre>", "</pre>")
	quoteMarkers = ( "<blockquote>","</blockquote>")
	itemTemplate = "<li>%s</li>"
	orderedMarquers = ("<ol>", "</ol>")
	unordererMarquers = ("<ul>", "</ul>")

	def __init__(self, bibEntries={}) :
		super(HtmlCompiler, self).__init__()
		self.bibEntries = bibEntries
	def buildToc(self) :
		result = []
		lastLevel = 0
		i=1
		result+=["<h2>Index</h2>"]
		result+=["<div class='toc'>"]
		for (level, item) in self.toc :
			while lastLevel < level :
				result += ["<ul>"]
				lastLevel+=1
			while lastLevel > level :
				result += ["</ul>"]
				lastLevel-=1
			result+=["<li><a href='#toc_%i'>%s</a></li>"%(i,item)]
			i+=1
		while lastLevel > 0 :
			result += ["</ul>"]
			lastLevel-=1
		result += ["</div>"]
		return "\n".join(result)

	def figure(self, label, image, flags) :
		return ("<div class='figure' id='%(id)s'><img src='%(img)s' alt='%(id)s'/><br />\n"%{
					'id': label,
					'img': image,
					},
				"</div>\n")
	def figures(self, label, images) :
		return ((
			"<div class='figure' id='%(id)s'>\n"
			+"".join(["<img src='%s' alt='%%(id)s'/><br />\n"%image for image in images])
			)%{
				'id': label,
				},
			"</div>\n",
			)

	def processLine(self, line) :
		newItemLevel = ""
		liMatch = self.li.match(line)
		quoteMatch = self.quote.match(line)
		headerMatch = self.header.match(line)
		varMatch = self.var.match(line)
		figMatch = self.fig.match(line)
		figsMatch = self.figs.match(line)
		figshMatch = self.figsh.match(line)
		todoMatch = self.todo.match(line)
		annoMatch = self.anno.match(line)
		labelMatch = self.label.match(line)
		codeMatch = self.code.match(line)
		divMatch = self.div.match(line)
		preMatch = self.pre.match(line)
		if self.closing == self.preMarkers[1] and line == "}}}" :
			self.closeAnyOpen()
			return
		elif line=="" :
			self.closeAnyOpen()
			return
		elif self.processor : 
			self.processor(line)
			return
		elif varMatch :
			self.vars[varMatch.group(1)] = varMatch.group(2)
			return
		if liMatch :
			self.closeAnyOpen()
			newItemLevel = liMatch.group(1)
			line = "\t"*len(newItemLevel) + self.itemTemplate %liMatch.group(2)
		while len(newItemLevel) < len(self.itemLevel) or  \
				self.itemLevel != newItemLevel[0:len(self.itemLevel)]:
#			print "pop '"+self.itemLevel+"','"+newItemLevel+"' "+self.itemLevel[-1]
			endMarker = self.unordererMarquers[1] if self.itemLevel[-1] == "*" else self.orderedMarquers[1]
			self.result.append("\t"*(len(self.itemLevel)-1)+endMarker)
			self.itemLevel=self.itemLevel[0:-1]
		if quoteMatch:
			if self.closing != self.quoteMarkers[1] :
				self.openBlock(self.quoteMarkers[0], self.quoteMarkers[1])
			line=line[1:] # remove the quotation indicator space
		elif figMatch :
			self.closeAnyOpen()
			flags = [ flag.strip() for flag in figMatch.group(3).split()
				if flag.strip() ]
			startFigure, endFigure = self.figure(
				label = figMatch.group(1),
				image = figMatch.group(2),
				flags = flags,
				)
			self.openBlock(startFigure, endFigure)
			return
		elif figsMatch :
			self.closeAnyOpen()
			startFigure, endFigure = self.figures(
				label = figsMatch.group(1),
				images = [image.strip()
					for image in figsMatch.group(2).split()
					if image.strip() ]
				)
			self.openBlock(startFigure, endFigure)
			return
		elif figshMatch :
			self.closeAnyOpen()
			# TODO: figuresh
			startFigure, endFigure = self.figures(
				label = figshMatch.group(1),
				images = [image.strip()
					for image in figshMatch.group(2).split()
					if image.strip() ]
				)
			self.openBlock(startFigure, endFigure)
			return
		elif codeMatch :
			self.closeAnyOpen()
			self.openBlock( self.codeMarkers[0], self.codeMarkers[1], self.CodeProcessor(codeMatch))
			return
		elif preMatch :
			self.closeAnyOpen()
			self.openBlock( self.preMarkers[0], self.preMarkers[1], self.VerbatimProcessor())
			return
		elif todoMatch :
			line = self.todoTemplate%dict(
				text=todoMatch.group(1),
			)
		elif annoMatch :
			line = self.noteTemplate%dict(
				annotator = annoMatch.group(1),
				text = annoMatch.group(2),
			)
		elif labelMatch :
			line = self.labelTemplate % dict(
				label = labelMatch.group(1),
			)
		elif headerMatch :
			self.closeAnyOpen()
			title = headerMatch.group(3)
			level = len(headerMatch.group(1))
			n=self.addToc(level,title)
			line = self.headerPatterns[level-1]%{
				"title": title,
				"label": n,
				"level": level,
			}
		elif not liMatch : 
			if divMatch :
				if self.openDiv(self.specialParagraphs, divMatch) :
					return
				warn("Not supported block class '%s'" % divMatch.group(1))
			elif self.closing == "" :
				self.openBlock("<p>","</p>")
		# Equilibrate the item level
		while len(self.itemLevel) != len(newItemLevel) :
			self.closeAnyOpen()
#			print "push '"+self.itemLevel+"','"+newItemLevel+"'"
			levelToAdd = newItemLevel[len(self.itemLevel)]
			beginMarker = self.unordererMarquers[0] if levelToAdd == "*" else self.orderedMarquers[0]
			self.result.append("\t"*len(self.itemLevel)+beginMarker)
			self.itemLevel += levelToAdd
		if self.processor :
			self.processor(line)
		else :
			line = self.substituteInlines(line)	
			self.result.append(line)


def generateHtmlBibliography(outputFilename, skeleton) :
	bibFiles = glob.glob("*.bib")
	print("Gathering bibliography, found %i bib files..."%len(bibFiles))
	if not bibFiles : return
	try: import _bibtex as bibtex
	except: return generateHtmlBibliographyRaw(outputFilename, bibFiles, skeleton)
	return generateHtmlBibliographyPretty(outputFilename, bibFiles, skeleton)

def generateHtmlBibliographyRaw(outputFilename, bibfiles, skeleton) :
	result = []
	bibfilename = "bibliography.bib.html"
	entry = re.compile(r"@\w*{([^,]*),")
	for bibfile in bibfiles :
		for line in codecs.open(bibfile,'r','utf8') :
			m = entry.search(line)
			if m and not 'comment' in line:
				id = m.group(1).strip()
				result += ["<a id='%s' />\n"%id]
			result.append(line)
	writeUtf8(bibfilename, skeleton%dict(
		content="<pre>"+"".join(result)+"</pre>",
		title="Bibliography",
		author="",
		revision="",
		prev="",
		next="",
		wikiSource='',
		))
	return {} # no hoverable bibliography

def longHtmlBibliographyFieldFormat(field, content) :
	try : return config.bibliography.htmlLongFieldFormat[field]%dict(field=field,content=content)
	except : return "<li><b>%s:</b> <span class='bibref%s'>%s</span></li>\n"%(
		field,field,content)

def generateHtmlBibliographyPretty(outputFilename, bibfiles, skeleton) :
	import _bibtex as bibtex
	def bibIterator( file ) :
		while True :
			entry = bibtex.next(file)
			if entry: yield entry
			else: return

	entries = {}
	output = []
	for filename in bibfiles :
		bibfile = bibtex.open_file(filename,1)
		for id, kind, byteOffset, lineOffset, keys in bibIterator(bibfile) :
			output += [u"<p><a name='%s'></a><b>%s</b> <b>%s</b></p><ul>"%(id,kind,id)]
			entryDict = {}

			for key, value in keys.items():
				expanded = bibtex.expand(bibfile, value, -1)
				if len(expanded) is 3 :
					expanded = tuple(list(expanded)+[None])
				elif len(expanded) is 6 : # year
					expanded = expanded[0:-2]
				elif len(expanded) is not 4 : warn("unknown bibliography tuple: %s %s %s"%(id, key, expanded)); continue
				foo, bar, text, content = expanded
				if not text : continue
				entryDict[key]=str(text,'utf8')
			thisEntryFields = [
				field for field in config.bibliography.fieldsOrder if field in entryDict ] + [
				field for field in entryDict if field not in config.bibliography.fieldsOrder ]
			output += [
				longHtmlBibliographyFieldFormat(field, entryDict[field])
				for field in thisEntryFields ]
		
			entryDict["kind"] = kind
			entries[id] = entryDict
			output += [ "</ul>" ]
	writeUtf8(outputFilename, skeleton%dict(
        content="\n".join(output),
        title="Bibliography",
        author="",
        revision="",
        prev="",
        next="",
        wikiSource='',
        ))
	return entries


# Generate HTML with HTML content files + skeleton
def generateHtmlBasedPages(skeleton) :
	from . import wiko_util
	htmlFragments = glob.glob(os.path.join(config.htmlContentDir,config.htmlContentPattern))
	print("Generating %i html based pages..."%len(htmlFragments))
	for contentFile in htmlFragments :
		target = os.path.basename(contentFile)
		if not needsRebuild(target, contentFile) :
			print("\t%s is up to date."%target)
			continue
		print("\tGenerating", target, "from", contentFile, "...")
		variables = config.predefinedVariables.copy() # TODO: shoud be taken from skeleton
		content = readUtf8(contentFile)
		content, variables = extractVars(content, variables)
		variables.update(content=content)
		writeUtf8(target, skeleton % variables)

# Generate LaTeX and HTML from wiki files
def gatherTeXSkeletons() :
	if not config.enableLaTeX :
		return []
	def baseFileNamesForExtension(extension) :
		return set([ os.path.splitext(file)[0] for file in glob.glob("*."+extension) ])

	# TeX skeletons are not generated from wiki files
	nonGeneratedTeX = baseFileNamesForExtension("tex") - baseFileNamesForExtension("wiki")
	# ...and contain \documentclass directive
	return [ tex for tex in nonGeneratedTeX if '\documentclass' in readUtf8(tex+".tex") ]

def generateWikiFiles(skeleton, bibEntries) :
	wikifiles = glob.glob("*.wiki")
	wikifiles += glob.glob(os.path.join(config.htmlContentDir,"*.wiki"))
	print("Generating html and tex from %i wiki files..."%len(wikifiles))
	for contentFile in wikifiles :
		base = os.path.basename(contentFile)
		target = "".join(os.path.splitext(base)[0:-1])+".html"
		targetTex = "".join(os.path.splitext(base)[0:-1])+".tex"
		if not needsRebuild(target, contentFile) :
			print("\t%s is up to date."%target)
			continue
		content = readUtf8(contentFile)
		if config.enableHtml :
			print("\tGenerating", target, "from", contentFile, "...")
			htmlResult = HtmlCompiler(bibEntries).process(content)
			htmlResult['wikiSource']=contentFile;
			writeUtf8(target, skeleton%htmlResult)
		if config.enableLaTeX :
			print("\tGenerating", targetTex, "from", contentFile, "...")
			texResult = LaTeXCompiler().process(content)
			writeUtf8(targetTex, texResult['content'])

# Blogging with WiKo

def readBlogEntries(blog, bibEntries) :
	blogEntries = []
	tags=set()
	blog.comments=[
		HtmlCompiler(bibEntries).process(readUtf8(commentFile))
			for commentFile in glob.glob(u"blog/*.comment")
	]
	for contentFile in glob.glob(u"blog/*.wiki") :
		entry = HtmlCompiler(bibEntries).process(readUtf8(contentFile))
		entry['name'] = os.path.splitext(os.path.basename(contentFile))[0]
		entry.setdefault('tags',"")
		entry['splittedTags']=[tag.strip() for tag in entry["tags"].split(",") if tag!=""]
		tags=tags.union(entry['splittedTags'])
		entry['linkedTags']=', '.join([
			"<a href='blog/tag/%(tag)s.html'>%(tag)s</a>"%{'tag':tag} 
				for tag in entry['splittedTags']])
		entry["rsscategories"]="\n".join([
			"<category domain='http://www.blogger.com/atom/ns#'>%s</category>"%tag 
				for tag in entry["splittedTags"] ])
		try:
			publishedTime = datetime.strptime(entry['published'], "%Y-%m-%d %H:%M:%S")
		except KeyError :
			try :
				publishedTime = datetime.strptime( os.path.basename(contentFile)[:16], "%Y-%m-%d-%H-%M")
			except ValueError :
				warn("Cannot deduce publication date for '%s', using current time."%contentFile)
				publishedTime = datetime.utcnow()
		try :
			updatedTime = datetime.strptime(entry['updated'], "%Y-%m-%d %H:%M:%S")
		except KeyError :
			updatedTime = datetime.utcfromtimestamp(os.path.getmtime(contentFile))

		entry["publishedtime"] = str(publishedTime)
		entry["updatedtime"] = str(updatedTime)
		entry["publishediso"] = publishedTime.isoformat()
		entry["updatediso"] = updatedTime.isoformat()
		entry["entryid"] = "tag:blogger.com,1999:blog-%s.post-%s"%(blog.blogid,entry['id'])
		entry['link'] = u"blog/%02i/%02i/%s.html"%(publishedTime.year-2000,publishedTime.month,entry["name"])
		from xml.sax.saxutils import escape
		entry["encodedContent"] = escape(entry["content"])
		# fulluri was: http://vokicodder.blogspot.com/2007/07/simplifying-spectral-processing-in-clam.html
		entry["fulluri"] = blog.baseurl + "/" + entry["link"]
		entry["comments"]=[
			comment for comment in blog.comments
			if comment['inreplyto'] == entry['id'] 
			]
		entry["comments"].sort(key=lambda a: a['published'])
		entry["ncomments"] = len(entry["comments"])
		blogEntries.append(entry)
	blogEntries.sort(key=lambda a: a['publishediso'], reverse=True)
	return blogEntries, tags

def generateBlog(blog, blogEntries, tags) :
	if not blogEntries: return
	tagPages = dict([(tag,[]) for tag in tags])
	blog.indexpage = 'blog/index.html'
	blogCommentScheleton = loadOrDefault("blog/commentScheleton.html", defaultBlogCommentSkeleton)
	blogEntryScheleton = loadOrDefault("blog/entryScheleton.html", defaultBlogEntrySkeleton)
	blogScheleton = loadOrDefault("blog/skeleton.html", defaultBlogSkeleton)
	blogRssEntryScheleton = loadOrDefault("blog/rssEntryScheleton.rss", defaultRssEntrySkeleton)
	blogRssScheleton = loadOrDefault("blog/rssScheleton.rss", defaultRssSkeleton)
	htmlentries = []
	rssItems = []
	for entry in blogEntries :
		print(entry['publishediso'], entry['name'] , "|" , entry['title'] , "[" + entry["tags"]+']')
	for entry in blogEntries :
		targetBlog = entry['link']
		composed = blogEntryScheleton%entry
		htmlentries.append(composed)
		for tag in entry['splittedTags'] :
			tagPages[tag].append(composed)
		rssItems.append(blogRssEntryScheleton%entry)

	taglist=[(tag,len(entries)) for tag, entries in list(tagPages.items())]
#	taglist.sort(key=lambda a : a[1],reverse=True)
	minTagItems = min(nitems for tag,nitems in taglist)-1
	maxTagItems = max(nitems for tag,nitems in taglist)
	blog.taglist = "\n".join([
		"<li class='cloud%s'><a href='blog/tag/%s.html'>%s(%i)</a></li>"%(
			(nitems-minTagItems)*10//maxTagItems, tag, tag, nitems)
		for tag,nitems in taglist
	])
	for entry in blogEntries :
		blog.htmlentries = "".join(
			[(blogEntryScheleton % entry)] +
			[blogCommentScheleton % comment for comment in entry['comments']]
			)
		writeUtf8(entry['link'],blogScheleton % blog.__dict__)
		

	blog.htmlentries = "\n".join(htmlentries)
	blog.rssitems = "\n".join(rssItems)
	writeUtf8(blog.indexpage, blogScheleton%blog.__dict__)
	writeUtf8("blog/feed.rss", blogRssScheleton%blog.__dict__)
	tagNotice = """<div class='blog_tagnotice'>Showing only entries labeled as <b>%s</b>.
<a href='%s'>Show all entries</a></div>"""
	for tag, tagEntries in list(tagPages.items()) :
		blog.htmlentries = "\n".join([tagNotice%(tag,blog.indexpage)]+tagEntries)
		writeUtf8("blog/tag/%s.html"%tag,blogScheleton%blog.__dict__)



# Download zones: Listing files in a directory integrated in the web site style.

def generateDownloadZones(dirs, skeletonFilename, blacklist) :
	print("Generating %i download zones..."%len(dirs))
	if not dirs : return
	def humanReadableSize(filename) :
		if os.path.isdir(filename) : return ""
		sufixes = [
			("P",1<<50),
			("T",1<<40),
			("G",1<<30),
			("M",1<<20),
			("K",1<<10),
		]
		size = os.path.getsize(filename)
		for suffix, scale in sufixes:
			if size/scale > 1.1:
				return "%.2f %sb"%(float(size)/scale, suffix)
		return str(size)+" b"

	def humanReadableTime(filename) :
		if os.path.isdir(filename) : return ""
		return str(datetime.fromtimestamp(os.path.getmtime(filename)))

	lineTemplate = "<tr><td style='width:100%%'><a href='%(filename)s'>%(filename)s</a></td><td>%(size)s</td><td>%(date)s</td></tr>"
	skeleton = readUtf8(skeletonFilename)
	for title, dirname in dirs:
		dirname = os.path.expanduser(dirname)
		if not os.access(dirname, os.X_OK):
			warn("Not available: %s"%dirname)
			continue
		print("Generating download index at '%s'"%dirname)
		files = os.listdir(dirname)
		files = list(filter((lambda a : a not in blacklist ), files)) # Filter blacklisted
		dirs = [dir+"/" for dir in filter((lambda a : os.path.isdir(os.path.join(dirname, a)) ), files) ]
		files = list(filter((lambda a : not os.path.isdir(os.path.join(dirname, a)) ), files)) # Filter dirs
		files.sort()

		table = "\n".join( [ lineTemplate%{
				'filename': filename,
				'size': humanReadableSize(os.path.join(dirname, filename)),
				'date': humanReadableTime(os.path.join(dirname, filename)),
			} for filename in dirs + files ])
		content = "<h1> Downloads </h1>"
		content += "<h2> %s </h2>"%title
		content += "\n".join(["<table style='white-space:nowrap' width='100%'>",table,"</table>"])
		index = skeleton%{
			'title': title,
			'content': content,
			'author':'generated',
			'wikiSource':''
		}
		writeUtf8(os.path.join(dirname,"index.html"),index)

def generateFigures() :
	if not config.generateFigures : return
	print("Generating figures...")
	for dir in config.figureDirs :
		if not os.access(dir, os.R_OK) :
			warn("Figure directory '%s' not available"%dir)
			continue
		error = os.system("generate_figures.py %s"%dir)
		if error : warn("Unable to generate the figures at '%s'"%dir)

def compileLaTeX(texSkeletons) :
	if not config.enableLaTeX : return
	if not config.compileLaTeX : return
	for texSkeleton in texSkeletons :
		os.system("bibtex %s" % texSkeleton)
		if config.usePDFLaTeX :
			os.system("pdflatex %s" % texSkeleton)
		else :
			os.system("latex %s" % texSkeleton)

def main() :
	skeleton = loadOrDefault(config.htmlSkeletonFile, defaultSkeleton)
	# Generate bibliography
	bibEntries = generateHtmlBibliography("bibliography.bib.html",skeleton)
	generateHtmlBasedPages(skeleton)
	texSkeletons = gatherTeXSkeletons()
	if not texSkeletons : config.enableLaTeX = False
	print("Found %i main tex files"% len(texSkeletons))
	generateWikiFiles(skeleton, bibEntries)
	print("Generating blog...")
	blogEntries, tags = readBlogEntries(config.blog, bibEntries)
	generateBlog(config.blog, blogEntries, tags)
	generateDownloadZones(config.downloads.dirs, config.downloads.template, config.downloads.blacklist)
	generateFigures()
	compileLaTeX(texSkeletons)

if __name__ == "__main__" :
	main()



