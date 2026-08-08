import re

with open('app/src/main/java/com/example/ui/AddProductScreen.kt', 'r') as f:
    content = f.read()

old_textfield = '''                OutlinedTextField(
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

new_textfield = '''                OutlinedTextField(
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

content = content.replace(old_textfield, new_textfield)

old_load = '''    LaunchedEffect(productToEdit) {
        productToEdit?.let {
            name = it.name
            otherNames = it.otherNames
            location = it.location
            quantity = it.quantity.toString()
            expirationDate = it.expirationDate
            existingImagePath = it.imagePath
        }
    }'''

new_load = '''    LaunchedEffect(productToEdit) {
        productToEdit?.let {
            name = it.name
            otherNames = it.otherNames
            location = it.location
            quantity = it.quantity.toString()
            expirationDate = it.expirationDate.replace("/", "")
            existingImagePath = it.imagePath
        }
    }'''

content = content.replace(old_load, new_load)


old_save = '''                                viewModel.addProduct(
                                name = name.trim(),
                                otherNames = otherNames.trim(),
                                location = location.trim(),
                                quantity = qty,
                                expirationDate = expirationDate.trim(),
                                imagePath = imagePath
                            )
                        } else {
                            productToEdit?.let {
                                viewModel.updateProduct(it.copy(
                                    name = name.trim(),
                                    otherNames = otherNames.trim(),
                                    location = location.trim(),
                                    quantity = qty,
                                    expirationDate = expirationDate.trim(),
                                    imagePath = imagePath
                                ))
                            }'''

new_save = '''                                val formattedDate = if (expirationDate.length == 4) {
                                "${expirationDate.substring(0, 2)}/${expirationDate.substring(2, 4)}"
                            } else {
                                expirationDate.trim()
                            }
                            viewModel.addProduct(
                                name = name.trim(),
                                otherNames = otherNames.trim(),
                                location = location.trim(),
                                quantity = qty,
                                expirationDate = formattedDate,
                                imagePath = imagePath
                            )
                        } else {
                            productToEdit?.let {
                                val formattedDate = if (expirationDate.length == 4) {
                                    "${expirationDate.substring(0, 2)}/${expirationDate.substring(2, 4)}"
                                } else {
                                    expirationDate.trim()
                                }
                                viewModel.updateProduct(it.copy(
                                    name = name.trim(),
                                    otherNames = otherNames.trim(),
                                    location = location.trim(),
                                    quantity = qty,
                                    expirationDate = formattedDate,
                                    imagePath = imagePath
                                ))
                            }'''

content = content.replace(old_save, new_save)


date_visual_transformation = '''
class DateVisualTransformation : VisualTransformation {
    override fun filter(text: AnnotatedString): TransformedText {
        val trimmed = if (text.text.length >= 4) text.text.substring(0..3) else text.text
        var out = ""
        for (i in trimmed.indices) {
            out += trimmed[i]
            if (i == 1 && trimmed.length > 2) out += "/"
        }

        val offsetMapping = object : OffsetMapping {
            override fun originalToTransformed(offset: Int): Int {
                if (text.text.length <= 2) return offset
                if (offset <= 1) return offset
                if (offset <= 4) return offset + 1
                return 5
            }

            override fun transformedToOriginal(offset: Int): Int {
                if (text.text.length <= 2) return offset
                if (offset <= 2) return offset
                if (offset <= 5) return offset - 1
                return 4
            }
        }

        return TransformedText(AnnotatedString(out), offsetMapping)
    }
}
'''

content = content + date_visual_transformation

with open('app/src/main/java/com/example/ui/AddProductScreen.kt', 'w') as f:
    f.write(content)
