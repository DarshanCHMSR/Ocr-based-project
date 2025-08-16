from indic_transliteration import sanscript
from indic_transliteration.sanscript import transliterate
print('sanscript module found')
print('transliterate callable:', callable(transliterate))
schemes = [s for s in dir(sanscript) if s.isupper()]
print('schemes sample:', schemes[:20])
# Transliterate sample
try:
    out = transliterate('namaste', sanscript.ITRANS, sanscript.KANNADA)
    print('transliterate("namaste", ITRANS -> KANNADA):', out)
except Exception as e:
    print('transliteration failed:', e)
