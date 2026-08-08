import re

with open('app/src/main/java/com/example/ui/HomeScreen.kt', 'r') as f:
    content = f.read()

imports = """import androidx.compose.material3.ModalBottomSheet
import androidx.compose.material3.rememberModalBottomSheetState
import androidx.compose.runtime.setValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.material.icons.filled.Info
"""

content = content.replace('import androidx.compose.runtime.getValue', 'import androidx.compose.runtime.getValue\n' + imports)

with open('app/src/main/java/com/example/ui/HomeScreen.kt', 'w') as f:
    f.write(content)
