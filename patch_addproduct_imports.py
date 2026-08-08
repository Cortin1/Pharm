import re

with open('app/src/main/java/com/example/ui/AddProductScreen.kt', 'r') as f:
    content = f.read()

imports = """import androidx.compose.ui.text.input.VisualTransformation
import androidx.compose.ui.text.input.TransformedText
import androidx.compose.ui.text.input.OffsetMapping
import androidx.compose.ui.text.AnnotatedString
"""

content = content.replace('import androidx.compose.ui.Modifier', 'import androidx.compose.ui.Modifier\n' + imports)

with open('app/src/main/java/com/example/ui/AddProductScreen.kt', 'w') as f:
    f.write(content)
