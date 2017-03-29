"""
    OVERALL CREDIT TO:
        t0mm0, Eldorado, VOINAGE, BSTRDMKR, tknorris, smokdpi, TheHighway

    urlresolver XBMC Addon
    Copyright (C) 2011 t0mm0

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""
import re
from lib import helpers
from urlresolver import common
from urlresolver.resolver import UrlResolver, ResolverError

class StreamangoResolver(UrlResolver):
    name = "streamango"
    domains = ['streamango.com']
    pattern = '(?://|\.)(streamango\.com)/\w/(\w+)'
    
    def __init__(self):
        self.net = common.Net()

    def get_media_url(self, host, media_id):
        web_url = self.get_url(host, media_id)
        headers = {'User-Agent': common.FF_USER_AGENT}
        html = self.net.http_GET(web_url, headers=headers).content
        headers['Referer'] = web_url
        
        if html:
            r = re.search(r'srces\.push\({type:[\"\']video/mp4[\"\'],src:[\"\'](.*?)[\"\'].*?}\);', html)
            if r:
                source = r.group(1)
                if source.startswith("//"): source = "http:%s" % source
            else:
                raise ResolverError('No playable video found.')

            return source + helpers.append_headers(headers)
            
        raise ResolverError('No playable video found.')
    
    def get_url(self, host, media_id):
        return 'https://streamango.com/f/%s' % media_id
