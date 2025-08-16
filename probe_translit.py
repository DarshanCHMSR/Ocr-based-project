import inspect
import indic_transliteration
print('module:', indic_transliteration)
print('dir:', [x for x in dir(indic_transliteration) if not x.startswith('_')])

try:
    from indic_transliteration import sanscript, transliterate
    print('\nImported sanscript and transliterate')
    schemes = [s for s in dir(sanscript) if s.isupper()]
    print('Sanscript sample schemes count:', len(schemes))
    print('Some schemes sample:', schemes[:10])
    print('transliterate doc sample:', transliterate.__doc__ and transliterate.__doc__[:200])
    # Try a sample transliteration from IAST to Kannada (if supported)
    try:
        out = transliterate('namaste', 'iast', 'kn')
        print('transliterate("namaste", "iast", "kn") =>', out)
    except Exception as e:
        print('sample transliterate failed:', e)
except Exception as e:
    print('probe failed:', e)
