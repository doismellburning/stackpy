# What is stackpy? #

stackpy is a simple Python wrapper for the [StackExchange API v2](http://api.stackexchange.com/docs).

It was written by [Kristian Glass](http://www.doismellburning.co.uk/) for [StackCompare](http://stackcompare.com/).

Currently somewhat alpha.

# Getting Started #

For the latest stable version:

    pip install stackpy

OR for the bleeding edge:

    git clone https://github.com/doismellburning/stackpy.git

# Examples #

## Sites ##

    >>> from stackpy import Stackpy
    >>> s = Stackpy()
    >>> sites = s.sites().items
    >>> stackoverflow = [site for site in sites if site.name == 'Stack Overflow'][0]
    >>> stackoverflow.site_url
    u'http://stackoverflow.com'
    >>> stackoverflow.audience
    u'professional and enthusiast programmers'


## Users ##

    >>> from stackpy import Stackpy
    >>> s = Stackpy()
    >>> kristian = s.users([928098]).items[0]
    >>> kristian.display_name
    u'Kristian Glass'

## Other StackExchange Sites ##

    >>> from stackpy import Stackpy
    >>> s = Stackpy()
    >>> kristian = s.users([114764], site='serverfault').items[0]
    >>> kristian.display_name
    u'Kristian Glass'
