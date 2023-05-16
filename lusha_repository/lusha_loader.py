from models.Contact import Contact
from .session_handler import LushaSession
from dacite import from_dict


class LushaLoader:
    def __init__(self):
        self.session = LushaSession()

    def load_contacts(self, contact_filter):
        response = self.session.get_contacts(contact_filter).json()
        contacts_json = response['contacts']['results']
        contacts = []
        for c in contacts_json:
            contacts.append(from_dict(data_class=Contact, data=c))

        return contacts
