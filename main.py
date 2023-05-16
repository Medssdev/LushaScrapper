from lusha_repository.lusha_loader import LushaLoader
import json

loader = LushaLoader()

with open('content.json') as f:
    filter = json.load(f)

contacts = loader.load_contacts(filter)

print(*contacts, sep='\n')
