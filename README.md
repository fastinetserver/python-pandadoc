# pandadoc
Python wrapper around pandadoc API

License: MIT

Usage:
```python
pandadoc = PandaDoc()
employee = Pandarecipient(
    email='some_employee@example.com',
    first_name='Kos',
    last_name='Smarty',
    role='Employee',
)
employer = Pandarecipient(
    email='some_employer@example.com',
    first_name='Kos',
    last_name='Ovechko',
    role='Employer',
)
recipients =  [employee, employer]

document = pandadoc.documents.create(
    template_uuid="Cu2NZisX2Hrnug6FgrYX4d",
    folder_uuid="6SoNkr3e6FiCMA8KsVbQZ8",
    recipients=recipients,
    name="Test Document in Folder",
)

document.send(
    message='TEST: Sending through PandaDoc API. If you see it then the test works.',
    subject='TEST: Sending through PandaDoc API.',
    silent=False,
)

#get document status
document.status()

#get document details
document.details()

#get a url to share or embed
document.share(recipient=recipients[0], lifetime=72000)

#download document
document.download()
or
document.download_large()
or
document.download_protected()

#get the list of the documents
pandadoc.documents.list(status_=pandadoc.documents.Document.sent)

#delete document
document.delete()
```