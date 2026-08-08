import re

with open('app/src/main/java/com/example/ui/AddProductScreen.kt', 'r') as f:
    content = f.read()

# Add import
if 'androidx.compose.ui.text.input.TextFieldValue' not in content:
    content = content.replace('import androidx.compose.ui.text.input.VisualTransformation', 'import androidx.compose.ui.text.input.TextFieldValue\nimport androidx.compose.ui.text.TextRange\nimport androidx.compose.ui.text.input.VisualTransformation')


# Change state
old_state = 'var expirationDate by remember { mutableStateOf("") }'
new_state = 'var expirationDate by remember { mutableStateOf(TextFieldValue("")) }'
content = content.replace(old_state, new_state)

# Change LaunchedEffect
old_load = '''    LaunchedEffect(productToEdit) {
        productToEdit?.let {
            name = it.name
            otherNames = it.otherNames
            location = it.location
            quantity = it.quantity.toString()
            expirationDate = it.expirationDate.replace("/", "")
            existingImagePath = it.imagePath
        }
    }'''
new_load = '''    LaunchedEffect(productToEdit) {
        productToEdit?.let {
            name = it.name
            otherNames = it.otherNames
            location = it.location
            quantity = it.quantity.toString()
            val dateStr = it.expirationDate.replace("/", "")
            expirationDate = TextFieldValue(text = dateStr, selection = TextRange(dateStr.length))
            existingImagePath = it.imagePath
        }
    }'''
content = content.replace(old_load, new_load)

# Change OutlinedTextField
old_textfield = '''                OutlinedTextField(
                    value = expirationDate,
                    onValueChange = { newValue ->
                        val digits = newValue.filter { it.isDigit() }
                        if (digits.length <= 4) {
                            expirationDate = digits
                        }
                    },
                    label = { Text("Date d'expiration") },
                    placeholder = { Text("MM/AA") },
                    visualTransformation = DateVisualTransformation(),
                    keyboardOptions = androidx.compose.foundation.text.KeyboardOptions(keyboardType = androidx.compose.ui.text.input.KeyboardType.Number),
                    modifier = Modifier.weight(1f),
                    singleLine = true,
                    shape = RoundedCornerShape(24.dp)
                )'''

new_textfield = '''                OutlinedTextField(
                    value = expirationDate,
                    onValueChange = { newValue ->
                        val digits = newValue.text.filter { it.isDigit() }
                        if (digits.length <= 4) {
                            expirationDate = newValue.copy(text = digits)
                        }
                    },
                    label = { Text("Date d'expiration") },
                    placeholder = { Text("MM/AA") },
                    visualTransformation = DateVisualTransformation(),
                    keyboardOptions = androidx.compose.foundation.text.KeyboardOptions(keyboardType = androidx.compose.ui.text.input.KeyboardType.Number),
                    modifier = Modifier.weight(1f),
                    singleLine = true,
                    shape = RoundedCornerShape(24.dp)
                )'''
content = content.replace(old_textfield, new_textfield)

# Change Save button usage
old_save_1 = '''                                val formattedDate = if (expirationDate.length == 4) {
                                "${expirationDate.substring(0, 2)}/${expirationDate.substring(2, 4)}"
                            } else {
                                expirationDate.trim()
                            }'''
new_save_1 = '''                                val formattedDate = if (expirationDate.text.length == 4) {
                                "${expirationDate.text.substring(0, 2)}/${expirationDate.text.substring(2, 4)}"
                            } else {
                                expirationDate.text.trim()
                            }'''

content = content.replace(old_save_1, new_save_1)

# Wait, there are TWO instances of save, one for add and one for update! Let's just do regex replace for all expirationDate.length to expirationDate.text.length
# Actually, the replacement above is safe.
with open('app/src/main/java/com/example/ui/AddProductScreen.kt', 'w') as f:
    f.write(content)
