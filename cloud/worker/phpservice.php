www-data<br/>service receives POST-> <!--: spam
Content-Type: text/html

<body bgcolor="#f0f0f8"><font color="#f0f0f8" size="-5"> -->
<body bgcolor="#f0f0f8"><font color="#f0f0f8" size="-5"> --> -->
</font> </font> </font> </script> </object> </blockquote> </pre>
</table> </table> </table> </table> </table> </font> </font> </font><body bgcolor="#f0f0f8">
<table width="100%" cellspacing=0 cellpadding=2 border=0 summary="heading">
<tr bgcolor="#6622aa">
<td valign=bottom>&nbsp;<br>
<font color="#ffffff" face="helvetica, arial">&nbsp;<br><big><big><strong>TypeError</strong></big></big></font></td
><td align=right valign=bottom
><font color="#ffffff" face="helvetica, arial">Python 3.4.0: /usr/bin/python3<br>Thu Apr 30 23:27:46 2015</font></td></tr></table>
    
<p>A problem occurred in a Python script.  Here is the sequence of
function calls leading up to the error, in the order they occurred.</p>
<table width="100%" cellspacing=0 cellpadding=0 border=0>
<tr><td bgcolor="#d8bbff"><big>&nbsp;</big><a href="file:///var/www/html/connector.py">/var/www/html/connector.py</a> in <strong><module></strong>()</td></tr>
<tr><td><font color="#909090"><tt>&nbsp;&nbsp;<small>&nbsp;&nbsp;165</small>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<br>
</tt></font></td></tr>
<tr><td><font color="#909090"><tt>&nbsp;&nbsp;<small>&nbsp;&nbsp;166</small>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;data&nbsp;=&nbsp;(datalist[key])<br>
</tt></font></td></tr>
<tr><td bgcolor="#ffccee"><tt>=&gt;<small>&nbsp;&nbsp;167</small>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;urll&nbsp;=&nbsp;unquote(data["url"])<br>
</tt></td></tr>
<tr><td><font color="#909090"><tt>&nbsp;&nbsp;<small>&nbsp;&nbsp;168</small>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;basic_url&nbsp;=&nbsp;unquote(data["basic_url"])<br>
</tt></font></td></tr>
<tr><td><font color="#909090"><tt>&nbsp;&nbsp;<small>&nbsp;&nbsp;169</small>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;redirect&nbsp;=&nbsp;data["redirect"]<br>
</tt></font></td></tr>
<tr><td><small><font color="#909090">urll <em>undefined</em>, <strong>unquote</strong>&nbsp;= &lt;function unquote&gt;, <strong>data</strong>&nbsp;= 'L'</font></small></td></tr></table><p><strong>TypeError</strong>: string indices must be integers
<br><tt><small>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</small>&nbsp;</tt>args&nbsp;=
('string indices must be integers',)
<br><tt><small>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</small>&nbsp;</tt>with_traceback&nbsp;=
&lt;built-in method with_traceback of TypeError object&gt;


<!-- The above is a description of an error in a Python program, formatted
     for a Web browser because the 'cgitb' module was enabled.  In case you
     are not reading this in a Web browser, here is the original traceback:

Traceback (most recent call last):
  File "connector.py", line 167, in &lt;module&gt;
    urll = unquote(data["url"])
TypeError: string indices must be integers

-->

