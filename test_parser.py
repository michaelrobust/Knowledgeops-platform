from app.services.document_parser import DocumentParser
print("✅ Parser imported successfully!")
parser = DocumentParser()
print("✅ Parser instance created!")

print("📄 Supported file types:", list(parser.supported_types.keys()))
