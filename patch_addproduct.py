import re

with open('app/src/main/java/com/example/ui/AddProductScreen.kt', 'r') as f:
    content = f.read()

old_textfield = '''                OutlinedTextField(
                    value = expirationDate,
                    onValueChange = { expirationDate = it },
                    label = { Text("Date d'expiration") },
                    placeholder = { Text("MM/AAAA") },
                    modifier = Modifier.weight(1f),
                    singleLine = true,
                    shape = RoundedCornerShape(24.dp)
                )'''

new_textfield = '''                OutlinedTextField(
                    value = expirationDate,
                    onValueChange = { newValue ->
                        val isDeleting = newValue.length < expirationDate.length
                        var digits = newValue.filter { it.isDigit() }.take(4)
                        
                        if (isDeleting && expirationDate.endsWith("/") && !newValue.endsWith("/")) {
                            digits = digits.dropLast(1)
                        }
                        
                        val formatted = buildString {
                            for (i in digits.indices) {
                                append(digits[i])
                                if (i == 1 && digits.length > 2) {
                                    append("/")
                                }
                            }
                        }
                        
                        expirationDate = if (digits.length == 2 && !isDeleting) {
                            "$formatted/"
                        } else {
                            formatted
                        }
                    },
                    label = { Text("Date d'expiration") },
                    placeholder = { Text("MM/AA") },
                    keyboardOptions = androidx.compose.foundation.text.KeyboardOptions(keyboardType = androidx.compose.ui.text.input.KeyboardType.Number),
                    modifier = Modifier.weight(1f),
                    singleLine = true,
                    shape = RoundedCornerShape(24.dp)
                )'''

content = content.replace(old_textfield, new_textfield)

with open('app/src/main/java/com/example/ui/AddProductScreen.kt', 'w') as f:
    f.write(content)
