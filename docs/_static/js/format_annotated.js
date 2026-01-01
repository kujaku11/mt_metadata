/**
 * Reformat Pydantic Annotated field displays
 * 
 * This script parses Annotated[type, Field(...)] strings and wraps
 * semantic parts in colored spans for better readability.
 */

document.addEventListener('DOMContentLoaded', function() {
    // Find all field entries in the Fields summary
    const fieldEntries = document.querySelectorAll('.field-odd code.xref.py.py-obj');
    
    fieldEntries.forEach(function(codeElement) {
        const spans = Array.from(codeElement.querySelectorAll('span.pre'));
        if (spans.length < 2) return;
        
        // Get the full text content
        const fullText = spans.map(s => s.textContent).join(' ');
        
        // Check if this contains an Annotated field
        if (!fullText.includes('Annotated[')) return;
        
        // More flexible regex to handle variations in Sphinx's HTML generation
        // Pattern: fieldname (Annotated[...])
        const match = fullText.match(/^(\w+)\s+\(Annotated\[(.+)\]\)$/);
        if (!match) {
            // Try alternative pattern without closing paren-bracket
            const altMatch = fullText.match(/^(\w+)\s+\(Annotated\[(.+)$/);
            if (!altMatch) return;
            
            const fieldName = altMatch[1];
            const annotatedContent = altMatch[2];
            
            // Find where the Field/FieldInfo starts
            const fieldMatch = annotatedContent.match(/^(.*?),\s*(Field(?:Info)?\(.*)$/);
            if (!fieldMatch) return;
            
            const type = fieldMatch[1].trim();
            const field = fieldMatch[2].trim();
            
            rebuildSpans(codeElement, fieldName, type, field, false);
            return;
        }
        
        const fieldName = match[1];
        const annotatedContent = match[2];
        
        // Split the content on the first comma that's not inside brackets/parens
        const { type, field } = splitAnnotatedContent(annotatedContent);
        
        rebuildSpans(codeElement, fieldName, type, field, true);
    });
});

function rebuildSpans(codeElement, fieldName, type, field, hasClosing) {
    // Clear existing spans
    codeElement.innerHTML = '';
    
    // Rebuild with semantic spans
    codeElement.appendChild(createSpan(fieldName, 'field-name'));
    codeElement.appendChild(createSpan(' (', ''));
    codeElement.appendChild(createSpan('Annotated', 'annotated-keyword'));
    codeElement.appendChild(createSpan('[', 'annotated-bracket'));
    
    // Type annotation - keep all union types together (e.g., "str | int" or "float | None")
    codeElement.appendChild(createSpan(type, 'type-annotation'));
    
    codeElement.appendChild(createSpan(', ', 'separator'));
    codeElement.appendChild(createSpan(field, 'field-info'));
    
    if (hasClosing) {
        codeElement.appendChild(createSpan(']', 'annotated-bracket'));
        codeElement.appendChild(createSpan(')', ''));
    }
}

function splitAnnotatedContent(content) {
    // Find the first comma that's not inside parentheses or brackets
    let depth = 0;
    let splitIndex = -1;
    
    for (let i = 0; i < content.length; i++) {
        const char = content[i];
        
        if (char === '(' || char === '[' || char === '{') {
            depth++;
        } else if (char === ')' || char === ']' || char === '}') {
            depth--;
        } else if (char === ',' && depth === 0) {
            splitIndex = i;
            break;
        }
    }
    
    if (splitIndex === -1) {
        return { type: content.trim(), field: '' };
    }
    
    return {
        type: content.substring(0, splitIndex).trim(),
        field: content.substring(splitIndex + 1).trim()
    };
}

function createSpan(text, className) {
    const span = document.createElement('span');
    span.className = 'pre ' + (className || '');
    span.textContent = text;
    return span;
}
