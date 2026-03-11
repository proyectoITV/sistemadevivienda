#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re

# Read the file
with open('portal/templates/desarrollo/empleados/listar_empleados.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace 40px with 50px in img avatar (object-fit style)
content = content.replace(
    'style="width: 40px; height: 40px; object-fit: cover;"',
    'style="width: 50px; height: 50px; object-fit: cover; display: block; margin: 0 auto;"'
)

# Replace 40px with 50px in div avatar (background style) and add font-size and margin
content = content.replace(
    'style="width: 40px; height: 40px; background: #ab0033; color: white; \n                                                    display: flex; align-items: center; justify-content: center; \n                                                    font-weight: bold;"',
    'style="width: 50px; height: 50px; background: #ab0033; color: white; \n                                                    display: flex; align-items: center; justify-content: center; \n                                                    font-weight: bold; font-size: 1.2rem; margin: 0 auto;"'
)

# Add vertical-align and padding to the TD element containing the avatar
# This should be the first occurrence of <td class="text-center"> in the photo column
pattern = r'<td class="text-center">\s+{% if empleado\.fotografia %}'
replacement = '<td class="text-center" style="vertical-align: middle; padding: 0.85rem 1rem;">\n                                    {% if empleado.fotografia %}'
content = re.sub(pattern, replacement, content, count=1)

# Write back
with open('portal/templates/desarrollo/empleados/listar_empleados.html', 'w', encoding='utf-8') as f:
    f.write(content)

print('✓ Avatar styling updated successfully')
print('  - Changed avatar size from 40px to 50px')
print('  - Added display: block and margin: 0 auto for centering')
print('  - Added font-size: 1.2rem to letter avatars')
print('  - Added vertical-align and padding to TD element')
