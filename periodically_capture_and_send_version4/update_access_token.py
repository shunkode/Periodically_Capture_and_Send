"""

MIT Licence

Copyright (c) 2020 Dropbox Inc., http://www.dropbox.com/

    Permission is hereby granted, free of charge, to any person obtaining
    a copy of this software and associated documentation files (the
    "Software"), to deal in the Software without restriction, including
    without limitation the rights to use, copy, modify, merge, publish,
    distribute, sublicense, and/or sell copies of the Software, and to
    permit persons to whom the Software is furnished to do so, subject to
    the following conditions:

    The above copyright notice and this permission notice shall be
    included in all copies or substantial portions of the Software.

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
    EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
    MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
    NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
    LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
    OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
    WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""


import dropbox

def update_access_token():
    dbx = dropbox.Dropbox("sl.BVfb66Eo_mldFVS1C61Ks7OfHJtS-sbZL0SP6MIoE00u1AcEAGVwixOLk3wCmq-AVK1l96fy7zp53fAu4ToMeZ8KXIdIu8MGJ5T14hX6nzZIL3ivOgdAH7TQ6v8tTXunDi1u5K7VekI:JPN")
    if dropbox.exceptions.AuthError:
        rdbx = dropbox.Dropbox(oauth2_refresh_token = "FytgLVT_jVEAAAAAAAAAAZkJsAyjEz7ATKn0FYwjLRVlS3N6yTpMzPIQOcLVppD0",
        app_key = "w6ht905tz6ijg0n", app_secret = "bc3pdkixfh2xqxi")
        rdbx.__dict__
        """
        {'_oauth2_access_token': None, '_oauth2_refresh_token': '******', '_oauth2_access_token_expiration': None, '_app_key': '*******', '_app_secret': '*******', '_scope': None, '_max_retries_on_error': 4, '_max_retries_on_rate_limit': None, '_session': <requests.sessions.Session object at 0x7fffd4cbe278>, '_headers': None, '_raw_user_agent': None, '_user_agent': 'OfficialDropboxPythonSDKv2/11.32.0', '_logger': <Logger dropbox (WARNING)>, '_host_map': {'api': 'api.dropboxapi.com', 'content': 'content.dropboxapi.com', 'notify': 'notify.dropboxapi.com'}, '_timeout': 100}
        """
        rdbx._oauth2_access_token

        drop = dropbox.base.DropboxBase()
        #oauth2_access_token=None, max_retries_on_error=4, max_retries_on_rate_limit=None, user_agent=None, session=None, headers=None, timeout=100, oauth2_refresh_token=None, oauth2_access_token_expiration=None, app_key=None, app_secret=None, scope=None, ca_certs=None)
        drop.users_get_current_account()
        rdbx._oauth2_access_token
        before = rdbx._oauth2_access_token
        print(before)
        rdbx.refresh_access_token()
        after = rdbx._oauth2_access_token
        print(after)
        before == after
        access_token = after
        dbx = dropbox.Dropbox(access_token, timeout=None)
    return dbx

"""
## Usage(update_access_token)
dbx = update_access_token()
print(dbx)
"""