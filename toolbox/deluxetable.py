def alphabet():
    alphabetlist=['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
    for value in alphabetlist:
        yield value

class deluxetable:
    """
    Note
    ----
    Originally written by Zhu, Weiwei
    (https://sites.google.com/site/zhuweiweipku/my-python-projects-2/tex-table-class)
    """

    def alphabet(self):
        alphabetlist=['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
        for value in alphabetlist:
            self.commentslines += '\\tablenotetext{%s}{%s}\n' % (value, self.comments.next())
            #print '\tablenotetext{%s}{%s}' % (value, self.comments.next())
            yield value

    def __init__(self, Caption='', colsetting='', colnames=[], data=[],
                 comments=[],label='', fmt="%.2f", half_width=False):
        """
        Create a LaTeX deluxetable.

        Parameters
        ----------
        Caption : str
            Table caption
        colsetting : str
            Column alignment (e.g. 'cccc')
        colnames : list
            List of table column name strings
        data : list
            List of table column data
        comments : list
            Table comments
        label : str
            Table label (e.g. "tab:example")
        fmt : str or list
            Table column formatting
        half_width: bool
            Make a table spanning the half page width (for two column)
        """

        if colnames == []: raise InputError('must have column names specified!')

        if data == []: raise InputError('must have data provided!')

        if not len(colnames) == len(data):
            raise InputError('number of column names does match number of columns in the data!')
        elif not colsetting == '' and not len(colsetting) == len(colnames):
            raise InputError('number of control characters in the colsetting does not match number of columns')
        elif colsetting == '':
            colsetting = 'c' * len(colnames)
        else:pass

        if type(fmt) == str:
            fmts = [fmt for i in range(len(colnames))]
        else:
            fmts = fmt

        if half_width:
            # Using multicol, half page width
            table_call = "deluxetable"
            table_width = "0.47\linewidth"
        else:
            # Using full page width
            table_call = "deluxetable*"
            table_width = "\linewidth"

        self.comments = comments
        self.commentslines = ''
        cols=''
        abc = self.alphabet()
        for name in colnames:
            while not name.find('#') == -1:name = name.replace('#',r'\tablenotemark{%s}' % abc.next(), 1)
            cols += '\colhead{%s}  &' % name
        cols = cols[:-1]
        rowcounts = len(data[0])
        colcounts = len(data)
        datalines = []
        for irow in range(rowcounts):
            datarow = fmts[0] %(data[0][irow])
            for icol in range(1,colcounts):
                datarow += '&  ' + fmts[icol] %(data[icol][irow])
            datalines.append(datarow)
        datatable = '\\\\\n'.join(datalines)
        while not datatable.find('#') == -1:datatable = datatable.replace('#',r'\tablenotemark{%s}' % abc.next(), 1)



        self.parsestring = r"""
\begin{%(table_call)s}{%(colsetting)s}
\tablewidth{%(table_width)s}
\tablecaption{\label{%(label)s} %(Caption)s }
\tablehead{ %(colnames)s }
\startdata
%(data)s
\enddata
\tablecomments{%(comments)s}
\end{%(table_call)s}
""" % {'label':label,
       'colsetting':colsetting,
       'Caption':Caption,
       'colnames':cols,
       'data':datatable,
       'comments':self.comments,
       'table_call':table_call,
       'table_width':table_width}


    def __str__(self):
        return self.parsestring
