/**
 * Pure ESM transliteration module for English to Kannada transliteration
 * No React dependencies - works in any modern browser with ES6+ support
 */

// ITRANS to Kannada character mapping
const ITRANS_TO_KANNADA = {
    // Vowels
    'a': 'ಅ', 'aa': 'ಆ', 'A': 'ಆ', 'i': 'ಇ', 'ii': 'ಈ', 'I': 'ಈ',
    'u': 'ಉ', 'uu': 'ಊ', 'U': 'ಊ', 'e': 'ಎ', 'ee': 'ಏ', 'E': 'ಏ',
    'o': 'ಒ', 'oo': 'ಓ', 'O': 'ಓ', 'ai': 'ಐ', 'au': 'ಔ',
    
    // Consonants
    'ka': 'ಕ', 'kha': 'ಖ', 'ga': 'ಗ', 'gha': 'ಘ', 'nga': 'ಙ',
    'cha': 'ಚ', 'chha': 'ಛ', 'ja': 'ಜ', 'jha': 'ಝ', 'nya': 'ಞ',
    'ta': 'ಟ', 'tha': 'ಠ', 'da': 'ಡ', 'dha': 'ಢ', 'na': 'ಣ',
    'tta': 'ತ', 'ttha': 'ಥ', 'dda': 'ದ', 'ddha': 'ಧ', 'nna': 'ನ',
    'pa': 'ಪ', 'pha': 'ಫ', 'ba': 'ಬ', 'bha': 'ಭ', 'ma': 'ಮ',
    'ya': 'ಯ', 'ra': 'ರ', 'la': 'ಲ', 'va': 'ವ', 'wa': 'ವ',
    'sha': 'ಶ', 'shha': 'ಷ', 'sa': 'ಸ', 'ha': 'ಹ',
    
    // Single consonants (halanta form)
    'k': 'ಕ್', 'kh': 'ಖ್', 'g': 'ಗ್', 'gh': 'ಘ್', 'ng': 'ಙ್',
    'ch': 'ಚ್', 'chh': 'ಛ್', 'j': 'ಜ್', 'jh': 'ಝ್', 'ny': 'ಞ್',
    't': 'ತ್', 'th': 'ಥ್', 'd': 'ದ್', 'dh': 'ಧ್', 'n': 'ನ್',
    'p': 'ಪ್', 'ph': 'ಫ್', 'b': 'ಬ್', 'bh': 'ಭ್', 'm': 'ಮ್',
    'y': 'ಯ್', 'r': 'ರ್', 'l': 'ಲ್', 'v': 'ವ್', 'w': 'ವ್',
    'sh': 'ಶ್', 's': 'ಸ್', 'h': 'ಹ್',
    
    // Common words/phrases
    'namaste': 'ನಮಸ್ತೆ', 'Namaste': 'ನಮಸ್ತೆ',
    'kannada': 'ಕನ್ನಡ', 'Kannada': 'ಕನ್ನಡ',
    'bangalore': 'ಬೆಂಗಳೂರು', 'Bangalore': 'ಬೆಂಗಳೂರು',
    'mysore': 'ಮೈಸೂರು', 'Mysore': 'ಮೈಸೂರು',
    'karnataka': 'ಕರ್ನಾಟಕ', 'Karnataka': 'ಕರ್ನಾಟಕ',
    'hello': 'ಹಲೋ', 'Hello': 'ಹಲೋ',
    'thanks': 'ಧನ್ಯವಾದ', 'Thanks': 'ಧನ್ಯವಾದ'
};

/**
 * Simple transliteration function from ITRANS to Kannada
 * @param {string} input - ITRANS input string
 * @returns {string} - Kannada output string
 */
function transliterateWord(input) {
    if (!input || typeof input !== 'string') return input;
    
    const word = input.trim();
    const lowerWord = word.toLowerCase();
    
    // Direct word mapping first (try both original case and lowercase)
    if (ITRANS_TO_KANNADA[word]) {
        return ITRANS_TO_KANNADA[word];
    }
    if (ITRANS_TO_KANNADA[lowerWord]) {
        return ITRANS_TO_KANNADA[lowerWord];
    }
    
    // Character-by-character transliteration for complex words
    let result = '';
    let i = 0;
    
    while (i < lowerWord.length) {
        let matched = false;
        
        // Try longest matches first (4 chars, then 3, then 2, then 1)
        for (let len = Math.min(4, lowerWord.length - i); len >= 1; len--) {
            const substr = lowerWord.substring(i, i + len);
            if (ITRANS_TO_KANNADA[substr]) {
                result += ITRANS_TO_KANNADA[substr];
                i += len;
                matched = true;
                break;
            }
        }
        
        if (!matched) {
            // No match found, keep original character
            result += lowerWord[i];
            i++;
        }
    }
    
    return result || input; // Return original if no transliteration possible
}

/**
 * Main transliteration class/function compatible with expected API
 */
export class IndicTransliterate {
    constructor(options = {}) {
        this.source = options.source || 'eng';
        this.target = options.target || 'kn';
    }
    
    transliterate(text) {
        if (this.source === 'eng' && this.target === 'kn') {
            return transliterateWord(text);
        }
        return text; // Return unchanged for unsupported language pairs
    }
    
    transform(text) {
        return this.transliterate(text);
    }
}

/**
 * Direct export function for simple usage
 * @param {string} text - Input text to transliterate
 * @param {string} source - Source language (default: 'eng')  
 * @param {string} target - Target language (default: 'kn')
 * @returns {string} - Transliterated text
 */
export function transliterate(text, source = 'eng', target = 'kn') {
    if (source === 'eng' && target === 'kn') {
        return transliterateWord(text);
    }
    return text;
}

// Default export
export default IndicTransliterate;
