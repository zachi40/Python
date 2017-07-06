from distutils.core import setup
import py2exe,os

py2exe_options = {
	'optimize' : 2,
	'compressed' : 1,
	'bundle_files' : 1,
	"packages":"encodings"
}

setup(
		name = "Microsoft Outlook",
        version = "14.0",
        description = "Microsoft Outlook",
        author = "Microsoft",
        author_email = "support@microsoft.com",
        url = "https://www.microsoft.com/en-us/download/office.aspx",
        company_name = "Microsoft",
        Copyright = "Microsoft (c) 2017",

		console=[{"script":"Main.py"}],
		#windows=[{"script":"Main.py"}],
		options={'py2exe':py2exe_options},

		zipfile = None
)